#!/bin/bash

echo "📦 创建项目备份包..."

# 创建备份目录
BACKUP_DIR="$HOME/Desktop/game_backup_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# 复制所有项目文件
cp -r /Users/sckicker/Documents/game/* "$BACKUP_DIR/"

# 创建压缩包
cd "$HOME/Desktop"
tar -czf "game_backup_$(date +%Y%m%d_%H%M%S).tar.gz" "$(basename "$BACKUP_DIR")"

echo "✅ 备份完成！"
echo "📁 备份位置: $BACKUP_DIR"
echo "📦 压缩包位置: $HOME/Desktop/game_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

# 显示文件大小
ls -lh "$HOME/Desktop/game_backup_$(date +%Y%m%d_%H%M%S).tar.gz"