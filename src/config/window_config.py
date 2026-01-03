"""
Enhanced Window Configuration for Snake Game
Provides flexible window sizing and display options
"""

import pygame
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from .config import *

class WindowManager:
    """Manages window display modes and screen configurations"""
    
    def __init__(self):
        """Initialize window manager with display options"""
        self.display_modes = {
            'windowed': (1200, 900),
            'large': (1400, 1050),
            'fullscreen': None,  # Will be set to current display resolution
            'custom': None
        }
        self.current_mode = 'windowed'
        self.screen = None
        
    def get_available_modes(self):
        """Get list of available display modes"""
        modes = ['windowed', 'large']
        
        # Add fullscreen if display info is available
        pygame.init()
        display_info = pygame.display.Info()
        if display_info.current_w and display_info.current_h:
            modes.append('fullscreen')
            self.display_modes['fullscreen'] = (display_info.current_w, display_info.current_h)
            
        return modes
    
    def set_display_mode(self, mode, custom_size=None):
        """Set the display mode"""
        if mode == 'custom' and custom_size:
            self.display_modes['custom'] = custom_size
            self.current_mode = 'custom'
        elif mode in self.display_modes:
            self.current_mode = mode
        else:
            print(f"⚠️  Unknown display mode: {mode}")
            return False
            
        return True
    
    def create_window(self):
        """Create the game window based on current mode"""
        size = self.display_modes.get(self.current_mode)
        
        if not size:
            print(f"⚠️  Invalid display mode: {self.current_mode}")
            return None
            
        try:
            if self.current_mode == 'fullscreen':
                self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
                print(f"🖥️  Fullscreen mode: {size[0]}x{size[1]}")
            elif self.current_mode == 'large':
                self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                print(f"🖼️  Large window mode: {size[0]}x{size[1]}")
            else:
                self.screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                print(f"🖼️  Windowed mode: {size[0]}x{size[1]}")
                
            pygame.display.set_caption(GAME_TITLE)
            return self.screen
            
        except pygame.error as e:
            print(f"❌ 创建窗口失败: {e}")
            return None
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        if self.current_mode == 'fullscreen':
            self.current_mode = 'windowed'
        else:
            # Check if fullscreen mode is available
            available_modes = self.get_available_modes()
            if 'fullscreen' not in available_modes:
                print("⚠️  Fullscreen mode not available on this system")
                return None
            self.current_mode = 'fullscreen'
            
        return self.create_window()
    
    def get_current_size(self):
        """Get current window size"""
        if self.screen:
            return self.screen.get_size()
        return self.display_modes.get(self.current_mode, (WINDOW_WIDTH, WINDOW_HEIGHT))

# 全局窗口管理器实例
window_manager = WindowManager()

# 快捷函数
def create_game_window():
    """Create the game window using window manager"""
    return window_manager.create_window()

def toggle_fullscreen_mode():
    """Toggle fullscreen mode"""
    return window_manager.toggle_fullscreen()

def get_window_size():
    """Get current window size"""
    return window_manager.get_current_size()