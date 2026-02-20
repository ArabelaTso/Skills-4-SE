---
name: interval-profiling-performance-analyzer
description: Profile programs at the function/method level to identify performance hotspots, bottlenecks, and optimization opportunities. Records execution time, memory usage, and call frequency for each interval. Generates actionable recommendations and visualizations. Use when users need to (1) analyze program performance, (2) identify slow functions or bottlenecks, (3) optimize execution time or memory usage, (4) profile Python, Java, or C/C++ programs with test cases or workload scenarios, or (5) generate performance reports with flame graphs and recommendations.
---

# Interval Profiling & Performance Analyzer

Profile programs to identify performance bottlenecks and generate optimization recommendations with visualizations.

## Workflow

### 1. Understand Requirements

Clarify the profiling task:
- **Target program:** Which file/executable to profile?
- **Language:** Python, Java, or C/C++?
- **Test scenarios:** What workload or test cases to run?
- **Focus area:** CPU time, memory usage, or both?

### 2. Select Profiling Tool

Choose based on language and environment:

**Python:**
- Use `scripts/profile_python.py` (cProfile + tracemalloc)
- Captures function-level timing and memory usage
- No code modification required

**Java:**
- Use `scripts/profile_java.py` (Java Flight Recorder)
- Requires JDK 11+ with JFR support
- Low overhead, production-safe

**C/C++:**
- Use `scripts/profile_cpp.py` (perf or gprof)
- `perf`: Linux only, no recompilation needed
- `gprof`: Cross-platform, requires `-pg` compilation flag

For detailed tool information, see [references/profiling-tools.md](references/profiling-tools.md).

### 3. Run Profiling

Execute the appropriate profiling script:

**Python example:**
```bash
python scripts/profile_python.py target_script.py
```

**Java example:**
```bash
python scripts/profile_java.py MainClass ./bin 30
# Arguments: MainClass, classpath, duration_seconds
```

**C/C++ example:**
```bash
python scripts/profile_cpp.py ./program --tool perf
# Or use gprof (requires compilation with -pg):
python scripts/profile_cpp.py ./program --tool gprof
```

All scripts generate `profile_results.json` containing:
- **intervals:** All profiled functions with metrics
- **hotspots:** Functions exceeding 5% of execution time
- **recommendations:** Actionable optimization suggestions
- **summary:** Overall statistics

### 4. Generate Visualizations

Create interactive HTML report and flame graph data:

```bash
python scripts/generate_visualization.py profile_results.json profile_report.html
```

Outputs:
- `profile_report.html`: Interactive report with charts and recommendations
- `flamegraph.txt`: Data for flame graph generation (use flamegraph.pl if available)

### 5. Analyze Results

Review the generated report:

**Hotspots section:** Functions consuming the most time
- Focus optimization efforts here (80/20 rule)
- Look for high call counts or slow per-call times

**Recommendations section:** Specific suggestions for each hotspot
- Language-specific patterns (e.g., use StringBuilder in Java)
- Algorithm improvements (e.g., reduce call frequency)
- Data structure optimizations

**Memory usage:** Identify memory-intensive operations
- Large allocations or many small objects
- Potential memory leaks

### 6. Provide Recommendations

Summarize findings for the user:

1. **Top 3-5 hotspots** with their impact (% of total time)
2. **Specific optimization suggestions** from the recommendations
3. **Quick wins:** Easy changes with high impact
4. **Deeper optimizations:** Algorithm or architecture changes

Reference [references/optimization-patterns.md](references/optimization-patterns.md) for detailed optimization techniques.

## Common Patterns

### Pattern 1: Quick Performance Check
User wants to know "why is my program slow?"

1. Run profiling script on the program
2. Generate HTML report
3. Identify top 3 hotspots
4. Provide specific recommendations for each

### Pattern 2: Before/After Comparison
User wants to verify optimization effectiveness.

1. Profile original version → save as `before.json`
2. User applies optimizations
3. Profile optimized version → save as `after.json`
4. Compare hotspots and total execution time
5. Quantify improvement

### Pattern 3: Memory Leak Investigation
User suspects memory issues.

1. Run Python profiling (includes memory tracking)
2. Review memory_usage section in results
3. Identify functions with high memory allocation
4. Suggest using generators, object pooling, or cleanup

### Pattern 4: Multi-Scenario Profiling
User wants to profile different workloads.

1. Create test scripts for each scenario
2. Profile each scenario separately
3. Compare hotspots across scenarios
4. Identify common bottlenecks vs scenario-specific issues

## Important Notes

### Python Profiling
- Profiling adds ~10-30% overhead
- Memory tracking (tracemalloc) adds additional overhead
- Results are deterministic (not sampling-based)

### Java Profiling
- Requires JDK 11+ for JFR
- JFR has <1% overhead, safe for production
- May need to adjust duration for long-running programs
- Alternative: Use VisualVM for GUI-based profiling

### C/C++ Profiling
- **perf:** Linux only, requires debug symbols for readable output
  - Compile with `-g` flag for function names
  - May need `sudo` for system-wide profiling
- **gprof:** Requires recompilation with `-pg` flag
  - Not suitable for multithreaded programs
  - Higher overhead than perf

### Optimization Guidelines
- **Profile first, optimize second:** Don't guess where the bottleneck is
- **Focus on hotspots:** Optimizing cold code wastes time
- **Measure impact:** Verify optimizations actually help
- **Consider readability:** Don't sacrifice maintainability for minor gains
- **Algorithm > micro-optimizations:** O(n²) → O(n log n) beats loop tweaks

## Troubleshooting

**"perf not found" (C/C++):**
```bash
sudo apt-get install linux-tools-generic
```

**"JFR file not created" (Java):**
- Ensure JDK 11+ is installed
- Check program actually runs and completes
- Try increasing duration parameter

**"No profiling data" (any language):**
- Verify program actually executes (doesn't exit immediately)
- Check for errors in program output
- Ensure test scenarios exercise the code

**"Flame graph not generating":**
- Install flamegraph.pl from github.com/brendangregg/FlameGraph
- Or use the HTML report which includes bar charts

## Resources

- **[references/profiling-tools.md](references/profiling-tools.md):** Detailed tool documentation and selection guide
- **[references/optimization-patterns.md](references/optimization-patterns.md):** Language-specific optimization patterns and best practices
