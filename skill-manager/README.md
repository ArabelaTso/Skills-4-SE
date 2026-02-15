# Skills Manager

一个简单易用的 Web 界面，用于管理和安装 LLM4SE Skills 到 Claude Code。

## 🌐 在线访问

**前端界面已部署到 GitHub Pages：**

👉 [https://your-username.github.io/LLM4SE-Skills/skill-manager/frontend/](https://your-username.github.io/LLM4SE-Skills/skill-manager/frontend/)

> 注意：在线版本是完全静态的，不需要后端服务。点击安装按钮会显示安装命令供你复制执行。

## 功能特性

- 📦 **浏览所有技能** - 查看 74+ 个可用技能
- ✅ **选择性安装** - 选择需要的技能获取安装命令
- 🔍 **搜索和筛选** - 按名称、描述或类别筛选技能
- 📊 **分类展示** - 9 大类别，清晰组织
- 🎨 **彩色类别标签** - 每个类别都有独特的渐变色
- 📖 **双语帮助文档** - 中英文切换的使用指南
- 🎨 **现代化界面** - 美观易用的用户界面
- 🚀 **完全静态** - 可部署到 GitHub Pages，无需后端

## 快速开始

### 在线使用（推荐）

1. 访问 GitHub Pages 部署的版本
2. 浏览和搜索技能
3. 选择需要的技能
4. 点击安装按钮获取安装命令
5. 在终端执行命令安装

### 本地使用

```bash
cd skill-manager/frontend
python3 -m http.server 8000
# 访问 http://localhost:8000
```

或直接在浏览器中打开 `frontend/index.html`。

## 使用方法

### 安装技能

1. 在界面上浏览和搜索技能
2. 点击技能卡片选择需要的技能
3. 点击 **"Install Selected Skills"** 按钮
4. 复制显示的安装命令
5. 在终端执行命令

**示例安装命令：**

```bash
git clone https://github.com/YOUR_USERNAME/LLM4SE-Skills.git
cd LLM4SE-Skills
mkdir -p ~/.claude/skills
cp -r unit-test-generator ~/.claude/skills/
cp -r code-review-assistant ~/.claude/skills/
```

### 搜索技能

在搜索框中输入关键词，可以按名称或描述搜索技能。

### 按类别筛选

点击顶部的类别标签，可以按以下类别筛选技能：

- **Code Generation**（代码生成）- 7 个技能
- **Testing**（测试）- 13 个技能
- **Documentation**（文档）- 10 个技能
- **Code Quality**（代码质量）- 9 个技能
- **Requirements**（需求）- 7 个技能
- **DevOps**（开发运维）- 5 个技能
- **Debugging**（调试）- 5 个技能
- **Verification**（验证）- 7 个技能
- **Maintenance**（维护）- 3 个技能

## 技能安装位置

技能将被安装到：

```
~/.claude/skills/
```

这是 Claude Code 的默认技能目录。

## API 端点

后端提供以下 API 端点：

### GET /api/skills

获取所有可用技能列表。

**响应示例：**
```json
{
  "skills": [
    {
      "name": "unit-test-generator",
      "description": "Generates unit tests for functions and classes...",
      "installed": false,
      "path": "/path/to/skill"
    }
  ],
  "total": 50
}
```

### POST /api/install

安装选定的技能。

**请求体：**
```json
{
  "skills": ["unit-test-generator", "code-review-assistant"]
}
```

**响应示例：**
```json
{
  "installed": 2,
  "failed": 0,
  "details": {
    "installed": ["unit-test-generator", "code-review-assistant"],
    "failed": []
  }
}
```

### POST /api/uninstall

卸载选定的技能。

**请求体：**
```json
{
  "skills": ["unit-test-generator"]
}
```

### GET /api/status

获取安装状态信息。

**响应示例：**
```json
{
  "claude_skills_dir": "/Users/username/.claude/skills",
  "exists": true,
  "writable": true
}
```

## 技术栈

### 前端（静态）
- HTML5
- CSS3 (现代化渐变设计)
- Vanilla JavaScript (无框架依赖)
- 静态 JSON 数据文件

### 后端（可选 - 仅用于本地开发）
- Python 3.8+
- Flask (Web 框架)
- Flask-CORS (跨域支持)
- PyYAML (YAML 解析)

## 项目结构

```
skill-manager/
├── frontend/
│   ├── index.html           # 主页面
│   ├── styles.css           # 样式文件
│   ├── app.js               # 前端逻辑
│   └── skills-data.json     # 静态技能数据（自动生成）
├── backend/
│   ├── app.py               # Flask 后端服务（可选）
│   └── requirements.txt     # Python 依赖
├── generate-skills-data.py  # 数据生成脚本
└── README.md                # 本文件
```

## 更新技能数据

当仓库中添加新技能时，需要重新生成静态数据文件：

```bash
cd skill-manager
python3 generate-skills-data.py
```

这会扫描所有 SKILL.md 文件并更新 `frontend/skills-data.json`。

## 部署到 GitHub Pages

1. 确保 `frontend/skills-data.json` 是最新的
2. 将更改推送到 GitHub
3. 在仓库设置中启用 GitHub Pages
4. 选择 `main` 分支和 `/` 根目录
5. 访问 `https://YOUR_USERNAME.github.io/LLM4SE-Skills/skill-manager/frontend/`

## API 端点（仅后端模式）

如果使用本地后端服务，提供以下 API 端点：
