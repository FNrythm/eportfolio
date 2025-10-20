"""
Comprehensive Test Suite for Email Forensics System

This test suite validates all core functionality of the multi-agent system,
ensuring correctness, robustness, and maintainability.

Testing Philosophy:
1. Unit Tests: Test individual agent methods in isolation
2. Integration Tests: Test agent interactions and data flow
3. Edge Cases: Verify behavior with unusual/malicious inputs
4. Regression Tests: Prevent reintroduction of fixed bugs

Design Rationale for test organization:
- Test classes group related tests (one per agent)
- Fixtures provide reusable test data
- Descriptive test names document expected behavior
- Comments explain WHY we test specific scenarios, not just WHAT

References:
- Beck, K. (2002). Test Driven Development: By Example
- Martin, R. (2008). Clean Code: A Handbook of Agile Software Craftsmanship
"""

import pytest
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import tempfile
import shutil

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import SimpleEmail, Finding, DiscoveryAgent, AnalysisAgent, DashboardAgent, ReportAgent
from utils import EnhancedEmailGenerator


# =============================================================================
# TEST FIXTURES
# =============================================================================
# Fixtures provide reusable test data and setup/teardown logic
# Design choice: Fixtures over repeated initialization for DRY principle

@pytest.fixture
def sample_email_normal():
    """
    Normal email fixture for testing negative cases.
    
    Why this fixture: Tests need to verify that legitimate emails
    don't trigger false positives. This provides a canonical "safe" email.
    """
    return SimpleEmail(
        id="test_001",
        subject="Project status update",
        sender="john@company.com",
        recipient="jane@company.com",
        date=datetime(2025, 1, 10, 14, 30),  # Business hours
        content="The project is progressing well. Here's the update.",
        file_path="test_email_001.txt"
    )


@pytest.fixture
def sample_email_suspicious():
    """
    Suspicious email fixture for testing positive detection cases.
    
    Why this fixture: Contains multiple red flags (urgent keyword,
    after-hours, external source) to test all detection mechanisms.
    """
    return SimpleEmail(
        id="test_002",
        subject="URGENT: Account verification required",
        sender="admin@phishing-site.com",
        recipient="victim@company.com",
        date=datetime(2025, 1, 10, 23, 45),  # After hours
        content="Click here to download verification form immediately.",
        file_path="test_email_002.txt"
    )


@pytest.fixture
def sample_email_list(sample_email_normal, sample_email_suspicious):
    """
    Mixed email collection for integration testing.
    
    Why this fixture: Real-world scenarios have both normal and
    suspicious emails. This fixture simulates realistic data.
    """
    # Create additional emails for volume testing
    additional_normal = SimpleEmail(
        id="test_003",
        subject="Meeting minutes",
        sender="alice@company.com",
        recipient="bob@company.com",
        date=datetime(2025, 1, 11, 10, 0),
        content="Please find attached meeting minutes.",
        file_path="test_email_003.txt"
    )
    
    return [sample_email_normal, sample_email_suspicious, additional_normal]


@pytest.fixture
def temp_email_directory():
    """
    Temporary directory for filesystem testing.
    
    Why this fixture: Tests should not pollute actual filesystem.
    tempfile provides clean isolated environment that auto-cleans.
    
    Yields directory path then cleans up after test completion.
    """
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)  # Cleanup after test


# =============================================================================
# SIMPLEMAIL DATA MODEL TESTS
# =============================================================================

