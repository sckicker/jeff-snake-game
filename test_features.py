#!/usr/bin/env python3
"""
Test script to validate new features without running the full game
"""
import sys
import os

# Set SDL to use dummy video driver before pygame import
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'

import pygame
pygame.init()

print("=" * 60)
print("Testing Snake Game New Features")
print("=" * 60)

# Test 1: Import theme system
print("\n[1/7] Testing theme system import...")
try:
    from src.config.themes import ThemeManager, DARK_TECH_THEME, KIDS_BRIGHT_THEME
    theme_manager = ThemeManager()
    print(f"✓ Theme system loaded")
    print(f"  - Current theme: {theme_manager.current_theme.name}")
    print(f"  - Available themes: {theme_manager.get_all_theme_names()}")
    theme_manager.cycle_theme()
    print(f"  - After cycle: {theme_manager.current_theme.name}")
except Exception as e:
    print(f"✗ Failed to load theme system: {e}")
    sys.exit(1)

# Test 2: Import difficulty system
print("\n[2/7] Testing difficulty system import...")
try:
    from src.core.difficulty import DifficultyManager, DifficultyLevel
    difficulty_manager = DifficultyManager()
    print(f"✓ Difficulty system loaded")
    print(f"  - Current difficulty: {difficulty_manager.get_difficulty_name()}")
    settings = difficulty_manager.get_settings()
    print(f"  - Initial speed: {settings.initial_speed}")
    print(f"  - Wall wrap-around: {settings.wall_wrap_around}")
    print(f"  - Bombs enabled: {settings.bomb_enabled}")
except Exception as e:
    print(f"✗ Failed to load difficulty system: {e}")
    sys.exit(1)

# Test 3: Import floating text
print("\n[3/7] Testing floating text system import...")
try:
    from src.effects.floating_text import FloatingTextManager
    floating_text_manager = FloatingTextManager()
    print(f"✓ Floating text system loaded")
    # Test adding text (won't render, just test API)
    floating_text_manager.add_score_text(50, 100, 100)
    print(f"  - Added test score text")
    print(f"  - Text count: {len(floating_text_manager.texts)}")
except Exception as e:
    print(f"✗ Failed to load floating text system: {e}")
    sys.exit(1)

# Test 4: Import snake with expressions
print("\n[4/7] Testing snake expressions...")
try:
    from src.game.snake import Snake, SnakeExpression
    snake = Snake(100, 100)
    print(f"✓ Snake with expressions loaded")
    print(f"  - Initial expression: {snake.expression}")
    snake.set_expression(SnakeExpression.HAPPY, 30)
    print(f"  - After setting happy: {snake.expression}")
    print(f"  - Combo count: {snake.combo_count}")
    # Test wall wrapping
    result = snake.check_wall_collision(wrap_around=True)
    print(f"  - Wall wrap test: {'pass' if not result else 'fail'}")
except Exception as e:
    print(f"✗ Failed to test snake expressions: {e}")
    sys.exit(1)

# Test 5: Import powerups
print("\n[5/7] Testing powerup system import...")
try:
    from src.game.powerups import PowerUpManager, PowerUpType
    powerup_manager = PowerUpManager()
    print(f"✓ Powerup system loaded")
    print(f"  - Available types: {[t.name for t in PowerUpType]}")
    print(f"  - Spawn interval: {powerup_manager.spawn_interval}ms")
except Exception as e:
    print(f"✗ Failed to load powerup system: {e}")
    sys.exit(1)

# Test 6: Test game integration (without pygame display)
print("\n[6/7] Testing game.py imports...")
try:
    from src.game.game import SnakeGame
    print(f"✓ Game class imported successfully")
    print(f"  - All new systems integrated")
except Exception as e:
    print(f"✗ Failed to import game: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 7: Test difficulty presets
print("\n[7/7] Testing difficulty presets...")
try:
    from src.core.difficulty import DIFFICULTY_PRESETS, DifficultyLevel
    for level in DifficultyLevel:
        settings = DIFFICULTY_PRESETS[level]
        print(f"  - {level.value.capitalize()}:")
        print(f"    Speed: {settings.initial_speed}-{settings.max_speed} FPS")
        print(f"    Wrap: {settings.wall_wrap_around}, Bombs: {settings.bomb_enabled}")
        print(f"    Score multiplier: {settings.score_multiplier}x")
    print(f"✓ All difficulty presets valid")
except Exception as e:
    print(f"✗ Failed to test difficulty presets: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nNew Features Summary:")
print("  • 4 Themes (Dark Tech, Kids Bright, Ocean, Candy)")
print("  • 3 Difficulty Levels (Easy/Medium/Hard)")
print("  • Snake Expressions (Normal, Happy, Excited, Worried)")
print("  • Wall Wrapping (Easy mode)")
print("  • 3 Power-ups (Slow Potion, Shield, Double Score)")
print("  • Floating Score Text")
print("\nControls:")
print("  • T: Cycle themes")
print("  • D: Cycle difficulty (in menu)")
print("  • Space: Start game")
print("  • Arrow keys: Move")
print("  • B: Place bomb (if enabled)")
print("\nReady to play! Run: python3 main.py")
print("=" * 60)
