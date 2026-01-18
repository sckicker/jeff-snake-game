"""
Enhanced Game Main Class with Sound Effects
Responsible for game logic, state management, enhanced user interface and sound effects
"""

import pygame
import sys
import math
import os
import random

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from .snake import Snake
from .food import Food
from .sound_manager import SoundManager
from .bomb import Bomb
from .powerups import PowerUpManager
from src.config.config import *
from src.config.window_config import window_manager, create_game_window, toggle_fullscreen_mode, get_window_size
from src.config.themes import ThemeManager
from src.core.difficulty import DifficultyManager, DifficultyLevel
from src.effects.floating_text import FloatingTextManager
from src.effects.particle_system import ParticleSystem
from src.ui.hud_renderer import HUDRenderer

class SnakeGame:
    """Enhanced Snake Game Main Class with visual effects and sound effects"""
    
    def __init__(self):
        """Initialize enhanced game with sound effects and advanced window management"""
        pygame.init()
        
        # Use window manager for flexible display options
        self.screen = create_game_window()
        if not self.screen:
            print("❌ 创建窗口失败，使用默认设置")
            self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            
        self.clock = pygame.time.Clock()
        
        # Get actual screen size and adjust fonts accordingly
        screen_width, screen_height = get_window_size()
        
        # Adjust font sizes based on actual screen size
        self.font = pygame.font.Font(None, max(24, screen_height // 25))
        self.big_font = pygame.font.Font(None, max(36, screen_height // 15))
        self.score_font = pygame.font.Font(None, max(20, screen_height // 30))
        
        # Initialize sound manager
        self.sound_manager = SoundManager()

        # Initialize theme manager
        self.theme_manager = ThemeManager()

        # Initialize difficulty manager
        self.difficulty_manager = DifficultyManager()

        # Initialize power-up manager
        self.powerup_manager = PowerUpManager()

        # Initialize floating text manager
        self.floating_text_manager = FloatingTextManager()

        # Initialize HUD renderer
        self.hud_renderer = HUDRenderer(self.theme_manager)

        # Initialize particle system for trail effects
        self.particle_system = ParticleSystem()

        # Start menu music when game initializes
        self.sound_manager.start_menu_music()

        # Create background surface
        self.background_surface = self.create_enhanced_background()

        # Initialize game state
        self.game_state = GAME_MENU  # Start with menu state
        self.snake = None
        self.food = None
        self.score = 0
        self.score_multiplier = 1.0  # For double score power-up
        self.shield_active = False    # For shield power-up
        self.walls = []
        self.bombs = []
        self.particles = []
        self.explosions = []
        self.bombs_available = 3
        self.bomb_cooldown = 0
        self.max_bombs = 3
        self.explosion_active = False

        # Screen shake effects
        self.screen_shake_intensity = 0
        self.screen_shake_duration = 0
        self.screen_offset_x = 0
        self.screen_offset_y = 0
        
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode using window manager"""
        new_screen = toggle_fullscreen_mode()
        if new_screen:
            self.screen = new_screen
            # Recreate background for new screen size
            self.background_surface = self.create_enhanced_background()
            
            # Update font sizes for new resolution
            screen_width, screen_height = get_window_size()
            self.font = pygame.font.Font(None, max(24, screen_height // 25))
            self.big_font = pygame.font.Font(None, max(36, screen_height // 15))
            self.score_font = pygame.font.Font(None, max(20, screen_height // 30))
            
            print(f"🖥️  切换显示模式: {window_manager.current_mode}")
        else:
            print("❌ 切换显示模式失败，保持当前模式")
        
    def create_enhanced_background(self):
        """Create enhanced background with grid and gradient effects using current theme"""
        background = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        theme = self.theme_manager.current_theme

        # Create gradient background using theme colors
        for y in range(WINDOW_HEIGHT):
            # Gradient from primary to secondary
            progress = y / WINDOW_HEIGHT
            r = int(theme.background_primary[0] * (1 - progress) + theme.background_secondary[0] * progress)
            g = int(theme.background_primary[1] * (1 - progress) + theme.background_secondary[1] * progress)
            b = int(theme.background_primary[2] * (1 - progress) + theme.background_secondary[2] * progress)
            color = (r, g, b)
            pygame.draw.line(background, color, (0, y), (WINDOW_WIDTH, y))

        # Add subtle grid pattern using theme grid color
        grid_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            pygame.draw.line(grid_surface, (*theme.grid_color, theme.grid_alpha), (x, 0), (x, WINDOW_HEIGHT))
        for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
            pygame.draw.line(grid_surface, (*theme.grid_color, theme.grid_alpha), (0, y), (WINDOW_WIDTH, y))

        background.blit(grid_surface, (0, 0))
        return background
        
    def start_game(self):
        """Start the game from menu"""
        self.reset_game()
        self.game_state = GAME_RUNNING  # Set game state to running
        self.sound_manager.start_background_music()  # Start game music
        
    def reset_game(self):
        """Reset game to initial state"""
        # Get difficulty settings
        difficulty = self.difficulty_manager.get_settings()

        # Create snake with difficulty-based speed
        self.snake = Snake(100, 100)
        self.snake.speed = difficulty.initial_speed

        self.food = Food()
        self.score = 0
        self.score_multiplier = 1.0
        self.shield_active = False
        self.game_state = GAME_MENU
        self.paused = False

        # Reset explosion effect
        self.explosion_active = False
        self.explosion_particles = []
        self.explosion_timer = 0
        self.explosion_duration = 60  # 1 second at 60 FPS

        # Reset bomb system based on difficulty
        self.bombs = []
        self.bomb_cooldown = 0
        self.bombs_available = self.max_bombs if difficulty.bomb_enabled else 0

        # Clear power-ups and floating text
        self.powerup_manager.clear()
        self.floating_text_manager.clear()

        # Clear particle system
        self.particle_system.clear()
        
    def handle_events(self):
        """Handle game events with sound effects"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if self.game_state == GAME_MENU:
                    if event.key == pygame.K_SPACE:
                        self.start_game()
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_m:
                        self.sound_manager.toggle_background_music()
                    elif event.key == pygame.K_n:
                        self.sound_manager.switch_music_style()
                    elif event.key == pygame.K_t:
                        # Toggle theme
                        theme_name = self.theme_manager.cycle_theme()
                        self.background_surface = self.create_enhanced_background()
                        self.sound_manager.play_theme_switch_sound()  # Play theme switch sound
                        print(f"🎨 主题切换到: {theme_name}")
                    elif event.key == pygame.K_d:
                        # Cycle difficulty
                        difficulty_name = self.difficulty_manager.cycle_difficulty()
                        print(f"⚙️ 难度设置: {difficulty_name}")
                    elif event.key == pygame.K_q:
                        return False
                        
                elif self.game_state == GAME_RUNNING:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
                    elif event.key == pygame.K_b:
                        self.place_bomb()
                    elif event.key == pygame.K_p:
                        self.game_state = GAME_PAUSED
                        self.sound_manager.play_pause_sound()
                    elif event.key == pygame.K_q:
                        # Return to menu when Q is pressed during game
                        self.game_state = GAME_MENU
                        self.sound_manager.stop_background_music()
                        self.sound_manager.start_menu_music()
                        print("🏠 返回主菜单")
                    elif event.key == pygame.K_f:
                        self.toggle_fullscreen()
                    elif event.key == pygame.K_m:
                        self.sound_manager.toggle_background_music()
                    elif event.key == pygame.K_n:
                        self.sound_manager.switch_music_style()
                    elif event.key == pygame.K_t:
                        # Toggle theme during game
                        theme_name = self.theme_manager.cycle_theme()
                        self.background_surface = self.create_enhanced_background()
                        self.sound_manager.play_theme_switch_sound()  # Play theme switch sound
                        print(f"🎨 主题切换到: {theme_name}")
                        
                elif self.game_state == GAME_PAUSED:
                    if event.key == pygame.K_p:
                        self.game_state = GAME_RUNNING
                        self.sound_manager.play_pause_sound()
                        
                elif self.game_state == GAME_OVER:
                    if event.key == pygame.K_r:
                        self.sound_manager.stop_game_over_music()  # Stop game over music
                        self.reset_game()
                    elif event.key == pygame.K_q:
                        return False
                        
        return True
        
    def update(self):
        """Update game state with sound effects"""
        if self.game_state == GAME_RUNNING:
            self.snake.move()

            # Emit trail particles from snake tail
            if len(self.snake.positions) > 0:
                # Get snake color from theme
                snake_color = self.theme_manager.current_theme.snake_body_color
                # Emit from tail position
                tail_x, tail_y = self.snake.positions[-1]
                self.particle_system.emit_trail_particle(
                    tail_x + GRID_SIZE // 2,
                    tail_y + GRID_SIZE // 2,
                    snake_color,
                    intensity=0.5
                )

            # Update particle system
            self.particle_system.update()

            # Update snake expression timer
            self.snake.update_expression()

            # Get difficulty settings
            difficulty = self.difficulty_manager.get_settings()

            # Check collisions with wall wrapping support
            wall_collision = self.snake.check_wall_collision(difficulty.wall_wrap_around)
            self_collision = self.snake.check_self_collision()

            if self_collision or wall_collision:
                # Check if shield is active
                if self.shield_active:
                    # Shield protects once
                    self.shield_active = False
                    self.sound_manager.play_shield_break_sound()  # Play shield break sound
                    self.floating_text_manager.add_message(
                        "Shield Saved You!",
                        WINDOW_WIDTH // 2,
                        WINDOW_HEIGHT // 2,
                        color=(255, 215, 0)
                    )
                else:
                    # Trigger explosion effect at snake head position
                    self.trigger_explosion(self.snake.positions[0])
                    self.trigger_screen_shake(intensity=15, duration=20)  # Strong shake on death
                    self.game_state = GAME_OVER
                    self.sound_manager.play_crash_sound()
                    self.sound_manager.play_game_over_sound()
                    self.sound_manager.stop_background_music()  # Stop game music
                    self.sound_manager.start_game_over_music()  # Start game over music
                
            # Update explosion animation if active
            if self.explosion_active:
                self.update_explosion()

            # Update screen shake effect
            self.update_screen_shake()

            # Update bombs
            self.update_bombs()

            # Update power-ups
            self.powerup_manager.update()

            # Check for power-up collection
            collected_powerup = self.powerup_manager.check_collection(
                self.snake.positions[0], self
            )
            if collected_powerup:
                # Play power-up collection sound
                from .powerups import PowerUpType
                powerup_type_map = {
                    PowerUpType.SLOW_POTION: 'slow_potion',
                    PowerUpType.SHIELD: 'shield',
                    PowerUpType.DOUBLE_SCORE: 'double_score'
                }
                self.sound_manager.play_powerup_sound(powerup_type_map.get(collected_powerup.type, 'slow_potion'))

                # Show floating text for power-up
                self.floating_text_manager.add_message(
                    f"{collected_powerup.name}!",
                    collected_powerup.x + GRID_SIZE // 2,
                    collected_powerup.y + GRID_SIZE // 2,
                    color=collected_powerup.color
                )

            # Remove expired power-up effects
            self.powerup_manager.remove_effects(self)

            # Update floating text
            self.floating_text_manager.update()

            # Check if food is eaten
            if self.snake.positions[0] == self.food.position:
                self.snake.grow()

                # Play combo sound based on combo count
                if self.snake.combo_count == 2:
                    self.sound_manager.play_combo_sound(2)
                elif self.snake.combo_count == 3:
                    self.sound_manager.play_combo_sound(3)
                elif self.snake.combo_count >= 5:
                    self.sound_manager.play_combo_sound(5)

                # Apply score multiplier
                points = int(SCORE_PER_FOOD * self.score_multiplier * difficulty.score_multiplier)
                self.score += points

                # Show floating score text
                food_x, food_y = self.food.position
                self.floating_text_manager.add_score_text(
                    points,
                    food_x + GRID_SIZE // 2,
                    food_y + GRID_SIZE // 2
                )

                self.food.respawn(self.snake.positions)
                self.sound_manager.play_eat_sound()

                # Play speed up sound if speed increased
                if self.snake.speed > SNAKE_INITIAL_SPEED:
                    self.sound_manager.play_speed_up_sound()

                # Update last eat time for combo tracking
                self._last_eat_time = pygame.time.get_ticks()
            else:
                # Reset combo if not eating consecutively
                # (reset after not eating for 2 seconds)
                if not hasattr(self, '_last_eat_time'):
                    self._last_eat_time = pygame.time.get_ticks()
                if pygame.time.get_ticks() - self._last_eat_time > 2000:
                    self.snake.reset_combo()
                    self._last_eat_time = pygame.time.get_ticks()
                
    def draw(self):
        """Draw enhanced game interface"""
        # Check if screen is valid
        if self.screen is None:
            return
            
        # Draw enhanced background with screen shake offset
        self.screen.blit(self.background_surface, (self.screen_offset_x, self.screen_offset_y))

        # Draw game area border with glow effect (also affected by shake)
        self.draw_glowing_border()
        
        if self.game_state == GAME_RUNNING:
            # Draw in order: particles -> bombs -> power-ups -> snake -> food (food on top)
            self.particle_system.draw(self.screen)  # Draw particles first (background layer)
            self.draw_bombs()
            self.powerup_manager.draw(self.screen)
            self.snake.draw(self.screen)
            self.food.draw(self.screen)  # Food drawn last so it's never hidden
            self.draw_enhanced_score()
            self.powerup_manager.draw_active_effects(self.screen)
            self.floating_text_manager.draw(self.screen)
            
        elif self.game_state == GAME_PAUSED:
            self.draw_enhanced_paused_screen()
            
        elif self.game_state == GAME_OVER:
            self.draw_enhanced_game_over_screen()
            
        elif self.game_state == GAME_MENU:
            self.draw_menu_screen()
            
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
        """Draw enhanced HUD with all game information"""
        # Prepare game state data for HUD
        difficulty_settings = self.difficulty_manager.get_settings()
        current_time = pygame.time.get_ticks()

        # Prepare active power-ups data
        active_powerups = []
        for effect_type, end_time, original_value in self.powerup_manager.active_effects:
            # Get power-up details
            from .powerups import PowerUpType
            if effect_type == PowerUpType.SLOW_POTION:
                color = (100, 149, 237)
                name = "Slow Potion"
                duration = 5000
            elif effect_type == PowerUpType.SHIELD:
                color = (255, 215, 0)
                name = "Shield"
                duration = 3000
            elif effect_type == PowerUpType.DOUBLE_SCORE:
                color = (255, 20, 147)
                name = "2x Score"
                duration = 8000

            active_powerups.append({
                'type': effect_type,
                'end_time': end_time,
                'color': color,
                'name': name,
                'duration': duration
            })

        game_state = {
            'score': self.score,
            'speed': self.snake.speed,
            'max_speed': difficulty_settings.max_speed,
            'difficulty': self.difficulty_manager.get_difficulty_name(),
            'music_style': self.sound_manager.current_music_style.replace('_', ' ').title(),
            'active_powerups': active_powerups,
            'bomb_count': self.bombs_available,
            'bomb_cooldown_remaining': self.bomb_cooldown,
            'bomb_cooldown_total': 3000,  # 3 seconds
        }

        # Draw all HUD panels
        self.hud_renderer.draw_all_panels(self.screen, game_state)

        # Draw combo indicator if applicable
        if hasattr(self.snake, 'combo_count'):
            self.hud_renderer.draw_combo_indicator(self.screen, self.snake.combo_count)
        
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
        
    def trigger_explosion(self, position):
        """Trigger explosion effect at specified position"""
        self.explosion_active = True
        self.explosion_timer = 0
        self.explosion_duration = 60  # 1 second at 60 FPS
        self.explosion_position = position
        self.explosion_particles = []
        
        # Create explosion particles
        for _ in range(50):  # Create 50 particles
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            size = random.randint(2, 6)
            lifetime = random.randint(20, 40)
            
            particle = {
                'x': position[0],
                'y': position[1],
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': size,
                'color': (random.randint(200, 255), random.randint(50, 150), random.randint(0, 50)),
                'lifetime': lifetime,
                'max_lifetime': lifetime
            }
            self.explosion_particles.append(particle)
    
    def update_explosion(self):
        """Update explosion animation"""
        self.explosion_timer += 1
        
        # Update particles
        for particle in self.explosion_particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= 1
            
            # Remove dead particles
            if particle['lifetime'] <= 0:
                self.explosion_particles.remove(particle)
        
        # End explosion if timer exceeds duration or no particles left
        if self.explosion_timer >= self.explosion_duration or not self.explosion_particles:
            self.explosion_active = False

    def trigger_screen_shake(self, intensity=10, duration=15):
        """
        Trigger screen shake effect
        Args:
            intensity: Maximum pixel offset for shake
            duration: Number of frames to shake
        """
        self.screen_shake_intensity = intensity
        self.screen_shake_duration = duration

    def update_screen_shake(self):
        """Update screen shake effect"""
        if self.screen_shake_duration > 0:
            # Random offset based on remaining intensity
            current_intensity = self.screen_shake_intensity * (self.screen_shake_duration / 15)
            self.screen_offset_x = random.randint(-int(current_intensity), int(current_intensity))
            self.screen_offset_y = random.randint(-int(current_intensity), int(current_intensity))
            self.screen_shake_duration -= 1
        else:
            # Reset offset when shake ends
            self.screen_offset_x = 0
            self.screen_offset_y = 0

    def draw_explosion(self):
        """Draw explosion particles"""
        for particle in self.explosion_particles:
            # Calculate alpha based on lifetime
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            color = (*particle['color'], alpha)
            
            # Create particle surface with alpha
            particle_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, 
                             (particle['size']//2, particle['size']//2), 
                             particle['size']//2)
            
            self.screen.blit(particle_surface, (particle['x'], particle['y']))
    
    def place_bomb(self):
        """Place a bomb at snake's head position"""
        if self.bombs_available > 0 and self.bomb_cooldown <= 0:
            snake_head = self.snake.positions[0]
            bomb = Bomb(snake_head[0], snake_head[1])
            self.bombs.append(bomb)
            self.bombs_available -= 1
            self.bomb_cooldown = 30
            self.sound_manager.play_bomb_place_sound()
            print(f"💣 炸弹放置成功！剩余: {self.bombs_available}")
    
    def update_bombs(self):
        """Update all active bombs"""
        # Update bomb cooldown
        if self.bomb_cooldown > 0:
            self.bomb_cooldown -= 1
        
        # Update each bomb
        for bomb in self.bombs[:]:
            bomb.update()

            # Trigger screen shake when bomb first explodes
            if bomb.exploded and bomb.explosion_timer == 1:
                self.trigger_screen_shake(intensity=12, duration=18)

            # Check if bomb explosion hits snake
            if bomb.exploded and bomb.explosion_timer < 10:
                for segment in self.snake.positions:
                    if bomb.is_colliding(segment[0], segment[1], 5):
                        # Snake hit by bomb explosion
                        self.trigger_explosion(segment)
                        self.game_state = GAME_OVER
                        self.sound_manager.play_bomb_explosion_sound()
                        self.sound_manager.play_game_over_sound()
                        self.sound_manager.stop_background_music()
                        self.sound_manager.start_game_over_music()
                        break
            
            # Remove inactive bombs
            if not bomb.active:
                self.bombs.remove(bomb)
                # Replenish bomb if it exploded naturally
                if bomb.exploded and self.bombs_available < self.max_bombs:
                    self.bombs_available += 1
                    print(f"💣 炸弹补充！剩余炸弹: {self.bombs_available}")
    
    def draw_bombs(self):
        """Draw all active bombs"""
        for bomb in self.bombs:
            bomb.draw(self.screen)
    

    
    def draw_enhanced_game_over_screen(self):
        """Draw enhanced game over screen with explosion effect"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Draw explosion effect if active
        if self.explosion_active:
            self.draw_explosion()
        
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
        
    def draw_menu_screen(self):
        """Draw redesigned modular menu screen with organized panels"""
        theme = self.theme_manager.current_theme

        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 100))
        self.screen.blit(overlay, (0, 0))

        y_pos = 150

        # ===== TITLE SECTION =====
        title_font = pygame.font.Font(None, 64)
        subtitle_font = pygame.font.Font(None, 28)

        # Title with enhanced glow effect
        title_text = title_font.render("🐍 SNAKE GAME 🐍", True, theme.accent_color)
        subtitle_text = subtitle_font.render("Enhanced Edition v3.0", True, theme.text_secondary)

        title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos + 50))

        # Multi-layer glow for title
        for i in range(4):
            glow = title_font.render("🐍 SNAKE GAME 🐍", True, (*theme.accent_color, 80 - i * 20))
            glow_rect = glow.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            self.screen.blit(glow, glow_rect)

        self.screen.blit(title_text, title_rect)
        self.screen.blit(subtitle_text, subtitle_rect)

        y_pos += 100

        # ===== SETTINGS PANEL =====
        panel_width = 600
        panel_x = (WINDOW_WIDTH - panel_width) // 2

        # Settings background panel
        settings_panel = pygame.Surface((panel_width, 100), pygame.SRCALPHA)
        settings_panel.fill((*theme.background_secondary, 200))
        pygame.draw.rect(settings_panel, theme.accent_color, (0, 0, panel_width, 100), 2)
        self.screen.blit(settings_panel, (panel_x, y_pos))

        # Current settings with emoji icons
        theme_name = self.theme_manager.current_theme.name
        difficulty_name = self.difficulty_manager.get_difficulty_name()
        music_style = self.sound_manager.current_music_style.replace('_', ' ').title()

        settings_y = y_pos + 15
        setting_font = pygame.font.Font(None, 26)

        theme_text = setting_font.render(f"🎨 Theme: {theme_name}", True, theme.text_primary)
        diff_text = setting_font.render(f"⚙️  Difficulty: {difficulty_name}", True, theme.text_primary)
        music_text = setting_font.render(f"🎵 Music: {music_style}", True, theme.text_primary)

        self.screen.blit(theme_text, (panel_x + 20, settings_y))
        self.screen.blit(diff_text, (panel_x + 20, settings_y + 30))
        self.screen.blit(music_text, (panel_x + 20, settings_y + 60))

        y_pos += 130

        # ===== SEPARATOR LINE =====
        pygame.draw.line(self.screen, theme.accent_color,
                        (panel_x, y_pos), (panel_x + panel_width, y_pos), 2)
        y_pos += 20

        # ===== 3-COLUMN CONTROLS SECTION =====
        controls_panel = pygame.Surface((panel_width, 120), pygame.SRCALPHA)
        controls_panel.fill((*theme.background_secondary, 200))
        pygame.draw.rect(controls_panel, theme.accent_color, (0, 0, panel_width, 120), 2)
        self.screen.blit(controls_panel, (panel_x, y_pos))

        control_font = pygame.font.Font(None, 20)
        header_font = pygame.font.Font(None, 24)

        # Column positions
        col_width = panel_width // 3
        col1_x = panel_x + 15
        col2_x = panel_x + col_width + 15
        col3_x = panel_x + col_width * 2 + 15
        controls_y = y_pos + 10

        # Column 1: Movement Controls
        header1 = header_font.render("【Movement】", True, theme.accent_color)
        self.screen.blit(header1, (col1_x, controls_y))
        move_text = control_font.render("↑↓←→  Move", True, theme.text_primary)
        self.screen.blit(move_text, (col1_x, controls_y + 30))

        # Column 2: Game Controls
        header2 = header_font.render("【Game】", True, theme.accent_color)
        self.screen.blit(header2, (col2_x, controls_y))
        pause_text = control_font.render("P - Pause", True, theme.text_primary)
        bomb_text = control_font.render("B - Use Bomb", True, theme.text_primary)
        q_text = control_font.render("Q - Menu", True, theme.text_primary)
        self.screen.blit(pause_text, (col2_x, controls_y + 30))
        self.screen.blit(bomb_text, (col2_x, controls_y + 50))
        self.screen.blit(q_text, (col2_x, controls_y + 70))
        # Show bomb count
        bomb_count_text = control_font.render(f"💣 x{self.bombs_available if hasattr(self, 'bombs_available') else 3}",
                                              True, theme.accent_color)
        self.screen.blit(bomb_count_text, (col2_x, controls_y + 90))

        # Column 3: Menu Controls
        header3 = header_font.render("【Menu】", True, theme.accent_color)
        self.screen.blit(header3, (col3_x, controls_y))
        d_text = control_font.render("D - Difficulty", True, theme.text_primary)
        t_text = control_font.render("T - Theme", True, theme.text_primary)
        n_text = control_font.render("N - Music", True, theme.text_primary)
        self.screen.blit(d_text, (col3_x, controls_y + 30))
        self.screen.blit(t_text, (col3_x, controls_y + 55))
        self.screen.blit(n_text, (col3_x, controls_y + 80))

        y_pos += 140

        # ===== SEPARATOR LINE =====
        pygame.draw.line(self.screen, theme.accent_color,
                        (panel_x, y_pos), (panel_x + panel_width, y_pos), 2)
        y_pos += 30

        # ===== START BUTTON with PULSING ANIMATION =====
        pulse = 1 + 0.15 * math.sin(pygame.time.get_ticks() * 0.005)
        start_font = pygame.font.Font(None, int(42 * pulse))
        start_text = start_font.render(">>> Press SPACE to Start <<<", True, theme.accent_color)
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH // 2, y_pos))

        # Glow for start text
        for i in range(3):
            glow = start_font.render(">>> Press SPACE to Start <<<",
                                    True, (*theme.accent_color, 60 - i * 20))
            glow_rect = glow.get_rect(center=(WINDOW_WIDTH // 2, y_pos))
            self.screen.blit(glow, glow_rect)

        self.screen.blit(start_text, start_rect)

        # Quit hint at bottom
        quit_font = pygame.font.Font(None, 22)
        quit_text = quit_font.render("Press Q to Quit | F for Fullscreen", True, theme.text_secondary)
        quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(quit_text, quit_rect)
        
    def run(self):
        """Main game loop with sound cleanup"""
        running = True
        try:
            while running:
                running = self.handle_events()
                self.update()
                self.draw()
                # Only tick the clock based on snake speed if game is running
                if self.game_state == GAME_RUNNING:
                    self.clock.tick(self.snake.speed)
                else:
                    self.clock.tick(60)  # Default 60 FPS for menu and other states
                    
                # Check if snake exists and is valid
                if self.game_state == GAME_RUNNING and (not hasattr(self, 'snake') or self.snake is None):
                    print("⚠️  Snake object is None, returning to menu")
                    self.game_state = GAME_MENU
        except KeyboardInterrupt:
            print("\n👋 Game interrupted by user, exiting gracefully...")
            running = False
        except Exception as e:
            print(f"❌ Error in main game loop: {e}")
            running = False
        
        # Cleanup sound resources
        self.sound_manager.cleanup()
        pygame.quit()
        sys.exit()
        
        # Cleanup sound resources
        self.sound_manager.cleanup()
        pygame.quit()
        sys.exit()