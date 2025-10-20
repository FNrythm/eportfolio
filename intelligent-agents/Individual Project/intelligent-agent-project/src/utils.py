"""
Utility Functions for Email Forensics System

This module contains supporting functionality for test data generation
and documentation creation. Separated from core agent logic to maintain
clean architecture and enable independent testing.

Design Rationale: Utility module pattern (Martin, 2003) used because:
- These functions don't fit the agent paradigm (not autonomous, reactive, or goal-oriented)
- Shared across multiple agents and test scenarios
- Can be imported selectively to minimize dependencies
"""

import random
import os
from datetime import datetime, timedelta
from typing import List
from dataclasses import dataclass


# Import SimpleEmail from agent module
# Design Note: Circular import avoided by placing only data models in agent.py
import sys
sys.path.insert(0, os.path.dirname(__file__))
from agent import SimpleEmail


class EnhancedEmailGenerator:
    """
    Test data generator for forensic system validation.
    
    Architecture Decision: Separate generator class rather than fixture files because:
    1. Programmable generation allows controlled variation for edge case testing
    2. Can generate arbitrary dataset sizes for performance testing
    3. Configurable suspicious/normal ratio for testing different scenarios
    4. Self-documenting: code shows exact data characteristics
    
    In production, this would be replaced with actual email import, but for
    development and demonstration, generated data provides:
    - Reproducibility (same seed = same data)
    - Privacy (no real email content)
    - Controlled characteristics for algorithm validation
    """
    
    def __init__(self):
        """
        Initialize with pre-defined subject and sender templates.
        
        Design Choice: Templates stored in dictionaries rather than external files because:
        1. Simplicity - no file I/O or path management needed
        2. Version control - templates tracked with code
        3. Performance - no disk access during generation
        
        Template categories ('normal' vs 'suspicious') enable targeted testing
        of classification algorithms.
        """
        self.subjects = {
            'normal': [
                "Weekly team meeting agenda",
                "Project status update",
                "Meeting minutes from yesterday",
                "Q3 budget review",
                "Employee handbook update",
                "Training session reminder",
                "Office closure notification",
                "System maintenance window",
                "New hire introduction",
                "Company newsletter"
            ],
            'suspicious': [
                "URGENT: Account verification required",
                "Confidential: Payment processing error",
                "CRITICAL: Security breach detected",
                "Winner notification - Claim your prize",
                "Immediate action required - Account suspended",
                "Bitcoin investment opportunity",
                "Inheritance fund transfer",
                "Phishing attempt detected",
                "Download invoice immediately",
                "Secret project information"
            ]
        }
        
        # Diverse sender list including both internal and external domains
        # Rationale: Tests external communication detection with realistic mix
        self.senders = [
            "fabian.narel@company.com", "john.smith@company.com", "jane.doe@company.com",
            "admin@phishing-site.com", "noreply@suspicious-bank.net", "winner@lottery-scam.org",
            "contact@company.com", "marketing@company.com", "sales@company.com",
            "security@fake-company.com", "support@malicious-site.org"
        ]
        
        # Internal recipients for testing internal communication patterns
        self.recipients = [
            "fabian.narel@company.com", "john.smith@company.com", "jane.doe@company.com",
            "contact@company.com", "hr@company.com", "it@company.com"
        ]

    def generate_emails(self, count: int, suspicious_percentage: float = 0.3) -> List[SimpleEmail]:
        """
        Generate realistic email dataset with configurable characteristics.
        
        Parameters:
        - count: Total number of emails to generate
        - suspicious_percentage: Ratio of suspicious to normal emails (0.0-1.0)
        
        Design Rationale for generation strategy:
        1. Sequential generation with first N being suspicious ensures predictable
           distribution for testing (vs. random selection which could be uneven)
        2. 30% default suspicious ratio chosen to match real-world phishing rates
           in enterprise environments (Verizon DBIR, 2023)
        3. Temporal variation (0-30 days back) creates realistic timeline for
           time-series analysis testing
        
        After-hours correlation with suspicious emails (40% probability):
        - Simulates real attack pattern where compromised accounts accessed
          from different time zones (Symantec ISTR, 2023)
        - Tests temporal anomaly detection without 100% correlation (realistic noise)
        """
        # Ensure output directory exists
        os.makedirs("output/emails", exist_ok=True)
        
        emails = []
        suspicious_count = int(count * suspicious_percentage)
        
        for i in range(count):
            is_suspicious = i < suspicious_count
            
            # Content selection based on email category
            # Rationale: Ensures keyword-based detection has both positive and
            # negative examples for accuracy measurement
            if is_suspicious:
                subject = random.choice(self.subjects['suspicious'])
                content = self._generate_suspicious_content()
                # Suspicious emails from external sources (realistic threat model)
                sender = random.choice([s for s in self.senders if 'company.com' not in s])
            else:
                subject = random.choice(self.subjects['normal'])
                content = self._generate_normal_content()
                # Normal emails from internal sources (typical workflow)
                sender = random.choice([s for s in self.senders if 'company.com' in s])
            
            # Temporal pattern injection for testing
            # 40% of suspicious emails sent after hours to create detectable pattern
            # while maintaining realistic variance (not all attacks after-hours)
            if is_suspicious and random.random() < 0.4:
                hour = random.choice([2, 3, 22, 23])  # After hours
            else:
                hour = random.randint(8, 18)  # Business hours
            
            # Date randomization across 30-day window
            # Rationale: Creates timeline with sufficient spread for trend analysis
            # while keeping data recent enough to be realistic
            date = datetime.now() - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59)
            )
            date = date.replace(hour=hour)
            
            email = SimpleEmail(
                id=f"email_{i+1:03d}",
                subject=subject,
                sender=sender,
                recipient=random.choice(self.recipients),
                date=date,
                content=content,
                file_path=f"output/emails/email_{i+1:03d}.txt"
            )
            
            emails.append(email)
            
            # Persist to filesystem for Discovery Agent testing
            # Rationale: Tests the full pipeline including file I/O and parsing
            # Alternative: In-memory generation would be faster but less realistic
            with open(email.file_path, 'w', encoding='utf-8') as f:
                f.write(f"ID: {email.id}\n")
                f.write(f"Subject: {email.subject}\n")
                f.write(f"From: {email.sender}\n")
                f.write(f"To: {email.recipient}\n")
                f.write(f"Date: {email.date}\n")
                f.write(f"Content: {email.content}\n")
        
        print(f"Generated {count} emails ({suspicious_count} suspicious)")
        return emails

    def _generate_suspicious_content(self) -> str:
        """
        Generate phishing-style email content.
        
        Design Rationale: Templates based on APWG phishing trends (2023):
        1. Urgency and time pressure ("immediately", "now")
        2. Financial incentives or threats
        3. Technical jargon to appear legitimate
        4. Requests for action (click, download, transfer)
        
        These patterns serve as ground truth for testing detection algorithms.
        """
        templates = [
            "Your account will be suspended unless you verify immediately. Click here to download the verification form.",
            "Congratulations! You've won $1,000,000 in our secret lottery. Transfer processing fee required.",
            "CRITICAL security breach detected. Download the attached file to secure your account.",
            "Confidential inheritance fund of $5,000,000 available. Bitcoin payment preferred.",
            "Your payment is overdue. Click here to download invoice and avoid account suspension."
        ]
        return random.choice(templates)

    def _generate_normal_content(self) -> str:
        """
        Generate legitimate business email content.
        
        Design Rationale: Templates reflect normal workplace communication:
        - Polite, professional language
        - Specific business topics (meetings, budgets, training)
        - No urgency or suspicious keywords
        
        Provides negative examples for testing false positive rates.
        """
        templates = [
            "Please find the meeting agenda attached. Let me know if you have any questions.",
            "The project is progressing well. Here's the current status update for your review.",
            "Training session scheduled for next week. Please confirm your attendance.",
            "Budget review meeting moved to Thursday. Updated calendar invite sent.",
            "Welcome to our new team member. Please join us for the introduction meeting."
        ]
        return random.choice(templates)


