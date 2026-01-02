"""
Sound Effects Manager for Enhanced Snake Game
Handles all sound effects using pygame's sound capabilities
"""

import pygame
import numpy as np
from config import *

class SoundManager:
    """Manages all game sound effects"""
    
    def __init__(self):
        """Initialize sound manager"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = SOUND_ENABLED
            self.initialized = True
            print("✅ Sound system initialized successfully!")
        except Exception as e:
            print(f"❌ Warning: Could not initialize sound system: {e}")
            self.enabled = False
            self.initialized = False
            return
        
        # Pre-generate sound effects
        self.eat_sound = self.create_sound(EAT_SOUND_FREQ, EAT_SOUND_DURATION, volume=0.3)
        self.crash_sound = self.create_sound(CRASH_SOUND_FREQ, CRASH_SOUND_DURATION, volume=0.5)
        self.game_over_sound = self.create_sound(GAME_OVER_SOUND_FREQ, GAME_OVER_SOUND_DURATION, volume=0.6)
        self.pause_sound = self.create_sound(PAUSE_SOUND_FREQ, PAUSE_SOUND_DURATION, volume=0.2)
        self.speed_up_sound = self.create_sound(SPEED_UP_SOUND_FREQ, SPEED_UP_SOUND_DURATION, volume=0.3)
        
    def create_sound(self, frequency, duration, volume=0.3):
        """Create a sound effect with given frequency and duration"""
        if not self.enabled or not self.initialized:
            return None
            
        try:
            # Generate a simple tone using sine wave
            sample_rate = 22050
            samples = int(sample_rate * duration / 1000)
            
            # Create time array
            t = np.linspace(0, duration / 1000, samples, False)
            
            # Generate sine wave with some harmonics for richer sound
            wave = np.sin(2 * np.pi * frequency * t)
            # Add some harmonics for better sound quality
            wave += 0.3 * np.sin(2 * np.pi * frequency * 2 * t)
            wave += 0.1 * np.sin(2 * np.pi * frequency * 3 * t)
            
            # Apply envelope to make sound smoother
            envelope = np.exp(-t * 5)  # Exponential decay
            wave *= envelope
            
            # Convert to 16-bit integers
            wave = (wave * 32767 * volume).astype(np.int16)
            
            # Create stereo sound (duplicate for both channels)
            stereo_wave = np.column_stack([wave, wave])
            
            # Convert to pygame sound
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create sound effect: {e}")
            return None
    
    def play_eat_sound(self):
        """Play eating sound effect"""
        if self.eat_sound:
            self.eat_sound.play()
            print("🔊 Playing eat sound")
    
    def play_crash_sound(self):
        """Play crash/collision sound effect"""
        if self.crash_sound:
            self.crash_sound.play()
            print("🔊 Playing crash sound")
    
    def play_game_over_sound(self):
        """Play game over sound effect"""
        if self.game_over_sound:
            self.game_over_sound.play()
            print("🔊 Playing game over sound")
    
    def play_pause_sound(self):
        """Play pause sound effect"""
        if self.pause_sound:
            self.pause_sound.play()
            print("🔊 Playing pause sound")
    
    def play_speed_up_sound(self):
        """Play speed up sound effect"""
        if self.speed_up_sound:
            self.speed_up_sound.play()
            print("🔊 Playing speed up sound")
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        print(f"🔊 Sound {status}")
        
    def cleanup(self):
        """Clean up sound resources"""
        if self.initialized:
            pygame.mixer.quit()
            print("🔊 Sound system cleaned up")