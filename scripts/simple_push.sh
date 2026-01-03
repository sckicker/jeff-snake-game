#!/bin/bash

echo "🚀 开始推送到GitHub..."

# 检查网络连接
echo "检查网络连接..."
ping -c 1 github.com > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ 无法连接到GitHub，请检查网络连接"
    exit 1
fi

echo "✅ 网络连接正常"

# 尝试推送
echo "正在推送代码到GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo "✅ 推送成功！"
    echo "🌐 访问你的仓库: https://github.com/sckicker/jeff-snake-game"
else
    echo "❌ 推送失败"
    echo "可能的解决方案:"
    echo "1. 检查GitHub用户名是否正确: sckicker"
    echo "2. 检查仓库是否存在: jeff-snake-game"
    echo "3. 检查是否有推送权限"
    echo "4. 尝试使用GitHub Token进行身份验证"
fi