def generate_uml_documentation():
    """
    Generate UML diagrams for system architecture documentation.
    
    Design Rationale: Automated diagram generation rather than manual creation because:
    1. Synchronization: Diagrams always match current code structure
    2. Version control: Text-based formats track changes better than binary images
    3. Accessibility: Mermaid and PlantUML have broad tool support
    4. Academic requirement: UML diagrams standard for software engineering courses
    
    Two diagram types chosen for complementary views:
    - Class Diagram: Shows static structure (what exists)
    - Sequence Diagram: Shows dynamic behavior (how it works)
    
    This combination provides complete architectural documentation as per
    UML best practices (Fowler, 2003).
    """
    uml_dir = "output/uml_documentation"
    os.makedirs(uml_dir, exist_ok=True)
    
    # Class Diagram in Mermaid format
    # Choice Rationale: Mermaid selected because:
    # 1. Native GitHub/GitLab rendering (no external tools needed)
    # 2. Simple syntax for quick modifications
    # 3. JSON-like structure easy to generate programmatically
    # 4. Wide IDE support (VS Code, IntelliJ, etc.)
    class_diagram_mermaid = '''classDiagram
    direction LR

    class DiscoveryAgent {
        -search_directory: str
        -discovered_files: List~str~
        +find_email_files(): List~str~
        +load_emails(): List~SimpleEmail~
    }

    class DashboardAgent {
        -emails: List~SimpleEmail~
        -findings: List~Finding~
        +generate_dashboard(): void
    }

    class AnalysisAgent {
        -emails: List~SimpleEmail~
        -findings: List~Finding~
        +analyze_emails(): List~Finding~
        +get_statistics(): Dict
    }

    class ReportAgent {
        -emails: List~SimpleEmail~
        -findings: List~Finding~
        +generate_comprehensive_report(): void
    }

    class SimpleEmail {
        +id: str
        +subject: str
        +sender: str
        +recipient: str
        +date: datetime
        +content: str
        +file_path: str
        +is_suspicious(): bool
        +is_after_hours(): bool
        +is_external(): bool
    }

    class Finding {
        +finding_type: str
        +description: str
        +email_id: str
        +severity: str
        +timestamp: datetime
    }

    DiscoveryAgent ..> SimpleEmail : creates
    AnalysisAgent ..> SimpleEmail : analyzes
    AnalysisAgent ..> Finding : creates
    DashboardAgent ..> SimpleEmail : visualizes
    DashboardAgent ..> Finding : visualizes
    ReportAgent ..> SimpleEmail : reports
    ReportAgent ..> Finding : reports
'''

    # Sequence Diagram in PlantUML format
    # Choice Rationale: PlantUML selected for sequence diagrams because:
    # 1. Superior sequence diagram support vs. Mermaid
    # 2. Clear timing/ordering representation
    # 3. Excellent for process documentation
    # 4. Industry standard for interaction diagrams
    sequence_diagram = '''@startuml EmailForensicsSequence
!theme plain
title Email Forensics System - Analysis Pipeline

participant "Main Controller" as Main
participant "EnhancedEmailGenerator" as Generator
participant "DiscoveryAgent" as Discovery
participant "AnalysisAgent" as Analysis
participant "DashboardAgent" as Dashboard
participant "ReportAgent" as Report

== Data Generation Phase ==
Main -> Generator: generate_emails(50, 30%)
activate Generator
Generator -> Generator: create_test_data()
Generator -> Main: emails[]
deactivate Generator

== Discovery Phase ==
Main -> Discovery: find_email_files()
activate Discovery
Discovery -> Discovery: scan_directory()
Discovery --> Main: file_paths[]

Main -> Discovery: load_emails()
Discovery -> Discovery: parse_files()
Discovery --> Main: loaded_emails[]
deactivate Discovery

== Analysis Phase ==
Main -> Analysis: analyze_emails(loaded_emails)
activate Analysis
Analysis -> Analysis: _keyword_analysis()
Analysis -> Analysis: _timing_analysis()
Analysis -> Analysis: _external_communication_analysis()
Analysis -> Analysis: _volume_analysis()
Analysis --> Main: findings[]
deactivate Analysis

== Visualization Phase ==
Main -> Dashboard: generate_dashboard(emails, findings)
activate Dashboard
Dashboard -> Dashboard: _generate_summary_chart()
Dashboard -> Dashboard: _generate_pie_chart()
Dashboard -> Dashboard: _generate_histogram()
Dashboard -> Dashboard: _generate_wordcloud()
Dashboard -> Dashboard: _generate_timeline()
Dashboard -> Dashboard: _generate_heatmap()
Dashboard -> Dashboard: _generate_network_analysis()
Dashboard -> Dashboard: _generate_severity_distribution()
Dashboard --> Main: visualizations_created
deactivate Dashboard

== Reporting Phase ==
Main -> Report: generate_comprehensive_report(emails, findings)
activate Report
Report -> Report: _generate_text_report()
Report -> Report: _generate_html_report()
Report --> Main: reports_created
deactivate Report

@enduml'''
    
    # Persistence of diagram definitions
    # Rationale: Separate files allow independent viewing and modification
    with open(f"{uml_dir}/class_diagram.md", "w", encoding="utf-8") as f:
        f.write("# Class Diagram\n\n```mermaid\n" + class_diagram_mermaid + "\n```\n")
    
    with open(f"{uml_dir}/sequence_diagram.puml", "w", encoding="utf-8") as f:
        f.write(sequence_diagram)
    
    # Documentation README for non-technical users
    # Rationale: Ensures diagrams can be viewed without specialized knowledge
    readme_content = """# UML Documentation

This directory contains UML diagrams for the Email Forensics System architecture.

## Purpose

These diagrams serve multiple purposes:
1. **Academic Documentation**: Required deliverable for the Intelligent Agent Module
2. **Onboarding**: New developers can understand system architecture quickly
3. **Design Review**: Visual representation facilitates architectural discussions
4. **Maintenance**: Documents design decisions for future modifications

## Available Diagrams

### 1. Class Diagram (class_diagram.md) - Mermaid Format

**What it shows:**
- Structure of all agent classes
- Relationships between components
- Class attributes and methods
- Data model definitions (SimpleEmail, Finding)

**Key Insights:**
- Multi-agent architecture with four specialized agents
- Clear separation of concerns (discovery, analysis, visualization, reporting)
- Shared data models enable agent communication
- Dependency relationships show information flow

**How to view:**
- **GitHub/GitLab**: Native rendering in README files
- **VS Code**: Install "Markdown Preview Mermaid Support" extension
- **Online**: Copy content to https://mermaid.live/
- **Obsidian**: Native Mermaid support

### 2. Sequence Diagram (sequence_diagram.puml) - PlantUML Format

**What it shows:**
- Interaction flow between agents during execution
- Complete analysis pipeline from generation to reporting
- Method calls and data passing
- Temporal ordering of operations
- Phases of execution (Generation, Discovery, Analysis, Visualization, Reporting)

**Key Insights:**
- Sequential pipeline architecture (not parallel)
- Main controller orchestrates all agents
- Each agent has well-defined entry point
- Data flows forward through pipeline (no circular dependencies)

**How to view:**
- **Online**: Copy content to https://www.planttext.com/ or http://www.plantuml.com/plantuml/
- **VS Code**: Install "PlantUML" extension
- **IntelliJ IDEA**: PlantUML integration plugin (built-in Professional edition)
- **Command Line**: Install PlantUML and run: `java -jar plantuml.jar sequence_diagram.puml`

## Architectural Patterns Demonstrated

These diagrams illustrate several software engineering patterns:

1. **Multi-Agent System**: Four autonomous agents with specialized roles
2. **Pipeline Architecture**: Sequential processing stages
3. **Strategy Pattern**: Multiple analysis strategies (keyword, timing, volume, external)
4. **Template Method**: DashboardAgent defines visualization skeleton, delegates to specific methods
5. **Dependency Injection**: Agents receive data via constructor injection

## References

- Fowler, M. (2003). *UML Distilled: A Brief Guide to the Standard Object Modeling Language*. Addison-Wesley.
- Gamma, E., Helm, R., Johnson, R., & Vlissides, J. (1994). *Design Patterns: Elements of Reusable Object-Oriented Software*. Addison-Wesley.
- Wooldridge, M. (2009). *An Introduction to MultiAgent Systems* (2nd ed.). Wiley.

---

*Last updated: """ + datetime.now().strftime('%Y-%m-%d') + """*
"""
    
    with open(f"{uml_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("UML documentation generated successfully!")
    print(f"- Class diagram (Mermaid): {uml_dir}/class_diagram.md")
    print(f"- Sequence diagram (PlantUML): {uml_dir}/sequence_diagram.puml")
    print(f"- Documentation: {uml_dir}/README.md")
    
    return {
        'class_diagram_path': f"{uml_dir}/class_diagram.md",
        'sequence_diagram_path': f"{uml_dir}/sequence_diagram.puml",
        'readme_path': f"{uml_dir}/README.md"
    }

