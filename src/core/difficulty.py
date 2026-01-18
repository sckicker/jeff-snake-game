"""
Difficulty System for Snake Game
Provides three difficulty levels with different game parameters
"""
from enum import Enum
from dataclasses import dataclass


class DifficultyLevel(Enum):
    """Available difficulty levels"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class DifficultySettings:
    """Configuration for a specific difficulty level"""
    initial_speed: int          # Starting FPS
    max_speed: int              # Maximum FPS
    speed_increment: int        # Speed increase per food
    bomb_enabled: bool          # Whether bombs appear
    wall_wrap_around: bool      # True = can wrap through walls (Easy mode)
    score_multiplier: float     # Score multiplier for difficulty


# Difficulty presets
DIFFICULTY_PRESETS = {
    DifficultyLevel.EASY: DifficultySettings(
        initial_speed=6,
        max_speed=15,
        speed_increment=1,
        bomb_enabled=False,
        wall_wrap_around=True,   # Can wrap through walls
        score_multiplier=0.5
    ),
    DifficultyLevel.MEDIUM: DifficultySettings(
        initial_speed=10,
        max_speed=25,
        speed_increment=2,
        bomb_enabled=True,
        wall_wrap_around=False,  # Wall collision
        score_multiplier=1.0
    ),
    DifficultyLevel.HARD: DifficultySettings(
        initial_speed=15,
        max_speed=35,
        speed_increment=3,
        bomb_enabled=True,
        wall_wrap_around=False,  # Wall collision
        score_multiplier=2.0
    ),
}


class DifficultyManager:
    """Manages game difficulty settings"""

    def __init__(self):
        self.current_level = DifficultyLevel.MEDIUM

    def get_settings(self) -> DifficultySettings:
        """Get current difficulty settings"""
        return DIFFICULTY_PRESETS[self.current_level]

    def set_difficulty(self, level: DifficultyLevel):
        """Set the difficulty level"""
        self.current_level = level

    def get_difficulty_name(self) -> str:
        """Get the current difficulty name"""
        return self.current_level.value.capitalize()

    def cycle_difficulty(self) -> str:
        """Cycle to next difficulty level"""
        levels = list(DifficultyLevel)
        current_idx = levels.index(self.current_level)
        next_idx = (current_idx + 1) % len(levels)
        self.current_level = levels[next_idx]
        return self.get_difficulty_name()
