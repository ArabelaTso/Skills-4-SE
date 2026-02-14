---
name: environment-setup-assistant
description: "Generate setup scripts and instructions for development environments across platforms. Use when: (1) Setting up new development machines (Python, Node.js, Docker, databases), (2) Creating automated setup scripts for team onboarding, (3) Need cross-platform setup instructions (macOS, Linux, Windows), (4) Installing development tools and dependencies, (5) Configuring version managers and package managers. Provides executable setup scripts, platform-specific guides, and tool installation instructions."
---

# Environment Setup Assistant

Generate automated setup scripts and detailed instructions for development environments across multiple platforms.

## Quick Start

### Generate Setup Script

Specify your requirements and get an automated setup script:

```bash
# Example: Python development environment
bash scripts/setup_python.sh

# Example: Node.js development environment
bash scripts/setup_nodejs.sh

# Example: Docker environment
bash scripts/setup_docker.sh
```

### Get Platform-Specific Instructions

For manual setup or understanding what the scripts do, see **[platform_instructions.md](references/platform_instructions.md)**.

## Common Setup Scenarios

### Scenario 1: New Team Member Onboarding

**Goal**: Set up complete development environment for a new developer

**Approach**:
1. Identify target platform (macOS, Linux, Windows)
2. List required tools (Git, Python, Node.js, Docker, etc.)
3. Generate comprehensive setup script
4. Provide verification checklist

**Example Request**: "Set up a Python and Node.js development environment on macOS"

**Generated Output**:
```bash
#!/usr/bin/env bash
# Complete Development Environment Setup

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Git
brew install git

# Install Python via pyenv
brew install pyenv
pyenv install 3.11.0
pyenv global 3.11.0

# Install Node.js via nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts

# Install Docker Desktop
echo "Please download Docker Desktop from https://www.docker.com/products/docker-desktop"

# Install VS Code
brew install --cask visual-studio-code

# Verify installations
git --version
python --version
node --version
```

### Scenario 2: Project-Specific Setup

**Goal**: Set up environment for a specific project with exact dependencies

**Approach**:
1. Analyze project requirements (package.json, requirements.txt, etc.)
2. Detect required runtime versions
3. Generate setup script with project initialization
4. Include virtual environment or project-specific configuration

**Example Request**: "Create setup script for a Django project requiring Python 3.11 and PostgreSQL"

**Generated Output**:
```bash
#!/usr/bin/env bash
# Django Project Environment Setup

# Install Python 3.11
if ! command -v python3.11 &> /dev/null; then
    # macOS
    brew install python@3.11
    # Linux: sudo apt-get install python3.11
fi

# Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install Django and dependencies
pip install django psycopg2-binary

# Create database
createdb myproject_dev

# Initialize Django project
django-admin startproject myproject .

echo "Setup complete! Activate venv: source venv/bin/activate"
```

### Scenario 3: CI/CD Environment Replication

**Goal**: Replicate CI/CD environment locally

**Approach**:
1. Analyze CI configuration (.github/workflows, .gitlab-ci.yml, etc.)
2. Extract runtime versions and dependencies
3. Generate matching local setup
4. Include container-based option if applicable

**Example Request**: "Match my GitHub Actions environment locally (Ubuntu, Python 3.10, Node 18)"

### Scenario 4: Multi-Language Development

**Goal**: Set up polyglot development environment

**Approach**:
1. Install version managers for each language
2. Set up common tools (Git, Docker, editor)
3. Configure shell environment
4. Provide switching instructions

**Example Request**: "Set up Python, Node.js, and Go development on Linux"

## Setup Script Templates

### Python Development

Use `scripts/setup_python.sh`:
- Installs Python 3.11
- Sets up virtual environment
- Installs common tools (pytest, black, mypy)
- Cross-platform (macOS, Linux, Windows/WSL)

### Node.js Development

Use `scripts/setup_nodejs.sh`:
- Installs Node.js via nvm
- Installs package managers (npm, pnpm)
- Installs global tools (TypeScript, ESLint, Prettier)
- Cross-platform support

### Docker Development

Use `scripts/setup_docker.sh`:
- Installs Docker Engine or Docker Desktop
- Installs Docker Compose
- Adds user to docker group (Linux)
- Verification steps

## Platform-Specific Guidance

### macOS Setup

