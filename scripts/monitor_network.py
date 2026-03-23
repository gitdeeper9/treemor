#!/usr/bin/env python3
"""
TREEMOR Network Monitor
Real-time monitoring of forest seismic network.
"""

import sys
import time
import argparse
from datetime import datetime


def main():
    parser = argparse.ArgumentParser(description="Monitor TREEMOR network")
    parser.add_argument("--interval", type=int, default=5, help="Update interval (seconds)")
    parser.add_argument("--once", action="store_true", help="Run once and exit")
    
    args = parser.parse_args()
    
    print("🌲 TREEMOR Network Monitor")
    print("=" * 50)
    
    try:
        sys.path.insert(0, '.')
        from treomor.network.forest_network import ForestNetwork
        from treomor.sensors.tree_sensor import TreeSensor
        
        network = ForestNetwork("TREEMOR Network")
        
        # Load sensors from file (example)
        print("📡 Loading sensors...")
        
        while True:
            stats = network.get_network_statistics()
            
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}]")
            print(f"   Total Sensors: {stats['total_sensors']}")
            print(f"   Active Sensors: {stats['active_sensors']}")
            print(f"   Average TSSI: {stats['average_tssi']:.3f}")
            print(f"   Network Health: {stats['network_health']}")
            print(f"   Events Detected: {stats['events_detected']}")
            
            if args.once:
                break
            
            time.sleep(args.interval)
            
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except ImportError:
        print("⚠️  TREEMOR package not installed")
        print("   Install with: pip install -e .")


if __name__ == "__main__":
    main()
