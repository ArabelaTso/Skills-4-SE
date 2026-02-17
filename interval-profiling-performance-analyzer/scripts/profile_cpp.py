#!/usr/bin/env python3
"""
C/C++ profiling wrapper script.
Uses perf, gprof, or valgrind for profiling.
"""

import subprocess
import json
import sys
import os
import re
from pathlib import Path


def profile_with_perf(executable, args=None, duration=10):
    """Profile C/C++ application using Linux perf."""
    perf_data = 'perf.data'

    # Build perf command
    cmd = ['perf', 'record', '-g', '--call-graph', 'dwarf', '-o', perf_data]

    if duration:
        cmd.extend(['--', 'timeout', str(duration)])

    cmd.append(executable)

    if args:
        cmd.extend(args)

    print(f"Running perf profiling: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Perf output:", result.stderr, file=sys.stderr)
    except FileNotFoundError:
        print("Error: perf not found. Install with: sudo apt-get install linux-tools-generic")
        sys.exit(1)

    return perf_data


def parse_perf_report(perf_data):
    """Parse perf report output."""
    try:
        result = subprocess.run(['perf', 'report', '-i', perf_data, '--stdio', '--no-children'],
                              capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error parsing perf data: {e}")
        return ""


def analyze_perf_output(perf_output):
    """Analyze perf report output and extract intervals."""
    intervals = []

    # Parse perf report format
    # Example line: "    5.23%  program  program  [.] function_name"
    pattern = r'\s*([\d.]+)%\s+\S+\s+\S+\s+\[.\]\s+(.+)'

    for line in perf_output.split('\n'):
        match = re.match(pattern, line)
        if match:
            percent = float(match.group(1))
            function = match.group(2).strip()

            intervals.append({
                'function': function,
                'percent_of_total': percent,
                'overhead': percent,
            })

    return sorted(intervals, key=lambda x: x['percent_of_total'], reverse=True)


def profile_with_gprof(executable, args=None):
    """Profile using gprof (requires compilation with -pg flag)."""
    print(f"Running {executable} for gprof profiling...")
    print("Note: Executable must be compiled with -pg flag")

    # Run the executable to generate gmon.out
    cmd = [f'./{executable}']
    if args:
        cmd.extend(args)

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Program exited with code {e.returncode}")

    if not os.path.exists('gmon.out'):
        print("Error: gmon.out not found. Ensure executable is compiled with -pg")
        return None

    # Generate gprof report
    try:
        result = subprocess.run(['gprof', executable, 'gmon.out'],
                              capture_output=True, text=True, check=True)
        return result.stdout
    except FileNotFoundError:
        print("Error: gprof not found. Install with: sudo apt-get install binutils")
        return None


def analyze_gprof_output(gprof_output):
    """Analyze gprof output and extract intervals."""
    intervals = []

    # Parse flat profile section
    in_flat_profile = False
    pattern = r'\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+([\d.]+)\s+(.+)'

    for line in gprof_output.split('\n'):
        if 'Flat profile:' in line:
            in_flat_profile = True
            continue
        if in_flat_profile and line.strip().startswith('---'):
            break
        if in_flat_profile and line.strip():
            match = re.match(pattern, line)
            if match:
                percent_time = float(match.group(1))
                cumulative = float(match.group(2))
                self_seconds = float(match.group(3))
                calls = int(match.group(4))
                function = match.group(7).strip()

                intervals.append({
                    'function': function,
                    'percent_of_total': percent_time,
                    'cumulative_time': cumulative,
                    'self_time': self_seconds,
                    'call_count': calls,
                })

    return sorted(intervals, key=lambda x: x['percent_of_total'], reverse=True)


def identify_cpp_hotspots(intervals, threshold_percent=5.0):
    """Identify C/C++ performance hotspots."""
    return [i for i in intervals if i.get('percent_of_total', 0) >= threshold_percent]


def generate_cpp_recommendations(hotspots):
    """Generate C/C++-specific optimization recommendations."""
    recommendations = []

    for hotspot in hotspots[:10]:
        rec = {
            'location': hotspot['function'],
            'issue': f"High CPU usage: {hotspot['percent_of_total']:.1f}% of execution time",
            'suggestions': []
        }

        func_lower = hotspot['function'].lower()

        # C/C++-specific suggestions
        if 'malloc' in func_lower or 'free' in func_lower or 'new' in func_lower:
            rec['suggestions'].append('Memory allocation hotspot - consider object pooling or arena allocation')

        if 'memcpy' in func_lower or 'strcpy' in func_lower or 'strcmp' in func_lower:
            rec['suggestions'].append('String/memory operation hotspot - optimize buffer sizes or use faster alternatives')

        if 'vector' in func_lower or 'map' in func_lower:
            rec['suggestions'].append('STL container usage - consider reserve() for vectors or alternative data structures')

        if 'sort' in func_lower:
            rec['suggestions'].append('Sorting hotspot - consider partial_sort, nth_element, or custom comparators')

        if hotspot.get('call_count', 0) > 10000:
            rec['suggestions'].append(f"Called {hotspot['call_count']} times - consider inlining or reducing call frequency")

        if not rec['suggestions']:
            rec['suggestions'].append('Review algorithm complexity and data structure efficiency')

        recommendations.append(rec)

    return recommendations


def main():
    if len(sys.argv) < 2:
        print("Usage: python profile_cpp.py <executable> [--tool perf|gprof] [args...]")
        sys.exit(1)

    executable = sys.argv[1]
    tool = 'perf'  # default
    args = []

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--tool':
            tool = sys.argv[i + 1]
            i += 2
        else:
            args.append(sys.argv[i])
            i += 1

    output_path = 'profile_results.json'

    print(f"Profiling C/C++ executable: {executable} using {tool}")

    # Profile based on tool
    if tool == 'perf':
        perf_data = profile_with_perf(executable, args)
        perf_output = parse_perf_report(perf_data)
        intervals = analyze_perf_output(perf_output)
    elif tool == 'gprof':
        gprof_output = profile_with_gprof(executable, args)
        if not gprof_output:
            sys.exit(1)
        intervals = analyze_gprof_output(gprof_output)
    else:
        print(f"Unknown tool: {tool}")
        sys.exit(1)

    # Identify hotspots and generate recommendations
    hotspots = identify_cpp_hotspots(intervals)
    recommendations = generate_cpp_recommendations(hotspots)

    # Prepare output
    results = {
        'language': 'c/c++',
        'executable': executable,
        'tool': tool,
        'summary': {
            'total_functions': len(intervals),
            'hotspot_count': len(hotspots),
        },
        'intervals': intervals,
        'hotspots': hotspots,
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
