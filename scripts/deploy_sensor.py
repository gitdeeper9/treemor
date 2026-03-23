#!/usr/bin/env python3
"""
TREEMOR Sensor Deployment Script
Deploy a new tree sensor to the network.
"""

import sys
import json
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Deploy TREEMOR tree sensor")
    parser.add_argument("--id", required=True, help="Tree ID")
    parser.add_argument("--species", required=True, help="Tree species")
    parser.add_argument("--height", type=float, required=True, help="Height (m)")
    parser.add_argument("--dbh", type=float, required=True, help="Diameter at breast height (m)")
    parser.add_argument("--lat", type=float, required=True, help="Latitude")
    parser.add_argument("--lon", type=float, required=True, help="Longitude")
    parser.add_argument("--soil", default="bedrock", help="Soil type")
    parser.add_argument("--output", help="Output file (JSON)")
    
    args = parser.parse_args()
    
    # Create sensor record
    sensor = {
        "tree_id": args.id,
        "species": args.species,
        "height": args.height,
        "dbh": args.dbh,
        "location": {"lat": args.lat, "lon": args.lon},
        "soil_type": args.soil,
        "deployed_at": datetime.now().isoformat(),
        "status": "active"
    }
    
    # Calculate FSIN parameters
    try:
        sys.path.insert(0, '.')
        from treomor.sensors.tree_sensor import TreeSensor
        
        tree = TreeSensor(
            tree_id=args.id,
            species=args.species,
            height=args.height,
            dbh=args.dbh,
            latitude=args.lat,
            longitude=args.lon,
            soil_type=args.soil
        )
        
        sensor["fsin"] = tree.get_fsin_parameters()
        sensor["mass_kg"] = tree.mass
        
        print(f"✅ Sensor deployed: {args.id}")
        print(f"   Mass: {tree.mass:.0f} kg")
        print(f"   f0: {sensor['fsin']['f0']:.3f} Hz")
        
    except ImportError:
        print("⚠️  TREEMOR package not installed. Install with: pip install -e .")
    
    # Save to file
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(sensor, f, indent=2)
        print(f"   Saved to: {args.output}")
    
    return sensor


if __name__ == "__main__":
    main()
