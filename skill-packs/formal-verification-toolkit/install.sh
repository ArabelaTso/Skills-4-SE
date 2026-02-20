#!/bin/bash

# Formal Verification Toolkit Installer
# Installs all skills in the formal verification toolkit

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default installation path
INSTALL_PATH="$HOME/.claude/skills"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --path)
            INSTALL_PATH="$2"
            shift 2
            ;;
        -h|--help)
            echo "Usage: $0 [--path INSTALL_PATH]"
            echo ""
            echo "Options:"
            echo "  --path PATH    Installation path (default: ~/.claude/skills)"
            echo "  -h, --help     Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Formal Verification Toolkit Installer             ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Get the repository root (two levels up from this script)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
REPO_ROOT="$( cd "$SCRIPT_DIR/../.." && pwd )"

echo -e "${BLUE}📦 Repository root: ${NC}$REPO_ROOT"
echo -e "${BLUE}📂 Installation path: ${NC}$INSTALL_PATH"
echo ""

# Create installation directory if it doesn't exist
if [ ! -d "$INSTALL_PATH" ]; then
    echo -e "${YELLOW}Creating installation directory...${NC}"
    mkdir -p "$INSTALL_PATH"
fi

# Read skills from pack.json
PACK_JSON="$SCRIPT_DIR/pack.json"
if [ ! -f "$PACK_JSON" ]; then
    echo -e "${RED}Error: pack.json not found${NC}"
    exit 1
fi

# Extract skill names from pack.json
SKILLS=$(python3 -c "import json; print('\n'.join(json.load(open('$PACK_JSON'))['skills']))")

# Count total skills
TOTAL=$(echo "$SKILLS" | wc -l | tr -d ' ')
CURRENT=0
INSTALLED=0
SKIPPED=0

echo -e "${GREEN}Installing $TOTAL skills...${NC}"
echo ""

# Install each skill
while IFS= read -r skill; do
    CURRENT=$((CURRENT + 1))
    echo -e "${BLUE}[$CURRENT/$TOTAL]${NC} Installing ${YELLOW}$skill${NC}..."

    SKILL_PATH="$REPO_ROOT/skills/$skill"

    if [ ! -d "$SKILL_PATH" ]; then
        echo -e "${RED}  ✗ Skill directory not found: $SKILL_PATH${NC}"
        SKIPPED=$((SKIPPED + 1))
        continue
    fi

    # Check if skill is already installed
    if [ -d "$INSTALL_PATH/$skill" ]; then
        echo -e "${YELLOW}  ⚠ Already installed, updating...${NC}"
        rm -rf "$INSTALL_PATH/$skill"
    fi

    # Copy skill to installation directory
    cp -r "$SKILL_PATH" "$INSTALL_PATH/"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}  ✓ Installed successfully${NC}"
        INSTALLED=$((INSTALLED + 1))
    else
        echo -e "${RED}  ✗ Installation failed${NC}"
        SKIPPED=$((SKIPPED + 1))
    fi

done <<< "$SKILLS"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║                Installation Complete                   ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓ Successfully installed: $INSTALLED skills${NC}"
if [ $SKIPPED -gt 0 ]; then
    echo -e "${YELLOW}⚠ Skipped: $SKIPPED skills${NC}"
fi
echo ""
echo -e "${BLUE}📖 Next steps:${NC}"
echo -e "  1. Check the workflow guide: ${YELLOW}$SCRIPT_DIR/demo/verification-workflow.md${NC}"
echo -e "  2. Try the examples: ${YELLOW}$SCRIPT_DIR/examples/${NC}"
echo -e "  3. Start using the skills in Claude Code!"
echo ""
echo -e "${GREEN}Happy verifying! 🎉${NC}"
