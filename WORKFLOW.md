# 工作流程指南

## 📝 添加新技能的完整流程

### 步骤 1: 在 main 分支创建新技能

```bash
# 1. 切换到 main 分支
git checkout main

# 2. 确保是最新的
git pull origin main

# 3. 创建新技能（例如使用 skill-creator）
# ... 创建你的技能文件 ...

# 4. 提交新技能
git add .
git commit -m "Add new skill: your-skill-name"
git push origin main
```

### 步骤 2: 自动同步到 gh-pages

```bash
# 运行自动同步脚本
./sync-to-gh-pages.sh
```

就这么简单！脚本会自动：
- ✅ 合并 main 到 gh-pages
- ✅ 重新生成技能数据
- ✅ 提交并推送更新
- ✅ 切回你原来的分支

### 步骤 3: 验证网站更新

等待几分钟后访问：https://arabelatso.github.io/Skills-4-SE/

---

## 🔧 手动同步（如果脚本失败）

如果自动脚本失败，可以手动执行：

```bash
# 1. 切换到 gh-pages
git checkout gh-pages

# 2. 合并 main
git merge main

# 3. 重新生成数据
cd skill-manager
python generate-skills-data.py
cd ..

# 4. 提交并推送
git add .
git commit -m "Update website with new skills"
git push origin gh-pages

# 5. 切回 main
git checkout main
```

---

## 📋 快速参考

| 任务 | 分支 | 命令 |
|------|------|------|
| 添加新技能 | main | `git checkout main` |
| 修改技能 | main | `git checkout main` |
| 同步到网站 | 自动 | `./sync-to-gh-pages.sh` |
| 修改网站UI | gh-pages | `git checkout gh-pages` |

---

## ⚠️ 注意事项

1. **始终在 main 分支开发技能**
2. **使用脚本同步到 gh-pages**
3. **不要直接在 gh-pages 添加技能**（除非是紧急情况）
4. **提交前确保工作目录干净**

---

## 🆘 常见问题

### Q: 我不小心在 gh-pages 添加了技能怎么办？

A: 按照之前的方法，合并到 main：
```bash
git checkout main
git merge gh-pages --allow-unrelated-histories
# 解决冲突
git push origin main
```

### Q: 脚本执行失败怎么办？

A: 查看错误信息，通常是：
- 工作目录有未提交的更改 → 先提交
- 合并冲突 → 手动解决冲突
- 网络问题 → 稍后重试

### Q: 如何只更新网站UI而不添加技能？

A: 直接在 gh-pages 分支修改：
```bash
git checkout gh-pages
# 修改 skill-manager/frontend/ 下的文件
git add .
git commit -m "Update website UI"
git push origin gh-pages
```

---

## 🎯 最佳实践

✅ **DO (推荐做法)**:
- 在 main 分支开发所有技能
- 使用自动化脚本同步
- 保持提交信息清晰
- 定期同步到 gh-pages

❌ **DON'T (避免做法)**:
- 不要在 gh-pages 直接添加技能
- 不要跳过同步步骤
- 不要在有未提交更改时运行脚本
- 不要手动编辑 skills-data.json（应该用脚本生成）
