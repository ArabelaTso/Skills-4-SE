# Development Tool Setup Guides

## Table of Contents
- [Version Managers](#version-managers)
- [Code Editors](#code-editors)
- [Database Tools](#database-tools)
- [Containerization](#containerization)
- [CI/CD Tools](#cicd-tools)

---

## Version Managers

### pyenv (Python Version Manager)

**Purpose**: Manage multiple Python versions

**Installation**

macOS/Linux:
```bash
curl https://pyenv.run | bash
```

Add to `~/.bashrc` or `~/.zshrc`:
```bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

**Usage**:
```bash
# List available versions
pyenv install --list

# Install specific version
pyenv install 3.11.0

# Set global version
pyenv global 3.11.0

# Set local version (per-directory)
pyenv local 3.9.0
```

### nvm (Node Version Manager)

**Purpose**: Manage multiple Node.js versions

**Installation**:
```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
```

Add to shell profile:
```bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
```

**Usage**:
```bash
# Install latest LTS
nvm install --lts

# Install specific version
nvm install 18.16.0

# Use version
nvm use 18.16.0

# Set default
nvm alias default 18.16.0

# List installed versions
nvm ls
```

### rbenv (Ruby Version Manager)

**Purpose**: Manage multiple Ruby versions

**Installation**:

macOS:
```bash
brew install rbenv ruby-build
```

Linux:
```bash
git clone https://github.com/rbenv/rbenv.git ~/.rbenv
git clone https://github.com/rbenv/ruby-build.git ~/.rbenv/plugins/ruby-build
```

**Usage**:
```bash
# Install Ruby
rbenv install 3.2.0

# Set global version
rbenv global 3.2.0

# Set local version
rbenv local 2.7.0
```

---

## Code Editors

### Visual Studio Code

**Installation**:

macOS:
```bash
brew install --cask visual-studio-code
```

Linux:
```bash
wget -O code.deb 'https://code.visualstudio.com/sha/download?build=stable&os=linux-deb-x64'
sudo apt install ./code.deb
```

Windows: Download from https://code.visualstudio.com/

**Essential Extensions**:
```bash
# Python
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance

# JavaScript/TypeScript
code --install-extension dbaeumer.vscode-eslint
code --install-extension esbenp.prettier-vscode

# Docker
code --install-extension ms-azuretools.vscode-docker

# Git
code --install-extension eamodio.gitlens

# Remote Development
code --install-extension ms-vscode-remote.remote-wsl
code --install-extension ms-vscode-remote.remote-ssh
```

**Settings**:
```json
{
    "editor.formatOnSave": true,
    "editor.tabSize": 4,
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "eslint.enable": true,
    "prettier.singleQuote": true
}
```

### JetBrains IDEs

**PyCharm (Python)**:
- Download: https://www.jetbrains.com/pycharm/download/
- Community Edition is free

**WebStorm (JavaScript/TypeScript)**:
- Download: https://www.jetbrains.com/webstorm/download/
- 30-day trial, then paid

**IntelliJ IDEA (Java/Kotlin)**:
- Download: https://www.jetbrains.com/idea/download/
- Community Edition is free

---

## Database Tools

### PostgreSQL

**Installation**:

macOS:
```bash
brew install postgresql@15
brew services start postgresql@15
```

Linux:
```bash
sudo apt-get install -y postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Initial Setup**:
```bash
# Create database
createdb myapp_dev

# Connect
psql myapp_dev
```

**GUI Client - pgAdmin**:
```bash
# macOS
brew install --cask pgadmin4

# Linux
sudo apt-get install pgadmin4
```

### MySQL/MariaDB

**Installation**:

macOS:
```bash
brew install mysql
brew services start mysql
```

Linux:
```bash
sudo apt-get install -y mysql-server
sudo systemctl start mysql
sudo systemctl enable mysql
```

**Secure Installation**:
```bash
sudo mysql_secure_installation
```

**GUI Client - MySQL Workbench**:
```bash
# macOS
brew install --cask mysqlworkbench

# Linux
sudo apt-get install mysql-workbench
```

### MongoDB

**Installation**:

macOS:
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

Linux:
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

**GUI Client - MongoDB Compass**:
Download from https://www.mongodb.com/products/compass

### Redis

**Installation**:

macOS:
```bash
brew install redis
brew services start redis
```

Linux:
```bash
sudo apt-get install -y redis-server
sudo systemctl start redis-server
```

**Test**:
```bash
redis-cli ping
# Should return: PONG
```

---

## Containerization

### Docker

See main setup scripts for Docker installation.

**Useful Docker Compose Example**:

```yaml
# docker-compose.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: password
      POSTGRES_DB: myapp_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

**Commands**:
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Execute command in container
docker-compose exec postgres psql -U postgres
```

### Kubernetes (k8s)

**Minikube (Local Kubernetes)**:

macOS:
```bash
brew install minikube
minikube start
```

Linux:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start
```

**kubectl**:

macOS:
```bash
brew install kubectl
```

Linux:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

---

## CI/CD Tools

### GitHub Actions

No installation needed - runs on GitHub's servers.

**Example Workflow** (`.github/workflows/test.yml`):
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: pytest
```

### Jenkins (Self-hosted)

**Installation with Docker**:
```bash
docker run -d -p 8080:8080 -p 50000:50000 \
  -v jenkins_home:/var/jenkins_home \
  jenkins/jenkins:lts
```

Access at http://localhost:8080

**Get initial password**:
```bash
docker exec $(docker ps -q -f name=jenkins) cat /var/jenkins_home/secrets/initialAdminPassword
```

### GitLab Runner (For GitLab CI)

**Installation**:

Linux:
```bash
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt-get install gitlab-runner
```

**Register Runner**:
```bash
sudo gitlab-runner register
```

---

## Additional Development Tools

### Postman (API Testing)

macOS:
```bash
brew install --cask postman
```

Download: https://www.postman.com/downloads/

### Insomnia (API Testing)

macOS:
```bash
brew install --cask insomnia
```

Download: https://insomnia.rest/download

### HTTPie (CLI HTTP Client)

```bash
# macOS
brew install httpie

# Linux
sudo apt-get install httpie

# Usage
http GET https://api.github.com/users/github
```

### jq (JSON Processor)

```bash
# macOS
brew install jq

# Linux
sudo apt-get install jq

# Usage
curl -s https://api.github.com/users/github | jq '.name'
```

### tmux (Terminal Multiplexer)

```bash
# macOS
brew install tmux

# Linux
sudo apt-get install tmux

# Usage
tmux new -s dev
tmux attach -t dev
```

### htop (Process Viewer)

```bash
# macOS
brew install htop

# Linux
sudo apt-get install htop
```

---

## Environment-Specific Tools

### macOS-Specific

**iTerm2** (Better Terminal):
```bash
brew install --cask iterm2
```

**Rectangle** (Window Management):
```bash
brew install --cask rectangle
```

### Linux-Specific

**Terminator** (Terminal Emulator):
```bash
sudo apt-get install terminator
```

**Tilix** (Terminal Emulator):
```bash
sudo apt-get install tilix
```

### Windows-Specific

**Windows Terminal**: Install from Microsoft Store

**WSL 2**: Essential for development on Windows
```powershell
wsl --install
```

**Chocolatey** (Package Manager):
```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```
