"""
Main Entry Point for Email Forensics System

This module orchestrates the multi-agent analysis pipeline, coordinating
data flow between specialized agents. Acts as the "blackboard" architecture
pattern where agents communicate through shared data structures.

Design Rationale: Main orchestrator separated from agent logic because:
1. Agents remain independent and reusable in different contexts
2. Pipeline order can be modified without changing agent code
3. Error handling centralized for consistent behavior
4. Enables future expansion to parallel/distributed execution

References:
- Ferber, J. (1999). Multi-Agent Systems: An Introduction to Distributed AI
- Nii, H. P. (1986). Blackboard Systems: The Blackboard Model of Problem Solving
"""

import os
import sys
from datetime import datetime

# Ensure output directories exist before any agent operations
# Rationale: Fail-fast if filesystem permissions insufficient,
# rather than partial execution with missing outputs
os.makedirs("output", exist_ok=True)
os.makedirs("output/emails", exist_ok=True)
os.makedirs("output/visualizations", exist_ok=True)
os.makedirs("output/reports", exist_ok=True)
os.makedirs("output/uml_documentation", exist_ok=True)

# Import agents and utilities
from agent import DiscoveryAgent, AnalysisAgent, DashboardAgent, ReportAgent
from utils import EnhancedEmailGenerator, generate_uml_documentation


