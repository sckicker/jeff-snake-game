"""
Theme System for Snake Game
Provides multiple color themes for different visual styles
"""
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Theme:
    """Theme configuration containing all color settings"""
    name: str

    # Background colors
    background_primary: Tuple[int, int, int]
    background_secondary: Tuple[int, int, int]
    grid_color: Tuple[int, int, int]
    grid_alpha: int

    # Snake colors
    snake_head_color: Tuple[int, int, int]
    snake_body_color: Tuple[int, int, int]
    snake_eye_color: Tuple[int, int, int]

    # Food colors
    food_color: Tuple[int, int, int]
    food_glow_color: Tuple[int, int, int]

    # UI colors
    text_primary: Tuple[int, int, int]
    text_secondary: Tuple[int, int, int]
    accent_color: Tuple[int, int, int]
    border_color: Tuple[int, int, int]


# Dark Tech Theme (Original)
DARK_TECH_THEME = Theme(
    name="Dark Tech",
    background_primary=(15, 15, 25),
    background_secondary=(10, 10, 15),
    grid_color=(40, 40, 40),
    grid_alpha=30,
    snake_head_color=(0, 255, 100),
    snake_body_color=(0, 200, 50),
    snake_eye_color=(255, 255, 255),
    food_color=(255, 100, 100),
    food_glow_color=(255, 200, 0),
    text_primary=(255, 255, 255),
    text_secondary=(120, 120, 120),
    accent_color=(0, 255, 255),
    border_color=(0, 255, 255),
)

# Kids Bright Theme (Child-friendly bright colors)
KIDS_BRIGHT_THEME = Theme(
    name="Kids Bright",
    background_primary=(255, 250, 240),  # Light beige
    background_secondary=(255, 245, 230),
    grid_color=(200, 200, 200),
    grid_alpha=50,
    snake_head_color=(50, 205, 50),      # Lime green
    snake_body_color=(34, 139, 34),      # Forest green
    snake_eye_color=(0, 0, 0),           # Black eyes
    food_color=(255, 99, 71),            # Tomato red
    food_glow_color=(255, 165, 0),       # Orange
    text_primary=(30, 30, 30),           # Darker gray (improved contrast)
    text_secondary=(100, 100, 100),
    accent_color=(255, 182, 193),        # Light pink
    border_color=(100, 149, 237),        # Cornflower blue
)

# Ocean Theme (Blue underwater aesthetic)
OCEAN_THEME = Theme(
    name="Ocean",
    background_primary=(0, 50, 80),      # Deep ocean blue
    background_secondary=(0, 30, 60),
    grid_color=(0, 80, 120),
    grid_alpha=40,
    snake_head_color=(64, 224, 208),     # Turquoise
    snake_body_color=(0, 139, 139),      # Dark cyan
    snake_eye_color=(255, 255, 255),
    food_color=(255, 215, 0),            # Gold
    food_glow_color=(255, 255, 100),     # Light yellow
    text_primary=(255, 255, 255),
    text_secondary=(150, 200, 220),
    accent_color=(0, 255, 255),          # Cyan
    border_color=(0, 191, 255),          # Deep sky blue
)

# Candy Theme (Sweet pastel colors)
CANDY_THEME = Theme(
    name="Candy",
    background_primary=(255, 240, 245),  # Lavender blush
    background_secondary=(255, 228, 235),
    grid_color=(255, 182, 193),          # Light pink
    grid_alpha=30,
    snake_head_color=(147, 112, 219),    # Medium purple
    snake_body_color=(186, 85, 211),     # Medium orchid
    snake_eye_color=(255, 255, 255),
    food_color=(255, 105, 180),          # Hot pink
    food_glow_color=(255, 192, 203),     # Pink
    text_primary=(50, 0, 100),           # Darker indigo (improved contrast)
    text_secondary=(138, 43, 226),       # Blue violet
    accent_color=(255, 20, 147),         # Deep pink
    border_color=(218, 112, 214),        # Orchid
)


class ThemeManager:
    """Manages theme switching and current theme state"""

    def __init__(self):
        self.themes = {
            'dark_tech': DARK_TECH_THEME,
            'kids_bright': KIDS_BRIGHT_THEME,
            'ocean': OCEAN_THEME,
            'candy': CANDY_THEME,
        }
        self.theme_order = ['dark_tech', 'kids_bright', 'ocean', 'candy']
        self.current_theme_key = 'dark_tech'

    @property
    def current_theme(self) -> Theme:
        """Get the currently active theme"""
        return self.themes[self.current_theme_key]

    def switch_theme(self, theme_key: str) -> bool:
        """Switch to a specific theme by key"""
        if theme_key in self.themes:
            self.current_theme_key = theme_key
            return True
        return False

    def cycle_theme(self) -> str:
        """Cycle to the next theme in order"""
        current_idx = self.theme_order.index(self.current_theme_key)
        next_idx = (current_idx + 1) % len(self.theme_order)
        self.current_theme_key = self.theme_order[next_idx]
        return self.current_theme.name

    def get_all_theme_names(self) -> list:
        """Get list of all available theme names"""
        return [self.themes[key].name for key in self.theme_order]
