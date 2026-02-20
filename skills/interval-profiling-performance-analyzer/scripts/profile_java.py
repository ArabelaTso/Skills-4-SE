#!/usr/bin/env python3
"""
Java profiling wrapper script.
Uses Java Flight Recorder (JFR) or custom instrumentation for profiling.
"""

import subprocess
import json
import sys
import os
import xml.etree.ElementTree as ET
from pathlib import Path


def profile_with_jfr(java_class, classpath='.', args=None, duration=30):
    """Profile Java application using Java Flight Recorder."""
    jfr_file = 'profile.jfr'

    # Build Java command with JFR enabled
    cmd = [
        'java',
        f'-XX:StartFlightRecording=duration={duration}s,filename={jfr_file}',
        '-cp', classpath,
        java_class
    ]

    if args:
        cmd.extend(args)

    print(f"Running Java profiling: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=duration + 10)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr, file=sys.stderr)
    except subprocess.TimeoutExpired:
        print("Warning: Java process timed out")

    return jfr_file


def parse_jfr_file(jfr_file):
    """Parse JFR file and extract profiling data."""
    # Convert JFR to JSON using jfr tool
    json_file = 'profile.json'

    try:
        subprocess.run(['jfr', 'print', '--json', jfr_file],
                      stdout=open(json_file, 'w'),
                      check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: jfr tool not available, using alternative parsing")
        return parse_jfr_alternative(jfr_file)

    with open(json_file, 'r') as f:
        data = json.load(f)

    return data


def parse_jfr_alternative(jfr_file):
    """Alternative JFR parsing when jfr tool is not available."""
    # Use jfr summary command
    try:
        result = subprocess.run(['jfr', 'summary', jfr_file],
                              capture_output=True, text=True, check=True)
        return {'summary': result.stdout, 'events': []}
    except:
        return {'summary': 'JFR parsing not available', 'events': []}


def analyze_java_profile(jfr_data):
    """Analyze Java profiling data."""
    intervals = []

    # Extract method profiling events
    events = jfr_data.get('events', [])
    method_stats = {}

    for event in events:
        if event.get('type') == 'jdk.ExecutionSample':
            method = event.get('stackTrace', {}).get('frames', [{}])[0].get('method', {})
            method_name = f"{method.get('type', {}).get('name', 'unknown')}.{method.get('name', 'unknown')}"

            if method_name not in method_stats:
                method_stats[method_name] = {
                    'function': method_name,
                    'call_count': 0,
                    'samples': 0,
                }

            method_stats[method_name]['samples'] += 1

    # Convert to intervals format
    total_samples = sum(m['samples'] for m in method_stats.values())

    for method_name, stats in method_stats.items():
        intervals.append({
            'function': method_name,
            'call_count': stats['samples'],
            'percent_of_total': (stats['samples'] / total_samples * 100) if total_samples > 0 else 0,
        })

    return sorted(intervals, key=lambda x: x['percent_of_total'], reverse=True)


def identify_java_hotspots(intervals, threshold_percent=5.0):
    """Identify Java performance hotspots."""
    return [i for i in intervals if i['percent_of_total'] >= threshold_percent]


def generate_java_recommendations(hotspots):
    """Generate Java-specific optimization recommendations."""
    recommendations = []

    for hotspot in hotspots[:10]:
        rec = {
            'location': hotspot['function'],
            'issue': f"High CPU usage: {hotspot['percent_of_total']:.1f}% of samples",
            'suggestions': []
        }

        # Java-specific suggestions
        if 'String' in hotspot['function'] or 'concat' in hotspot['function']:
            rec['suggestions'].append('Consider using StringBuilder for string concatenation')

        if 'ArrayList' in hotspot['function'] or 'HashMap' in hotspot['function']:
            rec['suggestions'].append('Review collection usage - consider pre-sizing or alternative data structures')

        if 'reflection' in hotspot['function'].lower():
            rec['suggestions'].append('Reflection is slow - consider caching or using direct method calls')

        if not rec['suggestions']:
            rec['suggestions'].append('Profile this method in detail to identify optimization opportunities')

        recommendations.append(rec)

    return recommendations


def main():
    if len(sys.argv) < 2:
        print("Usage: python profile_java.py <MainClass> [classpath] [duration_seconds]")
        sys.exit(1)

    java_class = sys.argv[1]
    classpath = sys.argv[2] if len(sys.argv) > 2 else '.'
    duration = int(sys.argv[3]) if len(sys.argv) > 3 else 30
    output_path = 'profile_results.json'

    print(f"Profiling Java class: {java_class}")

    # Profile with JFR
    jfr_file = profile_with_jfr(java_class, classpath, duration=duration)

    if not os.path.exists(jfr_file):
        print(f"Error: JFR file not created. Profiling may have failed.")
        sys.exit(1)

    # Parse JFR data
    jfr_data = parse_jfr_file(jfr_file)

    # Analyze profile
    intervals = analyze_java_profile(jfr_data)
    hotspots = identify_java_hotspots(intervals)
    recommendations = generate_java_recommendations(hotspots)

    # Prepare output
    results = {
        'language': 'java',
        'class': java_class,
        'summary': {
            'total_methods': len(intervals),
            'hotspot_count': len(hotspots),
            'profiling_duration': duration,
        },
        'intervals': intervals,
        'hotspots': hotspots,
        'recommendations': recommendations,
    }

    # Save results
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Profiling complete. Results saved to {output_path}")
    print(f"  - Total methods profiled: {len(intervals)}")
    print(f"  - Hotspots identified: {len(hotspots)}")
    print(f"  - Recommendations: {len(recommendations)}")


if __name__ == '__main__':
    main()
