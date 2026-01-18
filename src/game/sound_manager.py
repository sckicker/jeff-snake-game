"""
Sound Effects Manager for Enhanced Snake Game
Handles all sound effects using pygame's sound capabilities
"""

import pygame
import numpy as np
import os
import sys

# Add parent directory to Python path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.config import *

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
        
        # Bomb sound effects
        self.bomb_place_sound = self.create_bomb_place_sound()
        self.bomb_explosion_sound = self.create_bomb_explosion_sound()

        # Power-up collection sounds (3 types)
        self.powerup_slow_sound = self.create_powerup_sound('slow_potion')
        self.powerup_shield_sound = self.create_powerup_sound('shield')
        self.powerup_double_sound = self.create_powerup_sound('double_score')

        # Theme switching sound
        self.theme_switch_sound = self.create_theme_switch_sound()

        # Combo sounds (3 levels)
        self.combo_2x_sound = self.create_combo_sound(2)
        self.combo_3x_sound = self.create_combo_sound(3)
        self.combo_5x_sound = self.create_combo_sound(5)

        # Shield break sound
        self.shield_break_sound = self.create_shield_break_sound()

        # Create background music for different game phases
        if BACKGROUND_MUSIC_STYLE == "chiptune":
            self.background_music = self.create_chiptune_background_music()
            self.menu_music = self.create_chiptune_menu_music()
            self.game_over_music = self.create_chiptune_game_over_music()
        elif BACKGROUND_MUSIC_STYLE == "ambient":
            self.background_music = self.create_ambient_background_music()
            self.menu_music = self.create_ambient_menu_music()
            self.game_over_music = self.create_ambient_game_over_music()
        elif BACKGROUND_MUSIC_STYLE == "kids":
            self.background_music = self.create_kids_background_music()
            self.menu_music = self.create_kids_menu_music()
            self.game_over_music = self.create_kids_game_over_music()
        else:
            self.background_music = self.create_retro_background_music()
            self.menu_music = self.create_retro_menu_music()
            self.game_over_music = self.create_retro_game_over_music()
        
        self.music_channel = None
        self.current_music = "menu"  # Track current music phase
        self.current_music_style = BACKGROUND_MUSIC_STYLE  # Track current music style
        
    def create_chiptune_background_music(self):
        """Create modern chiptune-style background music"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / BACKGROUND_MUSIC_BPM
            
            # Create 8-bar chiptune loop
            total_duration = beat_duration * 32  # 8 bars * 4 beats
            samples = int(sample_rate * total_duration)
            
            # Define notes for chiptune (C major pentatonic for happy feel)
            c_major_pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 659.25]
            
            music_pattern = np.zeros(samples)
            
            # Create chiptune pattern with duty cycle modulation
            for bar in range(8):
                bar_start = int(bar * samples / 8)
                bar_end = int((bar + 1) * samples / 8)
                
                # Melody progression
                melody_notes = [
                    c_major_pentatonic[0],  # C
                    c_major_pentatonic[2],  # E
                    c_major_pentatonic[4],  # G
                    c_major_pentatonic[5],  # C (higher)
                ]
                
                for i in range(bar_start, bar_end):
                    t = (i - bar_start) / sample_rate
                    global_t = i / sample_rate
                    
                    # Lead voice with square wave (chiptune characteristic)
                    note_idx = int(t / (beat_duration * 2)) % len(melody_notes)
                    lead_freq = melody_notes[note_idx]
                    
                    # Square wave generation
                    period = sample_rate / lead_freq
                    square_wave = np.sign(np.sin(2 * np.pi * global_t * lead_freq))
                    lead = 0.2 * square_wave
                    
                    # Bass line with triangle wave
                    bass_freq = c_major_pentatonic[0] / 2
                    triangle_wave = 2 * np.arcsin(np.sin(2 * np.pi * global_t * bass_freq)) / np.pi
                    bass = 0.15 * triangle_wave
                    
                    # Simple percussion on beats
                    beat_phase = (t % beat_duration) / beat_duration
                    if beat_phase < 0.1:  # Kick on beat
                        kick = 0.3 * np.sin(2 * np.pi * 60 * t) * np.exp(-t * 10)
                    else:
                        kick = 0
                    
                    if 0.4 < beat_phase < 0.5:  # Snare on off-beat
                        snare = 0.2 * (np.random.random() - 0.5) * np.exp(-t * 5)
                    else:
                        snare = 0
                    
                    # Combine all elements
                    music_pattern[i] = lead + bass + kick + snare
                    
                    # Apply chiptune-style volume envelope
                    envelope = 0.8 + 0.2 * np.sin(2 * np.pi * global_t / total_duration * 4)
                    music_pattern[i] *= envelope
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            
            # Create stereo
            stereo_music = np.column_stack([music_pattern, music_pattern])
            
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create chiptune background music: {e}")
            return None
    
    def create_ambient_background_music(self):
        """Create soothing ambient background music"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / BACKGROUND_MUSIC_BPM
            
            # Create longer ambient loop (32 bars)
            total_duration = beat_duration * 128  # 32 bars * 4 beats
            samples = int(sample_rate * total_duration)
            
            # Use pentatonic scale for ambient feel
            d_pentatonic = [293.66, 329.63, 392.00, 440.00, 523.25, 659.25]  # D major pentatonic
            
            music_pattern = np.zeros(samples)
            
            # Create slow, evolving ambient pad
            for i in range(samples):
                t = i / sample_rate
                
                # Multiple layers of slow-moving pads
                pad1_freq = d_pentatonic[0] * 0.5  # Deep drone
                pad1 = 0.2 * np.sin(2 * np.pi * pad1_freq * t) * np.exp(-t * 0.1)
                
                pad2_freq = d_pentatonic[2] * 0.7  # Mid pad
                pad2 = 0.15 * np.sin(2 * np.pi * pad2_freq * t + np.sin(2 * np.pi * 0.1 * t))  # Slow LFO
                
                pad3_freq = d_pentatonic[4] * 0.8  # Higher pad
                pad3 = 0.1 * np.sin(2 * np.pi * pad3_freq * t + 0.5 * np.sin(2 * np.pi * 0.05 * t))  # Even slower LFO
                
                # Gentle bell-like tones occasionally
                bell_intensity = 0.05 * (1 + np.sin(2 * np.pi * t / 20))  # Every 20 seconds
                bell_freq = d_pentatonic[int(t / 5) % len(d_pentatonic)]  # Changes every 5 seconds
                bell = bell_intensity * np.sin(2 * np.pi * bell_freq * t) * np.exp(-(t % 5) * 2)
                
                # Combine all layers
                music_pattern[i] = pad1 + pad2 + pad3 + bell
                
                # Very slow volume envelope (breathing effect)
                envelope = 0.7 + 0.3 * np.sin(2 * np.pi * t / 30)  # 30-second cycle
                music_pattern[i] *= envelope
            
            # Apply heavy smoothing for ambient feel
            def heavy_smooth(signal, window_size=50):
                smoothed = np.zeros_like(signal)
                for i in range(len(signal)):
                    start = max(0, i - window_size // 2)
                    end = min(len(signal), i + window_size // 2 + 1)
                    smoothed[i] = np.mean(signal[start:end])
                return smoothed
            
            music_pattern = heavy_smooth(music_pattern)
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            
            # Create stereo with wide ambient feel
            stereo_music = np.column_stack([music_pattern, music_pattern])
            
            # Add stereo width with different delays
            delay1 = int(sample_rate * 0.02)  # 20ms delay
            delay2 = int(sample_rate * 0.03)  # 30ms delay
            
            if len(music_pattern) > delay2:
                stereo_music[delay1:, 0] += (music_pattern[:-delay1] * 0.2).astype(np.int16)
                stereo_music[delay2:, 1] += (music_pattern[:-delay2] * 0.15).astype(np.int16)
            
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create ambient background music: {e}")
            return None
    
    def create_chiptune_menu_music(self):
        """Create energetic chiptune music for menu/lobby"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 1.2)  # Slightly faster tempo
            
            # Create 4-bar energetic menu loop
            total_duration = beat_duration * 16
            samples = int(sample_rate * total_duration)
            
            # Use C major pentatonic for upbeat feel
            c_major_pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]
            
            music_pattern = np.zeros(samples)
            
            for i in range(samples):
                t = i / sample_rate
                
                # Lead melody - more energetic
                melody_note = c_major_pentatonic[(int(t / (beat_duration * 2))) % len(c_major_pentatonic)]
                lead = 0.25 * np.sign(np.sin(2 * np.pi * melody_note * t))
                
                # Bass line - driving rhythm
                bass_note = c_major_pentatonic[0] / 2
                bass_intensity = 0.3 if (i % int(sample_rate * beat_duration)) < int(sample_rate * beat_duration * 0.7) else 0.1
                bass = bass_intensity * np.sign(np.sin(2 * np.pi * bass_note * t))
                
                # Simple percussion - more prominent
                beat_phase = (t % beat_duration) / beat_duration
                if beat_phase < 0.15:  # Stronger kick
                    kick = 0.4 * np.sin(2 * np.pi * 80 * t) * np.exp(-t * 8)
                else:
                    kick = 0
                
                if 0.45 < beat_phase < 0.6:  # Snare
                    snare = 0.3 * (np.random.random() - 0.5) * np.exp(-t * 6)
                else:
                    snare = 0
                
                # Combine with slightly higher volume for menu
                music_pattern[i] = lead + bass + kick + snare
                music_pattern[i] *= 1.2  # Slightly louder for menu
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create chiptune menu music: {e}")
            return None
    
    def create_chiptune_game_over_music(self):
        """Create calming chiptune music for game over"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 0.7)  # Slower tempo for game over
            
            # Create 8-bar calming loop
            total_duration = beat_duration * 32
            samples = int(sample_rate * total_duration)
            
            # Use A minor pentatonic for melancholic feel
            a_minor_pentatonic = [220.00, 261.63, 293.66, 329.63, 392.00, 440.00]
            
            music_pattern = np.zeros(samples)
            
            for i in range(samples):
                t = i / sample_rate
                
                # Slow, gentle melody
                melody_note = a_minor_pentatonic[(int(t / (beat_duration * 4))) % len(a_minor_pentatonic)]
                lead = 0.15 * np.sign(np.sin(2 * np.pi * melody_note * t))
                
                # Deep, slow bass
                bass_note = a_minor_pentatonic[0] / 2
                bass = 0.2 * np.sign(np.sin(2 * np.pi * bass_note * t))
                
                # Very subtle percussion
                beat_phase = (t % (beat_duration * 2)) / (beat_duration * 2)
                if beat_phase < 0.1:
                    kick = 0.1 * np.sin(2 * np.pi * 60 * t) * np.exp(-t * 5)
                else:
                    kick = 0
                
                # Combine with lower volume for game over
                music_pattern[i] = lead + bass + kick
                music_pattern[i] *= 0.8  # Quieter for game over
            
            # Apply heavy smoothing for calming effect
            def smooth_signal(signal, window_size=20):
                smoothed = np.zeros_like(signal)
                for i in range(len(signal)):
                    start = max(0, i - window_size // 2)
                    end = min(len(signal), i + window_size // 2 + 1)
                    smoothed[i] = np.mean(signal[start:end])
                return smoothed
            
            music_pattern = smooth_signal(music_pattern)
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create chiptune game over music: {e}")
            return None
    
    def create_retro_menu_music(self):
        """Create energetic retro arcade music for menu/lobby"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 1.3)  # Faster tempo for menu
            
            # Create 4-bar energetic menu loop
            total_duration = beat_duration * 16
            samples = int(sample_rate * total_duration)
            
            # Use C major scale for upbeat menu feel
            c_major = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
            
            music_pattern = np.zeros(samples)
            
            for bar in range(4):
                bar_start = int(bar * samples / 4)
                bar_end = int((bar + 1) * samples / 4)
                
                # Simple chord progression for menu
                chord_progressions = [
                    [c_major[0], c_major[2], c_major[4]],  # C major
                    [c_major[3], c_major[5], c_major[0] * 0.5],  # F major
                    [c_major[4], c_major[0] * 0.5, c_major[2] * 0.5],  # G major
                    [c_major[0], c_major[2], c_major[4]],  # Back to C major
                ]
                current_chord = chord_progressions[bar]
                
                for i in range(bar_start, bar_end):
                    t = (i - bar_start) / sample_rate
                    global_t = i / sample_rate
                    
                    # Driving bass line
                    bass_note = current_chord[0] / 2
                    bass_intensity = 0.5 if (i % int(sample_rate * beat_duration)) < int(sample_rate * beat_duration * 0.8) else 0.2
                    bass = bass_intensity * np.sin(2 * np.pi * bass_note * global_t)
                    
                    # Energetic melody
                    melody_note = current_chord[(i // int(sample_rate * beat_duration * 2)) % len(current_chord)]
                    melody_intensity = 0.4 * (0.6 + 0.4 * np.sin(2 * np.pi * 1 * global_t))
                    melody = melody_intensity * np.sin(2 * np.pi * melody_note * global_t)
                    
                    # Percussion - more driving for menu
                    beat_phase = (t % beat_duration) / beat_duration
                    if beat_phase < 0.2:
                        kick = 0.5 * np.sin(2 * np.pi * 80 * t) * np.exp(-t * 12)
                    else:
                        kick = 0
                    
                    if 0.4 < beat_phase < 0.6:
                        snare = 0.3 * (np.random.random() - 0.5) * np.exp(-t * 8)
                    else:
                        snare = 0
                    
                    # Combine - louder for menu
                    music_pattern[i] = bass + melody + kick + snare
                    music_pattern[i] *= 1.3
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create retro menu music: {e}")
            return None
    
    def create_retro_game_over_music(self):
        """Create calming retro music for game over"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 0.6)  # Much slower for game over
            
            # Create 8-bar melancholic loop
            total_duration = beat_duration * 32
            samples = int(sample_rate * total_duration)
            
            # Use A minor for melancholic feel
            a_minor = [220.00, 246.94, 261.63, 293.66, 329.63, 392.00, 440.00]
            
            music_pattern = np.zeros(samples)
            
            for bar in range(8):
                bar_start = int(bar * samples / 8)
                bar_end = int((bar + 1) * samples / 8)
                
                # Melancholic chord progression
                chord_progressions = [
                    [a_minor[0], a_minor[2], a_minor[4]],  # A minor
                    [a_minor[3], a_minor[5], a_minor[0] * 0.5],  # D minor
                    [a_minor[4], a_minor[0] * 0.5, a_minor[2] * 0.5],  # E major
                    [a_minor[0], a_minor[2], a_minor[4]],  # Back to A minor
                ]
                current_chord = chord_progressions[bar % len(chord_progressions)]
                
                for i in range(bar_start, bar_end):
                    t = (i - bar_start) / sample_rate
                    global_t = i / sample_rate
                    
                    # Deep, slow bass
                    bass_note = current_chord[0] / 2
                    bass_intensity = 0.3 if (i % int(sample_rate * beat_duration * 2)) < int(sample_rate * beat_duration * 1.5) else 0.1
                    bass = bass_intensity * np.sin(2 * np.pi * bass_note * global_t)
                    
                    # Gentle, melancholic melody
                    melody_note = current_chord[(i // int(sample_rate * beat_duration * 4)) % len(current_chord)]
                    melody_intensity = 0.2 * (0.4 + 0.6 * np.sin(2 * np.pi * 0.2 * global_t))
                    melody = melody_intensity * np.sin(2 * np.pi * melody_note * global_t)
                    
                    # Very subtle percussion
                    if i % int(sample_rate * beat_duration * 2) < int(sample_rate * 0.1):
                        kick = 0.15 * np.sin(2 * np.pi * 50 * t) * np.exp(-t * 4)
                    else:
                        kick = 0
                    
                    # Combine - quieter for game over
                    music_pattern[i] = bass + melody + kick
                    music_pattern[i] *= 0.7
            
            # Apply smoothing for calming effect
            def smooth_signal(signal, window_size=15):
                smoothed = np.zeros_like(signal)
                for i in range(len(signal)):
                    start = max(0, i - window_size // 2)
                    end = min(len(signal), i + window_size // 2 + 1)
                    smoothed[i] = np.mean(signal[start:end])
                return smoothed
            
            music_pattern = smooth_signal(music_pattern)
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create retro game over music: {e}")
            return None
    
    def create_ambient_menu_music(self):
        """Create ambient music for menu/lobby"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 1.1)  # Slightly faster for menu
            
            # Create 8-bar ambient menu loop
            total_duration = beat_duration * 32
            samples = int(sample_rate * total_duration)
            
            # Use C major pentatonic for welcoming feel
            c_pentatonic = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25]
            
            music_pattern = np.zeros(samples)
            
            for i in range(samples):
                t = i / sample_rate
                
                # Multiple ambient layers
                pad1_freq = c_pentatonic[0] * 0.7  # Root note
                pad1 = 0.25 * np.sin(2 * np.pi * pad1_freq * t + np.sin(2 * np.pi * 0.2 * t))
                
                pad2_freq = c_pentatonic[2] * 0.8  # Third
                pad2 = 0.2 * np.sin(2 * np.pi * pad2_freq * t + 0.3 * np.sin(2 * np.pi * 0.15 * t))
                
                pad3_freq = c_pentatonic[4] * 0.9  # Fifth
                pad3 = 0.15 * np.sin(2 * np.pi * pad3_freq * t + 0.5 * np.sin(2 * np.pi * 0.1 * t))
                
                # Occasional bell tones
                bell_intensity = 0.1 * (1 + np.sin(2 * np.pi * t / 15))
                bell_freq = c_pentatonic[int(t / 8) % len(c_pentatonic)]
                bell = bell_intensity * np.sin(2 * np.pi * bell_freq * t) * np.exp(-(t % 8) * 0.5)
                
                # Combine - slightly more energetic for menu
                music_pattern[i] = pad1 + pad2 + pad3 + bell
                music_pattern[i] *= 1.1
            
            # Apply smoothing
            def smooth_signal(signal, window_size=10):
                smoothed = np.zeros_like(signal)
                for i in range(len(signal)):
                    start = max(0, i - window_size // 2)
                    end = min(len(signal), i + window_size // 2 + 1)
                    smoothed[i] = np.mean(signal[start:end])
                return smoothed
            
            music_pattern = smooth_signal(music_pattern)
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create ambient menu music: {e}")
            return None
    
    def create_ambient_game_over_music(self):
        """Create deep ambient music for game over"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 0.5)  # Much slower for game over
            
            # Create 16-bar deep ambient loop
            total_duration = beat_duration * 64
            samples = int(sample_rate * total_duration)
            
            # Use D minor pentatonic for deep, contemplative feel
            d_minor_pentatonic = [293.66, 329.63, 392.00, 440.00, 587.33]
            
            music_pattern = np.zeros(samples)
            
            for i in range(samples):
                t = i / sample_rate
                
                # Deep drone layers
                drone1_freq = d_minor_pentatonic[0] * 0.3  # Very deep
                drone1 = 0.3 * np.sin(2 * np.pi * drone1_freq * t)
                
                drone2_freq = d_minor_pentatonic[2] * 0.4  # Slightly higher
                drone2 = 0.25 * np.sin(2 * np.pi * drone2_freq * t + np.sin(2 * np.pi * 0.05 * t))
                
                # Slow moving pad
                pad_freq = d_minor_pentatonic[1] * 0.6
                pad = 0.2 * np.sin(2 * np.pi * pad_freq * t + 0.4 * np.sin(2 * np.pi * 0.08 * t))
                
                # Occasional deep bell
                bell_intensity = 0.08 * (1 + np.sin(2 * np.pi * t / 25))
                bell_freq = d_minor_pentatonic[int(t / 12) % len(d_minor_pentatonic)] * 0.8
                bell = bell_intensity * np.sin(2 * np.pi * bell_freq * t) * np.exp(-(t % 12) * 0.3)
                
                # Combine - quieter and deeper
                music_pattern[i] = drone1 + drone2 + pad + bell
                music_pattern[i] *= 0.8
            
            # Apply heavy smoothing for deep ambient feel
            def smooth_signal(signal, window_size=30):
                smoothed = np.zeros_like(signal)
                for i in range(len(signal)):
                    start = max(0, i - window_size // 2)
                    end = min(len(signal), i + window_size // 2 + 1)
                    smoothed[i] = np.mean(signal[start:end])
                return smoothed
            
            music_pattern = smooth_signal(music_pattern)
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create ambient game over music: {e}")
            return None

    def create_kids_background_music(self):
        """Create fun, cheerful music for kids"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None

        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 1.2)  # Slightly faster for kids

            # Create 8-bar cheerful loop
            total_duration = beat_duration * 32
            samples = int(sample_rate * total_duration)

            # C major pentatonic scale for happy, cheerful sound (no dissonance)
            c_pentatonic = [523.25, 587.33, 659.25, 783.99, 880.00, 1046.50]  # C D E G A C (higher octave)

            # Happy melody pattern (Mary Had a Little Lamb style)
            melody_pattern = [2, 1, 0, 1, 2, 2, 2, 1, 1, 1, 2, 4, 4, 2, 1, 0]

            music_pattern = np.zeros(samples)

            for beat in range(16):
                beat_start = int(beat * samples / 16)
                beat_end = int((beat + 1) * samples / 16)

                # Get melody note for this beat
                melody_note = c_pentatonic[melody_pattern[beat]]

                for i in range(beat_start, beat_end):
                    t = (i - beat_start) / sample_rate

                    # Simple, bright melody
                    melody = 0.4 * np.sin(2 * np.pi * melody_note * t)
                    # Add second harmonic for brightness
                    melody += 0.15 * np.sin(2 * np.pi * melody_note * 2 * t)

                    # Simple bouncy bass (root note pattern)
                    bass_note = c_pentatonic[0] * 0.5  # Low C
                    bass = 0.2 * np.sin(2 * np.pi * bass_note * t)

                    # Simple rhythm accompaniment
                    if int(t * 4) % 2 == 0:  # Quarter note rhythm
                        rhythm = 0.1 * np.sin(2 * np.pi * c_pentatonic[2] * t)
                    else:
                        rhythm = 0.1 * np.sin(2 * np.pi * c_pentatonic[4] * t)

                    # Combine with simple ADSR envelope
                    attack = min(1.0, t * 20)
                    decay = max(0.3, 1.0 - t * 2)
                    envelope = attack * decay

                    music_pattern[i] = (melody + bass + rhythm) * envelope

            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME * 0.9).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])

            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound

        except Exception as e:
            print(f"❌ Warning: Could not create kids background music: {e}")
            return None

    def create_kids_menu_music(self):
        """Create friendly, inviting menu music for kids"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None

        try:
            sample_rate = 22050
            beat_duration = 60.0 / (BACKGROUND_MUSIC_BPM * 1.1)

            # Create 4-bar friendly loop
            total_duration = beat_duration * 16
            samples = int(sample_rate * total_duration)

            # C major pentatonic for happy sound
            c_pentatonic = [523.25, 587.33, 659.25, 783.99, 880.00]  # C D E G A

            # Simple ascending and descending pattern
            melody_pattern = [0, 2, 4, 2, 0, 2, 4, 2]

            music_pattern = np.zeros(samples)

            for beat in range(8):
                beat_start = int(beat * samples / 8)
                beat_end = int((beat + 1) * samples / 8)

                melody_note = c_pentatonic[melody_pattern[beat]]

                for i in range(beat_start, beat_end):
                    t = (i - beat_start) / sample_rate

                    # Bright, cheerful tone
                    tone = 0.5 * np.sin(2 * np.pi * melody_note * t)
                    tone += 0.2 * np.sin(2 * np.pi * melody_note * 2 * t)

                    # Gentle envelope
                    envelope = np.exp(-t * 3)
                    music_pattern[i] = tone * envelope

            # Apply volume
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME * 0.8).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])

            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound

        except Exception as e:
            print(f"❌ Warning: Could not create kids menu music: {e}")
            return None

    def create_kids_game_over_music(self):
        """Create encouraging, non-sad game over music for kids"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None

        try:
            sample_rate = 22050
            duration = 3.0  # 3 seconds

            samples = int(sample_rate * duration)

            # C major arpeggio (encouraging, not sad)
            c_arpeggio = [523.25, 659.25, 783.99, 1046.50]  # C E G C

            music_pattern = np.zeros(samples)

            # Play ascending arpeggio (encouraging)
            for note_idx, freq in enumerate(c_arpeggio):
                note_start = int(note_idx * samples / len(c_arpeggio))
                note_end = int((note_idx + 1) * samples / len(c_arpeggio))

                for i in range(note_start, note_end):
                    t = (i - note_start) / sample_rate

                    # Gentle, encouraging tone
                    tone = 0.4 * np.sin(2 * np.pi * freq * t)
                    tone += 0.15 * np.sin(2 * np.pi * freq * 2 * t)

                    # Gentle decay
                    envelope = np.exp(-t * 2)
                    music_pattern[i] = tone * envelope

            # Apply volume
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME * 0.7).astype(np.int16)
            stereo_music = np.column_stack([music_pattern, music_pattern])

            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound

        except Exception as e:
            print(f"❌ Warning: Could not create kids game over music: {e}")
            return None

    def create_retro_background_music(self):
        """Create professional retro arcade-style background music"""
        if not self.enabled or not self.initialized or not BACKGROUND_MUSIC_ENABLED:
            return None
            
        try:
            sample_rate = 22050
            beat_duration = 60.0 / BACKGROUND_MUSIC_BPM  # Duration of one beat in seconds
            
            # Create a 16-bar loop (more interesting progression)
            total_duration = beat_duration * 64  # 16 bars * 4 beats
            samples = int(sample_rate * total_duration)
            
            # Define musical notes (C minor scale for more interesting feel)
            c_minor = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 523.25]  # C, D, Eb, F, G, A, C
            
            # Create chord progressions (more musical)
            chord_progressions = [
                [c_minor[0], c_minor[2], c_minor[4]],  # C minor (i)
                [c_minor[3], c_minor[5], c_minor[0] * 0.5],  # F major (iv)
                [c_minor[4], c_minor[0] * 0.5, c_minor[2] * 0.5],  # G major (V)
                [c_minor[3], c_minor[5], c_minor[2]],  # F major (iv) variation
            ]
            
            # Initialize music pattern
            music_pattern = np.zeros(samples)
            
            # Create more sophisticated musical pattern
            for bar in range(16):
                bar_start = int(bar * samples / 16)
                bar_end = int((bar + 1) * samples / 16)
                
                # Use different chord every 4 bars
                chord_idx = (bar // 4) % len(chord_progressions)
                current_chord = chord_progressions[chord_idx]
                
                for i in range(bar_start, bar_end):
                    t = (i - bar_start) / sample_rate
                    global_t = i / sample_rate
                    
                    # Bass line - more rhythmic
                    bass_note = current_chord[0] / 2  # Lower octave
                    bass_intensity = 0.4 if (i % int(sample_rate * beat_duration)) < int(sample_rate * beat_duration * 0.8) else 0.1
                    bass = bass_intensity * np.sin(2 * np.pi * bass_note * global_t)
                    
                    # Melody line - more varied
                    melody_note = current_chord[(i // int(sample_rate * beat_duration * 2)) % len(current_chord)]
                    melody_intensity = 0.3 * (0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * global_t))  # Pulsing
                    melody = melody_intensity * np.sin(2 * np.pi * melody_note * global_t)
                    
                    # Arpeggio for movement
                    arp_note = current_chord[(i // int(sample_rate * beat_duration * 0.5)) % len(current_chord)] * 2
                    arp_intensity = 0.15 * (0.3 + 0.7 * np.sin(2 * np.pi * 2 * global_t))
                    arpeggio = arp_intensity * np.sin(2 * np.pi * arp_note * global_t)
                    
                    # Subtle percussion using noise
                    if i % int(sample_rate * beat_duration) < int(sample_rate * 0.05):
                        percussion = 0.2 * (np.random.random() - 0.5)
                    else:
                        percussion = 0
                    
                    # Combine all elements with better mixing
                    music_pattern[i] = bass + melody + arpeggio + percussion
                    
                    # Apply envelope to make it smoother
                    envelope = 1.0 - 0.3 * np.sin(2 * np.pi * global_t / total_duration)
                    music_pattern[i] *= envelope
            
            # Apply low-pass filter effect for smoother sound
            def smooth_signal(signal, window_size=5):
                smoothed = np.zeros_like(signal)
                for i in range(len(signal)):
                    start = max(0, i - window_size // 2)
                    end = min(len(signal), i + window_size // 2 + 1)
                    smoothed[i] = np.mean(signal[start:end])
                return smoothed
            
            music_pattern = smooth_signal(music_pattern)
            
            # Apply volume and convert to 16-bit
            music_pattern = (music_pattern * 32767 * BACKGROUND_MUSIC_VOLUME).astype(np.int16)
            
            # Create stereo with slight delay for depth
            stereo_music = np.column_stack([music_pattern, music_pattern])
            
            # Add slight stereo effect
            delay_samples = int(sample_rate * 0.01)  # 10ms delay
            if len(music_pattern) > delay_samples:
                stereo_music[delay_samples:, 1] += (music_pattern[:-delay_samples] * 0.1).astype(np.int16)
            
            # Convert to pygame sound
            music_sound = pygame.sndarray.make_sound(stereo_music)
            return music_sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create background music: {e}")
            return None
    
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
    
    def create_bomb_place_sound(self):
        """Create bomb placement sound effect"""
        if not self.enabled or not self.initialized:
            return None
            
        try:
            sample_rate = 22050
            duration = 300  # 0.3 seconds
            samples = int(sample_rate * duration / 1000)
            
            t = np.linspace(0, duration / 1000, samples, False)
            
            # Create a metallic click sound with high frequency
            base_freq = 800
            wave = np.sin(2 * np.pi * base_freq * t)
            wave += 0.5 * np.sin(2 * np.pi * base_freq * 2 * t)  # Second harmonic
            wave += 0.3 * np.sin(2 * np.pi * base_freq * 3 * t)  # Third harmonic
            
            # Apply sharp envelope
            envelope = np.exp(-t * 10)  # Quick decay
            wave *= envelope
            
            # Add some noise for metallic texture
            noise = 0.1 * (np.random.random(samples) - 0.5)
            wave += noise
            
            wave = (wave * 32767 * 0.4).astype(np.int16)  # Lower volume
            stereo_wave = np.column_stack([wave, wave])
            
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create bomb place sound: {e}")
            return None
    
    def create_bomb_explosion_sound(self):
        """Create bomb explosion sound effect"""
        if not self.enabled or not self.initialized:
            return None
            
        try:
            sample_rate = 22050
            duration = 800  # 0.8 seconds
            samples = int(sample_rate * duration / 1000)
            
            t = np.linspace(0, duration / 1000, samples, False)
            
            # Create explosion sound with multiple components
            explosion = np.zeros(samples)
            
            # Low frequency boom
            boom_freq = 60
            boom = 0.8 * np.sin(2 * np.pi * boom_freq * t)
            boom *= np.exp(-t * 3)  # Slow decay
            
            # Mid-range explosion noise
            noise_freq = 200
            noise = 0.6 * np.sin(2 * np.pi * noise_freq * t)
            noise *= np.exp(-t * 8)  # Medium decay
            
            # High frequency crackle
            crackle_freq = 1200
            crackle = 0.4 * np.sin(2 * np.pi * crackle_freq * t)
            crackle *= np.exp(-t * 15)  # Fast decay
            
            # Combine all components
            explosion = boom + noise + crackle
            
            # Add some random noise for realism
            random_noise = 0.2 * (np.random.random(samples) - 0.5)
            explosion += random_noise
            
            # Apply overall envelope
            envelope = np.exp(-t * 4)
            explosion *= envelope
            
            explosion = (explosion * 32767 * 0.6).astype(np.int16)
            stereo_explosion = np.column_stack([explosion, explosion])
            
            sound = pygame.sndarray.make_sound(stereo_explosion)
            return sound
            
        except Exception as e:
            print(f"❌ Warning: Could not create bomb explosion sound: {e}")
            return None

    def create_powerup_sound(self, powerup_type):
        """
        Create power-up collection sound effect
        Args:
            powerup_type: 'slow_potion', 'shield', or 'double_score'
        """
        if not self.enabled or not self.initialized:
            return None

        try:
            sample_rate = 22050
            note_duration = 150  # Each note 150ms

            # Define frequency sequences for each power-up type
            if powerup_type == 'slow_potion':
                # Descending scale (calming effect)
                frequencies = [600, 480, 360]
            elif powerup_type == 'shield':
                # Ascending scale (protective, rising effect)
                frequencies = [800, 960, 1200]
            elif powerup_type == 'double_score':
                # Flickering pattern (exciting)
                frequencies = [1000, 1500, 2000, 1500]
            else:
                frequencies = [440, 550, 660]

            # Create sound for each note
            total_samples = 0
            note_samples = []

            for freq in frequencies:
                samples = int(sample_rate * note_duration / 1000)
                t = np.linspace(0, note_duration / 1000, samples, False)

                # Generate tone with harmonics
                wave = np.sin(2 * np.pi * freq * t)
                wave += 0.3 * np.sin(2 * np.pi * freq * 2 * t)
                wave += 0.15 * np.sin(2 * np.pi * freq * 3 * t)

                # Simple ADSR envelope
                attack = int(samples * 0.1)
                decay = int(samples * 0.2)
                release = int(samples * 0.3)

                envelope = np.ones(samples)
                # Attack
                envelope[:attack] = np.linspace(0, 1, attack)
                # Release
                envelope[-release:] = np.linspace(1, 0, release)

                wave *= envelope
                note_samples.append(wave)
                total_samples += samples

            # Concatenate all notes
            full_wave = np.concatenate(note_samples)
            full_wave = (full_wave * 32767 * 0.4).astype(np.int16)
            stereo_wave = np.column_stack([full_wave, full_wave])

            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound

        except Exception as e:
            print(f"❌ Warning: Could not create power-up sound: {e}")
            return None

    def create_theme_switch_sound(self):
        """Create theme switching sound (C major arpeggio)"""
        if not self.enabled or not self.initialized:
            return None

        try:
            sample_rate = 22050
            note_duration = 80  # Quick 80ms per note

            # C major arpeggio: C-E-G-C
            frequencies = [261.63, 329.63, 392.00, 523.25]

            note_samples = []
            for freq in frequencies:
                samples = int(sample_rate * note_duration / 1000)
                t = np.linspace(0, note_duration / 1000, samples, False)

                # Bell-like tone
                wave = np.sin(2 * np.pi * freq * t)
                wave += 0.5 * np.sin(2 * np.pi * freq * 2 * t)

                # Quick envelope
                envelope = np.exp(-t * 12)
                wave *= envelope
                note_samples.append(wave)

            full_wave = np.concatenate(note_samples)
            full_wave = (full_wave * 32767 * 0.35).astype(np.int16)
            stereo_wave = np.column_stack([full_wave, full_wave])

            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound

        except Exception as e:
            print(f"❌ Warning: Could not create theme switch sound: {e}")
            return None

    def create_combo_sound(self, combo_level):
        """
        Create combo sound effect
        Args:
            combo_level: 2, 3, or 5+ for different levels
        """
        if not self.enabled or not self.initialized:
            return None

        try:
            sample_rate = 22050
            duration = 200  # 0.2 seconds
            samples = int(sample_rate * duration / 1000)
            t = np.linspace(0, duration / 1000, samples, False)

            # Higher pitch for higher combos
            if combo_level == 2:
                freq = 600
            elif combo_level == 3:
                freq = 800
            else:  # 5+
                freq = 1000

            # Generate tone with excitement (more harmonics)
            wave = np.sin(2 * np.pi * freq * t)
            wave += 0.4 * np.sin(2 * np.pi * freq * 2 * t)
            wave += 0.2 * np.sin(2 * np.pi * freq * 3 * t)

            # Pulsing envelope for excitement
            envelope = np.exp(-t * 8)
            pulse = 1 + 0.3 * np.sin(2 * np.pi * 10 * t)  # 10 Hz pulse
            wave *= envelope * pulse

            wave = (wave * 32767 * 0.4).astype(np.int16)
            stereo_wave = np.column_stack([wave, wave])

            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound

        except Exception as e:
            print(f"❌ Warning: Could not create combo sound: {e}")
            return None

    def create_shield_break_sound(self):
        """Create shield breaking sound (glass shatter effect)"""
        if not self.enabled or not self.initialized:
            return None

        try:
            sample_rate = 22050
            duration = 400  # 0.4 seconds
            samples = int(sample_rate * duration / 1000)
            t = np.linspace(0, duration / 1000, samples, False)

            # High frequency descending (breaking glass)
            start_freq = 2000
            end_freq = 400
            freq_sweep = start_freq + (end_freq - start_freq) * t / (duration / 1000)

            # Create sweep with noise
            wave = np.sin(2 * np.pi * freq_sweep * t)

            # Add high-frequency noise for "shatter" effect
            noise = 0.3 * (np.random.random(samples) - 0.5)
            wave += noise

            # Sharp attack, quick decay
            envelope = np.exp(-t * 10)
            wave *= envelope

            wave = (wave * 32767 * 0.5).astype(np.int16)
            stereo_wave = np.column_stack([wave, wave])

            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound

        except Exception as e:
            print(f"❌ Warning: Could not create shield break sound: {e}")
            return None

    def play_bomb_place_sound(self):
        """Play bomb placement sound effect"""
        if self.bomb_place_sound:
            self.bomb_place_sound.play()
            print("💣 Playing bomb place sound")
    
    def play_bomb_explosion_sound(self):
        """Play bomb explosion sound effect"""
        if self.bomb_explosion_sound:
            self.bomb_explosion_sound.play()
            print("💥 Playing bomb explosion sound")

    def play_powerup_sound(self, powerup_type):
        """
        Play power-up collection sound
        Args:
            powerup_type: 'slow_potion', 'shield', or 'double_score'
        """
        sound_map = {
            'slow_potion': self.powerup_slow_sound,
            'shield': self.powerup_shield_sound,
            'double_score': self.powerup_double_sound
        }

        sound = sound_map.get(powerup_type)
        if sound:
            sound.play()
            print(f"🎁 Playing {powerup_type} power-up sound")

    def play_theme_switch_sound(self):
        """Play theme switching sound effect"""
        if self.theme_switch_sound:
            self.theme_switch_sound.play()
            print("🎨 Playing theme switch sound")

    def play_combo_sound(self, combo_level):
        """
        Play combo sound effect
        Args:
            combo_level: 2, 3, or 5+ for different combo levels
        """
        if combo_level == 2 and self.combo_2x_sound:
            self.combo_2x_sound.play()
            print("🔥 Playing 2x combo sound")
        elif combo_level == 3 and self.combo_3x_sound:
            self.combo_3x_sound.play()
            print("🔥🔥 Playing 3x combo sound")
        elif combo_level >= 5 and self.combo_5x_sound:
            self.combo_5x_sound.play()
            print("🔥🔥🔥 Playing 5x+ combo sound")

    def play_shield_break_sound(self):
        """Play shield breaking sound effect"""
        if self.shield_break_sound:
            self.shield_break_sound.play()
            print("💔 Playing shield break sound")

    def start_background_music(self):
        """Start playing background music in loop"""
        if self.background_music and BACKGROUND_MUSIC_ENABLED and self.enabled:
            try:
                # Stop current music if playing
                if self.music_channel and self.music_channel.get_busy():
                    self.music_channel.stop()
                
                # Find an available channel for music
                self.music_channel = pygame.mixer.find_channel()
                if self.music_channel:
                    self.music_channel.play(self.background_music, loops=-1)  # Loop indefinitely
                    self.current_music = "game"
                    print("🎵 Game background music started")
                else:
                    print("⚠️  No available channel for background music")
            except Exception as e:
                print(f"❌ Warning: Could not start background music: {e}")
    
    def start_menu_music(self):
        """Start playing menu music"""
        if self.menu_music and BACKGROUND_MUSIC_ENABLED and self.enabled:
            try:
                # Stop current music if playing
                if self.music_channel:
                    self.music_channel.stop()
                
                # Find an available channel for music
                self.music_channel = pygame.mixer.find_channel()
                if self.music_channel:
                    self.music_channel.play(self.menu_music, loops=-1)  # Loop indefinitely
                    self.current_music = "menu"
                    print("🎵 Menu music started")
                else:
                    print("⚠️  No available channel for menu music")
            except Exception as e:
                print(f"❌ Warning: Could not start menu music: {e}")
    
    def start_game_over_music(self):
        """Start playing game over music"""
        if self.game_over_music and BACKGROUND_MUSIC_ENABLED and self.enabled:
            try:
                # Stop current music if playing
                if self.music_channel:
                    self.music_channel.stop()
                
                # Find an available channel for music
                self.music_channel = pygame.mixer.find_channel()
                if self.music_channel:
                    self.music_channel.play(self.game_over_music, loops=-1)  # Loop indefinitely
                    self.current_music = "game_over"
                    print("🎵 Game over music started")
                else:
                    print("⚠️  No available channel for game over music")
            except Exception as e:
                print(f"❌ Warning: Could not start game over music: {e}")
    
    def stop_background_music(self):
        """Stop background music"""
        if self.music_channel:
            try:
                self.music_channel.stop()
                self.music_channel = None
                print("🎵 Background music stopped")
            except Exception as e:
                print(f"❌ Warning: Could not stop background music: {e}")
    
    def toggle_background_music(self):
        """Toggle background music on/off"""
        global BACKGROUND_MUSIC_ENABLED
        BACKGROUND_MUSIC_ENABLED = not BACKGROUND_MUSIC_ENABLED
        
        if BACKGROUND_MUSIC_ENABLED:
            self.start_background_music()
            print("🎵 Background music enabled")
        else:
            self.stop_background_music()
            print("🎵 Background music disabled")
    
    def switch_music_style(self, style=None):
        """Switch between different music styles"""
        global BACKGROUND_MUSIC_STYLE
        
        if style is None:
            # Cycle through styles (now includes kids!)
            styles = ["retro_arcade", "chiptune", "ambient", "kids"]
            current_idx = styles.index(BACKGROUND_MUSIC_STYLE)
            BACKGROUND_MUSIC_STYLE = styles[(current_idx + 1) % len(styles)]
        else:
            BACKGROUND_MUSIC_STYLE = style

        # Update instance attribute
        self.current_music_style = BACKGROUND_MUSIC_STYLE

        # Stop current music
        self.stop_background_music()

        # Create new music for all phases based on style
        if BACKGROUND_MUSIC_STYLE == "chiptune":
            self.background_music = self.create_chiptune_background_music()
            self.menu_music = self.create_chiptune_menu_music()
            self.game_over_music = self.create_chiptune_game_over_music()
        elif BACKGROUND_MUSIC_STYLE == "ambient":
            self.background_music = self.create_ambient_background_music()
            self.menu_music = self.create_ambient_menu_music()
            self.game_over_music = self.create_ambient_game_over_music()
        elif BACKGROUND_MUSIC_STYLE == "kids":
            self.background_music = self.create_kids_background_music()
            self.menu_music = self.create_kids_menu_music()
            self.game_over_music = self.create_kids_game_over_music()
        else:
            self.background_music = self.create_retro_background_music()
            self.menu_music = self.create_retro_menu_music()
            self.game_over_music = self.create_retro_game_over_music()
        
        # Start appropriate music for current phase if enabled
        if BACKGROUND_MUSIC_ENABLED:
            if self.current_music == "menu":
                self.start_menu_music()
            elif self.current_music == "game":
                self.start_background_music()
            elif self.current_music == "game_over":
                self.start_game_over_music()
        
        print(f"🎵 Switched to {BACKGROUND_MUSIC_STYLE} style music")
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        print(f"🔊 Sound {status}")
        
    def stop_game_over_music(self):
        """Stop game over music"""
        if self.music_channel:
            try:
                self.music_channel.stop()
                self.music_channel = None
                print("🎵 Game over music stopped")
            except Exception as e:
                print(f"❌ Warning: Could not stop game over music: {e}")
    
    def cleanup(self):
        """Clean up sound resources"""
        if self.initialized:
            pygame.mixer.quit()
            print("🔊 Sound system cleaned up")