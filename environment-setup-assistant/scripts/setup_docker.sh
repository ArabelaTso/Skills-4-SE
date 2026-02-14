#!/usr/bin/env bash
# Docker Development Environment Setup Script
# Supports: macOS, Linux (Ubuntu/Debian)

set -e  # Exit on error

echo "🐳 Docker Development Environment Setup"
echo "========================================"
echo ""

# Detect OS
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "linux"
    else
        echo "unknown"
    fi
}

OS=$(detect_os)
echo "Detected OS: $OS"
echo ""

# Install Docker
install_docker() {
    if [[ "$OS" == "macos" ]]; then
        echo "📦 Installing Docker Desktop for macOS..."
        echo "Please download Docker Desktop from:"
        echo "https://www.docker.com/products/docker-desktop"
        echo ""
        echo "After installation, start Docker Desktop and return here."
        read -p "Press Enter when Docker Desktop is running..."

    elif [[ "$OS" == "linux" ]]; then
        echo "📦 Installing Docker on Linux..."

        # Remove old versions
        sudo apt-get remove -y docker docker-engine docker.io containerd runc || true

        # Install dependencies
        sudo apt-get update
        sudo apt-get install -y \
            ca-certificates \
            curl \
            gnupg \
            lsb-release

        # Add Docker's official GPG key
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

        # Set up repository
        echo \
          "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
          $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

        # Install Docker Engine
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

        # Add user to docker group
        sudo usermod -aG docker $USER

        echo "✅ Docker installed"
        echo "⚠️  You need to log out and back in for group changes to take effect"
    fi
}

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    install_docker
else
    echo "✅ Docker already installed: $(docker --version)"
fi

echo ""

# Verify Docker is running
echo "🔍 Verifying Docker installation..."
if docker ps &> /dev/null; then
    echo "✅ Docker is running"
else
    echo "⚠️  Docker is installed but not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo ""

# Install Docker Compose (if not already included)
if ! command -v docker-compose &> /dev/null && [[ "$OS" == "linux" ]]; then
    echo "📦 Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "✅ Docker Compose installed: $(docker-compose --version)"
else
    echo "✅ Docker Compose already available"
fi

echo ""
echo "🎉 Docker development environment setup complete!"
echo ""
echo "Quick test:"
echo "  docker run hello-world"
