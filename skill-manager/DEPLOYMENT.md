# 部署 Skills Manager 到 GitHub Pages

本指南将帮助你把 Skills Manager 部署到 GitHub Pages，让任何人都可以通过网页访问。

## 📋 前提条件

- 已有 GitHub 账号
- 本地已安装 Git
- 仓库已推送到 GitHub

## 🚀 部署步骤

### 方法一：使用自动化脚本（推荐）

我们提供了一个自动化部署脚本，一键完成所有配置：

```bash
cd skill-manager
./deploy-to-github.sh
```

脚本会自动：
1. 创建 `gh-pages` 分支
2. 配置前端文件
3. 推送到 GitHub
4. 提供访问链接

### 方法二：手动部署

#### 1. 修改前端 API 配置

由于 GitHub Pages 是静态托管，后端需要在本地运行。编辑 `frontend/app.js`：

```javascript
// 开发环境（本地）
const API_BASE = 'http://localhost:8080/api';

// 或者使用你自己部署的后端服务
// const API_BASE = 'https://your-backend-url.com/api';
```

#### 2. 创建 gh-pages 分支

```bash
# 进入 skill-manager 目录
cd skill-manager

# 创建并切换到 gh-pages 分支
git checkout --orphan gh-pages

# 只保留前端文件
git rm -rf .
git checkout main -- frontend/
mv frontend/* .
rm -rf frontend backend

# 创建 index.html（如果需要）
# 前端的 index.html 已经在根目录了

# 提交更改
git add .
git commit -m "Deploy Skills Manager to GitHub Pages"

# 推送到 GitHub
git push origin gh-pages

# 切回 main 分支
git checkout main
```

#### 3. 在 GitHub 上启用 Pages

1. 打开你的 GitHub 仓库
2. 点击 **Settings** (设置)
3. 在左侧菜单找到 **Pages**
4. 在 **Source** 下选择：
   - Branch: `gh-pages`
   - Folder: `/ (root)`
5. 点击 **Save**

#### 4. 访问你的网站

几分钟后，你的网站将在以下地址可用：

```
https://<your-username>.github.io/<repository-name>/
```

例如：
```
https://bella.github.io/LLM4SE-Skills/
```

## 🔧 配置后端

由于 GitHub Pages 只能托管静态文件，后端服务需要单独部署。有以下几种选择：

### 选项 1：本地运行后端（开发/个人使用）

用户需要在本地运行后端服务：

```bash
cd skill-manager/backend
pip install -r requirements.txt
python app.py
```

然后访问 GitHub Pages 上的前端。

### 选项 2：部署后端到云服务（生产环境）

可以将后端部署到：

- **Heroku**（免费层）
- **Railway**（免费层）
- **Render**（免费层）
- **Vercel**（需要配置 Python 运行时）
- **AWS Lambda + API Gateway**
- **Google Cloud Run**

部署后，更新前端的 `API_BASE` 为你的后端 URL。

### 选项 3：使用 GitHub Actions 自动部署

创建 `.github/workflows/deploy.yml`：

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./skill-manager/frontend
```

## 📝 使用说明

部署后，用户访问网站时：

1. **前端**：直接在 GitHub Pages 上访问
2. **后端**：需要在本地运行（或使用你部署的后端服务）

在网站上添加使用说明，告诉用户如何启动后端：

```markdown
## 使用前准备

1. 克隆仓库：
   git clone https://github.com/your-username/LLM4SE-Skills.git

2. 启动后端服务：
   cd LLM4SE-Skills/skill-manager/backend
   pip install -r requirements.txt
   python app.py

3. 访问网站：
   https://your-username.github.io/LLM4SE-Skills/
```

## 🔄 更新部署

当你更新了前端代码后，重新部署：

```bash
cd skill-manager
./deploy-to-github.sh
```

或手动：

```bash
git checkout gh-pages
git merge main --no-edit
# 解决冲突（如果有）
git push origin gh-pages
git checkout main
```

## 🐛 故障排除

### 问题 1：页面显示 404

**解决方案**：
- 确认 GitHub Pages 已启用
- 检查分支是否为 `gh-pages`
- 等待几分钟让 GitHub 构建网站

### 问题 2：前端无法连接后端

**解决方案**：
- 确认后端服务正在运行
- 检查 `app.js` 中的 `API_BASE` 配置
- 检查浏览器控制台的 CORS 错误

### 问题 3：样式或脚本加载失败

**解决方案**：
- 确保所有资源路径是相对路径
- 检查 `index.html` 中的引用：
  ```html
  <link rel="stylesheet" href="styles.css">
  <script src="app.js"></script>
  ```

## 🌟 进阶配置

### 自定义域名

1. 在仓库根目录创建 `CNAME` 文件：
   ```
   skills.yourdomain.com
   ```

2. 在你的域名提供商配置 DNS：
   ```
   Type: CNAME
   Name: skills
   Value: your-username.github.io
   ```

### 启用 HTTPS

GitHub Pages 自动为 `.github.io` 域名提供 HTTPS。

对于自定义域名：
1. 在 GitHub Pages 设置中勾选 "Enforce HTTPS"

## 📚 相关资源

- [GitHub Pages 文档](https://docs.github.com/en/pages)
- [部署 Flask 应用到 Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)
- [CORS 配置指南](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)

## 💡 提示

- 前端是静态的，可以直接托管在 GitHub Pages
- 后端需要服务器运行，建议部署到云服务
- 对于个人使用，本地运行后端即可
- 对于公开使用，需要部署后端到云服务
