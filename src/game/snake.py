"""
Enhanced Snake Class Definition
Responsible for snake movement, growth and collision detection with visual effects
"""

import pygame
import os
import sys
import math

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.config import *


class SnakeExpression:
    """Snake facial expressions"""
    NORMAL = "normal"
    HAPPY = "happy"      # Just ate food
    EXCITED = "excited"  # Combo eating
    WORRIED = "worried"  # Near danger


class Snake:
    """Enhanced Snake class with visual effects and expressions"""

    def __init__(self, start_x, start_y):
        """
        Initialize snake
        Args:
            start_x: starting x coordinate
            start_y: starting y coordinate
        """
        self.positions = [(start_x, start_y)]  # Snake body segment positions
        self.direction = (1, 0)  # Initial direction: right
        self.grow_flag = False  # Growth flag
        self.speed = SNAKE_INITIAL_SPEED
        self.expression = SnakeExpression.NORMAL
        self.expression_timer = 0
        self.combo_count = 0
        
    def move(self):
        """Move snake"""
        # Calculate new head position
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (head_x + dx * GRID_SIZE, head_y + dy * GRID_SIZE)
        
        # Add new head
        self.positions.insert(0, new_head)
        
        # Remove tail if no growth flag
        if not self.grow_flag:
            self.positions.pop()
        else:
            self.grow_flag = False
            
    def change_direction(self, direction):
        """
        Change snake direction
        Args:
            direction: new direction in format (dx, dy)
        """
        # Prevent snake from turning back directly
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
            
    def grow(self):
        """Set growth flag"""
        self.grow_flag = True
        # Increase speed
        self.speed = min(self.speed + SPEED_INCREMENT, MAX_SPEED)
        # Update combo count
        self.combo_count += 1
        # Set expression based on combo
        if self.combo_count >= 3:
            self.set_expression(SnakeExpression.EXCITED, 40)
        else:
            self.set_expression(SnakeExpression.HAPPY, 30)

    def set_expression(self, expression, duration=30):
        """Set snake expression for a duration"""
        self.expression = expression
        self.expression_timer = duration

    def update_expression(self):
        """Update expression timer"""
        if self.expression_timer > 0:
            self.expression_timer -= 1
        else:
            self.expression = SnakeExpression.NORMAL

    def reset_combo(self):
        """Reset eating combo"""
        self.combo_count = 0

    def check_self_collision(self):
        """Check if snake hits its own body"""
        head = self.positions[0]
        return head in self.positions[1:]

    def check_wall_collision(self, wrap_around=False):
        """
        Check if snake hits the wall
        Args:
            wrap_around: If True, wrap through walls (Easy mode)
        """
        head_x, head_y = self.positions[0]

        if wrap_around:
            # Wrap around mode - teleport to opposite side
            new_x = head_x % WINDOW_WIDTH
            new_y = head_y % WINDOW_HEIGHT
            if (new_x, new_y) != self.positions[0]:
                self.positions[0] = (new_x, new_y)
            return False
        else:
            # Normal collision detection
            return (head_x < 0 or head_x >= WINDOW_WIDTH or
                    head_y < 0 or head_y >= WINDOW_HEIGHT)
        
    def draw(self, screen):
        """Draw enhanced snake with gradient effects and expressions"""
        for i, position in enumerate(self.positions):
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)

            # Head is brighter, body is darker
            if i == 0:  # Head
                # Draw glowing effect
                glow_rect = pygame.Rect(position[0]-2, position[1]-2, GRID_SIZE+4, GRID_SIZE+4)
                pygame.draw.rect(screen, SNAKE_HEAD_COLOR, glow_rect, 2)
                pygame.draw.rect(screen, SNAKE_HEAD_COLOR, rect)
            else:  # Body
                # Gradient effect - darker towards the tail
                color_intensity = max(50, 200 - (i * 10))
                body_color = (0, color_intensity, color_intensity // 2)
                pygame.draw.rect(screen, body_color, rect)

            # Draw border
            pygame.draw.rect(screen, WHITE, rect, 1)

            # Add eyes to the head with expressions
            if i == 0:
                self._draw_eyes(screen, position)

    def _draw_eyes(self, screen, position):
        """Draw eyes based on current expression"""
        x, y = position
        eye_offset = 5

        if self.expression == SnakeExpression.HAPPY:
            # Happy eyes - curved arcs (^_^)
            pygame.draw.arc(screen, WHITE,
                          (x + 5, y + 5, 6, 6), 0, math.pi, 2)
            pygame.draw.arc(screen, WHITE,
                          (x + GRID_SIZE - 11, y + 5, 6, 6), 0, math.pi, 2)
        elif self.expression == SnakeExpression.EXCITED:
            # Star eyes
            self._draw_star(screen, x + 8, y + 8, 3, GOLD)
            self._draw_star(screen, x + GRID_SIZE - 8, y + 8, 3, GOLD)
        elif self.expression == SnakeExpression.WORRIED:
            # Wide eyes (worried)
            eye_size = 4
            left_eye = pygame.Rect(x + eye_offset - 1, y + eye_offset, eye_size, eye_size)
            pygame.draw.rect(screen, WHITE, left_eye)
            right_eye = pygame.Rect(x + GRID_SIZE - eye_offset - eye_size + 1, y + eye_offset, eye_size, eye_size)
            pygame.draw.rect(screen, WHITE, right_eye)
        else:
            # Normal eyes
            eye_size = 3
            left_eye = pygame.Rect(x + eye_offset, y + eye_offset, eye_size, eye_size)
            pygame.draw.rect(screen, WHITE, left_eye)
            right_eye = pygame.Rect(x + GRID_SIZE - eye_offset - eye_size, y + eye_offset, eye_size, eye_size)
            pygame.draw.rect(screen, WHITE, right_eye)

    def _draw_star(self, screen, cx, cy, radius, color):
        """Draw a star shape for excited eyes"""
        points = []
        for i in range(10):
            angle = i * math.pi / 5 - math.pi / 2
            r = radius if i % 2 == 0 else radius / 2
            px = cx + r * math.cos(angle)
            py = cy + r * math.sin(angle)
            points.append((px, py))
        if len(points) >= 3:
            pygame.draw.polygon(screen, color, points)