def run_email_forensics_system(email_count: int = 50, suspicious_ratio: float = 0.3):
    """
    Execute the complete multi-agent forensic analysis pipeline.
    
    Parameters:
    - email_count: Number of test emails to generate (default: 50)
    - suspicious_ratio: Proportion of suspicious emails (default: 0.3 = 30%)
    
    Architecture Pattern: Pipeline Architecture (Shaw & Garlan, 1996)
    - Each stage processes data and passes results to next stage
    - Stages are independent and can be tested separately
    - Linear flow simplifies reasoning about data transformations
    
    Design Decision: Single-threaded sequential execution chosen because:
    1. Simplicity: Easier to debug and maintain than parallel version
    2. Dependencies: Each stage requires previous stage's output
    3. Performance: For typical dataset sizes (<10k emails), overhead of
       threading/multiprocessing exceeds benefits
    4. Determinism: Sequential execution ensures reproducible results
       for testing and demonstrations
    
    Future Enhancement: For large-scale deployments (>100k emails),
    this could be refactored to use:
    - Multiprocessing for CPU-bound analysis stage
    - Async I/O for report generation stage
    - Message queue (RabbitMQ/Kafka) for distributed processing
    """
    
    print("\n" + "="*70)
    print("MULTI-AGENT EMAIL FORENSICS SYSTEM")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Configuration: {email_count} emails, {suspicious_ratio*100:.0f}% suspicious")
    print("="*70 + "\n")
    
    try:
        # =================================================================
        # STAGE 1: DATA GENERATION
        # =================================================================
        # Generate synthetic test data for demonstration and validation
        # In production: Replace with actual email import from mail server/PST files
        
        print("="*70)
        print("STAGE 1: DATA GENERATION")
        print("="*70)
        print("Generating synthetic email dataset for analysis...\n")
        
        generator = EnhancedEmailGenerator()
        emails = generator.generate_emails(email_count, suspicious_ratio)
        
        print(f"✓ Generated {len(emails)} test emails")
        print(f"  - Suspicious: {int(email_count * suspicious_ratio)}")
        print(f"  - Normal: {email_count - int(email_count * suspicious_ratio)}")
        print(f"  - Location: output/emails/\n")
        
        # =================================================================
        # STAGE 2: DISCOVERY
        # =================================================================
        # Autonomous agent locates and loads email files from filesystem
        # Demonstrates agent autonomy: operates independently with minimal instruction
        
        print("="*70)
        print("STAGE 2: DISCOVERY")
        print("="*70)
        print("DiscoveryAgent scanning filesystem and loading emails...\n")
        
        discovery_agent = DiscoveryAgent()
        discovered_files = discovery_agent.find_email_files()
        loaded_emails = discovery_agent.load_emails()
        
        print(f"✓ Discovered {len(discovered_files)} email files")
        print(f"✓ Successfully parsed {len(loaded_emails)} emails")
        
        # Data integrity check
        # Rationale: Early detection of parsing issues before expensive analysis
        if len(loaded_emails) != len(discovered_files):
            print(f"⚠ Warning: {len(discovered_files) - len(loaded_emails)} files failed to parse")
        print()
        
        # =================================================================
        # STAGE 3: ANALYSIS
        # =================================================================
        # Multi-strategy threat detection using AnalysisAgent
        # Implements reactive agent model: responds to email characteristics
        # with appropriate findings
        
        print("="*70)
        print("STAGE 3: ANALYSIS")
        print("="*70)
        print("AnalysisAgent performing multi-strategy threat detection...\n")
        
        analysis_agent = AnalysisAgent(loaded_emails)
        findings = analysis_agent.analyze_emails()
        stats = analysis_agent.get_statistics()
        
        # Display analysis summary
        # Rationale: Immediate feedback for operators on threat landscape
        print(f"✓ Analysis complete: {len(findings)} findings detected")
        print(f"\nThreat Summary:")
        print(f"  - High Severity:   {stats['high_severity_findings']:>3} findings")
        print(f"  - Medium Severity: {stats['medium_severity_findings']:>3} findings")
        print(f"  - Low Severity:    {stats['low_severity_findings']:>3} findings")
        print(f"\nPattern Detection:")
        print(f"  - Suspicious content:  {stats['suspicious_emails']:>3} emails")
        print(f"  - External sources:    {stats['external_emails']:>3} emails")
        print(f"  - After-hours timing:  {stats['after_hours_emails']:>3} emails")
        print()
        
        # =================================================================
        # STAGE 4: VISUALIZATION
        # =================================================================
        # Generate comprehensive visual analytics dashboard
        # Supports human decision-making through pattern visualization
        
        print("="*70)
        print("STAGE 4: VISUALIZATION")
        print("="*70)
        print("DashboardAgent generating visual analytics...\n")
        
        dashboard_agent = DashboardAgent(loaded_emails, findings)
        dashboard_agent.generate_dashboard()
        
        print("✓ Generated 8 visualizations:")
        print("  1. Summary statistics bar chart")
        print("  2. Email distribution pie chart")
        print("  3. Hourly activity histogram")
        print("  4. Subject word cloud")
        print("  5. Activity timeline")
        print("  6. Day-hour heatmap")
        print("  7. Communication network analysis")
        print("  8. Severity distribution")
        print(f"  Location: output/visualizations/\n")
        
        # =================================================================
        # STAGE 5: REPORTING
        # =================================================================
        # Generate multi-format reports for various stakeholders
        # Demonstrates agent adaptability: same data, different formats
        
        print("="*70)
        print("STAGE 5: REPORTING")
        print("="*70)
        print("ReportAgent compiling comprehensive reports...\n")
        
        report_agent = ReportAgent(loaded_emails, findings)
        report_agent.generate_comprehensive_report()
        
        print("✓ Generated reports:")
        print("  - Text report:  output/reports/forensics_report.txt")
        print("  - HTML report:  output/reports/forensics_report.html")
        print()
        
        # =================================================================
        # STAGE 6: DOCUMENTATION
        # =================================================================
        # Generate UML architectural documentation
        # Required for academic submission and future maintenance
        
        print("="*70)
        print("STAGE 6: DOCUMENTATION")
        print("="*70)
        print("Generating UML architectural documentation...\n")
        
        uml_paths = generate_uml_documentation()
        
        print("✓ Generated UML diagrams:")
        print(f"  - Class diagram:    {uml_paths['class_diagram_path']}")
        print(f"  - Sequence diagram: {uml_paths['sequence_diagram_path']}")
        print(f"  - README:          {uml_paths['readme_path']}")
        print()
        
        # =================================================================
        # COMPLETION SUMMARY
        # =================================================================
        
        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print(f"Finished: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("\nKey Results:")
        print(f"  • Total emails processed: {stats['total_emails']}")
        print(f"  • Suspicious emails detected: {stats['suspicious_emails']} ({stats['suspicious_emails']/stats['total_emails']*100:.1f}%)")
        print(f"  • Security findings: {stats['total_findings']}")
        print(f"  • High-risk findings: {stats['high_severity_findings']}")
        print("\nOutput Files:")
        print(f"  • Raw data:        output/emails/")
        print(f"  • Visualizations:  output/visualizations/")
        print(f"  • Reports:         output/reports/")
        print(f"  • Documentation:   output/uml_documentation/")
        print("\nRecommended Next Steps:")
        print(f"  1. Open output/reports/forensics_report.html in browser")
        print(f"  2. Review high-severity findings first")
        print(f"  3. Examine visualizations for pattern confirmation")
        print(f"  4. Consult UML documentation for system architecture")
        print("="*70 + "\n")
        
        # Return results for programmatic access
        # Rationale: Enables scripting, testing, and integration with other tools
        return {
            'success': True,
            'emails': loaded_emails,
            'findings': findings,
            'statistics': stats,
            'visualization_count': 8,
            'report_paths': {
                'text': 'output/reports/forensics_report.txt',
                'html': 'output/reports/forensics_report.html'
            },
            'uml_paths': uml_paths
        }
        
    except Exception as e:
        # Centralized error handling
        # Rationale: Consistent error reporting, facilitates debugging
        print(f"\n{'='*70}")
        print("ERROR: Analysis pipeline failed")
        print("="*70)
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        print(f"\nFor assistance, please:")
        print("  1. Check logs above for specific failure point")
        print("  2. Verify all dependencies installed (pip install -r requirements.txt)")
        print("  3. Ensure output directories are writable")
        print("  4. Contact support with error details")
        print("="*70 + "\n")
        
        # Re-raise for debugging if in development mode
        # In production: Would log to file and return error response
        raise


def main():
    """
    Command-line interface entry point.
    
    Design Note: Separate main() function from run_email_forensics_system()
    because:
    1. Testing: run_email_forensics_system() can be imported and tested
    2. Scripting: Other Python scripts can call it programmatically
    3. CLI: main() handles command-line argument parsing
    
    Future Enhancement: Add argparse for configurable parameters:
    - Email count
    - Suspicious ratio
    - Input directory (for real email files)
    - Output directory
    - Verbosity level
    """
    
    # Configuration
    # These would be command-line arguments in production
    EMAIL_COUNT = 50  # Number of test emails to generate
    SUSPICIOUS_RATIO = 0.3  # 30% suspicious emails (realistic ratio)
    
    # Execute pipeline
    results = run_email_forensics_system(
        email_count=EMAIL_COUNT,
        suspicious_ratio=SUSPICIOUS_RATIO
    )
    
    # Return success/failure code for scripting
    # Convention: 0 = success, non-zero = failure
    return 0 if results['success'] else 1


if __name__ == "__main__":
    """
    Python idiom for script execution.
    
    This block only executes when script is run directly (python main.py),
    not when imported as a module (import main).
    
    This pattern enables:
    1. Reusability: Functions can be imported by other scripts
    2. Testing: Test framework can import without executing
    3. Interactive: Can be imported in Python REPL for exploration
    """
    sys.exit(main())

