"""
Multi-Agent Email Forensics System - Core Agent Implementation

This module implements the four specialized agents that form the multi-agent architecture.
The design follows the principle of separation of concerns, where each agent has a single,
well-defined responsibility in the forensics analysis pipeline.

Design Rationale:
- Multi-agent architecture chosen over monolithic design to enable parallel processing,
  independent testing, and easier maintenance (Wooldridge, 2009)
- Reactive agents with internal state allow for both immediate response and learning
  from accumulated data patterns (Russell & Norvig, 2020)
"""

import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from typing import List
from collections import Counter
from wordcloud import WordCloud
from dataclasses import dataclass


# Data Models
@dataclass
class SimpleEmail:
    """
    Email data structure with forensic analysis capabilities.
    
    Design Note: Dataclass chosen over traditional class for immutability and 
    automatic generation of __init__, __repr__, and __eq__ methods, reducing
    boilerplate and potential bugs (Python Software Foundation, 2023).
    """
    id: str
    subject: str
    sender: str
    recipient: str
    date: datetime
    content: str
    file_path: str

    def is_suspicious(self) -> bool:
        """
        Keyword-based suspicious email detection.
        
        Design Rationale: Uses a dictionary-based approach rather than regex for:
        1. Performance - O(n) single pass vs. multiple regex compilations
        2. Maintainability - Easy to extend keyword list
        3. Explainability - Clear mapping between keywords and suspicion levels
        
        Limitation: This is a basic heuristic. Production systems would use
        ML-based approaches (Radev et al., 2020) but this serves our educational
        and demonstration purposes while remaining interpretable.
        """
        suspicious_words = [
            'confidential', 'secret', 'critical', 'account', 'payment', 'transfer',
            'urgent', 'immediate', 'verify', 'suspend', 'click here', 'download',
            'invoice', 'refund', 'winner', 'congratulations', 'inheritance',
            'million', 'dollars', 'bitcoin', 'cryptocurrency', 'phishing'
        ]
        text_to_check = (self.subject + " " + self.content).lower()
        return any(word in text_to_check for word in suspicious_words)

    def is_after_hours(self) -> bool:
        """
        Temporal anomaly detection for after-hours communication.
        
        Design Rationale: After-hours emails (outside 8 AM - 6 PM) can indicate:
        - Compromised accounts in different time zones (Siadati et al., 2017)
        - Automated bot activity
        - Data exfiltration attempts
        
        Hardcoded 8-18 range rather than configurable to match typical corporate
        hours. Future enhancement: organization-specific working hours.
        """
        return self.date.hour < 8 or self.date.hour > 18

    def is_external(self) -> bool:
        """
        Domain-based source verification.
        
        Design Rationale: External emails represent higher risk vectors:
        - Phishing attempts (Anti-Phishing Working Group, 2023)
        - Social engineering attacks
        - Malware distribution
        
        Internal domains hardcoded for demo; production would use organization's
        verified domain list from configuration.
        """
        internal_domains = ['company.com', 'internal.org']
        sender_domain = self.sender.split('@')[-1] if '@' in self.sender else ''
        return sender_domain not in internal_domains


@dataclass
class Finding:
    """
    Security finding with severity classification.
    
    Design Note: Separate Finding class enables:
    1. Aggregation and reporting across multiple emails
    2. Severity-based prioritization for incident response
    3. Audit trail for forensic chain of custody
    """
    finding_type: str
    description: str
    email_id: str
    severity: str  # "Low", "Medium", "High"
    timestamp: datetime


