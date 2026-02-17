#!/usr/bin/env python3
"""
Analyze and query snapshot data.

Usage:
    python analyze_snapshots.py <snapshot_file> [options]
"""

import json
import argparse
from typing import List, Dict, Any
from collections import defaultdict


def load_snapshots(filename: str) -> Dict[str, Any]:
    """Load snapshots from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


def list_snapshots(data: Dict) -> None:
    """List all snapshots with basic info."""
    print(f"Total snapshots: {data['total_snapshots']}")
    print(f"Language: {data['language']}")
    print(f"Format version: {data['format_version']}")
    print("\nSnapshots:")
    print("-" * 80)

    for snapshot in data['snapshots']:
        print(f"ID: {snapshot['snapshot_id']}")
        print(f"  Location: {snapshot['location']}")
        print(f"  Type: {snapshot['type']}")
        print(f"  Timestamp: {snapshot['timestamp']}")
        if 'call_stack' in snapshot:
            print(f"  Stack depth: {len(snapshot['call_stack'])}")
        print()


def show_snapshot(data: Dict, snapshot_id: int) -> None:
    """Show detailed information for a specific snapshot."""
    snapshot = None
    for s in data['snapshots']:
        if s['snapshot_id'] == snapshot_id:
            snapshot = s
            break

    if not snapshot:
        print(f"Snapshot {snapshot_id} not found")
        return

    print(f"Snapshot ID: {snapshot['snapshot_id']}")
    print(f"Location: {snapshot['location']}")
    print(f"Type: {snapshot['type']}")
    print(f"Timestamp: {snapshot['timestamp']}")
    print()

    # Show call stack
    if 'call_stack' in snapshot:
        print("Call Stack:")
        for i, frame in enumerate(snapshot['call_stack']):
            if isinstance(frame, dict):
                print(f"  {i}: {frame.get('function', 'unknown')} at {frame.get('filename', 'unknown')}:{frame.get('lineno', '?')}")
            else:
                print(f"  {i}: {frame}")
        print()

    # Show variables
    if 'local_variables' in snapshot:
        print("Local Variables:")
        for name, value in snapshot['local_variables'].items():
            print(f"  {name} = {json.dumps(value, indent=4)}")
        print()

    if 'variables' in snapshot:
        print("Variables:")
        for name, info in snapshot['variables'].items():
            print(f"  {name}: size={info['size']}, data={info['data'][:32]}...")
        print()


def compare_snapshots(data: Dict, id1: int, id2: int) -> None:
    """Compare two snapshots."""
    snap1 = None
    snap2 = None

    for s in data['snapshots']:
        if s['snapshot_id'] == id1:
            snap1 = s
        if s['snapshot_id'] == id2:
            snap2 = s

    if not snap1 or not snap2:
        print("One or both snapshots not found")
        return

    print(f"Comparing snapshot {id1} and {id2}")
    print("-" * 80)

    # Compare variables
    vars1 = snap1.get('local_variables', {})
    vars2 = snap2.get('local_variables', {})

    all_vars = set(vars1.keys()) | set(vars2.keys())

    print("\nVariable Changes:")
    for var in sorted(all_vars):
        if var not in vars1:
            print(f"  {var}: [NEW] = {vars2[var]}")
        elif var not in vars2:
            print(f"  {var}: [REMOVED]")
        elif vars1[var] != vars2[var]:
            print(f"  {var}: {vars1[var]} -> {vars2[var]}")


def filter_snapshots(data: Dict, location: str = None, snapshot_type: str = None) -> List[Dict]:
    """Filter snapshots by criteria."""
    filtered = data['snapshots']

    if location:
        filtered = [s for s in filtered if location in s['location']]

    if snapshot_type:
        filtered = [s for s in filtered if s['type'] == snapshot_type]

    return filtered


def extract_timeline(data: Dict) -> None:
    """Extract execution timeline from snapshots."""
    print("Execution Timeline:")
    print("-" * 80)

    for snapshot in data['snapshots']:
        print(f"{snapshot['timestamp']} | {snapshot['location']} ({snapshot['type']})")


def analyze_variable_changes(data: Dict, variable_name: str) -> None:
    """Track how a specific variable changes across snapshots."""
    print(f"Tracking variable: {variable_name}")
    print("-" * 80)

    for snapshot in data['snapshots']:
        vars_dict = snapshot.get('local_variables', {})
        if variable_name in vars_dict:
            print(f"Snapshot {snapshot['snapshot_id']} ({snapshot['location']}): {vars_dict[variable_name]}")


def main():
    parser = argparse.ArgumentParser(description='Analyze snapshot data')
    parser.add_argument('snapshot_file', help='Snapshot JSON file')
    parser.add_argument('--list', action='store_true', help='List all snapshots')
    parser.add_argument('--show', type=int, metavar='ID', help='Show detailed snapshot')
    parser.add_argument('--compare', nargs=2, type=int, metavar=('ID1', 'ID2'), help='Compare two snapshots')
    parser.add_argument('--timeline', action='store_true', help='Show execution timeline')
    parser.add_argument('--track-var', metavar='NAME', help='Track variable changes')
    parser.add_argument('--filter-location', metavar='PATTERN', help='Filter by location pattern')
    parser.add_argument('--filter-type', metavar='TYPE', help='Filter by snapshot type')

    args = parser.parse_args()

    # Load data
    data = load_snapshots(args.snapshot_file)

    # Apply filters if specified
    if args.filter_location or args.filter_type:
        filtered = filter_snapshots(data, args.filter_location, args.filter_type)
        data['snapshots'] = filtered
        data['total_snapshots'] = len(filtered)

    # Execute command
    if args.list:
        list_snapshots(data)
    elif args.show is not None:
        show_snapshot(data, args.show)
    elif args.compare:
        compare_snapshots(data, args.compare[0], args.compare[1])
    elif args.timeline:
        extract_timeline(data)
    elif args.track_var:
        analyze_variable_changes(data, args.track_var)
    else:
        # Default: list snapshots
        list_snapshots(data)


if __name__ == '__main__':
    main()