class TestSimpleEmail:
    """
    Tests for SimpleEmail data model and detection methods.
    
    Why test data models: Ensures core detection logic (is_suspicious,
    is_after_hours, is_external) works correctly across edge cases.
    These methods are used by all agents, so bugs here have wide impact.
    """
    
    def test_is_suspicious_with_keywords(self, sample_email_suspicious):
        """
        Verify that emails with suspicious keywords are correctly identified.
        
        Why this test: Keyword detection is primary threat identification
        mechanism. False negatives mean missed threats.
        """
        assert sample_email_suspicious.is_suspicious() == True
    
    def test_is_suspicious_normal_email(self, sample_email_normal):
        """
        Verify that normal emails don't trigger false positives.
        
        Why this test: False positives waste analyst time and reduce
        trust in the system. Must verify legitimate emails pass through.
        """
        assert sample_email_normal.is_suspicious() == False
    
    def test_is_suspicious_case_insensitive(self):
        """
        Verify keyword detection is case-insensitive.
        
        Why this test: Attackers use various capitalizations (URGENT,
        Urgent, urgent) to evade detection. System must catch all variants.
        """
        email = SimpleEmail(
            id="test_case",
            subject="urgent MESSAGE",  # Mixed case
            sender="test@test.com",
            recipient="user@company.com",
            date=datetime.now(),
            content="CONFIDENTIAL information",  # Mixed case
            file_path="test.txt"
        )
        assert email.is_suspicious() == True
    
    def test_is_after_hours_late_night(self, sample_email_suspicious):
        """
        Verify that emails sent late at night are flagged.
        
        Why this test: After-hours emails (23:45 in fixture) often indicate
        compromised accounts in different time zones or automated malware.
        """
        assert sample_email_suspicious.is_after_hours() == True
    
    def test_is_after_hours_early_morning(self):
        """
        Verify early morning emails (before 8 AM) are flagged.
        
        Why this test: Tests the other boundary of after-hours detection.
        Comprehensive boundary testing prevents off-by-one errors.
        """
        email = SimpleEmail(
            id="test_early",
            subject="Test",
            sender="test@test.com",
            recipient="user@company.com",
            date=datetime(2025, 1, 10, 5, 0),  # 5 AM
            content="Content",
            file_path="test.txt"
        )
        assert email.is_after_hours() == True
    
    def test_is_after_hours_business_hours(self, sample_email_normal):
        """
        Verify that emails during business hours are not flagged.
        
        Why this test: False positives on timing would flag legitimate
        communications. Tests negative case for after-hours detection.
        """
        assert sample_email_normal.is_after_hours() == False
    
    def test_is_external_domain(self, sample_email_suspicious):
        """
        Verify external domains are correctly identified.
        
        Why this test: External sources are primary attack vectors.
        System must reliably distinguish internal from external.
        """
        assert sample_email_suspicious.is_external() == True
    
    def test_is_internal_domain(self, sample_email_normal):
        """
        Verify internal domains are correctly identified as not external.
        
        Why this test: Internal communications should not be flagged as
        external. Tests the negative case of external detection.
        """
        assert sample_email_normal.is_external() == False
    
    def test_is_external_missing_at_symbol(self):
        """
        Verify handling of malformed email addresses.
        
        Why this test: Real-world data is messy. System must handle
        malformed addresses gracefully without crashing.
        """
        email = SimpleEmail(
            id="test_malformed",
            subject="Test",
            sender="invalidemail",  # No @ symbol
            recipient="user@company.com",
            date=datetime.now(),
            content="Content",
            file_path="test.txt"
        )
        # Should handle gracefully and classify as external (unknown)
        assert email.is_external() == True


# =============================================================================
# DISCOVERY AGENT TESTS
# =============================================================================

