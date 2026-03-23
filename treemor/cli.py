"""
TREEMOR Command Line Interface.
Pure Python implementation - NO NUMPY
"""

import sys
import json
import argparse
from typing import List, Dict


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="treomor",
        description="TREEMOR - Bio-Seismic Sensing & Planetary Infrasound Resonance",
        epilog="When forests become Earth's sentinels, conservation becomes infrastructure."
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"treomor {__import__('treomor').__version__}"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # tree command
    tree_parser = subparsers.add_parser("tree", help="Tree sensor operations")
    tree_parser.add_argument("action", choices=["create", "info", "calibrate"])
    tree_parser.add_argument("--id", help="Tree ID")
    tree_parser.add_argument("--species", help="Tree species")
    tree_parser.add_argument("--height", type=float, help="Tree height (m)")
    tree_parser.add_argument("--dbh", type=float, help="Diameter at breast height (m)")
    tree_parser.add_argument("--lat", type=float, help="Latitude")
    tree_parser.add_argument("--lon", type=float, help="Longitude")
    tree_parser.add_argument("--soil", default="bedrock", help="Soil type")
    
    # network command
    net_parser = subparsers.add_parser("network", help="Network operations")
    net_parser.add_argument("action", choices=["status", "add", "remove", "best"])
    net_parser.add_argument("--id", help="Tree ID")
    net_parser.add_argument("--top", type=int, default=10, help="Number of best sensors")
    
    # detect command
    detect_parser = subparsers.add_parser("detect", help="Detect seismic events")
    detect_parser.add_argument("--lat", type=float, required=True, help="Epicenter latitude")
    detect_parser.add_argument("--lon", type=float, required=True, help="Epicenter longitude")
    detect_parser.add_argument("--time", type=float, help="P-wave arrival time (seconds)")
    
    # fsin command
    fsin_parser = subparsers.add_parser("fsin", help="Calculate FSIN parameters")
    fsin_parser.add_argument("--tree-id", required=True, help="Tree ID")
    fsin_parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    # tssi command
    tssi_parser = subparsers.add_parser("tssi", help="Calculate TSSI")
    tssi_parser.add_argument("--tree-id", help="Tree ID")
    tssi_parser.add_argument("--network", action="store_true", help="Network average")
    
    args = parser.parse_args()
    
    if args.command == "tree":
        _handle_tree_command(args)
    elif args.command == "network":
        _handle_network_command(args)
    elif args.command == "detect":
        _handle_detect_command(args)
    elif args.command == "fsin":
        _handle_fsin_command(args)
    elif args.command == "tssi":
        _handle_tssi_command(args)
    else:
        parser.print_help()


def _handle_tree_command(args):
    """Handle tree commands."""
    from .sensors.tree_sensor import TreeSensor
    
    if args.action == "create":
        if not all([args.id, args.species, args.height, args.dbh, args.lat, args.lon]):
            print("Error: Missing required parameters")
            print("Required: --id, --species, --height, --dbh, --lat, --lon")
            return
        
        tree = TreeSensor(
            tree_id=args.id,
            species=args.species,
            height=args.height,
            dbh=args.dbh,
            latitude=args.lat,
            longitude=args.lon,
            soil_type=args.soil
        )
        
        print(f"🌲 Tree sensor created: {tree.tree_id}")
        print(f"   Species: {tree.species}")
        print(f"   Height: {tree.height}m")
        print(f"   DBH: {tree.dbh}m")
        print(f"   Mass: {tree.mass}kg")
        
    elif args.action == "info":
        # Would load from storage
        print("Info command - requires storage backend")
        
    elif args.action == "calibrate":
        print("Calibrate command - requires field measurements")


