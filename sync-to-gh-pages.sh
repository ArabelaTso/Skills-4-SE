#!/bin/bash

# 自动同步 main 分支的技能到 gh-pages 并更新网站
# 使用方法: ./sync-to-gh-pages.sh

set -e  # 遇到错误立即退出

echo "🚀 开始同步 main 到 gh-pages..."
echo

# 保存当前分支
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 当前分支: $CURRENT_BRANCH"

# 确保工作目录干净
if [[ -n $(git status -s) ]]; then
    echo "⚠️  工作目录有未提交的更改"
    echo "请先提交或暂存更改："
    git status -s
    exit 1
fi

# 切换到 main 并拉取最新
echo
echo "📥 更新 main 分支..."
git checkout main
git pull origin main

# 切换到 gh-pages
echo
echo "🔄 切换到 gh-pages 分支..."
git checkout gh-pages

# 合并 main
echo
echo "🔀 合并 main 到 gh-pages..."
if git merge main -m "Sync skills from main"; then
    echo "✅ 合并成功"
else
    echo "❌ 合并失败，可能有冲突"
    echo "请手动解决冲突后运行："
    echo "  git add ."
    echo "  git commit"
    echo "  git push origin gh-pages"
    exit 1
fi

# 重新生成技能数据
echo
echo "📊 重新生成技能数据..."
cd skill-manager
python generate-skills-data.py
cd ..

# 提交更新
echo
echo "💾 提交网站更新..."
git add .
if git diff --staged --quiet; then
    echo "ℹ️  没有需要提交的更改"
else
    git commit -m "Update website: sync skills from main and regenerate data"
    echo "✅ 提交成功"
fi

# 推送到远程
echo
echo "📤 推送到远程 gh-pages..."
git push origin gh-pages

# 切回原来的分支
echo
echo "🔙 切回 $CURRENT_BRANCH 分支..."
git checkout "$CURRENT_BRANCH"

echo
echo "🎉 同步完成！"
echo
echo "📋 总结："
echo "  ✅ main 分支已合并到 gh-pages"
echo "  ✅ 技能数据已重新生成"
echo "  ✅ 更改已推送到远程"
echo "  ✅ 已切回 $CURRENT_BRANCH 分支"
echo
echo "🌐 网站将在几分钟内更新: https://arabelatso.github.io/Skills-4-SE/"
