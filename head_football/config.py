"""
Configuration settings for the Head Football game.
"""

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (135, 206, 235)

# Game settings
GRAVITY = 0.5
GROUND_HEIGHT = SCREEN_HEIGHT - 100  # Ground is 100px from bottom
GOAL_WIDTH = 100
GOAL_HEIGHT = 150
GAME_TIME = 90  # seconds
MAX_SCORE = 5

# Asset paths
ASSETS_DIR = "assets/"
PLAYERS_DIR = ASSETS_DIR + "players/"
UI_DIR = ASSETS_DIR + "ui/"
BALL_IMG = ASSETS_DIR + "ball.png"
BACKGROUND_IMG = ASSETS_DIR + "background.png"
GOAL_IMG = ASSETS_DIR + "goal.png"

# Use placeholder images if actual images don't exist
USE_PLACEHOLDER_GRAPHICS = False

# Player profiles
PLAYER_PROFILES = {
    "Speedy": {
        "speed": 8,
        "jump": 12,
        "power": 7,
        "control": 6,
        "color": (255, 50, 50),  # Bright Red
        "sprite": "speedy_player"
    },
    "Powerful": {
        "speed": 5,
        "jump": 10,
        "power": 12,
        "control": 8,
        "color": (50, 50, 255),  # Bright Blue
        "sprite": "powerful_player"
    },
    "Balanced": {
        "speed": 6,
        "jump": 11,
        "power": 9,
        "control": 9,
        "color": (50, 255, 50),  # Bright Green
        "sprite": "balanced_player"
    },
    "Technical": {
        "speed": 7,
        "jump": 9,
        "power": 8,
        "control": 12,
        "color": (255, 255, 50),  # Bright Yellow
        "sprite": "technical_player"
    },
    "Jumper": {
        "speed": 6,
        "jump": 14,
        "power": 8,
        "control": 7,
        "color": (255, 50, 255),  # Bright Purple
        "sprite": "jumper_player"
    }
}

# Difficulty settings
DIFFICULTY_SETTINGS = {
    "Easy": {
        "reaction_time": 2.0,  # seconds
        "accuracy": 0.4,  # percentage
        "speed_factor": 0.6,
        "jump_probability": 0.3
    },
    "Medium": {
        "reaction_time": 0.8,
        "accuracy": 0.8,
        "speed_factor": 0.9,
        "jump_probability": 0.7
    },
    "Hard": {
        "reaction_time": 0.3,
        "accuracy": 0.95,
        "speed_factor": 1.0,
        "jump_probability": 0.9
    }
}

# Game states
MENU = "menu"
PLAYER_SELECT = "player_select"
DIFFICULTY_SELECT = "difficulty_select"
PLAYING = "playing"
GAME_OVER = "game_over"
