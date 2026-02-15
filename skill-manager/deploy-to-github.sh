#!/bin/bash

# Skills Manager - GitHub Pages 部署脚本
# 自动将前端部署到 GitHub Pages

set -e  # 遇到错误立即退出

echo "🚀 开始部署 Skills Manager 到 GitHub Pages..."
echo ""

# 获取当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 当前分支: $CURRENT_BRANCH"

# 确保在正确的目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR/.."

# 检查是否有未提交的更改
if [[ -n $(git status -s) ]]; then
    echo "⚠️  检测到未提交的更改"
    echo ""
    git status -s
    echo ""
    read -p "是否要先提交这些更改？(y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git add .
        read -p "请输入提交信息: " commit_msg
        git commit -m "$commit_msg"
        echo "✅ 更改已提交"
    else
        echo "⚠️  继续部署，但未提交的更改不会包含在部署中"
    fi
fi

# 创建临时目录
TEMP_DIR=$(mktemp -d)
echo "📁 创建临时目录: $TEMP_DIR"

# 复制前端文件到临时目录
echo "📋 复制前端文件..."
cp -r skill-manager/frontend/* "$TEMP_DIR/"

# 创建 README 说明
cat > "$TEMP_DIR/README.md" << 'EOF'
# Skills Manager

这是 LLM4SE-Skills 的 Skills Manager 前端界面。

## 使用方法

1. **启动后端服务**（在本地）：
   ```bash
   git clone https://github.com/your-username/LLM4SE-Skills.git
   cd LLM4SE-Skills/skill-manager/backend
   pip install -r requirements.txt
   python app.py
   ```

2. **访问网站**：
   打开浏览器访问此页面

3. **安装 Skills**：
   - 点击 "📦 Install All Skills" 安装所有技能
   - 或选择特定技能后点击 "✅ Install Selected Skills"

## 注意事项

- 后端服务需要在本地运行（端口 8080）
- 安装的 skills 会保存到 `~/.claude/skills/` 目录
- 需要 Claude Code 才能使用已安装的 skills

## 更多信息

访问主仓库：[LLM4SE-Skills](https://github.com/your-username/LLM4SE-Skills)
EOF

# 检查是否存在 gh-pages 分支
if git show-ref --verify --quiet refs/heads/gh-pages; then
    echo "📌 gh-pages 分支已存在"
    HAS_GH_PAGES=true
else
    echo "📌 gh-pages 分支不存在，将创建新分支"
    HAS_GH_PAGES=false
fi

# 切换到 gh-pages 分支
if [ "$HAS_GH_PAGES" = true ]; then
    echo "🔄 切换到 gh-pages 分支..."
    git checkout gh-pages

    # 清空当前内容（保留 .git）
    echo "🧹 清理旧文件..."
    git rm -rf . 2>/dev/null || true
else
    echo "🌱 创建 gh-pages 分支..."
    git checkout --orphan gh-pages
    git rm -rf . 2>/dev/null || true
fi

# 复制新文件
echo "📦 复制新文件到 gh-pages 分支..."
cp -r "$TEMP_DIR/"* .

# 添加 .nojekyll 文件（禁用 Jekyll 处理）
touch .nojekyll

# 提交更改
echo "💾 提交更改..."
git add .
git commit -m "Deploy Skills Manager to GitHub Pages - $(date '+%Y-%m-%d %H:%M:%S')" || {
    echo "ℹ️  没有更改需要提交"
}

# 推送到 GitHub
echo "⬆️  推送到 GitHub..."
read -p "是否要推送到 GitHub？(y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin gh-pages --force
    echo "✅ 推送成功！"
else
    echo "⏸️  跳过推送"
fi

# 切回原分支
echo "🔙 切回 $CURRENT_BRANCH 分支..."
git checkout "$CURRENT_BRANCH"

# 清理临时目录
echo "🧹 清理临时文件..."
rm -rf "$TEMP_DIR"

echo ""
echo "✨ 部署完成！"
echo ""
echo "📍 你的网站将在以下地址可用（几分钟后）："
echo ""

# 尝试获取 GitHub 仓库信息
REMOTE_URL=$(git config --get remote.origin.url)
if [[ $REMOTE_URL =~ github.com[:/]([^/]+)/([^/.]+) ]]; then
    USERNAME="${BASH_REMATCH[1]}"
    REPO="${BASH_REMATCH[2]}"
    echo "   https://${USERNAME}.github.io/${REPO}/"
    echo ""
    echo "🔧 配置 GitHub Pages："
    echo "   1. 打开 https://github.com/${USERNAME}/${REPO}/settings/pages"
    echo "   2. 在 Source 下选择 'gh-pages' 分支"
    echo "   3. 点击 Save"
else
    echo "   https://<your-username>.github.io/<repository-name>/"
    echo ""
    echo "🔧 配置 GitHub Pages："
    echo "   1. 打开你的 GitHub 仓库设置"
    echo "   2. 找到 Pages 选项"
    echo "   3. 在 Source 下选择 'gh-pages' 分支"
    echo "   4. 点击 Save"
fi

echo ""
echo "⚠️  重要提示："
echo "   - 前端已部署到 GitHub Pages"
echo "   - 用户需要在本地运行后端服务（端口 8080）"
echo "   - 或者将后端部署到云服务（Heroku、Railway 等）"
echo ""
echo "📚 查看完整部署指南："
echo "   cat skill-manager/DEPLOYMENT.md"
echo ""
