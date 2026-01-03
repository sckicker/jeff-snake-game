"""
Enhanced Snake Game Main Entry Point with Sound Effects
"""

from game import SnakeGame

def main():
    """Main function with launch options"""
    print("🐍 Welcome to Enhanced Snake Game! 🐍")
    print("✨ Enhanced with visual effects, animations and sound effects")
    print("🔊 Sound effects enabled - Different sounds for different collisions!")
    print("")
    print("🖥️  Enhanced display features:")
    print("   • Large window mode (1200x900)")
    print("   • Fullscreen mode support")
    print("   • Customizable window sizes")
    print("   • Borderless window option")
    print("")
    print("Game Controls:")
    print("🎮 Use arrow keys to control snake movement")
    print("⏸️  Press P to pause/resume game")
    print("🔄 Press R to restart after game over")
    print("❌ Press Q to quit after game over")
    print("🖥️  Press F to toggle fullscreen mode")
    print("🎵 Press M to toggle background music")
    print("🎶 Press N to switch music style (retro/chiptune/ambient)")
    print("")
    print("Sound Effects:")
    print("🍎 Eating food - High pitched beep")
    print("💥 Collision - Low pitched crash sound")
    print("🎵 Game over - Deep tone")
    print("⏸️  Pause/Resume - Short beep")
    print("⚡ Speed up - Quick high tone")
    print("🎵 Background music - Multiple styles: retro, chiptune, ambient")
    print("🎶 Press N to switch between music styles")
    print("")
    
    # Ask user if they want to configure display options
    print("🚀 启动选项:")
    print("1️⃣  快速启动 (默认窗口模式)")
    print("2️⃣  自定义显示设置")
    
    choice = input("请选择 (1-2, 默认1): ").strip() or "1"
    
    if choice == "2":
        # Import and run launch options
        try:
            from launch_options import show_launch_options
            if not show_launch_options():
                return
        except KeyboardInterrupt:
            print("\n❌ 用户取消")
            return
    else:
        print("🚀 快速启动游戏...")
    
    print("")
    print("🎮 开始游戏！")
    
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()