class TestDiscoveryAgent:
    """
    Tests for DiscoveryAgent file discovery and parsing logic.
    
    Why test DiscoveryAgent: This is the entry point for data into the
    system. Bugs here mean no data flows to downstream agents. Critical
    to test file I/O and parsing edge cases.
    """
    
    def test_find_email_files_success(self, temp_email_directory):
        """
        Verify that agent correctly discovers email files.
        
        Why this test: Core functionality of DiscoveryAgent is finding
        files. Must verify glob pattern matching works correctly.
        """
        # Create test email files
        for i in range(3):
            path = os.path.join(temp_email_directory, f"email_{i:03d}.txt")
            with open(path, 'w') as f:
                f.write(f"ID: email_{i:03d}\n")
        
        agent = DiscoveryAgent(temp_email_directory)
        files = agent.find_email_files()
        
        assert len(files) == 3
        assert all(f.endswith('.txt') for f in files)
    
    def test_find_email_files_empty_directory(self, temp_email_directory):
        """
        Verify agent handles empty directory gracefully.
        
        Why this test: Edge case where no emails exist. System should
        not crash, should return empty list for downstream handling.
        """
        agent = DiscoveryAgent(temp_email_directory)
        files = agent.find_email_files()
        
        assert len(files) == 0
        assert files == []
    
    def test_load_emails_valid_format(self, temp_email_directory):
        """
        Verify correct parsing of properly formatted email files.
        
        Why this test: Parsing logic is complex and error-prone. Must
        verify all fields extracted correctly from text format.
        """
        # Create well-formed email file
        email_path = os.path.join(temp_email_directory, "email_001.txt")
        with open(email_path, 'w') as f:
            f.write("ID: email_001\n")
            f.write("Subject: Test Subject\n")
            f.write("From: sender@test.com\n")
            f.write("To: recipient@test.com\n")
            f.write("Date: 2025-01-10T14:30:00\n")
            f.write("Content: Test content here\n")
        
        agent = DiscoveryAgent(temp_email_directory)
        agent.find_email_files()
        emails = agent.load_emails()
        
        assert len(emails) == 1
        assert emails[0].id == "email_001"
        assert emails[0].subject == "Test Subject"
        assert emails[0].sender == "sender@test.com"
    
    def test_load_emails_malformed_date(self, temp_email_directory):
        """
        Verify graceful handling of unparseable dates.
        
        Why this test: Date formats vary. System must not crash on
        malformed dates, should use fallback (current time).
        """
        email_path = os.path.join(temp_email_directory, "email_bad_date.txt")
        with open(email_path, 'w') as f:
            f.write("ID: email_001\n")
            f.write("Subject: Test\n")
            f.write("From: sender@test.com\n")
            f.write("To: recipient@test.com\n")
            f.write("Date: INVALID DATE FORMAT\n")  # Bad format
            f.write("Content: Test\n")
        
        agent = DiscoveryAgent(temp_email_directory)
        agent.find_email_files()
        emails = agent.load_emails()
        
        # Should parse successfully with fallback date
        assert len(emails) == 1
        assert isinstance(emails[0].date, datetime)
    
    def test_load_emails_corrupted_file(self, temp_email_directory):
        """
        Verify system continues despite corrupted individual files.
        
        Why this test: In forensic scenarios, some files may be corrupted.
        System should recover as much data as possible, not fail entirely.
        Demonstrates resilience design principle.
        """
        # Create one good file and one corrupted file
        good_path = os.path.join(temp_email_directory, "good.txt")
        with open(good_path, 'w') as f:
            f.write("ID: good\nSubject: Test\nFrom: a@b.com\nTo: c@d.com\nDate: 2025-01-10T10:00:00\nContent: Test\n")
        
        bad_path = os.path.join(temp_email_directory, "corrupted.txt")
        with open(bad_path, 'w') as f:
            f.write("CORRUPTED DATA\n\n\n")  # No proper key:value format
        
        agent = DiscoveryAgent(temp_email_directory)
        agent.find_email_files()
        emails = agent.load_emails()
        
        # Should successfully load good file, skip corrupted one
        assert len(emails) >= 1  # At least the good one


# =============================================================================
# ANALYSIS AGENT TESTS
# =============================================================================

