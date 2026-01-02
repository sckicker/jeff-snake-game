"""
Enhanced Snake Class Definition
Responsible for snake movement, growth and collision detection with visual effects
"""

import pygame
from config import *

class Snake:
    """Enhanced Snake class with visual effects"""
    
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
        
    def check_self_collision(self):
        """Check if snake hits its own body"""
        head = self.positions[0]
        return head in self.positions[1:]
        
    def check_wall_collision(self):
        """Check if snake hits the wall"""
        head_x, head_y = self.positions[0]
        return (head_x < 0 or head_x >= WINDOW_WIDTH or 
                head_y < 0 or head_y >= WINDOW_HEIGHT)
        
    def draw(self, screen):
        """Draw enhanced snake with gradient effects"""
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
            
            # Add eyes to the head
            if i == 0:
                eye_size = 3
                eye_offset = 5
                # Left eye
                left_eye = pygame.Rect(position[0] + eye_offset, position[1] + eye_offset, eye_size, eye_size)
                pygame.draw.rect(screen, WHITE, left_eye)
                # Right eye
                right_eye = pygame.Rect(position[0] + GRID_SIZE - eye_offset - eye_size, position[1] + eye_offset, eye_size, eye_size)
                pygame.draw.rect(screen, WHITE, right_eye)