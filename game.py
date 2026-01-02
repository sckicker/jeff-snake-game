"""
Enhanced Game Main Class with Sound Effects
Responsible for game logic, state management, enhanced user interface and sound effects
"""

import pygame
import sys
import math
from snake import Snake
from food import Food
from sound_manager import SoundManager
from config import *

class SnakeGame:
    """Enhanced Snake Game Main Class with visual effects and sound effects"""
    
    def __init__(self):
        """Initialize enhanced game with sound effects"""
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Create background surface
        self.background_surface = self.create_enhanced_background()
        
        self.reset_game()
        
    def create_enhanced_background(self):
        """Create enhanced background with grid and gradient effects"""
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Create gradient background
        for y in range(WINDOW_HEIGHT):
            # Dark blue to black gradient
            color_value = int(25 - (y / WINDOW_HEIGHT) * 15)
            color = (color_value, color_value, color_value + 5)
            pygame.draw.line(background, color, (0, y), (WINDOW_WIDTH, y))
        
        # Add subtle grid pattern
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(grid_surface, (*DARK_GRAY, GRID_ALPHA), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(grid_surface, (*DARK_GRAY, GRID_ALPHA), (0, y), (WINDOW_WIDTH, y))
        
        background.blit(grid_surface, (0, 0))
        return background
        
    def reset_game(self):
        """Reset game state"""
        self.snake = Snake(100, 100)
        self.food = Food()
        self.score = 0
        self.game_state = GAME_RUNNING
        self.food.respawn(self.snake.positions)
        
    def handle_events(self):
        """Handle game events with sound effects"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == GAME_RUNNING:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_p:
                        self.game_state = GAME_PAUSED
                        self.sound_manager.play_pause_sound()
                        
                elif self.game_state == GAME_PAUSED:
                    if event.key == pygame.K_p:
                        self.game_state = GAME_RUNNING
                        self.sound_manager.play_pause_sound()
                        
                elif self.game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        return False
                        
        return True
        
    def update(self):
        """Update game state with sound effects"""
        if self.game_state == GAME_RUNNING:
            self.snake.move()
            
            # Check collisions
            if self.snake.check_self_collision() or self.snake.check_wall_collision():
                self.game_state = GAME_OVER
                self.sound_manager.play_crash_sound()
                self.sound_manager.play_game_over_sound()
                
            # Check if food is eaten
            if self.snake.positions[0] == self.food.position:
                self.snake.grow()
                self.score += SCORE_PER_FOOD
                self.food.respawn(self.snake.positions)
                self.sound_manager.play_eat_sound()
                
                # Play speed up sound if speed increased
                if self.snake.speed > SNAKE_INITIAL_SPEED:
                    self.sound_manager.play_speed_up_sound()
                
    def draw(self):
        """Draw enhanced game interface"""
        # Draw enhanced background
        self.screen.blit(self.background_surface, (0, 0))
        
        # Draw game area border with glow effect
        self.draw_glowing_border()
        
        if self.game_state == GAME_RUNNING:
            self.snake.draw(self.screen)
            self.food.draw(self.screen)
            self.draw_enhanced_score()
            
        elif self.game_state == GAME_PAUSED:
            self.draw_enhanced_paused_screen()
            
        elif self.game_state == GAME_OVER:
            self.draw_enhanced_game_over_screen()
            
        pygame.display.flip()
        
    def draw_glowing_border(self):
        """Draw glowing border around game area"""
        # Outer glow
        for i in range(3):
            alpha = 100 - i * 30
            color = (*CYAN, alpha)
            pygame.draw.rect(self.screen, color, 
                           (i, i, WINDOW_WIDTH - 2*i, WINDOW_HEIGHT - 2*i), 1)
        
        # Main border
        pygame.draw.rect(self.screen, CYAN, (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 2)
        
    def draw_enhanced_score(self):
        """Draw enhanced score and speed with background panels"""
        # Score panel
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        speed_text = self.font.render(f"Speed: {self.snake.speed}", True, WHITE)
        
        # Draw semi-transparent background for text
        score_bg = pygame.Surface((150, 80), pygame.SRCALPHA)
        score_bg.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(score_bg, (10, 10))
        
        self.screen.blit(score_text, (20, 20))
        self.screen.blit(speed_text, (20, 60))
        
        # Draw speed bar
        speed_percentage = self.snake.speed / MAX_SPEED
        bar_width = 100
        bar_height = 8
        bar_x = 20
        bar_y = 90
        
        # Speed bar background
        pygame.draw.rect(self.screen, DARK_GRAY, (bar_x, bar_y, bar_width, bar_height))
        # Speed bar fill
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, int(bar_width * speed_percentage), bar_height))
        # Speed bar border
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
    def draw_enhanced_paused_screen(self):
        """Draw enhanced paused screen with overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Paused text with glow effect
        paused_text = self.big_font.render("PAUSED", True, CYAN)
        continue_text = self.font.render("Press P to continue", True, WHITE)
        
        paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30))
        continue_rect = continue_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 30))
        
        # Glow effect for paused text
        for i in range(3):
            glow_surface = self.big_font.render("PAUSED", True, (*CYAN, 100 - i*30))
            glow_rect = glow_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 30))
            self.screen.blit(glow_surface, glow_rect)
        
        self.screen.blit(paused_text, paused_rect)
        self.screen.blit(continue_text, continue_rect)
        
    def draw_enhanced_game_over_screen(self):
        """Draw enhanced game over screen with effects"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Game over text with red glow
        game_over_text = self.big_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Final Score: {self.score}", True, GOLD)
        restart_text = self.font.render("Press R to restart", True, WHITE)
        quit_text = self.font.render("Press Q to quit", True, WHITE)
        
        game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 10))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 40))
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 80))
        
        # Glow effect for game over text
        for i in range(3):
            glow_surface = self.big_font.render("GAME OVER", True, (*RED, 100 - i*30))
            glow_rect = glow_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 - 60))
            self.screen.blit(glow_surface, glow_rect)
        
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(score_text, score_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)
        
    def run(self):
        """Main game loop with sound cleanup"""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.snake.speed)
        
        # Cleanup sound resources
        self.sound_manager.cleanup()
        pygame.quit()
        sys.exit()