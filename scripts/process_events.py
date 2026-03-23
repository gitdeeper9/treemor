#!/usr/bin/env python3
"""
TREEMOR Event Processor
Process and analyze seismic events.
"""

import sys
import json
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Process TREEMOR events")
    parser.add_argument("--input", required=True, help="Input event file")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Output format")
    
    args = parser.parse_args()
    
    # Load events
    with open(args.input, 'r') as f:
        if args.input.endswith('.json'):
            events = json.load(f)
        else:
            print("Only JSON input supported")
            return
    
    # Process events
    print(f"📊 Processing {len(events) if isinstance(events, list) else 1} events")
    
    for event in events if isinstance(events, list) else [events]:
        print(f"\n🌍 Event: {event.get('event_id', 'Unknown')}")
        print(f"   Magnitude: {event.get('magnitude', 'N/A')}")
        print(f"   Lead Time: {event.get('lead_time_sec', 'N/A')}s")
        print(f"   Triggered Sensors: {event.get('triggered_sensors', 0)}")
    
    # Save output
    if args.output:
        with open(args.output, 'w') as f:
            if args.format == "json":
                json.dump(events, f, indent=2)
            else:
                import csv
                if isinstance(events, list) and events:
                    writer = csv.DictWriter(f, fieldnames=events[0].keys())
                    writer.writeheader()
                    writer.writerows(events)
        print(f"\n✅ Saved to: {args.output}")


if __name__ == "__main__":
    main()
