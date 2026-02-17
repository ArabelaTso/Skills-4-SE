#!/usr/bin/env python3
"""
Python profiling script for interval-based performance analysis.
Profiles function calls with execution time, memory usage, and call frequency.
"""

import cProfile
import pstats
import io
import json
import sys
import tracemalloc
from pathlib import Path


def profile_with_cprofile(script_path, args=None):
    """Profile a Python script using cProfile."""
    profiler = cProfile.Profile()

    # Start memory tracking
    tracemalloc.start()

    # Prepare script execution
    script_globals = {
        '__name__': '__main__',
        '__file__': script_path,
    }

    with open(script_path, 'r') as f:
        code = compile(f.read(), script_path, 'exec')

    # Profile execution
    profiler.enable()
    try:
        exec(code, script_globals)
    except SystemExit:
        pass
    finally:
        profiler.disable()

    # Get memory snapshot
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()

    return profiler, snapshot


def analyze_profile_data(profiler, snapshot):
    """Analyze profiling data and extract metrics."""
    # Get function call statistics
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.sort_stats('cumulative')

    # Extract interval data
    intervals = []
    for func, (cc, nc, tt, ct, callers) in stats.stats.items():
        filename, line, func_name = func
        intervals.append({
            'function': func_name,
            'file': filename,
            'line': line,
            'call_count': nc,
            'total_time': tt,
            'cumulative_time': ct,
            'time_per_call': tt / nc if nc > 0 else 0,
        })

    # Get memory statistics
    top_stats = snapshot.statistics('lineno')
    memory_data = []
    for stat in top_stats[:20]:
        memory_data.append({
            'file': str(stat.traceback[0].filename),
            'line': stat.traceback[0].lineno,
            'size_mb': stat.size / 1024 / 1024,
            'count': stat.count,
        })

    return intervals, memory_data


def identify_hotspots(intervals, threshold_percent=5.0):
    """Identify performance hotspots based on cumulative time."""
    if not intervals:
        return []

    total_time = sum(i['cumulative_time'] for i in intervals)
    hotspots = []

    for interval in intervals:
        percent = (interval['cumulative_time'] / total_time * 100) if total_time > 0 else 0
        if percent >= threshold_percent:
            hotspots.append({
                **interval,
                'percent_of_total': percent
            })

    return sorted(hotspots, key=lambda x: x['cumulative_time'], reverse=True)


def generate_recommendations(hotspots, memory_data):
    """Generate optimization recommendations."""
    recommendations = []

    for hotspot in hotspots[:10]:
        rec = {
            'location': f"{hotspot['file']}:{hotspot['line']} ({hotspot['function']})",
            'issue': f"High execution time: {hotspot['cumulative_time']:.3f}s ({hotspot['percent_of_total']:.1f}% of total)",
            'suggestions': []
        }

        # Add specific suggestions based on patterns
        if hotspot['call_count'] > 1000:
            rec['suggestions'].append(f"Called {hotspot['call_count']} times - consider caching or reducing call frequency")

        if hotspot['time_per_call'] > 0.01:
            rec['suggestions'].append(f"Slow per-call time ({hotspot['time_per_call']:.4f}s) - optimize algorithm or use faster data structures")

        recommendations.append(rec)

    # Add memory recommendations
    for mem in memory_data[:5]:
        if mem['size_mb'] > 10:
            recommendations.append({
                'location': f"{mem['file']}:{mem['line']}",
                'issue': f"High memory usage: {mem['size_mb']:.2f} MB",
                'suggestions': ['Consider using generators or streaming for large data', 'Review data structure efficiency']
            })

    return recommendations


def main():
    if len(sys.argv) < 2:
        print("Usage: python profile_python.py <script_path> [output_json]")
        sys.exit(1)

    script_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'profile_results.json'

    print(f"Profiling {script_path}...")

    # Profile the script
    profiler, snapshot = profile_with_cprofile(script_path)

    # Analyze data
    intervals, memory_data = analyze_profile_data(profiler, snapshot)

    # Identify hotspots
    hotspots = identify_hotspots(intervals)

    # Generate recommendations
    recommendations = generate_recommendations(hotspots, memory_data)

    # Prepare output
    results = {
        'language': 'python',
        'script': script_path,
        'summary': {
            'total_functions': len(intervals),
            'hotspot_count': len(hotspots),
            'total_time': sum(i['cumulative_time'] for i in intervals),
        },
        'intervals': intervals,
        'hotspots': hotspots,
        'memory_usage': memory_data,
        'recommendations': recommendations,
    }

    # Save results
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Profiling complete. Results saved to {output_path}")
    print(f"  - Total functions profiled: {len(intervals)}")
    print(f"  - Hotspots identified: {len(hotspots)}")
    print(f"  - Recommendations: {len(recommendations)}")


if __name__ == '__main__':
    main()
