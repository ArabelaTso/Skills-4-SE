#!/bin/bash
# bisect_template.sh - Template for git bisect run scripts
#
# Usage:
#   1. Copy this template and customize for your specific test
#   2. Make it executable: chmod +x your_bisect_test.sh
#   3. Run: git bisect run ./your_bisect_test.sh
#
# Exit codes:
#   0   = Good commit (test passes)
#   1   = Bad commit (test fails)
#   125 = Skip commit (cannot test)

set -e  # Exit on error (but we'll handle errors explicitly)

# Configuration
COMMIT=$(git rev-parse --short HEAD)
LOG_FILE="bisect_log_${COMMIT}.txt"
TIMEOUT=30  # seconds

# ============================================================================
# Logging Functions
# ============================================================================

log() {
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $1" | tee -a "$LOG_FILE"
}

log_good() {
    log "✓ GOOD: $1"
    exit 0
}

log_bad() {
    log "✗ BAD: $1"
    exit 1
}

log_skip() {
    log "⊘ SKIP: $1"
    exit 125
}

# ============================================================================
# Setup Phase
# ============================================================================

log "Testing commit: $COMMIT"
log "Message: $(git log -1 --format=%s)"

# Check for known broken commits (optional)
if git log -1 --format=%s | grep -qE "WIP|DO NOT MERGE|BROKEN"; then
    log_skip "Commit marked as work in progress"
fi

# ============================================================================
# Build Phase
# ============================================================================

log "Building..."

# Example: Make-based build
if ! make clean > /dev/null 2>&1; then
    log_skip "Make clean failed"
fi

if ! make build > /dev/null 2>&1; then
    log_skip "Build failed"
fi

# Example: npm-based build
# if [ -f package.json ]; then
#     if ! npm ci --silent 2>&1 | tee -a "$LOG_FILE"; then
#         log_skip "npm install failed"
#     fi
#     if ! npm run build 2>&1 | tee -a "$LOG_FILE"; then
#         log_skip "npm build failed"
#     fi
# fi

# Example: Python setup
# if [ -f requirements.txt ]; then
#     if ! pip install -q -r requirements.txt 2>&1 | tee -a "$LOG_FILE"; then
#         log_skip "pip install failed"
#     fi
# fi

log "Build successful"

# ============================================================================
# Test Phase
# ============================================================================

log "Running tests..."

# Clean environment for determinism
export RANDOM_SEED=42
export TZ=UTC
rm -rf /tmp/test_cache_*

# Run test with timeout
TEST_OUTPUT=$(mktemp)

# Example: Run a specific test command
# Customize this section for your specific test
if timeout ${TIMEOUT}s make test > "$TEST_OUTPUT" 2>&1; then
    TEST_RESULT=0
else
    TEST_RESULT=$?
fi

# Handle timeout
if [ $TEST_RESULT -eq 124 ]; then
    log_skip "Test timeout after ${TIMEOUT}s"
fi

# ============================================================================
# Result Interpretation
# ============================================================================

# Save test output to log
cat "$TEST_OUTPUT" >> "$LOG_FILE"
rm "$TEST_OUTPUT"

if [ $TEST_RESULT -eq 0 ]; then
    log_good "Test passed"
else
    log_bad "Test failed with exit code $TEST_RESULT"
fi