class TestAnalysisAgent:
    """
    Tests for AnalysisAgent threat detection logic.
    
    Why test AnalysisAgent: Core threat detection happens here. Bugs in
    analysis mean missed threats or false alarms. Critical to validate
    all detection strategies work correctly.
    """
    
    def test_keyword_analysis_detects_suspicious(self, sample_email_list):
        """
        Verify keyword analysis identifies suspicious emails.
        
        Why this test: Keyword detection is primary threat mechanism.
        Must verify it correctly flags emails with suspicious content.
        """
        agent = AnalysisAgent(sample_email_list)
        agent._keyword_analysis()
        
        # Should find at least one keyword-based finding
        keyword_findings = [f for f in agent.findings if f.finding_type == "Suspicious Keywords"]
        assert len(keyword_findings) > 0
    
    def test_keyword_analysis_severity_escalation(self):
        """
        Verify high-urgency keywords trigger High severity classification.
        
        Why this test: Severity levels drive incident response priorities.
        Must verify urgent keywords (suspend, critical) escalate severity
        as these indicate active threats requiring immediate action.
        """
        urgent_email = SimpleEmail(
            id="urgent_test",
            subject="CRITICAL: Account will be SUSPENDED",  # Two high-urgency keywords
            sender="attacker@phishing.com",
            recipient="victim@company.com",
            date=datetime.now(),
            content="Immediate action required",
            file_path="test.txt"
        )
        
        agent = AnalysisAgent([urgent_email])
        agent._keyword_analysis()
        
        assert len(agent.findings) > 0
        assert agent.findings[0].severity == "High"
    
    def test_timing_analysis_after_hours(self, sample_email_suspicious):
        """
        Verify timing analysis flags after-hours communications.
        
        Why this test: Temporal anomalies indicate compromised accounts
        or malware. Must verify detection of unusual send times.
        """
        agent = AnalysisAgent([sample_email_suspicious])
        agent._timing_analysis()
        
        timing_findings = [f for f in agent.findings if f.finding_type == "After Hours Communication"]
        assert len(timing_findings) > 0
    
    def test_external_communication_analysis(self, sample_email_suspicious):
        """
        Verify external source detection.
        
        Why this test: External sources are primary attack vectors.
        Must verify detection of emails from outside organization.
        """
        agent = AnalysisAgent([sample_email_suspicious])
        agent._external_communication_analysis()
        
        external_findings = [f for f in agent.findings if f.finding_type == "External Communication"]
        assert len(external_findings) > 0
    
    def test_volume_analysis_high_volume_sender(self):
        """
        Verify volume analysis detects high-frequency senders.
        
        Why this test: Unusual sending volumes indicate spam campaigns
        or compromised accounts. Must verify threshold detection works.
        """
        # Create 6 emails from same sender (threshold is 5)
        emails = [
            SimpleEmail(
                id=f"vol_{i}",
                subject="Test",
                sender="spammer@external.com",  # Same sender
                recipient=f"victim{i}@company.com",
                date=datetime.now(),
                content="Spam content",
                file_path=f"test_{i}.txt"
            )
            for i in range(6)
        ]
        
        agent = AnalysisAgent(emails)
        agent._volume_analysis()
        
        volume_findings = [f for f in agent.findings if f.finding_type == "High Volume Sender"]
        assert len(volume_findings) > 0
    
    def test_analyze_emails_integration(self, sample_email_list):
        """
        Integration test: verify all analysis strategies execute.
        
        Why this test: Tests orchestration of multiple strategies.
        Ensures analyze_emails() correctly calls all sub-methods and
        aggregates findings properly.
        """
        agent = AnalysisAgent(sample_email_list)
        findings = agent.analyze_emails()
        
        # Should have findings from multiple strategies
        assert len(findings) > 0
        assert isinstance(findings[0], Finding)
        assert findings[0].severity in ["Low", "Medium", "High"]
    
    def test_get_statistics(self, sample_email_list):
        """
        Verify statistics calculation returns correct metrics.
        
        Why this test: Statistics drive dashboards and reports. Incorrect
        calculations lead to wrong operational decisions. Must verify
        all metrics computed accurately.
        """
        agent = AnalysisAgent(sample_email_list)
        agent.analyze_emails()
        stats = agent.get_statistics()
        
        # Verify all required keys present
        required_keys = [
            'total_emails', 'suspicious_emails', 'external_emails',
            'after_hours_emails', 'total_findings',
            'high_severity_findings', 'medium_severity_findings', 'low_severity_findings'
        ]
        for key in required_keys:
            assert key in stats
        
        # Verify logical consistency
        assert stats['total_emails'] == len(sample_email_list)
        assert stats['total_findings'] == len(agent.findings)


# =============================================================================
# DASHBOARD AGENT TESTS
# =============================================================================

class TestDashboardAgent:
    """
    Tests for DashboardAgent visualization generation.
    
    Why test DashboardAgent: Visualization failures don't crash system
    but prevent human analysis. Must verify all chart types generate
    successfully and handle edge cases (empty data, single datapoint).
    """
    
    @patch('matplotlib.pyplot.savefig')
    @patch('matplotlib.pyplot.close')
    def test_generate_summary_chart(self, mock_close, mock_savefig, sample_email_list):
        """
        Verify summary chart generation executes without errors.
        
        Why this test: Summary chart is first view users see. Must work
        reliably. Mocking savefig prevents actual file I/O during testing.
        """
        agent = DashboardAgent(sample_email_list, [])
        agent._generate_summary_chart()
        
        # Verify matplotlib methods called correctly
        assert mock_savefig.called
        assert mock_close.called
    
    def test_dashboard_agent_with_empty_data(self):
        """
        Verify dashboard handles empty dataset gracefully.
        
        Why this test: Edge case where no emails found. System should
        generate empty visualizations, not crash. Tests error resilience.
        """
        agent = DashboardAgent([], [])
        # Should not raise exception
        try:
            agent._generate_summary_chart()
        except Exception as e:
            pytest.fail(f"Dashboard failed on empty data: {e}")


# =============================================================================
# REPORT AGENT TESTS
# =============================================================================

