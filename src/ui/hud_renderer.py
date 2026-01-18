"""
HUD (Heads-Up Display) Renderer for Snake Game
Displays game information in organized panels
"""
import pygame
import math
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.config import *


class HUDRenderer:
    """Renders all HUD panels for game information display"""

    def __init__(self, theme_manager):
        """
        Initialize HUD renderer
        Args:
            theme_manager: ThemeManager instance for color access
        """
        self.theme_manager = theme_manager
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)

    def draw_all_panels(self, screen, game_state):
        """
        Draw all HUD panels
        Args:
            screen: Pygame screen surface
            game_state: Dictionary containing all game state info
        """
        self.draw_top_left_panel(screen, game_state)
        self.draw_top_right_panel(screen, game_state)
        self.draw_left_powerup_panel(screen, game_state)
        self.draw_bottom_right_bomb_panel(screen, game_state)

    def draw_top_left_panel(self, screen, game_state):
        """
        Draw score and speed panel (top-left)
        Args:
            screen: Pygame screen surface
            game_state: Dict with 'score', 'speed', 'max_speed'
        """
        theme = self.theme_manager.current_theme
        x, y = 20, 20

        # Draw semi-transparent background panel
        panel_width = 200
        panel_height = 90
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*theme.background_secondary, 180))
        pygame.draw.rect(panel_surface, theme.accent_color, (0, 0, panel_width, panel_height), 2)
        screen.blit(panel_surface, (x, y))

        # Score text
        score_text = self.font_large.render(f"Score: {game_state.get('score', 0)}", True, theme.text_primary)
        screen.blit(score_text, (x + 10, y + 10))

        # Speed text
        speed_text = self.font_medium.render(f"Speed: {game_state.get('speed', 0)} FPS", True, theme.text_primary)
        screen.blit(speed_text, (x + 10, y + 40))

        # Speed progress bar
        current_speed = game_state.get('speed', SNAKE_INITIAL_SPEED)
        max_speed = game_state.get('max_speed', MAX_SPEED)
        progress = min((current_speed - SNAKE_INITIAL_SPEED) / (max_speed - SNAKE_INITIAL_SPEED), 1.0)

        bar_width = 170
        bar_height = 8
        bar_x = x + 10
        bar_y = y + 68

        # Background bar
        pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        # Progress fill with gradient effect
        if progress > 0:
            fill_width = int(bar_width * progress)
            # Color shifts from green to yellow to red
            if progress < 0.5:
                color = (int(255 * progress * 2), 200, 50)
            else:
                color = (255, int(200 * (2 - progress * 2)), 50)
            pygame.draw.rect(screen, color, (bar_x, bar_y, fill_width, bar_height))
        # Border
        pygame.draw.rect(screen, theme.accent_color, (bar_x, bar_y, bar_width, bar_height), 1)

    def draw_top_right_panel(self, screen, game_state):
        """
        Draw difficulty and music panel (top-right)
        Args:
            screen: Pygame screen surface
            game_state: Dict with 'difficulty', 'music_style'
        """
        theme = self.theme_manager.current_theme
        panel_width = 180
        panel_height = 70
        x = WINDOW_WIDTH - panel_width - 20
        y = 20

        # Draw semi-transparent background panel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*theme.background_secondary, 180))
        pygame.draw.rect(panel_surface, theme.accent_color, (0, 0, panel_width, panel_height), 2)
        screen.blit(panel_surface, (x, y))

        # Difficulty with emoji
        difficulty = game_state.get('difficulty', 'Medium')
        difficulty_emoji = {"Easy": "🎯", "Medium": "⚙️", "Hard": "🔥"}.get(difficulty, "⚙️")
        difficulty_text = self.font_medium.render(f"{difficulty_emoji} {difficulty}", True, theme.text_primary)
        screen.blit(difficulty_text, (x + 10, y + 10))

        # Music style with emoji
        music_style = game_state.get('music_style', 'Chiptune')
        music_emoji = "🎵"
        music_text = self.font_small.render(f"{music_emoji} {music_style}", True, theme.text_secondary)
        screen.blit(music_text, (x + 10, y + 40))

    def draw_left_powerup_panel(self, screen, game_state):
        """
        Draw active power-ups panel (left side)
        Args:
            screen: Pygame screen surface
            game_state: Dict with 'active_powerups' list
                Each powerup: {'type': PowerUpType, 'end_time': int, 'color': tuple, 'name': str}
        """
        theme = self.theme_manager.current_theme
        x = 20
        y = 130
        current_time = pygame.time.get_ticks()

        active_powerups = game_state.get('active_powerups', [])

        if not active_powerups:
            return

        # Calculate panel height based on number of active power-ups
        panel_height = len(active_powerups) * 50 + 10
        panel_width = 180

        # Draw semi-transparent background panel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*theme.background_secondary, 180))
        pygame.draw.rect(panel_surface, theme.accent_color, (0, 0, panel_width, panel_height), 2)
        screen.blit(panel_surface, (x, y))

        # Draw each active power-up
        y_offset = y + 10
        for powerup in active_powerups:
            remaining_ms = powerup['end_time'] - current_time
            remaining_sec = max(0, remaining_ms / 1000)

            if remaining_sec <= 0:
                continue

            # Draw icon circle (32px)
            icon_size = 16
            icon_x = x + 15
            icon_y = y_offset + 12
            pygame.draw.circle(screen, powerup['color'], (icon_x, icon_y), icon_size)
            pygame.draw.circle(screen, WHITE, (icon_x, icon_y), icon_size, 2)

            # Draw power-up name
            name_text = self.font_small.render(powerup['name'], True, theme.text_primary)
            screen.blit(name_text, (x + 45, y_offset + 2))

            # Draw countdown bar
            bar_width = 120
            bar_height = 6
            bar_x = x + 45
            bar_y = y_offset + 22

            # Calculate progress
            duration = powerup.get('duration', 5000)  # Default 5 seconds
            progress = remaining_ms / duration

            # Background
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
            # Progress fill
            fill_width = int(bar_width * progress)
            # Color changes based on remaining time
            if progress > 0.5:
                bar_color = powerup['color']
            elif progress > 0.2:
                bar_color = (255, 200, 0)  # Yellow warning
            else:
                bar_color = (255, 100, 100)  # Red urgent
            pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))
            # Border
            pygame.draw.rect(screen, theme.accent_color, (bar_x, bar_y, bar_width, bar_height), 1)

            # Time remaining text
            time_text = self.font_small.render(f"{remaining_sec:.1f}s", True, theme.text_secondary)
            screen.blit(time_text, (bar_x + bar_width + 5, y_offset + 17))

            y_offset += 50

    def draw_bottom_right_bomb_panel(self, screen, game_state):
        """
        Draw bomb status panel (bottom-right)
        Args:
            screen: Pygame screen surface
            game_state: Dict with 'bomb_count', 'bomb_cooldown_remaining'
        """
        theme = self.theme_manager.current_theme
        panel_width = 160
        panel_height = 80
        x = WINDOW_WIDTH - panel_width - 20
        y = WINDOW_HEIGHT - panel_height - 20

        bomb_count = game_state.get('bomb_count', 0)

        # Only show if bombs are available or on cooldown
        if bomb_count == 0 and game_state.get('bomb_cooldown_remaining', 0) == 0:
            return

        # Draw semi-transparent background panel
        panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        panel_surface.fill((*theme.background_secondary, 180))
        pygame.draw.rect(panel_surface, theme.accent_color, (0, 0, panel_width, panel_height), 2)
        screen.blit(panel_surface, (x, y))

        # Bomb emoji and count
        bomb_text = self.font_large.render(f"💣 x {bomb_count}", True, theme.text_primary)
        screen.blit(bomb_text, (x + 15, y + 10))

        # Cooldown display
        cooldown_remaining = game_state.get('bomb_cooldown_remaining', 0)
        if cooldown_remaining > 0:
            cooldown_sec = cooldown_remaining / 1000
            cooldown_text = self.font_small.render(f"Cooldown: {cooldown_sec:.1f}s", True, (255, 150, 0))
            screen.blit(cooldown_text, (x + 15, y + 45))

            # Cooldown progress bar
            bar_width = 130
            bar_height = 6
            bar_x = x + 15
            bar_y = y + 65

            total_cooldown = game_state.get('bomb_cooldown_total', 1000)
            progress = 1 - (cooldown_remaining / total_cooldown)

            # Background
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
            # Progress fill
            fill_width = int(bar_width * progress)
            pygame.draw.rect(screen, (0, 200, 255), (bar_x, bar_y, fill_width, bar_height))
            # Border
            pygame.draw.rect(screen, theme.accent_color, (bar_x, bar_y, bar_width, bar_height), 1)
        else:
            ready_text = self.font_small.render("Ready! Press 'B'", True, (100, 255, 100))
            screen.blit(ready_text, (x + 15, y + 50))

    def draw_combo_indicator(self, screen, combo_count):
        """
        Draw combo counter when player has eating streak
        Args:
            screen: Pygame screen surface
            combo_count: Current combo count
        """
        if combo_count < 2:
            return

        theme = self.theme_manager.current_theme

        # Position at top-center
        combo_text = self.font_large.render(f"🔥 {combo_count}x COMBO!", True, (255, 215, 0))
        rect = combo_text.get_rect(center=(WINDOW_WIDTH // 2, 30))

        # Pulsing effect
        pulse = 1 + 0.1 * math.sin(pygame.time.get_ticks() * 0.01)
        scaled_width = int(combo_text.get_width() * pulse)
        scaled_height = int(combo_text.get_height() * pulse)

        if scaled_width > 0 and scaled_height > 0:
            scaled_text = pygame.transform.scale(combo_text, (scaled_width, scaled_height))
            scaled_rect = scaled_text.get_rect(center=(WINDOW_WIDTH // 2, 30))

            # Glow effect
            glow_surface = pygame.Surface((scaled_width + 20, scaled_height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow_surface, (255, 215, 0, 50), (0, 0, scaled_width + 20, scaled_height + 20), border_radius=10)
            screen.blit(glow_surface, (scaled_rect.x - 10, scaled_rect.y - 10))

            screen.blit(scaled_text, scaled_rect)
