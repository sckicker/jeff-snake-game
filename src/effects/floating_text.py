"""
Floating Text Animation System
Displays score and messages with floating, fading animations
"""
import pygame
import math


class FloatingText:
    """A single floating text instance with animation"""

    def __init__(self, text, x, y, color=(255, 215, 0),
                 font_size=24, duration=60, rise_speed=2):
        """
        Initialize floating text

        Args:
            text: Text to display
            x, y: Starting position
            color: RGB color tuple
            font_size: Font size
            duration: Animation duration in frames (60 = 1 second)
            rise_speed: Upward movement speed
        """
        self.text = text
        self.x = x
        self.y = y
        self.original_y = y
        self.color = color
        self.font_size = font_size
        self.duration = duration
        self.rise_speed = rise_speed
        self.timer = 0
        self.active = True
        self.font = pygame.font.Font(None, font_size)

    def update(self):
        """Update animation state"""
        if not self.active:
            return

        self.timer += 1
        # Slow down rising over time
        progress = self.timer / self.duration
        self.y -= self.rise_speed * (1 - progress)

        if self.timer >= self.duration:
            self.active = False

    def draw(self, screen):
        """Draw the floating text"""
        if not self.active:
            return

        # Calculate fade-out alpha
        progress = self.timer / self.duration
        alpha = int(255 * (1 - progress))

        # Calculate scale (slight grow then shrink)
        scale = 1.0 + 0.3 * math.sin(progress * math.pi)

        # Render text
        text_surface = self.font.render(self.text, True, self.color)

        # Apply scale
        scaled_width = int(text_surface.get_width() * scale)
        scaled_height = int(text_surface.get_height() * scale)
        if scaled_width > 0 and scaled_height > 0:
            scaled_surface = pygame.transform.scale(
                text_surface, (scaled_width, scaled_height)
            )

            # Apply alpha
            scaled_surface.set_alpha(alpha)

            # Center and draw
            rect = scaled_surface.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(scaled_surface, rect)


class FloatingTextManager:
    """Manages multiple floating text instances"""

    def __init__(self):
        self.texts = []

    def add_text(self, text, x, y, **kwargs):
        """Add a new floating text"""
        self.texts.append(FloatingText(text, x, y, **kwargs))

    def add_score_text(self, score, x, y):
        """Add score text with color based on score value"""
        if score >= 50:
            # Big score - gold and large
            self.add_text(
                f"+{score}!",
                x, y,
                color=(255, 215, 0),  # Gold
                font_size=36,
                duration=80,
                rise_speed=3
            )
        elif score >= 20:
            # Medium score - bright green
            self.add_text(
                f"+{score}",
                x, y,
                color=(50, 255, 50),  # Bright green
                font_size=30,
                duration=70,
                rise_speed=2.5
            )
        else:
            # Small score - white
            self.add_text(
                f"+{score}",
                x, y,
                color=(255, 255, 255),  # White
                font_size=24,
                duration=60,
                rise_speed=2
            )

    def add_message(self, message, x, y, color=(255, 255, 255), font_size=28):
        """Add a custom message"""
        self.add_text(
            message,
            x, y,
            color=color,
            font_size=font_size,
            duration=90,
            rise_speed=1.5
        )

    def update(self):
        """Update all floating texts"""
        for text in self.texts[:]:
            text.update()
            if not text.active:
                self.texts.remove(text)

    def draw(self, screen):
        """Draw all floating texts"""
        for text in self.texts:
            text.draw(screen)

    def clear(self):
        """Remove all floating texts"""
        self.texts.clear()
