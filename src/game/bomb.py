"""
炸弹类
实现炸弹放置、倒计时、爆炸效果和声音
"""

import pygame
import random
import math
from src.config.config import *

class Bomb:
    """炸弹类，包含放置、倒计时和爆炸功能"""
    
    def __init__(self, x, y, explosion_radius=100, countdown=180):  # 3秒倒计时（60帧/秒）
        """初始化炸弹"""
        self.x = x
        self.y = y
        self.explosion_radius = explosion_radius
        self.countdown = countdown
        self.active = True
        self.exploded = False
        self.particles = []
        self.explosion_timer = 0
        self.explosion_duration = 45  # 爆炸效果持续时间
        
        # 炸弹颜色（红色到橙色的渐变）
        self.colors = [
            (255, 0, 0),      # 红色
            (255, 69, 0),     # 橙红色
            (255, 140, 0),    # 深橙色
            (255, 165, 0)     # 橙色
        ]
        
    def update(self):
        """更新炸弹状态"""
        if not self.exploded:
            self.countdown -= 1
            if self.countdown <= 0:
                self.explode()
        else:
            # 更新爆炸粒子
            self.update_explosion()
    
    def explode(self):
        """触发爆炸"""
        self.exploded = True
        self.active = True
        self.create_explosion_particles()
    
    def create_explosion_particles(self):
        """创建爆炸粒子效果"""
        # 创建中心爆炸粒子
        for _ in range(80):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 12)
            size = random.randint(3, 8)
            lifetime = random.randint(25, 50)
            
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': size,
                'color': (random.randint(200, 255), random.randint(50, 150), random.randint(0, 50)),
                'lifetime': lifetime,
                'max_lifetime': lifetime
            }
            self.particles.append(particle)
        
        # 创建冲击波粒子
        for _ in range(30):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(8, 15)
            size = random.randint(4, 10)
            lifetime = random.randint(15, 30)
            
            particle = {
                'x': self.x,
                'y': self.y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'size': size,
                'color': (255, 255, 200),  # 冲击波颜色
                'lifetime': lifetime,
                'max_lifetime': lifetime
            }
            self.particles.append(particle)
    
    def update_explosion(self):
        """更新爆炸动画"""
        self.explosion_timer += 1
        
        # 更新粒子
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['lifetime'] -= 1
            
            # 移除死亡的粒子
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
        
        # 爆炸结束
        if self.explosion_timer >= self.explosion_duration and not self.particles:
            self.active = False
    
    def draw(self, screen):
        """绘制炸弹"""
        if not self.exploded:
            # 绘制炸弹本体（闪烁效果）
            flash_intensity = (pygame.time.get_ticks() // 200) % 2  # 闪烁效果
            color_index = (pygame.time.get_ticks() // 100) % len(self.colors)
            
            bomb_color = self.colors[color_index]
            
            # 绘制炸弹主体（更大的尺寸）
            pygame.draw.circle(screen, bomb_color, (self.x, self.y), 15)
            pygame.draw.circle(screen, (50, 50, 50), (self.x, self.y), 10)
            
            # 绘制外圈闪烁效果
            if flash_intensity:
                pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 18, 2)
            
            # 绘制引线
            fuse_length = 15
            fuse_x = self.x + fuse_length
            fuse_y = self.y - fuse_length
            pygame.draw.line(screen, (200, 200, 0), (self.x, self.y), (fuse_x, fuse_y), 3)
            
            # 绘制倒计时文本
            font = pygame.font.Font(None, 24)
            countdown_text = font.render(str(max(0, self.countdown // 60)), True, (255, 255, 255))
            text_rect = countdown_text.get_rect(center=(self.x, self.y))
            screen.blit(countdown_text, text_rect)
        else:
            # 绘制爆炸效果
            self.draw_explosion(screen)
    
    def draw_explosion(self, screen):
        """绘制爆炸粒子"""
        for particle in self.particles:
            # 根据生命周期计算透明度
            alpha = int(255 * (particle['lifetime'] / particle['max_lifetime']))
            color = (*particle['color'], alpha)
            
            # 创建带透明度的粒子表面
            particle_surface = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, 
                             (particle['size']//2, particle['size']//2), 
                             particle['size']//2)
            
            screen.blit(particle_surface, (particle['x'], particle['y']))
            
            # 绘制爆炸冲击波（仅在爆炸初期）
            if self.explosion_timer < 15:
                wave_radius = self.explosion_timer * 8
                wave_alpha = 150 - self.explosion_timer * 10
                if wave_alpha > 0:
                    wave_surface = pygame.Surface((wave_radius*2, wave_radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(wave_surface, (255, 200, 0, wave_alpha), 
                                     (wave_radius, wave_radius), wave_radius)
                    screen.blit(wave_surface, (self.x - wave_radius, self.y - wave_radius))
    
    def get_explosion_area(self):
        """获取爆炸影响区域"""
        if self.exploded and self.explosion_timer < 10:  # 只在爆炸初期有效
            return (self.x, self.y, self.explosion_radius)
        return None
    
    def is_colliding(self, x, y, radius=0):
        """检查是否与指定位置碰撞"""
        if self.exploded and self.explosion_timer < 15:  # 爆炸影响时间
            distance = math.sqrt((x - self.x)**2 + (y - self.y)**2)
            return distance < self.explosion_radius + radius
        return False