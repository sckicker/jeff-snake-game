"""
Sound Test Program for Enhanced Snake Game
Test if sound effects are working properly
"""

import pygame
import numpy as np
import time

def test_sound_system():
    """Test the sound system"""
    print("🎵 Testing Snake Game Sound System...")
    
    try:
        # Initialize pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
        print("✅ Pygame mixer initialized successfully!")
        
        # Test different frequencies
        test_frequencies = [800, 200, 150, 600, 1000]  # eat, crash, game_over, pause, speed_up
        test_durations = [100, 300, 500, 50, 80]
        test_names = ["Eat Food", "Collision", "Game Over", "Pause", "Speed Up"]
        
        for freq, duration, name in zip(test_frequencies, test_durations, test_names):
            print(f"🔊 Testing {name} sound ({freq}Hz, {duration}ms)...")
            
            # Generate sound
            sample_rate = 22050
            samples = int(sample_rate * duration / 1000)
            t = np.linspace(0, duration / 1000, samples, False)
            
            # Create wave with harmonics
            wave = np.sin(2 * np.pi * freq * t)
            wave += 0.3 * np.sin(2 * np.pi * freq * 2 * t)
            wave += 0.1 * np.sin(2 * np.pi * freq * 3 * t)
            
            # Apply envelope
            envelope = np.exp(-t * 5)
            wave *= envelope
            
            # Convert to 16-bit integers
            wave = (wave * 32767 * 0.3).astype(np.int16)
            stereo_wave = np.column_stack([wave, wave])
            
            # Create and play sound
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
            
            # Wait for sound to finish
            time.sleep(duration / 1000 + 0.1)
            
        print("✅ All sound tests completed successfully!")
        
        # Test volume control
        print("🔊 Testing volume control...")
        freq = 440  # A4 note
        duration = 500
        
        for volume in [0.1, 0.3, 0.5, 0.8]:
            print(f"Playing at {volume*100}% volume...")
            sample_rate = 22050
            samples = int(sample_rate * duration / 1000)
            t = np.linspace(0, duration / 1000, samples, False)
            wave = np.sin(2 * np.pi * freq * t)
            wave = (wave * 32767 * volume).astype(np.int16)
            stereo_wave = np.column_stack([wave, wave])
            sound = pygame.sndarray.make_sound(stereo_wave)
            sound.play()
            time.sleep(duration / 1000 + 0.1)
        
        pygame.mixer.quit()
        print("✅ Sound system test completed!")
        
    except Exception as e:
        print(f"❌ Sound test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sound_system()