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
        
        # Create background music for different game phases
        if BACKGROUND_MUSIC_STYLE == "chiptune":
            self.background_music = self.create_chiptune_background_music()
            self.menu_music = self.create_chiptune_menu_music()
            self.game_over_music = self.create_chiptune_game_over_music()
        elif BACKGROUND_MUSIC_STYLE == "ambient":
            self.background_music = self.create_ambient_background_music()
            self.menu_music = self.create_ambient_menu_music()
            self.game_over_music = self.create_ambient_game_over_music()
        else:
            self.background_music = self.create_retro_background_music()
            self.menu_music = self.create_retro_menu_music()
            self.game_over_music = self.create_retro_game_over_music()
        
        self.music_channel = None
        self.current_music = "menu"  # Track current music phase
        
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
    
    def start_background_music(self):
        """Start playing background music in loop"""
        if self.background_music and BACKGROUND_MUSIC_ENABLED and self.enabled:
            try:
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
            # Cycle through styles
            styles = ["retro_arcade", "chiptune", "ambient"]
            current_idx = styles.index(BACKGROUND_MUSIC_STYLE)
            BACKGROUND_MUSIC_STYLE = styles[(current_idx + 1) % len(styles)]
        else:
            BACKGROUND_MUSIC_STYLE = style
        
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