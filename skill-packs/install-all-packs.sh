#!/bin/bash

# Install All Skill Packs
# Automatically detects and installs all available skill packs

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

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Install All Skill Packs                         ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Discover all skill packs
PACKS=()
for pack_dir in "$SCRIPT_DIR"/*/; do
    if [ -f "$pack_dir/pack.json" ]; then
        pack_name=$(basename "$pack_dir")
        PACKS+=("$pack_name")
    fi
done

if [ ${#PACKS[@]} -eq 0 ]; then
    echo -e "${RED}No skill packs found${NC}"
    exit 1
fi

echo -e "${BLUE}📂 Installation path: ${NC}$INSTALL_PATH"
echo -e "${BLUE}📦 Found ${#PACKS[@]} skill packs:${NC}"
for pack in "${PACKS[@]}"; do
    echo "  - $pack"
done
echo ""

read -p "Install all packs? (y/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled"
    exit 0
fi

echo ""

TOTAL=${#PACKS[@]}
CURRENT=0
SUCCESS=0
FAILED=0

# Install each pack
for pack_name in "${PACKS[@]}"; do
    CURRENT=$((CURRENT + 1))
    echo -e "${BLUE}[$CURRENT/$TOTAL]${NC} Installing ${YELLOW}$pack_name${NC}..."

    PACK_DIR="$SCRIPT_DIR/$pack_name"

    if [ ! -f "$PACK_DIR/install.sh" ]; then
        echo -e "${RED}  ✗ Install script not found${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Run the pack's install script
    cd "$PACK_DIR"
    if bash install.sh --path "$INSTALL_PATH"; then
        echo -e "${GREEN}  ✓ Installed successfully${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "${RED}  ✗ Installation failed${NC}"
        FAILED=$((FAILED + 1))
    fi
    cd "$SCRIPT_DIR"
    echo ""
done

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              Installation Complete                     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓ Successfully installed: $SUCCESS packs${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}✗ Failed: $FAILED packs${NC}"
fi
echo ""
echo -e "${BLUE}📖 Next steps:${NC}"
echo -e "  1. Check individual pack documentation in skill-packs/"
echo -e "  2. Try the examples and demos"
echo -e "  3. Start using the skills in Claude Code!"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