class DiscoveryAgent:
    """
    File system discovery and email data extraction agent.
    
    Architecture Decision: Discovery separated from Analysis because:
    1. Single Responsibility Principle - this agent only handles I/O
    2. Allows swapping data sources (filesystem, database, API) without
       affecting downstream analysis agents
    3. Enables independent testing of parsing logic (Gamma et al., 1994)
    
    In a distributed system, this would be the first agent in the pipeline,
    potentially running on a separate node (Ferber, 1999).
    """
    
    def __init__(self, search_directory: str = "output/emails"):
        """
        Initialize with configurable search path.
        
        Design Choice: Directory injection via constructor enables:
        - Testing with mock directories
        - Multi-environment support (dev/staging/prod)
        - Parallel processing of multiple email sets
        """
        self.search_directory = search_directory
        self.discovered_files = []

    def find_email_files(self) -> List[str]:
        """
        File discovery using glob pattern matching.
        
        Implementation Note: glob.glob() chosen over os.walk() because:
        1. Simpler syntax for pattern matching
        2. Returns flat list suitable for our single-directory structure
        3. Better performance for non-recursive searches
        
        Pattern "*.txt" assumes plain text format; production systems
        would support EML, MSG, MBOX formats (Radicati Group, 2023).
        """
        pattern = os.path.join(self.search_directory, "*.txt")
        self.discovered_files = glob.glob(pattern)
        print(f"Discovered {len(self.discovered_files)} email files")
        return self.discovered_files

    def load_emails(self) -> List[SimpleEmail]:
        """
        Parse email files into structured objects.
        
        Design Rationale for error handling strategy:
        - Continue on parse errors rather than failing fast to maximize
          data recovery in forensic scenarios
        - Log each failure for post-analysis review
        - Return partial results, allowing investigation of successfully
          parsed emails even when some are corrupted
        
        This resilience is critical in forensic contexts where evidence
        may be partially damaged (Casey, 2011).
        """
        emails = []
        for file_path in self.discovered_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                    # Key-value parsing with simple colon delimiter
                    # Chosen for human readability in test data
                    email_data = {}
                    for line in lines:
                        if ':' in line:
                            key, value = line.split(':', 1)
                            email_data[key.strip()] = value.strip()
                    
                    # Robust date parsing with fallback
                    # Critical for timeline analysis despite format variations
                    if 'Date' in email_data:
                        date_str = email_data['Date']
                        try:
                            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                        except:
                            date = datetime.now()
                    else:
                        date = datetime.now()
                    
                    email = SimpleEmail(
                        id=email_data.get('ID', ''),
                        subject=email_data.get('Subject', ''),
                        sender=email_data.get('From', ''),
                        recipient=email_data.get('To', ''),
                        date=date,
                        content=email_data.get('Content', ''),
                        file_path=file_path
                    )
                    emails.append(email)
            except Exception as e:
                # Graceful degradation: log and continue
                print(f"Error loading {file_path}: {e}")
        
        print(f"Successfully loaded {len(emails)} emails")
        return emails


