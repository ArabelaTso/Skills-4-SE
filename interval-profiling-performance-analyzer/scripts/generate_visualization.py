#!/usr/bin/env python3
"""
Generate visualizations from profiling data.
Creates flame graphs, bar charts, and HTML reports.
"""

import json
import sys
from pathlib import Path


def generate_html_report(profile_data, output_path='profile_report.html'):
    """Generate an interactive HTML report from profiling data."""

    language = profile_data.get('language', 'unknown')
    summary = profile_data.get('summary', {})
    hotspots = profile_data.get('hotspots', [])
    recommendations = profile_data.get('recommendations', [])

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Performance Profile Report</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            margin-bottom: 10px;
            font-size: 2em;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }}
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .summary-card {{
            background: #ecf0f1;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
        }}
        .summary-card .value {{
            font-size: 2em;
            font-weight: bold;
            color: #3498db;
        }}
        .summary-card .label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}
        .hotspot {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .hotspot .function {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #d35400;
        }}
        .hotspot .metric {{
            color: #7f8c8d;
            margin: 5px 0;
        }}
        .recommendation {{
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 15px;
            margin: 10px 0;
            border-radius: 4px;
        }}
        .recommendation .location {{
            font-family: 'Courier New', monospace;
            font-weight: bold;
            color: #0c5460;
        }}
        .recommendation .issue {{
            color: #856404;
            margin: 5px 0;
        }}
        .recommendation ul {{
            margin: 10px 0 0 20px;
        }}
        .recommendation li {{
            margin: 5px 0;
            color: #004085;
        }}
        .chart {{
            margin: 20px 0;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 6px;
        }}
        .bar {{
            display: flex;
            align-items: center;
            margin: 10px 0;
        }}
        .bar-label {{
            width: 200px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        .bar-visual {{
            flex: 1;
            height: 30px;
            background: linear-gradient(90deg, #3498db, #2980b9);
            border-radius: 4px;
            position: relative;
        }}
        .bar-value {{
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
        }}
        .badge {{
            display: inline-block;
            padding: 4px 8px;
            background: #3498db;
            color: white;
            border-radius: 3px;
            font-size: 0.85em;
            margin-right: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Performance Profile Report</h1>
        <p><span class="badge">{language.upper()}</span> Generated from interval profiling analysis</p>

        <h2>📊 Summary</h2>
        <div class="summary">
"""

    # Add summary cards
    for key, value in summary.items():
        label = key.replace('_', ' ').title()
        html_content += f"""
            <div class="summary-card">
                <div class="value">{value}</div>
                <div class="label">{label}</div>
            </div>
"""

    html_content += """
        </div>

        <h2>🔥 Performance Hotspots</h2>
        <p>Functions consuming the most execution time or resources:</p>
"""

    # Add hotspots
    for hotspot in hotspots[:10]:
        function = hotspot.get('function', 'unknown')
        percent = hotspot.get('percent_of_total', 0)

        html_content += f"""
        <div class="hotspot">
            <div class="function">{function}</div>
"""

        if 'cumulative_time' in hotspot:
            html_content += f'            <div class="metric">⏱️ Time: {hotspot["cumulative_time"]:.3f}s ({percent:.1f}% of total)</div>\n'
        else:
            html_content += f'            <div class="metric">⏱️ Overhead: {percent:.1f}% of total</div>\n'

        if 'call_count' in hotspot:
            html_content += f'            <div class="metric">📞 Calls: {hotspot["call_count"]}</div>\n'

        html_content += """        </div>
"""

    # Add hotspot chart
    html_content += """
        <div class="chart">
            <h3>Top 10 Hotspots by Time</h3>
"""

    max_percent = max([h.get('percent_of_total', 0) for h in hotspots[:10]], default=1)
    for hotspot in hotspots[:10]:
        function = hotspot.get('function', 'unknown')
        if len(function) > 30:
            function = function[:27] + '...'
        percent = hotspot.get('percent_of_total', 0)
        width = (percent / max_percent * 100) if max_percent > 0 else 0

        html_content += f"""
            <div class="bar">
                <div class="bar-label">{function}</div>
                <div class="bar-visual" style="width: {width}%">
                    <span class="bar-value">{percent:.1f}%</span>
                </div>
            </div>
"""

    html_content += """
        </div>

        <h2>💡 Optimization Recommendations</h2>
        <p>Actionable suggestions to improve performance:</p>
"""

    # Add recommendations
    for rec in recommendations:
        location = rec.get('location', 'unknown')
        issue = rec.get('issue', '')
        suggestions = rec.get('suggestions', [])

        html_content += f"""
        <div class="recommendation">
            <div class="location">{location}</div>
            <div class="issue">⚠️ {issue}</div>
            <ul>
"""

        for suggestion in suggestions:
            html_content += f'                <li>{suggestion}</li>\n'

        html_content += """            </ul>
        </div>
"""

    html_content += """
    </div>
</body>
</html>
"""

    # Write HTML file
    with open(output_path, 'w') as f:
        f.write(html_content)

    print(f"✓ HTML report generated: {output_path}")


def generate_flamegraph_data(profile_data, output_path='flamegraph.txt'):
    """Generate flame graph data in folded stack format."""
    intervals = profile_data.get('intervals', [])

    # Create folded stack format for flame graph
    # Format: stack;trace;here value
    lines = []

    for interval in intervals:
        function = interval.get('function', 'unknown')
        # Use cumulative_time if available, otherwise use call_count as proxy
        value = interval.get('cumulative_time', interval.get('call_count', 1))

        if value > 0:
            lines.append(f"{function} {int(value * 1000)}")

    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f"✓ Flame graph data generated: {output_path}")
    print(f"  Generate SVG with: flamegraph.pl {output_path} > flamegraph.svg")


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_visualization.py <profile_results.json> [output.html]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_html = sys.argv[2] if len(sys.argv) > 2 else 'profile_report.html'

    # Load profile data
    with open(input_file, 'r') as f:
        profile_data = json.load(f)

    # Generate visualizations
    generate_html_report(profile_data, output_html)
    generate_flamegraph_data(profile_data, 'flamegraph.txt')

    print(f"\n✓ Visualization complete!")
    print(f"  Open {output_html} in a browser to view the report")


if __name__ == '__main__':
    main()
