#!/bin/bash

echo "🚀 使用GitHub镜像站点推送..."

# 移除原有远程仓库
git remote remove origin 2>/dev/null

# 使用GitHub镜像（hub.fastgit.org）
echo "正在连接到GitHub镜像..."
git remote add origin https://hub.fastgit.org/sckicker/jeff-snake-game.git

# 尝试推送
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 镜像推送成功！"
else
    echo "❌ 镜像推送失败，尝试其他方案..."
fi