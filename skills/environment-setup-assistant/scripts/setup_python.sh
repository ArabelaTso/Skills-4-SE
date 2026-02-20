#!/usr/bin/env bash
# Python Development Environment Setup Script
# Supports: macOS, Linux (Ubuntu/Debian), Windows (Git Bash/WSL)

set -e  # Exit on error

echo "🐍 Python Development Environment Setup"
echo "========================================"
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

# Install Python
install_python() {
    echo "📦 Installing Python..."

    if [[ "$OS" == "macos" ]]; then
        if ! command -v brew &> /dev/null; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        brew install python@3.11

    elif [[ "$OS" == "linux" ]]; then
        sudo apt-get update
        sudo apt-get install -y python3.11 python3.11-venv python3-pip

    elif [[ "$OS" == "windows" ]]; then
        echo "Please install Python from https://www.python.org/downloads/"
        echo "Make sure to check 'Add Python to PATH' during installation"
        exit 1
    fi

    echo "✅ Python installed"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    install_python
else
    echo "✅ Python already installed: $(python3 --version)"
fi

echo ""

# Install pipenv
echo "📦 Installing pipenv..."
pip3 install --user pipenv
echo "✅ pipenv installed"

echo ""

# Install development tools
echo "📦 Installing development tools..."

if [[ "$OS" == "macos" ]]; then
    brew install git

elif [[ "$OS" == "linux" ]]; then
    sudo apt-get install -y git build-essential
fi

echo "✅ Development tools installed"

echo ""

# Setup virtual environment
echo "🔧 Setting up virtual environment..."
python3 -m venv venv

if [[ "$OS" == "windows" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "✅ Virtual environment created and activated"

echo ""

# Install common Python packages
echo "📦 Installing common Python packages..."
pip install --upgrade pip
pip install pytest black flake8 mypy pylint

echo "✅ Common packages installed"

echo ""
echo "🎉 Python development environment setup complete!"
echo ""
echo "To activate the virtual environment in the future, run:"
if [[ "$OS" == "windows" ]]; then
    echo "  source venv/Scripts/activate"
else
    echo "  source venv/bin/activate"
fi
