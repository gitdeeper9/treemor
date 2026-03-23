#!/usr/bin/env python3
"""
TREEMOR Tree Calibration Script
Calibrate tree sensor with field measurements.
"""

import sys
import json
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Calibrate TREEMOR tree sensor")
    parser.add_argument("--id", required=True, help="Tree ID")
    parser.add_argument("--f0", type=float, help="Measured resonance frequency (Hz)")
    parser.add_argument("--xi", type=float, help="Measured coupling coefficient")
    parser.add_argument("--input", help="Input sensor file (JSON)")
    parser.add_argument("--output", help="Output calibration file")
    
    args = parser.parse_args()
    
    # Load sensor data
    sensor = {}
    if args.input:
        with open(args.input, 'r') as f:
            sensor = json.load(f)
    
    # Update with calibration
    sensor["tree_id"] = args.id
    sensor["calibrated_at"] = datetime.now().isoformat()
    sensor["calibration"] = {}
    
    if args.f0:
        sensor["calibration"]["measured_f0"] = args.f0
        print(f"📊 f0 calibrated: {args.f0} Hz")
    
    if args.xi:
        sensor["calibration"]["measured_xi"] = args.xi
        print(f"📊 ξ calibrated: {args.xi}")
    
    # Save calibration
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(sensor, f, indent=2)
        print(f"✅ Calibration saved to: {args.output}")
    
    return sensor


if __name__ == "__main__":
    main()