class AnalysisAgent:
    """
    Pattern recognition and threat detection agent.
    
    Architectural Rationale:
    - Implements multiple analysis strategies in parallel (keyword, temporal,
      volume, external source) to provide comprehensive threat assessment
    - Each strategy is independent, allowing easy addition of new detection
      methods without modifying existing code (Open/Closed Principle)
    - Findings accumulated in a list rather than immediately acted upon,
      supporting batch processing and ML training data collection
    
    This design enables the agent to evolve from rule-based to ML-based
    detection without changing its interface (Nilsson, 1998).
    """
    
    def __init__(self, emails: List[SimpleEmail]):
        """
        Constructor accepts email collection for analysis.
        
        Design Choice: Entire dataset passed at initialization because:
        1. Enables cross-email pattern detection (volume analysis)
        2. Supports statistical methods requiring full dataset
        3. Simplifies state management vs. incremental processing
        
        Trade-off: Higher memory usage, but acceptable for typical
        forensic investigations (<100k emails) (Garfinkel, 2010).
        """
        self.emails = emails
        self.findings = []

    def analyze_emails(self) -> List[Finding]:
        """
        Orchestrator for multiple analysis strategies.
        
        Design Pattern: Template Method Pattern (Gamma et al., 1994)
        - Main method defines analysis skeleton
        - Delegates to specialized private methods
        - Easy to add new analysis types by adding method calls
        - Maintains consistent finding collection and reporting
        """
        self.findings = []
        
        # Execute analysis pipeline
        self._keyword_analysis()
        self._timing_analysis()
        self._external_communication_analysis()
        self._volume_analysis()
        
        print(f"Analysis complete: {len(self.findings)} findings")
        return self.findings

    def _keyword_analysis(self):
        """
        Content-based threat detection.
        
        Severity Assignment Logic:
        - High: Urgent action words (suspend, critical) indicating time pressure
          (common in phishing - APWG 2023 report)
        - Medium: Suspicious but less urgent keywords
        
        This tiered approach enables prioritized incident response.
        """
        for email in self.emails:
            if email.is_suspicious():
                # Severity escalation for high-pressure keywords
                # Rationale: Urgency is a primary phishing indicator
                severity = "High" if any(word in email.subject.lower() 
                                         for word in ['urgent', 'critical', 'suspend']) else "Medium"
                
                finding = Finding(
                    finding_type="Suspicious Keywords",
                    description=f"Email contains suspicious keywords: {email.subject}",
                    email_id=email.id,
                    severity=severity,
                    timestamp=datetime.now()
                )
                self.findings.append(finding)

    def _timing_analysis(self):
        """
        Temporal anomaly detection.
        
        Theoretical Basis: Temporal patterns in email behavior can reveal:
        - Compromised accounts accessed from different time zones
        - Automated malware activity
        - Insider threats working outside normal hours (Lundin & Jonsson, 2002)
        
        Classified as Medium severity because context-dependent - may be
        legitimate for global teams or flexible work schedules.
        """
        for email in self.emails:
            if email.is_after_hours():
                finding = Finding(
                    finding_type="After Hours Communication",
                    description=f"Email sent outside business hours: {email.date.strftime('%H:%M')}",
                    email_id=email.id,
                    severity="Medium",
                    timestamp=datetime.now()
                )
                self.findings.append(finding)

    def _external_communication_analysis(self):
        """
        Source verification and perimeter monitoring.
        
        Security Rationale: External emails are primary attack vectors:
        - 36% of breaches involved phishing (Verizon DBIR, 2023)
        - External sources have lower trust levels by default
        - Policy violations (data exfiltration to external addresses)
        
        Low severity as external communication is often legitimate;
        requires context for accurate threat assessment.
        """
        for email in self.emails:
            if email.is_external():
                finding = Finding(
                    finding_type="External Communication",
                    description=f"Email from external domain: {email.sender}",
                    email_id=email.id,
                    severity="Low",
                    timestamp=datetime.now()
                )
                self.findings.append(finding)

    def _volume_analysis(self):
        """
        Anomaly detection via statistical volume analysis.
        
        Design Rationale: Counter class from collections used because:
        1. Optimized C implementation for counting operations
        2. Cleaner syntax than manual dictionary management
        3. Supports most_common() for easy high-volume detection
        
        Threshold of 5 emails chosen as baseline for demo; production
        systems would use standard deviation or ML-based anomaly detection
        (Chandola et al., 2009) calculated from historical patterns.
        """
        sender_counts = Counter(email.sender for email in self.emails)
        
        # Threshold-based anomaly flagging
        # Future: Replace with statistical outlier detection
        for sender, count in sender_counts.items():
            if count > 5:
                finding = Finding(
                    finding_type="High Volume Sender",
                    description=f"Sender has {count} emails in dataset",
                    email_id="multiple",
                    severity="Medium",
                    timestamp=datetime.now()
                )
                self.findings.append(finding)

    def get_statistics(self) -> dict:
        """
        Statistical summary generation for reporting.
        
        Design Choice: Returns dictionary rather than custom object for:
        1. Easy JSON serialization for web APIs
        2. Flexible schema evolution
        3. Compatibility with various reporting frameworks
        
        Statistics chosen to align with NIST forensics reporting standards
        (NIST SP 800-86, 2006).
        """
        total_emails = len(self.emails)
        suspicious_emails = sum(1 for email in self.emails if email.is_suspicious())
        external_emails = sum(1 for email in self.emails if email.is_external())
        after_hours_emails = sum(1 for email in self.emails if email.is_after_hours())
        
        return {
            "total_emails": total_emails,
            "suspicious_emails": suspicious_emails,
            "external_emails": external_emails,
            "after_hours_emails": after_hours_emails,
            "total_findings": len(self.findings),
            "high_severity_findings": sum(1 for f in self.findings if f.severity == "High"),
            "medium_severity_findings": sum(1 for f in self.findings if f.severity == "Medium"),
            "low_severity_findings": sum(1 for f in self.findings if f.severity == "Low")
        }


