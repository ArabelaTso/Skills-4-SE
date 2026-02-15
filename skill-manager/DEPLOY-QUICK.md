# 快速部署到 GitHub Pages

## 🚀 一键部署

```bash
cd skill-manager
./deploy-to-github.sh
```

按照提示操作即可！

## 📋 部署后配置

1. 打开你的 GitHub 仓库
2. 进入 **Settings** → **Pages**
3. 在 **Source** 下选择：
   - Branch: `gh-pages`
   - Folder: `/ (root)`
4. 点击 **Save**

## 🌐 访问网站

几分钟后访问：
```
https://<your-username>.github.io/<repository-name>/
```

## ⚠️ 重要提示

GitHub Pages 只托管前端，用户需要在本地运行后端：

```bash
cd skill-manager/backend
pip install -r requirements.txt
python app.py
```

## 📚 详细文档

查看完整部署指南：[DEPLOYMENT.md](DEPLOYMENT.md)
