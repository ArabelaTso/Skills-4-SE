# Platform-Specific Setup Instructions

## Table of Contents
- [macOS Setup](#macos-setup)
- [Linux Setup](#linux-setup)
- [Windows Setup](#windows-setup)

---

## macOS Setup

### System Requirements
- macOS 10.15 (Catalina) or later
- At least 8GB RAM
- Command Line Tools or Xcode

### Initial Setup

#### 1. Install Homebrew
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, add Homebrew to PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

#### 2. Install Command Line Tools
```bash
xcode-select --install
```

### Common Development Tools

#### Git
```bash
brew install git
git --version
```

Configure Git:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Python
```bash
# Install Python 3.11
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

#### Node.js (via nvm)
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Load nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Install Node.js LTS
nvm install --lts
nvm use --lts
```

#### Docker Desktop
1. Download from https://www.docker.com/products/docker-desktop
2. Install the .dmg file
3. Start Docker Desktop from Applications
4. Verify: `docker --version`

#### VS Code
```bash
brew install --cask visual-studio-code
```

### Shell Configuration

macOS uses zsh by default. Configure your `~/.zshrc`:

```bash
# Add to ~/.zshrc

# Homebrew
eval "$(/opt/homebrew/bin/brew shellenv)"

# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Python
export PATH="/opt/homebrew/opt/python@3.11/bin:$PATH"

# Aliases
alias python=python3
alias pip=pip3
```

---

## Linux Setup

### Ubuntu/Debian-based Systems

#### System Update
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Essential Build Tools
```bash
sudo apt-get install -y build-essential curl git wget
```

### Common Development Tools

#### Git
```bash
sudo apt-get install -y git

# Configure
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Python
```bash
# Install Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Create symlinks (optional)
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.11 1
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
```

#### Node.js (via nvm)
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Reload shell configuration
source ~/.bashrc

# Install Node.js LTS
nvm install --lts
nvm use --lts
nvm alias default node
```

#### Docker
```bash
# Install dependencies
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in for group changes to take effect
```

#### VS Code
```bash
# Download and install
wget -O code.deb 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'
sudo apt install ./code.deb
rm code.deb
```

### Shell Configuration

Configure your `~/.bashrc`:

```bash
# Add to ~/.bashrc

# nvm
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"

# Aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
```

---

## Windows Setup

### Windows Subsystem for Linux (WSL) - Recommended

#### 1. Enable WSL
Open PowerShell as Administrator:
```powershell
wsl --install
```

This installs WSL 2 and Ubuntu by default.

#### 2. Set Up Ubuntu on WSL
After reboot, Ubuntu will launch automatically. Create a user account.

Update the system:
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

#### 3. Install Windows Terminal (Optional but Recommended)
Install from Microsoft Store: https://aka.ms/terminal

### Development Tools in WSL

Follow the [Linux Setup](#linux-setup) instructions above within your WSL Ubuntu environment.

### Native Windows Tools

#### Git for Windows
1. Download from https://git-scm.com/download/win
2. Install with default options
3. Configure:
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Python
1. Download from https://www.python.org/downloads/
2. **Important**: Check "Add Python to PATH" during installation
3. Verify in Command Prompt:
```cmd
python --version
pip --version
```

#### Node.js
1. Download from https://nodejs.org/
2. Install LTS version
3. Verify in Command Prompt:
```cmd
node --version
npm --version
```

#### Docker Desktop for Windows
1. Download from https://www.docker.com/products/docker-desktop
2. Install and enable WSL 2 backend
3. Start Docker Desktop
4. Verify: `docker --version`

#### VS Code
1. Download from https://code.visualstudio.com/
2. Install with default options
3. Install "Remote - WSL" extension for WSL integration

### PowerShell Configuration

Configure your PowerShell profile (`$PROFILE`):

```powershell
# Create profile if it doesn't exist
if (!(Test-Path -Path $PROFILE)) {
    New-Item -ItemType File -Path $PROFILE -Force
}

# Edit profile
notepad $PROFILE
```

Add to profile:
```powershell
# Aliases
Set-Alias -Name ll -Value Get-ChildItem
Set-Alias -Name python3 -Value python
Set-Alias -Name pip3 -Value pip

# Functions
function which($name) {
    Get-Command $name | Select-Object -ExpandProperty Definition
}
```

### Git Bash (Alternative to WSL)

Git for Windows includes Git Bash, a Unix-like terminal:

1. Install Git for Windows
2. Launch Git Bash
3. Follow similar commands as Linux setup
4. Configuration file: `~/.bashrc`

---

## Cross-Platform Considerations

### Environment Variables

**macOS/Linux** (`~/.bashrc` or `~/.zshrc`):
```bash
export API_KEY="your-key-here"
export DATABASE_URL="postgresql://localhost/mydb"
```

**Windows** (PowerShell `$PROFILE`):
```powershell
$env:API_KEY = "your-key-here"
$env:DATABASE_URL = "postgresql://localhost/mydb"
```

**Windows** (System Environment Variables):
- Right-click "This PC" → Properties
- Advanced system settings → Environment Variables
- Add/edit user or system variables

### Path Separators

- **Unix-like**: `/` (forward slash)
- **Windows**: `\` (backslash) or `/` (forward slash often works)

### Line Endings

Configure Git to handle line endings:

**macOS/Linux**:
```bash
git config --global core.autocrlf input
```

**Windows**:
```bash
git config --global core.autocrlf true
```

### File Permissions

Unix-like systems use file permissions (chmod). Windows uses different permission model:

**macOS/Linux**:
```bash
chmod +x script.sh
```

**Windows**: Right-click → Properties → Security

---

## Verification Checklist

After setup, verify your environment:

### All Platforms
```bash
# Git
git --version

# Python
python --version  # or python3 --version
pip --version     # or pip3 --version

# Node.js
node --version
npm --version

# Docker
docker --version
docker ps

# Editor
code --version  # VS Code
```

### Create Test Project
```bash
# Create directory
mkdir test-project
cd test-project

# Initialize Git
git init

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Initialize Node.js project
npm init -y

# Verify Docker
docker run hello-world
```

If all commands work successfully, your environment is ready! 🎉
