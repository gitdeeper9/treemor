#!/usr/bin/env python3
"""
TREEMOR Report Generator
Generate reports from network data.
"""

import sys
import json
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Generate TREEMOR reports")
    parser.add_argument("--network", help="Network data file")
    parser.add_argument("--events", help="Events file")
    parser.add_argument("--output", required=True, help="Output report file")
    parser.add_argument("--format", choices=["txt", "json", "html"], default="txt", help="Report format")
    
    args = parser.parse_args()
    
    report = {
        "generated_at": datetime.now().isoformat(),
        "title": "TREEMOR Monitoring Report",
        "network": {},
        "events": [],
        "summary": {}
    }
    
    # Load network data
    if args.network:
        with open(args.network, 'r') as f:
            report["network"] = json.load(f)
    
    # Load events
    if args.events:
        with open(args.events, 'r') as f:
            report["events"] = json.load(f)
    
    # Generate summary
    report["summary"] = {
        "total_sensors": report["network"].get("total_sensors", 0),
        "active_sensors": report["network"].get("active_sensors", 0),
        "avg_tssi": report["network"].get("average_tssi", 0),
        "events_today": len([e for e in report["events"] if e.get("date") == datetime.now().strftime("%Y-%m-%d")]),
        "network_health": report["network"].get("network_health", "UNKNOWN")
    }
    
    # Save report
    with open(args.output, 'w') as f:
        if args.format == "json":
            json.dump(report, f, indent=2)
        elif args.format == "txt":
            f.write("=" * 60 + "\n")
            f.write(f"🌲 {report['title']}\n")
            f.write(f"📅 Generated: {report['generated_at']}\n")
            f.write("=" * 60 + "\n\n")
            f.write("📊 SUMMARY\n")
            f.write("-" * 40 + "\n")
            for key, value in report["summary"].items():
                f.write(f"   {key}: {value}\n")
            f.write("\n✅ Report generated successfully\n")
        elif args.format == "html":
            f.write(f"""<!DOCTYPE html>
<html>
<head><title>{report['title']}</title>
<style>
body {{ font-family: monospace; margin: 40px; background: #1a1a2e; color: #eee; }}
h1 {{ color: #4caf50; }}
</style>
</head>
<body>
<h1>🌲 {report['title']}</h1>
<p>Generated: {report['generated_at']}</p>
<h2>Summary</h2>
<ul>
""")
            for key, value in report["summary"].items():
                f.write(f"<li><strong>{key}</strong>: {value}</li>\n")
            f.write("</ul>\n</body>\n</html>\n")
    
    print(f"✅ Report saved to: {args.output}")


if __name__ == "__main__":
    main()
