"""
Enhanced Snake Game Main Entry Point with Sound Effects
"""

from game import SnakeGame

def main():
    """Main function"""
    print("🐍 Welcome to Enhanced Snake Game! 🐍")
    print("✨ Enhanced with visual effects, animations and sound effects")
    print("🔊 Sound effects enabled - Different sounds for different collisions!")
    print("")
    print("Game Controls:")
    print("🎮 Use arrow keys to control snake movement")
    print("⏸️  Press P to pause/resume game")
    print("🔄 Press R to restart after game over")
    print("❌ Press Q to quit after game over")
    print("")
    print("Sound Effects:")
    print("🍎 Eating food - High pitched beep")
    print("💥 Collision - Low pitched crash sound")
    print("🎵 Game over - Deep tone")
    print("⏸️  Pause/Resume - Short beep")
    print("⚡ Speed up - Quick high tone")
    print("")
    print("🚀 Starting enhanced game with sound effects...")
    
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()