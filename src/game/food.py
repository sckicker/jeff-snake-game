"""
Enhanced Food Class Definition
Responsible for food generation and display with visual effects
"""

import pygame
import random
import math
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.config import *

class Food:
    """Enhanced Food class with pulsing and glowing effects"""
    
    def __init__(self):
        """Initialize food"""
        self.position = self.generate_position()
        self.pulse_timer = 0
        self.rotation_angle = 0
        
    def generate_position(self):
        """
        Generate random position
        Returns:
            tuple: (x, y) coordinates
        """
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return (x, y)
        
    def respawn(self, snake_positions):
        """
        Respawn food, ensuring it's not on the snake
        Args:
            snake_positions: list of snake body segment positions
        """
        while True:
            self.position = self.generate_position()
            if self.position not in snake_positions:
                break
                
    def update(self):
        """Update food animation"""
        self.pulse_timer += 1
        self.rotation_angle += 2
        
    def draw(self, screen):
        """Draw enhanced food with pulsing and glowing effects"""
        # Update animation
        self.update()
        
        x, y = self.position[0], self.position[1]
        center_x, center_y = x + FOOD_SIZE // 2, y + FOOD_SIZE // 2
        
        # Pulsing effect
        pulse_scale = 1 + 0.2 * math.sin(self.pulse_timer * 0.1 * FOOD_PULSE_SPEED)
        current_size = int(FOOD_SIZE * pulse_scale)
        
        # Draw outer glow
        glow_size = current_size + 10
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        for i in range(5):
            alpha = 50 - i * 10
            size = glow_size - i * 4
            pygame.draw.circle(glow_surface, (*FOOD_GLOW_COLOR, alpha), 
                             (glow_size // 2, glow_size // 2), size // 2, 2)
        screen.blit(glow_surface, (center_x - glow_size // 2, center_y - glow_size // 2))
        
        # Draw main food (rotating diamond)
        food_surface = pygame.Surface((current_size, current_size), pygame.SRCALPHA)
        points = [
            (current_size // 2, 0),
            (current_size, current_size // 2),
            (current_size // 2, current_size),
            (0, current_size // 2)
        ]
        
        # Rotate points
        rotated_points = []
        for px, py in points:
            # Translate to origin, rotate, translate back
            px -= current_size // 2
            py -= current_size // 2
            angle_rad = math.radians(self.rotation_angle)
            new_x = px * math.cos(angle_rad) - py * math.sin(angle_rad)
            new_y = px * math.sin(angle_rad) + py * math.cos(angle_rad)
            rotated_points.append((new_x + current_size // 2, new_y + current_size // 2))
        
        pygame.draw.polygon(food_surface, FOOD_COLOR, rotated_points)
        pygame.draw.polygon(food_surface, WHITE, rotated_points, 2)
        
        # Draw food on main screen
        screen.blit(food_surface, (center_x - current_size // 2, center_y - current_size // 2))
        
        # Add sparkle effect
        if self.pulse_timer % 30 < 15:
            sparkle_x = center_x + 8 * math.cos(self.pulse_timer * 0.2)
            sparkle_y = center_y + 8 * math.sin(self.pulse_timer * 0.2)
            pygame.draw.circle(screen, WHITE, (int(sparkle_x), int(sparkle_y)), 2)

        # Draw label below food (like power-ups)
        font = pygame.font.Font(None, 20)
        label_text = font.render("🍎 FOOD +10", True, (255, 255, 255))

        # Semi-transparent background for label
        label_rect = label_text.get_rect(center=(center_x, center_y + GRID_SIZE // 2 + 15))
        bg_surface = pygame.Surface((label_rect.width + 8, label_rect.height + 4), pygame.SRCALPHA)
        bg_surface.fill((255, 100, 100, 220))  # Red background
        screen.blit(bg_surface, (label_rect.x - 4, label_rect.y - 2))

        # Draw text
        screen.blit(label_text, label_rect)