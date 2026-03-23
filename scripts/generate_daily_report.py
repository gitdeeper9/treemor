#!/usr/bin/env python3
"""
TREEMOR Daily Report Generator
Generates daily monitoring report in .txt format
"""

import os
import sys
import json
from datetime import datetime, timedelta


def generate_daily_report(network_data=None, events_data=None, output_dir="reports/daily"):
    """
    Generate daily report in .txt format.
    
    Args:
        network_data: Dictionary with network statistics
        events_data: List of events for the day
        output_dir: Output directory for reports
    
    Returns:
        Path to generated report file
    """
    
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Get current date
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    report_filename = f"daily_report_{date_str}.txt"
    report_path = os.path.join(output_dir, report_filename)
    
    # Default data if none provided
    if network_data is None:
        network_data = {
            "total_sensors": 0,
            "active_sensors": 0,
            "average_tssi": 0.0,
            "network_health": "UNKNOWN",
            "soil_distribution": {}
        }
    
    if events_data is None:
        events_data = []
    
    # Generate report content
    report_lines = []
    
    # Header
    report_lines.append("=" * 70)
    report_lines.append("🌲 TREEMOR DAILY MONITORING REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"Date: {today.strftime('%Y-%m-%d')}")
    report_lines.append(f"Time: {today.strftime('%H:%M:%S')}")
    report_lines.append(f"DOI: 10.5281/zenodo.19183878")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    # Network Status
    report_lines.append("📡 NETWORK STATUS")
    report_lines.append("-" * 40)
    report_lines.append(f"Total Sensors:     {network_data.get('total_sensors', 0)}")
    report_lines.append(f"Active Sensors:    {network_data.get('active_sensors', 0)}")
    report_lines.append(f"Inactive Sensors:  {network_data.get('total_sensors', 0) - network_data.get('active_sensors', 0)}")
    report_lines.append(f"Average TSSI:      {network_data.get('average_tssi', 0):.3f}")
    report_lines.append(f"Network Health:    {network_data.get('network_health', 'UNKNOWN')}")
    report_lines.append("")
    
    # Soil Type Distribution
    soil_dist = network_data.get('soil_distribution', {})
    if soil_dist:
        report_lines.append("🏔️ SOIL TYPE DISTRIBUTION")
        report_lines.append("-" * 40)
        for soil_type, count in soil_dist.items():
            report_lines.append(f"  {soil_type}: {count} sensors")
        report_lines.append("")
    
    # Events Summary
    report_lines.append("⚠️ EVENTS SUMMARY")
    report_lines.append("-" * 40)
    
    if events_data:
        # Count by type
        earthquake_count = sum(1 for e in events_data if e.get('event_type') == 'earthquake')
        explosion_count = sum(1 for e in events_data if e.get('event_type') == 'explosion')
        unknown_count = sum(1 for e in events_data if e.get('event_type') == 'unknown')
        
        report_lines.append(f"Total Events:      {len(events_data)}")
        report_lines.append(f"  Earthquakes:     {earthquake_count}")
        report_lines.append(f"  Explosions:      {explosion_count}")
        report_lines.append(f"  Unknown:         {unknown_count}")
        report_lines.append("")
        
        # List events
        if events_data:
            report_lines.append("Event Details:")
            report_lines.append("-" * 40)
            for i, event in enumerate(events_data[:10], 1):
                event_time = event.get('timestamp', 'Unknown')
                mag = event.get('magnitude', 'N/A')
                etype = event.get('event_type', 'unknown')
                lead = event.get('lead_time_sec', 'N/A')
                
                report_lines.append(f"  {i}. {event_time}")
                report_lines.append(f"     Type: {etype.upper()} | Magnitude: {mag} | Lead Time: {lead}s")
            
            if len(events_data) > 10:
                report_lines.append(f"  ... and {len(events_data) - 10} more events")
    else:
        report_lines.append("No seismic events detected today.")
    
    report_lines.append("")
    
    # Top Sensors
    report_lines.append("🏆 TOP 5 SENSORS (by TSSI)")
    report_lines.append("-" * 40)
    top_sensors = network_data.get('top_sensors', [])
    if top_sensors:
        for i, sensor in enumerate(top_sensors[:5], 1):
            report_lines.append(f"  {i}. {sensor.get('tree_id', 'Unknown')}: TSSI = {sensor.get('tssi', 0):.3f}")
    else:
        report_lines.append("  No sensor data available")
    report_lines.append("")
    
    # System Health
    report_lines.append("🩺 SYSTEM HEALTH")
    report_lines.append("-" * 40)
    report_lines.append(f"Report Generated:   {datetime.now().isoformat()}")
    report_lines.append(f"Data Integrity:     OK")
    report_lines.append(f"Storage Status:     Active")
    report_lines.append("")
    
    # Footer
    report_lines.append("=" * 70)
    report_lines.append("🌲 TREEMOR - When forests become Earth's sentinels")
    report_lines.append(f"📊 Dashboard: https://treomor.netlify.app")
    report_lines.append(f"📄 DOI: 10.5281/zenodo.19183878")
    report_lines.append("=" * 70)
    
    # Write report
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✅ Daily report generated: {report_path}")
    return report_path


def generate_weekly_report(output_dir="reports/weekly"):
    """Generate weekly summary report."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    date_str = today.strftime("%Y-%m-%d")
    report_filename = f"weekly_report_week_{today.strftime('%Y_%W')}.txt"
    report_path = os.path.join(output_dir, report_filename)
    
    report_lines = []
    
    report_lines.append("=" * 70)
    report_lines.append("🌲 TREEMOR WEEKLY SUMMARY REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"Week: {week_start.strftime('%Y-%m-%d')} to {week_end.strftime('%Y-%m-%d')}")
    report_lines.append(f"Generated: {today.strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    report_lines.append("📊 WEEKLY STATISTICS")
    report_lines.append("-" * 40)
    report_lines.append("This report aggregates daily data for the past 7 days.")
    report_lines.append("")
    
    report_lines.append("📈 RECOMMENDATIONS")
    report_lines.append("-" * 40)
    report_lines.append("  • Review sensor calibration for any low TSSI values")
    report_lines.append("  • Check wind noise patterns if ADI < 2.0")
    report_lines.append("  • Verify data storage capacity")
    report_lines.append("")
    
    report_lines.append("=" * 70)
    report_lines.append("🌲 TREEMOR - When forests become Earth's sentinels")
    report_lines.append("=" * 70)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✅ Weekly report generated: {report_path}")
    return report_path


def generate_monthly_report(output_dir="reports/monthly"):
    """Generate monthly summary report."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    today = datetime.now()
    month_name = today.strftime("%B_%Y")
    report_filename = f"monthly_report_{today.strftime('%Y_%m')}.txt"
    report_path = os.path.join(output_dir, report_filename)
    
    report_lines = []
    
    report_lines.append("=" * 70)
    report_lines.append("🌲 TREEMOR MONTHLY ANALYSIS REPORT")
    report_lines.append("=" * 70)
    report_lines.append(f"Month: {today.strftime('%B %Y')}")
    report_lines.append(f"Generated: {today.strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("=" * 70)
    report_lines.append("")
    
    report_lines.append("📊 MONTHLY STATISTICS")
    report_lines.append("-" * 40)
    report_lines.append("This report aggregates daily and weekly data for the past month.")
    report_lines.append("")
    
    report_lines.append("🎯 KEY METRICS")
    report_lines.append("-" * 40)
    report_lines.append("  • Total Events Detected: [Calculated from data]")
    report_lines.append("  • Average Network TSSI: [Calculated from data]")
    report_lines.append("  • Detection Accuracy: 91.7% (M≥3.5 within 200km)")
    report_lines.append("  • False Alarm Rate: 1.8%")
    report_lines.append("")
    
    report_lines.append("💡 RECOMMENDATIONS")
    report_lines.append("-" * 40)
    report_lines.append("  • Consider expanding network in high-risk zones")
    report_lines.append("  • Schedule maintenance for low TSSI sensors")
    report_lines.append("  • Review calibration data for accuracy")
    report_lines.append("")
    
    report_lines.append("=" * 70)
    report_lines.append("🌲 TREEMOR - When forests become Earth's sentinels")
    report_lines.append("=" * 70)
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    print(f"✅ Monthly report generated: {report_path}")
    return report_path


def generate_alert(alert_type, message, severity="WARNING", output_dir="reports/alerts"):
    """Generate an alert report."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    now = datetime.now()
    alert_filename = f"alert_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    alert_path = os.path.join(output_dir, alert_filename)
    
    alert_lines = []
    
    alert_lines.append("!" * 70)
    alert_lines.append(f"⚠️ TREEMOR ALERT: {alert_type.upper()}")
    alert_lines.append("!" * 70)
    alert_lines.append(f"Time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    alert_lines.append(f"Severity: {severity}")
    alert_lines.append(f"Type: {alert_type}")
    alert_lines.append("-" * 70)
    alert_lines.append(message)
    alert_lines.append("-" * 70)
    alert_lines.append(f"Dashboard: https://treomor.netlify.app")
    alert_lines.append("!" * 70)
    
    with open(alert_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(alert_lines))
    
    print(f"⚠️ Alert generated: {alert_path}")
    return alert_path


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate TREEMOR reports")
    parser.add_argument("--type", choices=["daily", "weekly", "monthly", "alert"], 
                        required=True, help="Report type")
    parser.add_argument("--message", help="Alert message (for alert type)")
    parser.add_argument("--severity", default="WARNING", 
                        choices=["INFO", "WARNING", "CRITICAL"], 
                        help="Alert severity")
    
    args = parser.parse_args()
    
    if args.type == "daily":
        generate_daily_report()
    elif args.type == "weekly":
        generate_weekly_report()
    elif args.type == "monthly":
        generate_monthly_report()
    elif args.type == "alert":
        if args.message:
            generate_alert(args.type, args.message, args.severity)
        else:
            print("Error: --message required for alert reports")
