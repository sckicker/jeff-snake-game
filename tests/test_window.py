#!/usr/bin/env python3
"""
Test script for window display modes
Run this to test different window configurations
"""

import pygame
import sys
from window_config import window_manager, get_window_size
from config import *

def test_window_modes():
    """Test different window display modes"""
    pygame.init()
    
    print("🖥️  测试窗口显示模式")
    print("=" * 40)
    
    # Test available modes
    available_modes = window_manager.get_available_modes()
    print(f"📋 可用模式: {available_modes}")
    
    # Test each mode
    test_modes = ['windowed', 'large']
    if 'fullscreen' in available_modes:
        test_modes.append('fullscreen')
    
    for mode in test_modes:
        print(f"\n🧪 测试 {mode} 模式...")
        
        # Set display mode
        window_manager.set_display_mode(mode)
        
        # Create window
        screen = window_manager.create_window()
        if not screen:
            print(f"❌ {mode} 模式创建失败")
            continue
            
        # Get actual window size
        width, height = get_window_size()
        print(f"✅ {mode} 模式: {width}x{height}")
        
        # Simple test display
        screen.fill((50, 50, 50))
        font = pygame.font.Font(None, 36)
        
        # Display mode info
        mode_text = font.render(f"Mode: {mode}", True, (255, 255, 255))
        size_text = font.render(f"Size: {width}x{height}", True, (255, 255, 255))
        instruction_text = font.render("Press any key to continue...", True, (200, 200, 200))
        
        screen.blit(mode_text, (50, 50))
        screen.blit(size_text, (50, 100))
        screen.blit(instruction_text, (50, height - 100))
        
        pygame.display.flip()
        
        # Wait for key press
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    waiting = False
                    
        pygame.display.quit()
    
    print("\n🎉 窗口测试完成！")
    print("现在可以运行 python main.py 开始游戏")

if __name__ == "__main__":
    test_window_modes()