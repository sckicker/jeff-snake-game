"""
Enhanced Snake Game Configuration File
All game parameters are defined here for easy modification and maintenance
"""

# Game window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GAME_TITLE = "Enhanced Snake Game"
BACKGROUND_COLOR = (15, 15, 25)  # Dark blue-black gradient background

# Game area settings
GRID_SIZE = 20  # Size of each grid cell (pixels)
GRID_WIDTH = 30  # Number of horizontal grid cells
GRID_HEIGHT = 25  # Number of vertical grid cells

# Snake settings - Enhanced with gradient colors
SNAKE_HEAD_COLOR = (0, 255, 100)  # Bright green for head
SNAKE_BODY_COLOR = (0, 200, 50)   # Darker green for body
SNAKE_INITIAL_LENGTH = 3  # Initial snake length
SNAKE_INITIAL_SPEED = 10  # Initial snake speed (frame rate)

# Food settings - Enhanced with glowing effect
FOOD_COLOR = (255, 100, 100)  # Bright red with orange tint
FOOD_GLOW_COLOR = (255, 200, 0)  # Yellow glow
FOOD_SIZE = 20  # Food size

# Game speed settings
SPEED_INCREMENT = 2  # Speed increase per food eaten
MAX_SPEED = 30  # Maximum speed limit

# Score settings
SCORE_PER_FOOD = 10  # Points per food item

# Enhanced color definitions
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (120, 120, 120)
GOLD = (255, 215, 0)
PURPLE = (147, 0, 211)
CYAN = (0, 255, 255)

# Visual effects
GRID_ALPHA = 30  # Grid line transparency
SNAKE_ALPHA = 200  # Snake transparency
FOOD_PULSE_SPEED = 5  # Food pulsing animation speed

# Sound effects configuration
SOUND_ENABLED = True  # Enable/disable sound effects
EAT_SOUND_FREQ = 800  # Frequency for eating sound (Hz)
EAT_SOUND_DURATION = 100  # Duration for eating sound (ms)
CRASH_SOUND_FREQ = 200  # Frequency for crash sound (Hz)
CRASH_SOUND_DURATION = 300  # Duration for crash sound (ms)
GAME_OVER_SOUND_FREQ = 150  # Frequency for game over sound (Hz)
GAME_OVER_SOUND_DURATION = 500  # Duration for game over sound (ms)
PAUSE_SOUND_FREQ = 600  # Frequency for pause sound (Hz)
PAUSE_SOUND_DURATION = 50  # Duration for pause sound (ms)
SPEED_UP_SOUND_FREQ = 1000  # Frequency for speed up sound (Hz)
SPEED_UP_SOUND_DURATION = 80  # Duration for speed up sound (ms)

# Game states
GAME_OVER = "game_over"
GAME_RUNNING = "game_running"
GAME_PAUSED = "game_paused"