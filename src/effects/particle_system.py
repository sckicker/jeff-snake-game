"""
Particle System for Snake Trail Effects
Creates beautiful particle trails behind the snake
"""
import pygame
import random
import math
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.config import *


class Particle:
    """Individual particle in the trail"""

    def __init__(self, x, y, color, velocity_x=0, velocity_y=0):
        """
        Initialize particle
        Args:
            x, y: Starting position
            color: RGB tuple
            velocity_x, velocity_y: Movement direction
        """
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = random.randint(20, 40)  # Frames to live
        self.max_lifetime = self.lifetime
        self.size = random.uniform(2, 5)

    def update(self):
        """Update particle position and lifetime"""
        self.x += self.velocity_x
        self.y += self.velocity_y

        # Apply slight gravity/drift
        self.velocity_y += 0.05

        # Fade over time
        self.lifetime -= 1

    def is_alive(self):
        """Check if particle should still be drawn"""
        return self.lifetime > 0

    def draw(self, screen):
        """Draw particle with fade effect"""
        if not self.is_alive():
            return

        # Calculate alpha based on remaining lifetime
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        alpha = max(0, min(255, alpha))

        # Current size based on lifetime
        current_size = self.size * (self.lifetime / self.max_lifetime)
        current_size = max(1, int(current_size))

        # Create surface for transparency
        particle_surface = pygame.Surface((current_size * 2, current_size * 2), pygame.SRCALPHA)

        # Draw glow effect
        for i in range(3):
            glow_alpha = alpha // (i + 2)
            glow_color = (*self.color, glow_alpha)
            glow_size = current_size + i * 2
            pygame.draw.circle(particle_surface, glow_color,
                              (current_size, current_size), glow_size)

        # Draw main particle
        pygame.draw.circle(particle_surface, (*self.color, alpha),
                          (current_size, current_size), current_size)

        screen.blit(particle_surface, (int(self.x - current_size), int(self.y - current_size)))


class ParticleSystem:
    """Manages all particles for trail effects"""

    def __init__(self):
        """Initialize particle system"""
        self.particles = []

    def emit_trail_particle(self, x, y, color, intensity=1.0):
        """
        Emit particles for snake trail
        Args:
            x, y: Position to emit from
            color: RGB tuple for particle color
            intensity: Particle emission rate multiplier (0.0-1.0)
        """
        # Emit 2-5 particles per call based on intensity
        num_particles = int(random.randint(2, 5) * intensity)

        for _ in range(num_particles):
            # Random velocity for spread effect
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 1.5)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed

            # Add slight variation to position
            offset_x = random.uniform(-3, 3)
            offset_y = random.uniform(-3, 3)

            particle = Particle(
                x + offset_x,
                y + offset_y,
                color,
                velocity_x,
                velocity_y
            )
            self.particles.append(particle)

    def emit_burst(self, x, y, color, count=20):
        """
        Emit burst of particles (for special effects)
        Args:
            x, y: Position to emit from
            color: RGB tuple
            count: Number of particles to emit
        """
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed

            particle = Particle(x, y, color, velocity_x, velocity_y)
            self.particles.append(particle)

    def update(self):
        """Update all particles"""
        # Update all particles
        for particle in self.particles:
            particle.update()

        # Remove dead particles
        self.particles = [p for p in self.particles if p.is_alive()]

    def draw(self, screen):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)

    def clear(self):
        """Remove all particles"""
        self.particles.clear()

    def get_particle_count(self):
        """Get current number of active particles"""
        return len(self.particles)
