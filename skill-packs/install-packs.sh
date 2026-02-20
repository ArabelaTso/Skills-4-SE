#!/bin/bash

# Install Multiple Skill Packs
# Usage: ./install-packs.sh [pack1] [pack2] ...

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Default installation path
INSTALL_PATH="$HOME/.claude/skills"

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║          Skill Packs Batch Installer                  ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check if any packs specified
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No skill packs specified${NC}"
    echo ""
    echo "Usage: $0 [pack1] [pack2] ..."
    echo ""
    echo "Available packs:"
    for pack_dir in "$SCRIPT_DIR"/*/; do
        if [ -f "$pack_dir/pack.json" ]; then
            pack_name=$(basename "$pack_dir")
            echo "  - $pack_name"
        fi
    done
    exit 1
fi

echo -e "${BLUE}📂 Installation path: ${NC}$INSTALL_PATH"
echo -e "${BLUE}📦 Packs to install: ${NC}$#"
echo ""

TOTAL=$#
CURRENT=0
SUCCESS=0
FAILED=0

# Install each pack
for pack_name in "$@"; do
    CURRENT=$((CURRENT + 1))
    echo -e "${BLUE}[$CURRENT/$TOTAL]${NC} Installing ${YELLOW}$pack_name${NC}..."

    PACK_DIR="$SCRIPT_DIR/$pack_name"

    if [ ! -d "$PACK_DIR" ]; then
        echo -e "${RED}  ✗ Pack not found: $pack_name${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi

    if [ ! -f "$PACK_DIR/install.sh" ]; then
        echo -e "${RED}  ✗ Install script not found${NC}"
        FAILED=$((FAILED + 1))
        continue
    fi

    # Run the pack's install script
    cd "$PACK_DIR"
    if bash install.sh --path "$INSTALL_PATH" > /dev/null 2>&1; then
        echo -e "${GREEN}  ✓ Installed successfully${NC}"
        SUCCESS=$((SUCCESS + 1))
    else
        echo -e "${RED}  ✗ Installation failed${NC}"
        FAILED=$((FAILED + 1))
    fi
    cd "$SCRIPT_DIR"
done

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              Installation Summary                      ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✓ Successfully installed: $SUCCESS packs${NC}"
if [ $FAILED -gt 0 ]; then
    echo -e "${RED}✗ Failed: $FAILED packs${NC}"
fi
echo ""
echo -e "${GREEN}All done! 🎉${NC}"
