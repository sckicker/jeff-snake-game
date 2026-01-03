#!/bin/bash

# GitHub上传脚本 - 请根据你的实际情况修改

echo "🚀 准备上传到GitHub..."

# 请替换为你的GitHub用户名和仓库名
GITHUB_USERNAME="sckicker"
REPO_NAME="e-snake-game"

# 添加远程仓库（使用HTTPS）
git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git

# 推送到GitHub
git branch -M main
git push -u origin main

echo "✅ 上传完成！请访问: https://github.com/$GITHUB_USERNAME/$REPO_NAME"

# 如果推送失败，可以尝试以下备用命令:
# git remote remove origin
# git remote add origin https://github.com/$GITHUB_USERNAME/$REPO_NAME.git
# git push -f origin main