See **[platform_instructions.md](references/platform_instructions.md#macos-setup)** for:
- Homebrew installation
- Command Line Tools
- Common package installation patterns
- Shell configuration (zsh)

### Linux Setup

See **[platform_instructions.md](references/platform_instructions.md#linux-setup)** for:
- apt-get based installation (Ubuntu/Debian)
- Build tools and dependencies
- systemd service management
- Shell configuration (bash)

### Windows Setup

See **[platform_instructions.md](references/platform_instructions.md#windows-setup)** for:
- WSL 2 setup (recommended)
- Native Windows tools
- PowerShell configuration
- Git Bash alternative

## Development Tools

### Version Managers

See **[tool_guides.md](references/tool_guides.md#version-managers)** for:
- **pyenv**: Python version management
- **nvm**: Node.js version management
- **rbenv**: Ruby version management

### Code Editors

See **[tool_guides.md](references/tool_guides.md#code-editors)** for:
- **VS Code**: Installation and essential extensions
- **JetBrains IDEs**: PyCharm, WebStorm, IntelliJ
- Editor configuration

### Database Tools

See **[tool_guides.md](references/tool_guides.md#database-tools)** for:
- **PostgreSQL**: Installation and pgAdmin
- **MySQL/MariaDB**: Installation and Workbench
- **MongoDB**: Installation and Compass
- **Redis**: Installation and CLI

### Containerization

See **[tool_guides.md](references/tool_guides.md#containerization)** for:
- **Docker**: Setup and Docker Compose
- **Kubernetes**: Minikube and kubectl

## Workflow

### 1. Assess Requirements

Determine what needs to be installed:
```
Questions to ask:
- What programming languages? (Python, Node.js, Java, Go, etc.)
- What databases? (PostgreSQL, MySQL, MongoDB, Redis, etc.)
- What tools? (Docker, Git, editor, etc.)
- What platform? (macOS, Linux, Windows)
- Team-wide or personal setup?
```

### 2. Choose Approach

**Option A: Automated Script**
- Fast, repeatable
- Use for standard setups
- Generates executable bash/shell script

**Option B: Manual Instructions**
- More control, educational
- Use when customization needed
- Provides step-by-step guide

**Option C: Hybrid**
- Script + explanations
- Best for team onboarding
- Script does heavy lifting, docs explain

### 3. Generate Setup Content

Based on requirements, generate:
- Setup script with error handling
- Platform-specific instructions
- Verification steps
- Troubleshooting tips

### 4. Include Verification

Always include verification steps:
```bash
# Verify installations
echo "Verifying setup..."

git --version || echo "❌ Git not installed"
python3 --version || echo "❌ Python not installed"
node --version || echo "❌ Node.js not installed"
docker --version || echo "❌ Docker not installed"

echo "✅ Setup verification complete"
```

### 5. Add Cleanup Instructions

Provide cleanup/uninstall steps if needed:
```bash
# Uninstall (if needed)
brew uninstall python@3.11
rm -rf venv
```

## Best Practices

### 1. Make Scripts Idempotent

Scripts should be safe to run multiple times:
```bash
# Check before installing
if ! command -v python3 &> /dev/null; then
    brew install python@3.11
else
    echo "✅ Python already installed"
fi
```

### 2. Add Platform Detection

Detect OS and adapt:
```bash
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
```

### 3. Provide Progress Feedback

Show what's happening:
```bash
echo "📦 Installing Python..."
brew install python@3.11
echo "✅ Python installed"
```

### 4. Handle Errors Gracefully

```bash
set -e  # Exit on error

# Or handle specific errors
if ! brew install python@3.11; then
    echo "❌ Failed to install Python"
    echo "Try installing manually from python.org"
    exit 1
fi
```

### 5. Include Documentation

Add comments explaining each step:
```bash
# Install Node.js via nvm (Node Version Manager)
# This allows managing multiple Node.js versions
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

## Common Patterns

### Virtual Environment Setup
```bash
# Python
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows

# Node.js (using nvm)
nvm use 18
```

### Tool Installation Check
```bash
check_installed() {
    if command -v $1 &> /dev/null; then
        echo "✅ $1 is installed"
        return 0
    else
        echo "❌ $1 is not installed"
        return 1
    fi
}

check_installed git
check_installed python3
check_installed node
```

### Environment Variable Setup
```bash
# Add to ~/.bashrc or ~/.zshrc
cat >> ~/.bashrc << 'EOF'
export PATH="$HOME/.local/bin:$PATH"
export EDITOR=vim
EOF

source ~/.bashrc
```

## Troubleshooting

### Permission Issues
```bash
# macOS/Linux: Use sudo for system installations
sudo apt-get install package

# Avoid sudo for user-level tools
pip install --user package
```

### PATH Issues
```bash
# Check PATH
echo $PATH

# Add to PATH (temporary)
export PATH="/usr/local/bin:$PATH"

# Add to PATH (permanent, in ~/.bashrc)
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
```

### Version Conflicts
```bash
# Use version managers to avoid conflicts
pyenv install 3.11.0  # Python
nvm install 18.16.0   # Node.js
```

## Complete Example

**Request**: "Set up a full-stack JavaScript development environment on macOS"

**Generated Script**:
```bash
#!/usr/bin/env bash
# Full-Stack JavaScript Development Environment
# Platform: macOS

set -e

echo "🚀 Full-Stack JavaScript Setup"
echo "=============================="

# Install Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Install Git
echo "📦 Installing Git..."
brew install git

# Install Node.js via nvm
echo "📦 Installing Node.js..."
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
nvm install --lts
nvm use --lts

# Install global packages
echo "📦 Installing global packages..."
npm install -g pnpm typescript ts-node nodemon

# Install PostgreSQL
echo "📦 Installing PostgreSQL..."
brew install postgresql@15
brew services start postgresql@15

# Install Redis
echo "📦 Installing Redis..."
brew install redis
brew services start redis

# Install Docker Desktop
echo "📦 Docker Desktop..."
echo "Please download from https://www.docker.com/products/docker-desktop"

# Install VS Code
echo "📦 Installing VS Code..."
brew install --cask visual-studio-code

# Verify setup
echo ""
echo "✅ Setup Complete!"
echo ""
echo "Installed:"
echo "  - Git: $(git --version)"
echo "  - Node.js: $(node --version)"
echo "  - npm: $(npm --version)"
echo "  - pnpm: $(pnpm --version)"
echo "  - TypeScript: $(tsc --version)"
echo "  - PostgreSQL: $(postgres --version)"
echo "  - Redis: $(redis-server --version)"
```
