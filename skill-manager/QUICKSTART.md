# Skills Manager - 快速入门指南

## 一键启动

### macOS / Linux

```bash
cd skill-manager
./start.sh
```

### Windows

双击 `start.bat` 文件，或在命令行中运行：

```cmd
cd skill-manager
start.bat
```

## 手动启动

如果自动启动脚本不工作，可以手动启动：

### 1. 安装依赖

```bash
cd skill-manager/backend
pip install -r requirements.txt
```

### 2. 启动后端

```bash
python app.py
```

### 3. 打开前端

在浏览器中打开 `skill-manager/frontend/index.html`

## 使用截图

### 主界面
![主界面](screenshots/main.png)

### 安装技能
![安装技能](screenshots/install.png)

## 常见问题

### Q: 端口 5000 被占用怎么办？

A: 编辑 `backend/app.py`，修改最后一行的端口号：

```python
app.run(debug=True, port=5001)  # 改为其他端口
```

同时修改 `frontend/app.js` 中的 API_BASE：

```javascript
const API_BASE = 'http://localhost:5001/api';  // 改为相同端口
```

### Q: 浏览器显示 "Failed to load skills"？

A: 确保后端服务正在运行。检查：

1. 后端终端是否有错误信息
2. 访问 http://localhost:5000/api/skills 是否返回数据
3. 浏览器控制台是否有 CORS 错误

### Q: 技能安装后 Claude Code 看不到？

A: 重启 Claude Code 应用，或运行：

```bash
claude skills list
```

检查技能是否已安装到 `~/.claude/skills/`

## 技术支持

如有问题，请在 GitHub 仓库提交 Issue。
