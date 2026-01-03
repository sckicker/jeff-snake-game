#!/bin/bash

echo "🔍 Git推送诊断工具"
echo "=================="

# 检查Git配置
echo "1. 检查Git配置:"
echo "   用户名: $(git config user.name)"
echo "   邮箱: $(git config user.email)"
echo ""

# 检查远程仓库
echo "2. 检查远程仓库:"
git remote -v
echo ""

# 检查分支状态
echo "3. 检查分支状态:"
git status
echo ""

# 检查网络连接
echo "4. 检查网络连接:"
echo "   GitHub IP: $(nslookup github.com | grep "Address:" | tail -1)"
echo ""

# 尝试推送并捕获错误
echo "5. 尝试推送:"
git push -u origin main 2>&1 | tee push_error.log

if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✅ 推送成功！"
else
    echo "❌ 推送失败，错误信息已保存到 push_error.log"
    echo ""
    echo "🔧 可能的解决方案:"
    echo "   a) 使用HTTPS Token: git remote set-url origin https://<token>@github.com/sckicker/jeff-snake-game.git"
    echo "   b) 使用SSH: git remote set-url origin git@github.com:sckicker/jeff-snake-game.git"
    echo "   c) 检查GitHub仓库是否存在: https://github.com/sckicker/jeff-snake-game"
    echo "   d) 检查是否有推送权限"
fi