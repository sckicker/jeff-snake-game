#!/usr/bin/env python3
"""
Test script for different music styles
Tests retro arcade, chiptune, and ambient music styles
"""

import pygame
import sys
import time
from sound_manager import SoundManager
from config import *

def test_music_styles():
    """Test all music styles"""
    print("🎵 Testing Different Music Styles")
    print("=" * 50)
    
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Music Styles Test")
    
    # Create sound manager
    sound_manager = SoundManager()
    
    if not sound_manager.initialized:
        print("❌ Sound system not initialized!")
        return
    
    print("✅ Sound system initialized successfully!")
    print("")
    
    # Test different music styles
    styles = ["retro_arcade", "chiptune", "ambient"]
    current_style = 0
    
    print("🎶 Available music styles:")
    print("1️⃣  Retro Arcade - Professional retro game music")
    print("2️⃣  Chiptune - Classic 8-bit style music")
    print("3️⃣  Ambient - Calming background atmosphere")
    print("")
    print("Controls:")
    print("🎵 SPACE - Start/stop music")
    print("➡️  RIGHT - Next music style")
    print("⬅️  LEFT - Previous music style")
    print("❌ ESC - Exit test")
    print("")
    
    clock = pygame.time.Clock()
    running = True
    music_playing = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if music_playing:
                        sound_manager.stop_background_music()
                        music_playing = False
                    else:
                        sound_manager.start_background_music()
                        music_playing = True
                elif event.key == pygame.K_RIGHT:
                    current_style = (current_style + 1) % len(styles)
                    sound_manager.switch_music_style(styles[current_style])
                    music_playing = BACKGROUND_MUSIC_ENABLED
                elif event.key == pygame.K_LEFT:
                    current_style = (current_style - 1) % len(styles)
                    sound_manager.switch_music_style(styles[current_style])
                    music_playing = BACKGROUND_MUSIC_ENABLED
        
        # Display test info
        screen.fill((20, 20, 40))
        font = pygame.font.Font(None, 32)
        small_font = pygame.font.Font(None, 24)
        
        title_text = font.render("Music Styles Test", True, (255, 255, 255))
        current_text = font.render(f"Current: {styles[current_style].replace('_', ' ').title()}", True, (0, 255, 100))
        status_text = font.render(f"Status: {'Playing' if music_playing else 'Stopped'}", True, (255, 255, 0))
        
        controls = [
            "SPACE: Start/Stop music",
            "RIGHT/LEFT: Switch styles",
            "ESC: Exit test"
        ]
        
        screen.blit(title_text, (50, 50))
        screen.blit(current_text, (50, 100))
        screen.blit(status_text, (50, 150))
        
        y = 220
        for control in controls:
            control_text = small_font.render(control, True, (200, 200, 200))
            screen.blit(control_text, (50, y))
            y += 35
        
        # Draw style indicators
        x_start = 50
        y_start = 320
        for i, style in enumerate(styles):
            color = (255, 255, 255) if i == current_style else (100, 100, 100)
            style_text = small_font.render(f"{i+1}", True, color)
            screen.blit(style_text, (x_start + i * 40, y_start))
            
            # Draw circle for current style
            if i == current_style:
                pygame.draw.circle(screen, (0, 255, 100), (x_start + i * 40 + 12, y_start + 30), 8, 2)
        
        pygame.display.flip()
        clock.tick(30)
    
    # Cleanup
    print("\n🧹 Cleaning up sound resources...")
    sound_manager.cleanup()
    pygame.quit()
    print("✅ Music styles test completed!")

if __name__ == "__main__":
    test_music_styles()