# 部署检查清单

在部署到 GitHub Pages 之前，请确认以下事项：

## ✅ 部署前检查

- [ ] 所有更改已提交到 Git
- [ ] 前端代码已测试并正常工作
- [ ] API 端点配置正确（`app.js` 中的 `API_BASE`）
- [ ] 已阅读 [DEPLOYMENT.md](DEPLOYMENT.md) 部署指南

## 🚀 部署步骤

### 选项 1：自动部署（推荐）

```bash
cd skill-manager
./deploy-to-github.sh
```

### 选项 2：GitHub Actions 自动部署

1. 提交并推送更改到 `main` 分支
2. GitHub Actions 会自动部署
3. 查看部署状态：Actions 标签页

### 选项 3：手动部署

参考 [DEPLOYMENT.md](DEPLOYMENT.md) 中的手动部署步骤

## 🔧 部署后配置

1. **启用 GitHub Pages**
   - 仓库 Settings → Pages
   - Source: `gh-pages` 分支
   - 点击 Save

2. **验证部署**
   - 访问 `https://<username>.github.io/<repo>/`
   - 检查页面是否正常加载
   - 测试功能是否正常

3. **配置后端**
   - 本地运行：`cd backend && python app.py`
   - 或部署到云服务（Heroku、Railway 等）

## 📝 部署后测试

- [ ] 页面可以正常访问
- [ ] 样式和脚本正确加载
- [ ] 可以看到技能列表
- [ ] 搜索功能正常
- [ ] 筛选功能正常
- [ ] 帮助文档可以打开
- [ ] 语言切换正常

## 🐛 常见问题

### 页面显示 404
- 等待 5-10 分钟让 GitHub 构建
- 检查 Pages 设置是否正确
- 确认 `gh-pages` 分支存在

### 无法连接后端
- 确认后端服务正在运行
- 检查端口是否为 8080
- 查看浏览器控制台错误

### 样式加载失败
- 检查文件路径是否正确
- 确认所有文件都在 `gh-pages` 分支

## 📚 相关文档

- [DEPLOYMENT.md](DEPLOYMENT.md) - 完整部署指南
- [DEPLOY-QUICK.md](DEPLOY-QUICK.md) - 快速部署指南
- [README.md](README.md) - 项目说明

## 🎉 部署成功！

恭喜！你的 Skills Manager 现在可以在线访问了。

分享链接给其他人：
```
https://<your-username>.github.io/<repository-name>/
```

记得告诉他们需要在本地运行后端服务！
