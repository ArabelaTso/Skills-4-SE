# Profiling Tools Reference

This document provides detailed information about profiling tools for Python, Java, and C/C++.

## Python Profiling Tools

### cProfile
Built-in deterministic profiler that measures function call counts and execution time.

**Usage:**
```python
python -m cProfile -o output.prof script.py
```

**Pros:** Built-in, no dependencies, accurate function-level profiling
**Cons:** Overhead can affect timing, no line-level profiling

### line_profiler
Line-by-line profiling for detailed analysis.

**Installation:** `pip install line_profiler`

**Usage:**
```python
# Add @profile decorator to functions
kernprof -l -v script.py
```

**Pros:** Line-level detail, identifies exact bottlenecks
**Cons:** Requires code modification, higher overhead

### memory_profiler
Tracks memory usage line-by-line.

**Installation:** `pip install memory_profiler`

**Usage:**
```python
python -m memory_profiler script.py
```

**Pros:** Identifies memory leaks and high-memory operations
**Cons:** Very slow, high overhead

### py-spy
Sampling profiler that doesn't require code changes.

**Installation:** `pip install py-spy`

**Usage:**
```bash
py-spy record -o profile.svg -- python script.py
```

**Pros:** No code changes, low overhead, generates flame graphs
**Cons:** Sampling-based (less precise)

## Java Profiling Tools

### Java Flight Recorder (JFR)
Built-in production-grade profiler with minimal overhead.

**Usage:**
```bash
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr MyApp
jfr print --json recording.jfr
```

**Pros:** Low overhead (<1%), production-safe, comprehensive data
**Cons:** Requires JDK 11+, complex output format

### VisualVM
GUI-based profiler with real-time monitoring.

**Installation:** Download from visualvm.github.io

**Pros:** Visual interface, real-time monitoring, heap dumps
**Cons:** GUI-only, higher overhead

### Async-profiler
Low-overhead sampling profiler for Java.

**Installation:** Download from github.com/jvm-profiling-tools/async-profiler

**Usage:**
```bash
./profiler.sh -d 30 -f flamegraph.svg <pid>
```

**Pros:** Very low overhead, flame graphs, CPU and allocation profiling
**Cons:** Linux/macOS only

## C/C++ Profiling Tools

### perf
Linux performance analysis tool with hardware counter support.

**Installation:** `sudo apt-get install linux-tools-generic`

**Usage:**
```bash
perf record -g ./program
perf report
```

**Pros:** Low overhead, hardware counters, system-wide profiling
**Cons:** Linux-only, requires debug symbols

### gprof
GNU profiler for function-level profiling.

**Usage:**
```bash
# Compile with -pg flag
g++ -pg -o program program.cpp
./program
gprof program gmon.out > analysis.txt
```

**Pros:** Simple, built-in, function call graphs
**Cons:** High overhead, requires recompilation, no multithreading support

### Valgrind (Callgrind)
Detailed profiling with instruction-level accuracy.

**Installation:** `sudo apt-get install valgrind`

**Usage:**
```bash
valgrind --tool=callgrind ./program
callgrind_annotate callgrind.out.<pid>
```

**Pros:** Very detailed, no recompilation needed
**Cons:** Extremely slow (10-50x), not for production

### Intel VTune
Professional profiler with advanced features.

**Pros:** Hardware event analysis, GPU profiling, low overhead
**Cons:** Commercial (free for open source), Intel-focused

## Tool Selection Guide

### Choose based on language:
- **Python:** Start with cProfile, use line_profiler for hotspots
- **Java:** Use JFR for production, VisualVM for development
- **C/C++:** Use perf on Linux, Instruments on macOS

### Choose based on overhead tolerance:
- **Production (< 2% overhead):** JFR, perf, py-spy
- **Development (< 10% overhead):** cProfile, gprof
- **Deep analysis (any overhead):** Valgrind, line_profiler

### Choose based on detail level:
- **Function-level:** cProfile, gprof, JFR
- **Line-level:** line_profiler, perf annotate
- **Instruction-level:** Valgrind, VTune

## Profiling Best Practices

1. **Profile realistic workloads:** Use production-like data and scenarios
2. **Run multiple times:** Average results to reduce noise
3. **Profile optimized builds:** Use -O2/-O3 for C/C++, production mode for Java
4. **Disable frequency scaling:** `sudo cpupower frequency-set --governor performance`
5. **Isolate the system:** Close other applications, disable background tasks
6. **Focus on hotspots:** Optimize the top 10% of time-consuming code
7. **Measure before and after:** Verify optimizations actually improve performance
8. **Consider memory and I/O:** CPU time isn't everything