def _handle_network_command(args):
    """Handle network commands."""
    from .network.forest_network import ForestNetwork
    from .sensors.tree_sensor import TreeSensor
    
    network = ForestNetwork("TREEMOR Network")
    
    if args.action == "status":
        stats = network.get_network_statistics()
        print("🌳 TREEMOR Network Status")
        print("=" * 40)
        print(f"Network: {stats['name']}")
        print(f"Total Sensors: {stats['total_sensors']}")
        print(f"Active Sensors: {stats['active_sensors']}")
        print(f"Average TSSI: {stats['average_tssi']}")
        print(f"Events Detected: {stats['events_detected']}")
        print(f"Network Health: {stats['network_health']}")
        
        if stats['soil_type_distribution']:
            print("\nSoil Type Distribution:")
            for soil, count in stats['soil_type_distribution'].items():
                print(f"  {soil}: {count}")
                
    elif args.action == "add":
        print("Add sensor command - requires sensor creation first")
        
    elif args.action == "remove":
        print(f"Remove sensor: {args.id}")
        
    elif args.action == "best":
        best = network.get_best_sensors(args.top)
        print(f"🏆 Top {len(best)} Sensors by TSSI:")
        for i, sensor in enumerate(best, 1):
            print(f"  {i}. {sensor['tree_id']} ({sensor['species']}) - TSSI: {sensor['tssi']:.3f}")


def _handle_detect_command(args):
    """Handle detection commands."""
    from .network.forest_network import ForestNetwork
    
    network = ForestNetwork("TREEMOR Network")
    
    import time
    p_time = args.time if args.time else time.time()
    
    event = network.detect_event(p_time, (args.lat, args.lon))
    
    if event and event['detected']:
        print(f"⚠️  SEISMIC EVENT DETECTED!")
        print(f"   Event ID: {event['event_id']}")
        print(f"   Epicenter: {event['epicenter']}")
        print(f"   Triggered Sensors: {event['triggered_sensors']}")
        print(f"   Network Response: ACTIVE")
    else:
        print("✓ No event detected")


def _handle_fsin_command(args):
    """Handle FSIN calculation."""
    from .sensors.tree_sensor import TreeSensor
    
    # Create a sample tree for demonstration
    tree = TreeSensor(
        tree_id=args.tree_id,
        species="douglas_fir",
        height=50.0,
        dbh=1.2,
        latitude=47.6,
        longitude=-122.3,
        soil_type="bedrock"
    )
    
    params = tree.get_fsin_parameters()
    
    if args.json:
        print(json.dumps(params, indent=2))
    else:
        print(f"📊 FSIN Parameters for {args.tree_id}")
        print("=" * 50)
        print(f"  f₀ (Resonance Frequency):   {params['f0']:.3f} Hz")
        print(f"  ξ (Seismic Coupling):       {params['xi']:.3f}")
        print(f"  ζ (Damping Ratio):          {params['zeta']:.3f}")
        print(f"  EI (Bending Stiffness):     {params['EI']:.2e} N·m²")
        print(f"  σ_inf (Infrasonic Cross-Section): {params['sigma_inf']:.2f} m²")
        print(f"  ΔP_sap (Sap Pressure):      {params['delta_p_sap']:.1f} kPa")
        print(f"  Z_RS (Root-Soil Impedance): {params['Z_RS']:.2f} MPa·s/m")
        print(f"  ADI (Atmospheric Decoupling): {params['ADI']:.1f}")
        print(f"  τ_lead (Lead Time):         {params['tau_lead']:.1f} s")


def _handle_tssi_command(args):
    """Handle TSSI calculation."""
    from .sensors.tree_sensor import TreeSensor
    from .core.tssi import TSSICalculator
    
    tssi_calc = TSSICalculator()
    
    if args.network:
        print("Network TSSI calculation requires active network")
    elif args.tree_id:
        tree = TreeSensor(
            tree_id=args.tree_id,
            species="douglas_fir",
            height=50.0,
            dbh=1.2,
            latitude=47.6,
            longitude=-122.3,
            soil_type="bedrock"
        )
        
        params = tree.get_fsin_parameters()
        tssi = tssi_calc.calculate_tssi(params)
        category, desc = tssi_calc.classify_sensitivity(tssi)
        
        print(f"🌲 Tree: {args.tree_id}")
        print(f"📊 TSSI Score: {tssi:.3f}")
        print(f"🏷️  Category: {category}")
        print(f"📝 Description: {desc}")
        
        if tssi < 0.6:
            recommendations = tssi_calc.get_improvement_recommendations(params)
            if recommendations:
                print(f"\n💡 Recommendations:")
                for rec in recommendations:
                    print(f"   • {rec}")


if __name__ == "__main__":
    main()
