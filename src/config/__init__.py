"""
Configuration module for Enhanced Snake Game
Contains game settings and window configurations
"""

from .config import *
from .window_config import window_manager, create_game_window, toggle_fullscreen_mode, get_window_size

__all__ = ['window_manager', 'create_game_window', 'toggle_fullscreen_mode', 'get_window_size']