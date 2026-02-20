#!/usr/bin/env bash
# Node.js Development Environment Setup Script
# Supports: macOS, Linux (Ubuntu/Debian), Windows (Git Bash/WSL)

set -e  # Exit on error

echo "📦 Node.js Development Environment Setup"
echo "========================================="
echo ""

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "Detected OS: $OS"
echo ""

# Install Node.js via nvm
install_nodejs() {
    echo "📦 Installing Node.js via nvm..."

    # Install nvm
    if [ ! -d "$HOME/.nvm" ]; then
        echo "Installing nvm..."
        curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

        # Load nvm
        export NVM_DIR="$HOME/.nvm"
        [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
    fi

    # Load nvm for current session
    export NVM_DIR="$HOME/.nvm"
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

    # Install Node.js LTS
    nvm install --lts
    nvm use --lts
    nvm alias default node

    echo "✅ Node.js installed: $(node --version)"
    echo "✅ npm installed: $(npm --version)"
}

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    install_nodejs
else
    echo "✅ Node.js already installed: $(node --version)"
    echo "✅ npm already installed: $(npm --version)"
fi

echo ""

# Install pnpm (fast package manager)
echo "📦 Installing pnpm..."
npm install -g pnpm
echo "✅ pnpm installed: $(pnpm --version)"

echo ""

# Install global development tools
echo "📦 Installing global development tools..."
npm install -g typescript ts-node nodemon eslint prettier

echo "✅ Global tools installed:"
echo "  - TypeScript: $(tsc --version)"
echo "  - ts-node: $(ts-node --version)"
echo "  - nodemon: $(nodemon --version)"

echo ""
echo "🎉 Node.js development environment setup complete!"
echo ""
echo "Installed tools:"
echo "  - Node.js (via nvm)"
echo "  - npm, pnpm"
echo "  - TypeScript, ts-node"
echo "  - ESLint, Prettier"
echo "  - nodemon"
