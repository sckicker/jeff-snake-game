#!/bin/bash

echo "🔍 详细GitHub推送诊断"
echo "========================"

# 1. 检查仓库是否存在
echo "1. 检查GitHub仓库是否存在..."
curl -s -o /dev/null -w "%{http_code}" https://github.com/sckicker/jeff-snake-game > http_status.txt
HTTP_STATUS=$(cat http_status.txt)

echo "   HTTP状态码: $HTTP_STATUS"
if [ "$HTTP_STATUS" = "200" ]; then
    echo "   ✅ 仓库存在"
elif [ "$HTTP_STATUS" = "404" ]; then
    echo "   ❌ 仓库不存在，请先在GitHub创建仓库"
    echo "   🌐 访问: https://github.com/new"
    echo "   📝 仓库名: jeff-snake-game"
    echo "   ⚠️  不要勾选'Initialize this repository with a README'"
else
    echo "   ⚠️  未知状态: $HTTP_STATUS"
fi

# 2. 检查Git配置
echo ""
echo "2. Git配置检查:"
echo "   用户名: $(git config user.name)"
echo "   邮箱: $(git config user.email)"

# 3. 检查远程仓库
echo ""
echo "3. 远程仓库配置:"
git remote -v

# 4. 检查本地提交
echo ""
echo "4. 本地提交历史:"
git log --oneline -5

# 5. 尝试推送并显示详细错误
echo ""
echo "5. 尝试推送..."
git push -u origin main 2>&1 | tee push_detailed.log

PUSH_EXIT_CODE=${PIPESTATUS[0]}

if [ $PUSH_EXIT_CODE -eq 0 ]; then
    echo ""
    echo "🎉 推送成功！"
    echo "🌐 访问你的仓库: https://github.com/sckicker/jeff-snake-game"
else
    echo ""
    echo "❌ 推送失败 (退出码: $PUSH_EXIT_CODE)"
    echo ""
    echo "🔧 解决方案:"
    
    # 检查错误类型
    if grep -q "Permission denied" push_detailed.log; then
        echo "   🔐 身份验证问题:"
        echo "      - 使用GitHub Token: https://github.com/settings/tokens"
        echo "      - 或者使用SSH密钥: https://docs.github.com/en/authentication/connecting-to-github-with-ssh"
    elif grep -q "repository not found" push_detailed.log; then
        echo "   📂 仓库不存在:"
        echo "      - 请先在GitHub创建仓库: https://github.com/new"
        echo "      - 仓库名: jeff-snake-game"
    elif grep -q "could not read" push_detailed.log; then
        echo "   🔒 权限问题:"
        echo "      - 检查仓库是否为私有，需要推送权限"
    else
        echo "   🌐 网络或未知问题:"
        echo "      - 检查网络连接"
        echo "      - 查看详细错误信息: cat push_detailed.log"
    fi
fi

echo ""
echo "📋 完整错误日志已保存到: push_detailed.log"