class TestReportAgent:
    """
    Tests for ReportAgent report generation.
    
    Why test ReportAgent: Reports are final output delivered to stakeholders.
    Formatting errors or missing data undermine system credibility.
    Must verify all report formats generate correctly.
    """
    
    def test_generate_text_report(self, sample_email_list, temp_email_directory):
        """
        Verify text report generation creates file with expected content.
        
        Why this test: Text reports used for archival and automated
        processing. Must contain all required sections in correct format.
        """
        findings = [
            Finding(
                finding_type="Test Finding",
                description="Test description",
                email_id="test_001",
                severity="High",
                timestamp=datetime.now()
            )
        ]
        
        agent = ReportAgent(sample_email_list, findings)
        agent.output_dir = temp_email_directory  # Use temp directory
        agent._generate_text_report()
        
        report_path = os.path.join(temp_email_directory, "forensics_report.txt")
        assert os.path.exists(report_path)
        
        # Verify content includes key sections
        with open(report_path, 'r') as f:
            content = f.read()
            assert "EMAIL FORENSICS ANALYSIS REPORT" in content
            assert "EXECUTIVE SUMMARY" in content
            assert "DETAILED FINDINGS" in content
    
    def test_generate_html_report(self, sample_email_list, temp_email_directory):
        """
        Verify HTML report generation creates valid HTML file.
        
        Why this test: HTML reports presented to non-technical stakeholders.
        Must be well-formed, complete, and visually consistent.
        """
        findings = []
        agent = ReportAgent(sample_email_list, findings)
        agent.output_dir = temp_email_directory
        agent._generate_html_report()
        
        report_path = os.path.join(temp_email_directory, "forensics_report.html")
        assert os.path.exists(report_path)
        
        # Verify HTML structure
        with open(report_path, 'r') as f:
            content = f.read()
            assert "<!DOCTYPE html>" in content
            assert "<html" in content
            assert "</html>" in content


# =============================================================================
# EMAIL GENERATOR TESTS
# =============================================================================

class TestEnhancedEmailGenerator:
    """
    Tests for test data generation utility.
    
    Why test generator: Generated data used throughout testing and demos.
    Bugs here compromise all downstream testing. Must verify data
    characteristics match specifications.
    """
    
    def test_generate_emails_count(self):
        """
        Verify correct number of emails generated.
        
        Why this test: Basic contract of generator - must produce
        requested quantity. Tests parameter passing.
        """
        generator = EnhancedEmailGenerator()
        emails = generator.generate_emails(count=10, suspicious_percentage=0.3)
        
        assert len(emails) == 10
    
    def test_generate_emails_suspicious_ratio(self):
        """
        Verify suspicious email ratio matches specification.
        
        Why this test: Ratio control critical for testing detection
        accuracy. Must verify precise distribution for statistical tests.
        """
        generator = EnhancedEmailGenerator()
        emails = generator.generate_emails(count=100, suspicious_percentage=0.3)
        
        suspicious_count = sum(1 for e in emails if e.is_suspicious())
        # Allow small margin for rounding
        assert 25 <= suspicious_count <= 35  # 30% of 100 = 30
    
    def test_generate_emails_unique_ids(self):
        """
        Verify all generated emails have unique IDs.
        
        Why this test: Duplicate IDs would break finding-to-email mapping.
        Critical for forensic chain of custody. Must verify uniqueness.
        """
        generator = EnhancedEmailGenerator()
        emails = generator.generate_emails(count=50)
        
        ids = [e.id for e in emails]
        assert len(ids) == len(set(ids))  # All unique


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestSystemIntegration:
    """
    End-to-end integration tests verifying complete pipeline.
    
    Why integration tests: Unit tests verify components in isolation,
    but bugs often emerge at component boundaries. Integration tests
    verify data flows correctly through entire system.
    """
    
    def test_full_pipeline_execution(self, temp_email_directory):
        """
        Verify complete analysis pipeline executes successfully.
        
        Why this test: Most important test - verifies entire system works
        end-to-end. Simulates actual usage scenario. Catches integration
        bugs that unit tests miss.
        """
        # Generate test data
        generator = EnhancedEmailGenerator()
        emails = generator.generate_emails(count=10, suspicious_percentage=0.3)
        
        # Copy emails to temp directory
        for email in emails:
            src = email.file_path
            dst = os.path.join(temp_email_directory, os.path.basename(src))
            if os.path.exists(src):
                shutil.copy(src, dst)
        
        # Execute pipeline stages
        discovery = DiscoveryAgent(temp_email_directory)
        discovery.find_email_files()
        loaded_emails = discovery.load_emails()
        
        analysis = AnalysisAgent(loaded_emails)
        findings = analysis.analyze_emails()
        stats = analysis.get_statistics()
        
        # Verify pipeline success
        assert len(loaded_emails) > 0
        assert len(findings) > 0
        assert stats['total_emails'] == len(loaded_emails)


# =============================================================================
# TEST EXECUTION SUMMARY
# =============================================================================

if __name__ == "__main__":
    """
    Execute test suite from command line.
    
    Usage:
        python test_agent.py          # Run all tests
        pytest test_agent.py          # Run with pytest (recommended)
        pytest test_agent.py -v       # Verbose output
        pytest test_agent.py --cov    # With coverage report
    """
    pytest.main([__file__, "-v", "--tb=short"])

