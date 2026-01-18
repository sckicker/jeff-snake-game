"""
Enhanced Launch Options for Snake Game
Provides interactive window mode selection
"""

import pygame
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.window_config import window_manager

def show_launch_options():
    """Display launch options and let user choose window mode"""
    print("🐍 Enhanced Snake Game - Launch Options")
    print("=" * 50)
    print("")
    print("🖥️  选择显示模式:")
    print("")
    print("1️⃣  窗口模式 (1200x900) - 推荐")
    print("2️⃣  大窗口模式 (1400x1050)")
    print("3️⃣  全屏模式")
    print("4️⃣  自定义分辨率")
    print("5️⃣  启动游戏 (默认窗口模式)")
    print("")
    
    while True:
        choice = input("请输入选项 (1-5): ").strip()
        
        if choice == '1':
            window_manager.set_display_mode('windowed')
            print("✅ 选择窗口模式")
            break
        elif choice == '2':
            window_manager.set_display_mode('large')
            print("✅ 选择大窗口模式")
            break
        elif choice == '3':
            window_manager.set_display_mode('fullscreen')
            print("✅ 选择全屏模式")
            break
        elif choice == '4':
            try:
                width = int(input("请输入宽度 (800-1920): "))
                height = int(input("请输入高度 (600-1080): "))
                
                # Validate input
                if 800 <= width <= 1920 and 600 <= height <= 1080:
                    window_manager.set_display_mode('custom', (width, height))
                    print(f"✅ 选择自定义分辨率: {width}x{height}")
                    break
                else:
                    print("❌ 分辨率超出范围，请重新输入")
            except ValueError:
                print("❌ 请输入有效的数字")
        elif choice == '5':
            print("✅ 使用默认窗口模式启动")
            break
        else:
            print("❌ 无效选项，请重新选择")
    
    print("")
    print("🚀 启动游戏...")
    return True

def quick_launch():
    """Quick launch with default settings"""
    print("🚀 快速启动游戏...")
    return True

def show_controls_reminder():
    """Show game controls reminder"""
    print("")
    print("🎮 游戏控制:")
    print("   ↑↓←→ 方向键 - 控制蛇移动")
    print("   P - 暂停/继续")
    print("   F - 切换全屏模式")
    print("   R - 重新开始 (游戏结束后)")
    print("   Q - 退出 (游戏结束后)")
    print("")

if __name__ == "__main__":
    # Run launch options
    if show_launch_options():
        show_controls_reminder()
        
        # Import and start the game
        from src.game.game import SnakeGame
        game = SnakeGame()
        game.run()