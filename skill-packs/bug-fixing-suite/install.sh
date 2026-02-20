#!/bin/bash

# Bug Fixing Suite Installer
# Installs all bug detection, localization, and repair skills

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Default installation directory
DEFAULT_TARGET="$HOME/.claude/skills"
TARGET="${1:-$DEFAULT_TARGET}"

# If --target flag is used
if [ "$1" = "--target" ]; then
    TARGET="$2"
fi

PACK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$PACK_DIR/../.." && pwd)"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Bug Fixing Suite Installer${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Installation target: ${GREEN}${TARGET}${NC}"
echo ""

# Create target directory
mkdir -p "$TARGET"

# Skills to install
SKILLS=(
    "bug-localization"
    "bug-to-patch-generator"
    "bug-reproduction-test-generator"
    "regression-root-cause-analyzer"
    "semantic-bug-detector"
    "static-bug-detector"
    "test-guided-bug-detector"
    "szz-bug-identifier"
    "semantic-szz-analyzer"
    "counterexample-debugger"
    "runtime-error-explainer"
    "vulnerability-root-cause-analyzer"
)

echo -e "${YELLOW}Installing ${#SKILLS[@]} skills...${NC}"
echo ""

INSTALLED=0
SKIPPED=0
FAILED=0

for skill in "${SKILLS[@]}"; do
    SOURCE="$REPO_ROOT/skills/$skill"
    DEST="$TARGET/$skill"

    if [ ! -d "$SOURCE" ]; then
        echo -e "${RED}✗${NC} $skill (not found in repository)"
        ((FAILED++))
        continue
    fi

    if [ -d "$DEST" ]; then
        echo -e "${YELLOW}⊙${NC} $skill (already installed, skipping)"
        ((SKIPPED++))
        continue
    fi

    cp -r "$SOURCE" "$DEST"
    echo -e "${GREEN}✓${NC} $skill"
    ((INSTALLED++))
done

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Installation Complete!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo -e "Summary:"
echo -e "  ${GREEN}Installed: $INSTALLED${NC}"
echo -e "  ${YELLOW}Skipped: $SKIPPED${NC}"
echo -e "  ${RED}Failed: $FAILED${NC}"
echo ""

if [ $INSTALLED -gt 0 ]; then
    echo -e "${GREEN}Skills are ready to use!${NC}"
    echo ""
    echo "Try these commands:"
    echo "  /bug-localization --help"
    echo "  /bug-to-patch-generator --help"
    echo "  /static-bug-detector --help"
fi

if [ $FAILED -gt 0 ]; then
    echo ""
    echo -e "${YELLOW}Note: Some skills were not found. This may be normal if they haven't been created yet.${NC}"
fi
