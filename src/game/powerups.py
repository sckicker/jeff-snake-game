"""
Power-up System for Snake Game
Provides collectible items that grant temporary abilities
"""
import pygame
import random
import math
from enum import Enum, auto
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.config import *


class PowerUpType(Enum):
    """Available power-up types"""
    SLOW_POTION = auto()    # Reduces speed temporarily
    SHIELD = auto()         # Protects from one death
    DOUBLE_SCORE = auto()   # Doubles score temporarily


class PowerUp:
    """Base power-up class"""

    def __init__(self, x, y, powerup_type):
        """
        Initialize power-up
        Args:
            x, y: Position
            powerup_type: PowerUpType enum value
        """
        self.x = x
        self.y = y
        self.type = powerup_type
        self.active = True
        self.spawn_time = pygame.time.get_ticks()
        self.lifetime = 10000  # 10 seconds before disappearing
        self.pulse_timer = 0

        # Type-specific properties
        if powerup_type == PowerUpType.SLOW_POTION:
            self.color = (100, 149, 237)  # Blue
            self.duration = 5000  # 5 seconds
            self.name = "Slow Potion"
        elif powerup_type == PowerUpType.SHIELD:
            self.color = (255, 215, 0)  # Gold
            self.duration = 3000  # 3 seconds
            self.name = "Shield"
        elif powerup_type == PowerUpType.DOUBLE_SCORE:
            self.color = (255, 20, 147)  # Pink
            self.duration = 8000  # 8 seconds
            self.name = "Double Score"

    def update(self):
        """Update power-up state"""
        self.pulse_timer += 1
        # Check if expired
        if pygame.time.get_ticks() - self.spawn_time > self.lifetime:
            self.active = False

    def draw(self, screen):
        """Draw the power-up with pulsing animation and name label"""
        if not self.active:
            return

        # Enhanced pulsing effect (larger range)
        pulse = 1 + 0.35 * math.sin(self.pulse_timer * 0.1)
        size = int(GRID_SIZE * 1.2 * pulse)  # Increased from 0.8 to 1.2 (50% larger)

        center_x = self.x + GRID_SIZE // 2
        center_y = self.y + GRID_SIZE // 2

        # Draw 3-layer glow effect (instead of single layer)
        for i, (glow_size, alpha) in enumerate([(15, 30), (10, 50), (5, 70)]):
            glow_surface = pygame.Surface((size + glow_size * 2, size + glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.color, alpha),
                              (size // 2 + glow_size, size // 2 + glow_size), size // 2 + glow_size)
            screen.blit(glow_surface, (self.x - glow_size, self.y - glow_size))

        # Draw main circle
        pygame.draw.circle(screen, self.color, (center_x, center_y), size // 2)

        # Draw icon based on type
        self._draw_icon(screen, center_x, center_y, size // 2)

        # Draw border
        pygame.draw.circle(screen, WHITE, (center_x, center_y), size // 2, 2)

        # Draw name label below the icon
        font = pygame.font.Font(None, 18)
        label_text = font.render(self.name, True, (0, 0, 0))
        label_bg = font.render(self.name, True, WHITE)

        # Semi-transparent white background for label
        label_rect = label_text.get_rect(center=(center_x, center_y + GRID_SIZE // 2 + 12))
        bg_surface = pygame.Surface((label_rect.width + 6, label_rect.height + 2), pygame.SRCALPHA)
        bg_surface.fill((255, 255, 255, 200))
        screen.blit(bg_surface, (label_rect.x - 3, label_rect.y - 1))

        # Draw text
        screen.blit(label_text, label_rect)

    def _draw_icon(self, screen, cx, cy, radius):
        """Draw type-specific icon"""
        if self.type == PowerUpType.SLOW_POTION:
            # Draw potion bottle
            # Bottle neck
            pygame.draw.rect(screen, WHITE, (cx - 3, cy - radius + 2, 6, 4))
            # Bottle body
            pygame.draw.rect(screen, WHITE, (cx - 5, cy - 4, 10, 10), 2)
        elif self.type == PowerUpType.SHIELD:
            # Draw shield
            points = [
                (cx, cy - radius + 2),
                (cx + radius - 2, cy),
                (cx, cy + radius - 2),
                (cx - radius + 2, cy),
            ]
            pygame.draw.polygon(screen, WHITE, points, 2)
        elif self.type == PowerUpType.DOUBLE_SCORE:
            # Draw "x2" text
            font = pygame.font.Font(None, int(radius * 1.2))
            text = font.render("x2", True, WHITE)
            rect = text.get_rect(center=(cx, cy))
            screen.blit(text, rect)

    def check_collision(self, position):
        """Check if snake head collides with this power-up"""
        head_x, head_y = position
        return (abs(head_x - self.x) < GRID_SIZE and
                abs(head_y - self.y) < GRID_SIZE)


class PowerUpManager:
    """Manages power-up spawning and active effects"""

    def __init__(self):
        self.powerups = []
        self.active_effects = []  # List of (type, end_time, original_value) tuples
        self.spawn_interval = 15000  # 15 seconds between spawns
        self.last_spawn_time = pygame.time.get_ticks()
        self.powerup_types = list(PowerUpType)

    def update(self):
        """Update all power-ups and effects"""
        current_time = pygame.time.get_ticks()

        # Check if should spawn new power-up
        if current_time - self.last_spawn_time > self.spawn_interval:
            self.spawn_random_powerup()
            self.last_spawn_time = current_time

        # Update existing power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            if not powerup.active:
                self.powerups.remove(powerup)

        # Check if effects have expired
        for effect_tuple in self.active_effects[:]:
            effect_type, end_time, _ = effect_tuple
            if current_time > end_time:
                self.active_effects.remove(effect_tuple)

    def spawn_random_powerup(self):
        """Spawn a random power-up at a random location"""
        # Random position (avoid edges)
        x = random.randint(2, (WINDOW_WIDTH // GRID_SIZE) - 3) * GRID_SIZE
        y = random.randint(2, (WINDOW_HEIGHT // GRID_SIZE) - 3) * GRID_SIZE

        # Random type
        powerup_type = random.choice(self.powerup_types)

        # Create and add power-up
        powerup = PowerUp(x, y, powerup_type)
        self.powerups.append(powerup)

    def check_collection(self, snake_head, game):
        """
        Check if snake collected any power-ups
        Returns: PowerUp object if collected, None otherwise
        """
        current_time = pygame.time.get_ticks()

        for powerup in self.powerups[:]:
            if powerup.check_collision(snake_head):
                # Apply effect
                self._apply_effect(powerup, game, current_time)
                # Remove power-up
                self.powerups.remove(powerup)
                return powerup

        return None

    def _apply_effect(self, powerup, game, current_time):
        """Apply power-up effect to the game"""
        end_time = current_time + powerup.duration

        if powerup.type == PowerUpType.SLOW_POTION:
            # Store original speed and reduce it
            original_speed = game.snake.speed
            game.snake.speed = max(5, game.snake.speed - 5)
            self.active_effects.append((powerup.type, end_time, original_speed))

        elif powerup.type == PowerUpType.SHIELD:
            # Activate shield
            game.shield_active = True
            self.active_effects.append((powerup.type, end_time, None))

        elif powerup.type == PowerUpType.DOUBLE_SCORE:
            # Double score multiplier
            game.score_multiplier = 2.0
            self.active_effects.append((powerup.type, end_time, None))

    def remove_effects(self, game):
        """Remove expired effects from game"""
        current_time = pygame.time.get_ticks()

        for effect_tuple in self.active_effects[:]:
            effect_type, end_time, original_value = effect_tuple

            if current_time > end_time:
                # Restore original values
                if effect_type == PowerUpType.SLOW_POTION:
                    if original_value is not None:
                        game.snake.speed = original_value
                elif effect_type == PowerUpType.SHIELD:
                    game.shield_active = False
                elif effect_type == PowerUpType.DOUBLE_SCORE:
                    game.score_multiplier = 1.0

                self.active_effects.remove(effect_tuple)

    def draw(self, screen):
        """Draw all power-ups"""
        for powerup in self.powerups:
            powerup.draw(screen)

    def draw_active_effects(self, screen):
        """Draw indicators for active effects"""
        current_time = pygame.time.get_ticks()
        y_offset = 120

        for effect_type, end_time, _ in self.active_effects:
            remaining = (end_time - current_time) / 1000
            if remaining > 0:
                # Get color based on type
                if effect_type == PowerUpType.SLOW_POTION:
                    color = (100, 149, 237)
                    text = "Slow"
                elif effect_type == PowerUpType.SHIELD:
                    color = (255, 215, 0)
                    text = "Shield"
                elif effect_type == PowerUpType.DOUBLE_SCORE:
                    color = (255, 20, 147)
                    text = "2x Score"

                # Draw icon
                pygame.draw.circle(screen, color, (30, y_offset), 12)

                # Draw time remaining
                font = pygame.font.Font(None, 20)
                time_text = font.render(f"{text}: {remaining:.1f}s", True, WHITE)
                screen.blit(time_text, (50, y_offset - 8))

                y_offset += 30

    def clear(self):
        """Clear all power-ups and effects"""
        self.powerups.clear()
        self.active_effects.clear()