class DashboardAgent:
    """
    Visualization and reporting agent for forensic findings.
    
    Architectural Decision: Separate agent for visualization because:
    1. Visualization is computationally expensive - can be offloaded to different
       process/machine in distributed system
    2. Multiple output formats (charts, HTML) benefit from centralized management
    3. Visualization logic changes frequently; isolation reduces impact on
       core analysis agents (Martin, 2003)
    
    Design Pattern: Strategy Pattern for different visualization types,
    allowing easy addition of new chart types without modifying existing code.
    """
    
    def __init__(self, emails: List[SimpleEmail], findings: List[Finding]):
        """
        Initialization with full dataset for cross-correlation visualizations.
        
        Both emails and findings required because:
        - Some visualizations show raw data (email volume over time)
        - Others show analysis results (finding severity distribution)
        - Cross-correlation charts (e.g., suspicious emails by hour)
          require both datasets
        """
        self.emails = emails
        self.findings = findings
        self.output_dir = "output/visualizations"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_dashboard(self):
        """
        Orchestrates generation of all visualization types.
        
        Design Note: Sequential execution rather than parallel for simplicity,
        but structure allows easy conversion to parallel processing using
        multiprocessing or asyncio for performance improvement.
        
        Matplotlib state set globally to ensure consistent styling across
        all visualizations (Gestalt principles of visual design).
        """
        # Global styling for visual consistency
        # Rationale: Professional appearance, reduces cognitive load in interpretation
        plt.style.use('default')
        sns.set_palette("husl")
        
        # Generate all visualization types
        # Each method self-contained for independent testing and modification
        self._generate_summary_chart()
        self._generate_pie_chart()
        self._generate_histogram()
        self._generate_wordcloud()
        self._generate_timeline()
        self._generate_heatmap()
        self._generate_network_analysis()
        self._generate_severity_distribution()
        
        print("Dashboard generation complete!")

    def _generate_summary_chart(self):
        """
        High-level overview bar chart of key metrics.
        
        Visualization Choice: Bar chart selected because:
        1. Excellent for comparing discrete categories
        2. Easy to read absolute values
        3. Familiar to non-technical stakeholders
        
        Metrics chosen to provide immediate risk assessment snapshot,
        following information dashboard design principles (Few, 2006).
        """
        stats = AnalysisAgent(self.emails).get_statistics()
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        categories = ['Total Emails', 'Suspicious', 'External', 'After Hours', 'Findings']
        values = [stats['total_emails'], stats['suspicious_emails'], 
                 stats['external_emails'], stats['after_hours_emails'], stats['total_findings']]
        
        # Color coding for semantic meaning
        # Red for threats, amber for warnings, green for info, purple/blue for neutral
        bars = ax.bar(categories, values, color=['#3498db', '#e74c3c', '#f39c12', '#9b59b6', '#2ecc71'])
        
        # Value labels for precise reading without consulting axis
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax.set_title('Email Forensics Summary Statistics', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Count', fontsize=12)
        ax.grid(True, alpha=0.3)  # Subtle grid for easier value estimation
        plt.xticks(rotation=45)
        plt.tight_layout()  # Prevents label cutoff
        plt.savefig(f"{self.output_dir}/summary_chart.png", dpi=300, bbox_inches='tight')
        plt.close()  # Close to free memory; critical in batch processing

    def _generate_pie_chart(self):
        """
        Proportional representation of normal vs. suspicious emails.
        
        Visualization Choice: Pie chart appropriate here because:
        1. Only two categories (binary classification)
        2. Emphasizes proportion rather than absolute values
        3. "Exploded" slice draws attention to threat category
        
        Generally avoid pie charts for >3 categories due to angle
        comparison difficulties (Cleveland & McGill, 1984).
        """
        suspicious_count = sum(1 for email in self.emails if email.is_suspicious())
        normal_count = len(self.emails) - suspicious_count
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 8))
        
        labels = ['Normal Emails', 'Suspicious Emails']
        sizes = [normal_count, suspicious_count]
        colors = ['#2ecc71', '#e74c3c']  # Green/red for good/bad semantic mapping
        explode = (0, 0.1)  # Explode suspicious slice for emphasis
        
        wedges, texts, autotexts = ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                                         autopct='%1.1f%%', shadow=True, startangle=90,
                                         textprops={'fontsize': 12})
        
        ax.set_title('Email Distribution: Normal vs Suspicious', fontsize=16, fontweight='bold', pad=20)
        plt.savefig(f"{self.output_dir}/email_distribution_pie.png", dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_histogram(self):
        """
        Temporal distribution analysis via histogram.
        
        Design Rationale: 24-hour binning chosen to:
        1. Reveal circadian patterns in email traffic
        2. Highlight after-hours anomalies (colored red)
        3. Support policy enforcement (e.g., after-hours alerts)
        
        Color coding (blue=normal, red=after-hours) uses preattentive
        visual processing for immediate pattern recognition (Ware, 2020).
        """
        hours = [email.date.hour for email in self.emails]
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 6))
        
        n, bins, patches = ax.hist(hours, bins=24, range=(0, 24), color='skyblue', 
                                  alpha=0.7, edgecolor='black', linewidth=0.5)
        
        # After-hours highlighting using conditional color coding
        # Rationale: Immediate visual identification of temporal anomalies
        for i, patch in enumerate(patches):
            if bins[i] < 8 or bins[i] > 18:
                patch.set_facecolor('#e74c3c')
                patch.set_alpha(0.8)
        
        ax.set_title('Email Distribution by Hour of Day', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Number of Emails', fontsize=12)
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, alpha=0.3)
        
        # Legend for color interpretation
        normal_patch = plt.Rectangle((0,0),1,1, facecolor='skyblue', alpha=0.7, label='Business Hours')
        after_patch = plt.Rectangle((0,0),1,1, facecolor='#e74c3c', alpha=0.8, label='After Hours')
        ax.legend(handles=[normal_patch, after_patch])
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/hourly_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_wordcloud(self):
        """
        Visual term frequency analysis using word cloud.
        
        Visualization Choice: Word cloud selected because:
        1. Intuitive representation of term frequency (size = importance)
        2. Pattern recognition: common phishing keywords become obvious
        3. Engaging visual for presentations
        
        Limitations: Not quantitative, doesn't show relationships between terms.
        Better for initial exploration than rigorous analysis (McNaught & Lam, 2010).
        """
        all_subjects = ' '.join([email.subject for email in self.emails])
        
        # WordCloud configuration for optimal readability
        # max_words=100 prevents clutter while capturing key themes
        # relative_scaling balances frequent vs. distinctive terms
        wordcloud = WordCloud(width=1200, height=600, background_color='white',
                             colormap='viridis', max_words=100, relative_scaling=0.5).generate(all_subjects)
        
        fig, ax = plt.subplots(1, 1, figsize=(15, 8))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')  # Remove axes for cleaner presentation
        ax.set_title('Email Subject Word Cloud', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/wordcloud.png", dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_timeline(self):
        """
        Time series visualization of email activity.
        
        Design Rationale: Timeline critical for forensic analysis:
        1. Reveals attack timing (coordinated campaigns show spikes)
        2. Supports incident reconstruction
        3. Identifies long-term trends vs. anomalies
        
        Line chart with fill emphasizes volume trends over time,
        following time series visualization best practices (Tufte, 2001).
        """
        # Daily aggregation chosen over hourly to reduce noise
        # Trade-off: Lose intraday patterns but gain long-term clarity
        dates = [email.date.date() for email in self.emails]
        date_counts = Counter(dates)
        
        sorted_dates = sorted(date_counts.keys())
        counts = [date_counts[date] for date in sorted_dates]
        
        fig, ax = plt.subplots(1, 1, figsize=(14, 6))
        
        # Line + area fill combination shows both trend and magnitude
        ax.plot(sorted_dates, counts, marker='o', linewidth=2, markersize=6, color='#3498db')
        ax.fill_between(sorted_dates, counts, alpha=0.3, color='#3498db')
        
        ax.set_title('Email Activity Timeline', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Number of Emails', fontsize=12)
        ax.grid(True, alpha=0.3)
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/timeline.png", dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_heatmap(self):
        """
        Two-dimensional temporal pattern visualization.
        
        Design Rationale: Heatmap chosen for day-hour correlation because:
        1. Shows patterns in 2D data (day × hour) more effectively than
           multiple line charts
        2. Color intensity leverages preattentive processing
        3. Reveals "hotspots" of activity immediately
        
        This visualization type particularly effective for identifying:
        - Weekly patterns (e.g., Friday afternoon spikes)
        - After-hours anomalies on specific days
        - Time-zone related patterns (Wilkinson, 2005)
        """
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        hours = list(range(24))
        
        # 2D matrix initialization for heatmap data
        heatmap_data = [[0 for _ in hours] for _ in days]
        
        # Population of matrix from email timestamps
        for email in self.emails:
            day_idx = email.date.weekday()
            hour = email.date.hour
            heatmap_data[day_idx][hour] += 1
        
        fig, ax = plt.subplots(1, 1, figsize=(16, 8))
        
        # YlOrRd colormap: yellow (low) to red (high) matches heat metaphor
        im = ax.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
        
        # Explicit labeling critical for interpretation
        ax.set_xticks(range(len(hours)))
        ax.set_yticks(range(len(days)))
        ax.set_xticklabels(hours)
        ax.set_yticklabels(days)
        
        # Colorbar with explicit labeling for quantitative interpretation
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Number of Emails', rotation=270, labelpad=20)
        
        ax.set_title('Email Activity Heatmap (Day vs Hour)', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Hour of Day', fontsize=12)
        ax.set_ylabel('Day of Week', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/activity_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_network_analysis(self):
        """
        Communication pattern visualization using network metrics.
        
        Design Rationale: Domain-level aggregation chosen because:
        1. Individual email addresses too granular for pattern recognition
        2. Domain shows organizational relationships
        3. Highlights external vs. internal communication patterns
        
        Horizontal bar chart selected for:
        - Easy reading of long domain names
        - Natural ordering by frequency
        - Space efficiency for labels (Robbins, 2013)
        """
        # Domain extraction and aggregation
        # Rationale: Organization-level view more actionable than individual users
        connections = Counter()
        for email in self.emails:
            sender_domain = email.sender.split('@')[-1] if '@' in email.sender else email.sender
            recipient_domain = email.recipient.split('@')[-1] if '@' in email.recipient else email.recipient
            connections[(sender_domain, recipient_domain)] += 1
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        
        # Top 10 chosen to avoid visual clutter while showing key patterns
        top_connections = connections.most_common(10)
        labels = [f"{sender} -> {recipient}" for (sender, recipient), count in top_connections]
        counts = [count for (sender, recipient), count in top_connections]
        
        bars = ax.barh(range(len(labels)), counts, color='lightcoral')
        ax.set_yticks(range(len(labels)))
        ax.set_yticklabels(labels)
        ax.set_xlabel('Number of Emails')
        ax.set_title('Top Email Communication Paths', fontsize=16, fontweight='bold', pad=20)
        
        # Value labels for precise reading
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                   f'{int(width)}', ha='left', va='center')
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/network_analysis.png", dpi=300, bbox_inches='tight')
        plt.close()

    def _generate_severity_distribution(self):
        """
        Risk assessment summary visualization.
        
        Design Rationale: Severity distribution critical for:
        1. Resource allocation (high severity gets immediate attention)
        2. Trend monitoring (increasing high severity indicates growing risk)
        3. Stakeholder communication (executives need risk summaries)
        
        Color coding (green/yellow/red) uses universal traffic light
        metaphor for immediate interpretation without training (Norman, 2013).
        """
        severity_counts = Counter(finding.severity for finding in self.findings)
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        severities = ['Low', 'Medium', 'High']
        counts = [severity_counts.get(severity, 0) for severity in severities]
        colors = ['#2ecc71', '#f39c12', '#e74c3c']  # Traffic light colors
        
        bars = ax.bar(severities, counts, color=colors, alpha=0.8)
        
        # Value labels for exact counts
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                   f'{int(height)}', ha='center', va='bottom', fontweight='bold')
        
        ax.set_title('Findings by Severity Level', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('Number of Findings', fontsize=12)
        ax.grid(True, alpha=0.3, axis='y')  # Horizontal grid only for cleaner look
        
        plt.tight_layout()
        plt.savefig(f"{self.output_dir}/severity_distribution.png", dpi=300, bbox_inches='tight')
        plt.close()


class ReportAgent:
    """
    Multi-format report generation agent.
    
    Architectural Decision: Separate reporting agent because:
    1. Report formats change frequently based on stakeholder needs
    2. Reporting logic is I/O intensive; can be offloaded in distributed system
    3. Allows multiple simultaneous report formats without code duplication
    4. Supports template-based customization for different organizations
    
    Design Pattern: Strategy Pattern for different report formats (text, HTML, PDF).
    Factory Pattern could be added for report type selection (Gamma et al., 1994).
    """
    
    def __init__(self, emails: List[SimpleEmail], findings: List[Finding]):
        """
        Initialize with complete dataset for comprehensive reporting.
        
        Both datasets required because reports interleave:
        - Raw data summaries (email counts, date ranges)
        - Analysis results (findings, severity breakdown)
        - Cross-referenced information (finding → email details)
        """
        self.emails = emails
        self.findings = findings
        self.output_dir = "output/reports"
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_comprehensive_report(self):
        """
        Orchestrates generation of all report formats.
        
        Design Note: Multiple formats simultaneously generated because:
        1. Text reports for archival and grep-ability
        2. HTML reports for browser viewing and sharing
        3. Easy to extend with PDF, JSON, XML formats
        
        Sequential generation acceptable for typical datasets; parallel
        generation could be implemented using threading for larger datasets.
        """
        self._generate_text_report()
        self._generate_html_report()
        print("Report generation complete!")

    def _generate_text_report(self):
        """
        Plain text report generation for archival and CLI analysis.
        
        Format Choice: Plain text selected because:
        1. Universal compatibility (any editor, any OS)
        2. Searchable with standard tools (grep, awk, sed)
        3. Version control friendly (git diff works well)
        4. Required for audit trails and legal proceedings
        
        Structure follows NIST forensic reporting guidelines (NIST SP 800-86).
        """
        stats = AnalysisAgent(self.emails).get_statistics()
        
        # Report structure: Executive summary → statistics → detailed findings
        # Rationale: Pyramid structure (most important first) for busy readers
        report_content = f"""
EMAIL FORENSICS ANALYSIS REPORT
================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
-----------------
Total Emails Analyzed: {stats['total_emails']}
Suspicious Emails: {stats['suspicious_emails']} ({stats['suspicious_emails']/stats['total_emails']*100:.1f}%)
External Communications: {stats['external_emails']}
After-Hours Communications: {stats['after_hours_emails']}
Total Security Findings: {stats['total_findings']}

FINDINGS BREAKDOWN
------------------
High Severity: {stats['high_severity_findings']}
Medium Severity: {stats['medium_severity_findings']}
Low Severity: {stats['low_severity_findings']}

DETAILED FINDINGS
-----------------
"""
        
        # Severity-sorted findings for prioritized reading
        # Rationale: Incident responders should see critical items first
        for finding in sorted(self.findings, key=lambda x: {'High': 3, 'Medium': 2, 'Low': 1}[x.severity], reverse=True):
            report_content += f"""
Finding: {finding.finding_type}
Severity: {finding.severity}
Email ID: {finding.email_id}
Description: {finding.description}
Timestamp: {finding.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
{'='*50}
"""
        
        with open(f"{self.output_dir}/forensics_report.txt", 'w', encoding='utf-8') as f:
            f.write(report_content)

    def _generate_html_report(self):
        """
        Interactive HTML report with embedded visualizations.
        
        Design Rationale: HTML chosen for stakeholder reports because:
        1. Interactive (hover effects, collapsible sections possible)
        2. Embeds visualizations directly (no separate file management)
        3. Professional appearance for executive presentations
        4. Shareable via email or web (no special software required)
        
        Template uses Jinja2 for separation of concerns: logic vs. presentation.
        This enables non-programmers to modify report appearance.
        """
        stats = AnalysisAgent(self.emails).get_statistics()
        
        # Embedded CSS for self-contained HTML file
        # Rationale: Single-file distribution simpler than CSS + HTML
        # Trade-off: Larger file size, but acceptable for typical reports
        html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Forensics Analysis Report</title>
    <style>
        /* Modern, professional styling following web design best practices */
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        
        /* Gradient header for visual appeal and brand identity */
        .header { text-align: center; margin-bottom: 30px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; }
        
        .section { margin: 25px 0; }
        
        /* Finding cards with hover effects for interactivity */
        .finding { 
            background-color: #f8f9fa; 
            padding: 15px; 
            margin: 15px 0; 
            border-radius: 8px; 
            border-left: 5px solid #ffc107; 
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .finding:hover { transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        
        /* Severity-based color coding (traffic light metaphor) */
        .high { border-left-color: #e74c3c; background-color: #fbeae5; }
        .medium { border-left-color: #f39c12; background-color: #fef5e7; }
        .low { border-left-color: #2ecc71; background-color: #eafaf1; }
        
        /* Responsive grid for statistics display */
        .stats { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
            gap: 20px; 
            margin: 20px 0; 
        }
        .stat-box { 
            text-align: center; 
            padding: 20px; 
            background-color: #34495e; 
            color: white; 
            border-radius: 10px; 
        }
        .stat-number { font-size: 2.2em; font-weight: 700; }
        
        /* Responsive grid for visualization gallery */
        .visualizations { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr)); 
            gap: 20px; 
            margin: 20px 0; 
        }
        .viz-item { text-align: center; padding: 15px; background-color: #f8f9fa; border-radius: 8px; }
        .viz-item img { max-width: 100%; height: auto; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
        footer { text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Email Forensics Analysis Report</h1>
            <p>Multi-Agent System & Advanced Analytics Dashboard</p>
        </div>

        <div class="section">
            <h2>Executive Summary</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{{ stats.total_emails }}</div>
                    <div>Total Emails</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ stats.suspicious_emails }}</div>
                    <div>Suspicious Emails</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ stats.total_findings }}</div>
                    <div>Security Findings</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{{ stats.high_severity_findings }}</div>
                    <div>High Risk</div>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>Key Findings</h2>
            {% for finding in findings %}
            <div class="finding {{ finding.severity.lower() }}">
                <h4>{{ finding.finding_type }} - {{ finding.severity }} Severity</h4>
                <p><strong>Email:</strong> {{ finding.email_id }}</p>
                <p><strong>Description:</strong> {{ finding.description }}</p>
                <p><strong>Detected:</strong> {{ finding.timestamp.strftime('%Y-%m-%d %H:%M:%S') }}</p>
            </div>
            {% endfor %}
        </div>

        <div class="section">
            <h2>Visualizations Dashboard</h2>
            <div class="visualizations">
                <div class="viz-item">
                    <h3>Summary Statistics</h3>
                    <img src="../visualizations/summary_chart.png" alt="Summary Chart">
                </div>
                <div class="viz-item">
                    <h3>Email Distribution</h3>
                    <img src="../visualizations/email_distribution_pie.png" alt="Distribution Pie Chart">
                </div>
                <div class="viz-item">
                    <h3>Hourly Activity</h3>
                    <img src="../visualizations/hourly_distribution.png" alt="Hourly Distribution">
                </div>
                <div class="viz-item">
                    <h3>Subject Analysis</h3>
                    <img src="../visualizations/wordcloud.png" alt="Word Cloud">
                </div>
                <div class="viz-item">
                    <h3>Timeline Analysis</h3>
                    <img src="../visualizations/timeline.png" alt="Timeline">
                </div>
                <div class="viz-item">
                    <h3>Activity Heatmap</h3>
                    <img src="../visualizations/activity_heatmap.png" alt="Activity Heatmap">
                </div>
                <div class="viz-item">
                    <h3>Communication Patterns</h3>
                    <img src="../visualizations/network_analysis.png" alt="Network Analysis">
                </div>
                <div class="viz-item">
                    <h3>Risk Assessment</h3>
                    <img src="../visualizations/severity_distribution.png" alt="Severity Distribution">
                </div>
            </div>
        </div>

        <footer>
            <p>Report generated by Multi-Agent Email Forensics System | {{ timestamp }}</p>
        </footer>
    </div>
</body>
</html>
        """
        
        # Jinja2 template rendering with context injection
        # Rationale: Clean separation of data and presentation logic
        from jinja2 import Template
        template = Template(html_template)
        html_content = template.render(
            stats=stats,
            findings=self.findings,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(f"{self.output_dir}/forensics_report.html", 'w', encoding='utf-8') as f:
            f.write(html_content)

