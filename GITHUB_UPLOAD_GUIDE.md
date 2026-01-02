# GitHub上传指南

## 步骤1：在GitHub上创建新仓库

1. 登录你的GitHub账户
2. 点击右上角的 "+" 号，选择 "New repository"
3. 输入仓库名称，比如 "snake-game"
4. 选择公开(Public)或私有(Private)
5. 不要勾选 "Initialize this repository with a README"
6. 点击 "Create repository"

## 步骤2：在本地初始化Git仓库

打开终端，进入项目目录：

```bash
cd /Users/sckicker/Documents/game
```

初始化Git仓库：

```bash
git init
```

## 步骤3：添加文件到Git

添加所有文件：

```bash
git add .
```

或者只添加特定文件：

```bash
git add README.md config.py food.py game.py main.py requirements.txt snake.py sound_manager.py
```

## 步骤4：提交文件

```bash
git commit -m "Initial commit: Enhanced Snake Game with visual effects and sound"
```

## 步骤5：连接到GitHub仓库

将本地仓库连接到GitHub（用你的仓库URL替换）：

```bash
git remote add origin https://github.com/你的用户名/snake-game.git
```

## 步骤6：推送到GitHub

```bash
git push -u origin master
```

如果GitHub默认分支是main：

```bash
git branch -M main
git push -u origin main
```

## 常见问题解决

### 1. 如果提示需要身份验证：

设置Git用户名和邮箱：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub邮箱"
```

### 2. 如果使用HTTPS推送需要密码：

使用GitHub个人访问令牌代替密码，或者设置SSH密钥。

### 3. 如果推送失败：

先拉取远程仓库：

```bash
git pull origin main --allow-unrelated-histories
```

然后再次推送：

```bash
git push origin main
```

## 验证上传成功

1. 访问你的GitHub仓库页面
2. 确认所有文件都已上传
3. 检查README是否正确显示

## 后续更新

如果以后需要更新代码：

```bash
# 添加修改的文件
git add 文件名

# 提交修改
git commit -m "描述你的修改"

# 推送到GitHub
git push origin main
```

## 项目亮点

这个项目包含：
- 🐍 增强的贪吃蛇游戏
- 🎨 炫酷的视觉效果（渐变、发光、动画）
- 🔊 程序化生成的音效
- 📚 完整的教学文档
- 🎯 适合Python初学者学习

祝你上传成功！🚀