#!/usr/bin/env python3
"""
Test script for sound effects and background music
Tests all sound effects including the new background music
"""

import pygame
import sys
import time
from sound_manager import SoundManager
from config import *

def test_sound_effects():
    """Test all sound effects including background music"""
    print("🎵 Testing Sound Effects and Background Music")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("Sound Effects Test")
    
    # Create sound manager
    sound_manager = SoundManager()
    
    if not sound_manager.initialized:
        print("❌ Sound system not initialized!")
        return
    
    print("✅ Sound system initialized successfully!")
    print("")
    
    # Test different sound effects
    print("🔊 Testing individual sound effects:")
    
    print("1. Eating sound...")
    sound_manager.play_eat_sound()
    time.sleep(0.5)
    
    print("2. Crash sound...")
    sound_manager.play_crash_sound()
    time.sleep(0.8)
    
    print("3. Game over sound...")
    sound_manager.play_game_over_sound()
    time.sleep(1.0)
    
    print("4. Pause sound...")
    sound_manager.play_pause_sound()
    time.sleep(0.3)
    
    print("5. Speed up sound...")
    sound_manager.play_speed_up_sound()
    time.sleep(0.5)
    
    print("")
    print("🎵 Testing background music...")
    print("Background music will play for 10 seconds...")
    print("Press M to toggle music on/off")
    print("Press ESC to exit test")
    
    # Start background music
    sound_manager.start_background_music()
    
    # Main test loop
    clock = pygame.time.Clock()
    start_time = time.time()
    
    while time.time() - start_time < 10:  # Test for 10 seconds
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_manager.cleanup()
                pygame.quit()
                return
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    sound_manager.toggle_background_music()
                elif event.key == pygame.K_ESCAPE:
                    sound_manager.cleanup()
                    pygame.quit()
                    return
        
        # Display test info
        screen.fill((0, 0, 0))
        font = pygame.font.Font(None, 24)
        
        title_text = font.render("Sound Effects Test", True, (255, 255, 255))
        music_text = font.render(f"Music: {'ON' if BACKGROUND_MUSIC_ENABLED else 'OFF'}", True, (0, 255, 0))
        time_text = font.render(f"Time left: {10 - int(time.time() - start_time)}s", True, (255, 255, 0))
        control_text = font.render("Press M to toggle music, ESC to exit", True, (200, 200, 200))
        
        screen.blit(title_text, (20, 20))
        screen.blit(music_text, (20, 60))
        screen.blit(time_text, (20, 100))
        screen.blit(control_text, (20, 140))
        
        pygame.display.flip()
        clock.tick(30)
    
    # Cleanup
    print("\n🧹 Cleaning up sound resources...")
    sound_manager.cleanup()
    pygame.quit()
    print("✅ Sound test completed!")

if __name__ == "__main__":
    test_sound_effects()