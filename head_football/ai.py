"""
AI opponent for the Head Football game.
"""
import random
import pygame
from player import Player
from config import SCREEN_WIDTH

class AIOpponent(Player):
    def __init__(self, x, y, profile, difficulty):
        super().__init__(x, y, profile, is_player=False)
        self.difficulty = difficulty
        self.reaction_time = difficulty["reaction_time"] * 60  # convert to frames
        self.accuracy = difficulty["accuracy"]
        self.speed_factor = difficulty["speed_factor"]
        self.jump_probability = difficulty["jump_probability"]
        
        # Adjust speed based on difficulty
        self.speed *= self.speed_factor
        
        # AI state
        self.target_x = x
        self.decision_timer = 0
        self.last_ball_pos = None
        
        # Debug info
        print(f"AI initialized with difficulty: {self.difficulty}")
        print(f"Reaction time: {self.reaction_time/60} seconds")
        print(f"Accuracy: {self.accuracy}")
        print(f"Speed factor: {self.speed_factor}")
        print(f"Jump probability: {self.jump_probability}")
        
    def decide_action(self, ball):
        """Decide what action to take based on ball position"""
        # Only make decisions after reaction time has passed
        if self.decision_timer > 0:
            self.decision_timer -= 1
            return
            
        # Store current ball position
        current_ball_pos = (ball.x, ball.y)
        
        # Reset decision timer
        self.decision_timer = int(self.reaction_time * random.uniform(0.8, 1.2))
        
        # Calculate where to move
        ball_x = ball.x
        
        # Add inaccuracy based on difficulty
        if random.random() > self.accuracy:
            # Add random offset to target position
            ball_x += random.randint(-100, 100)
            
        # Constrain to screen bounds
        ball_x = max(0, min(ball_x, SCREEN_WIDTH - self.width))
        
        # Set target x position
        self.target_x = ball_x
        
        # Decide whether to jump
        if (ball.y < self.y and  # Ball is above AI
            abs(ball.x - self.x) < 100 and  # Ball is close horizontally
            random.random() < self.jump_probability):  # Random chance based on difficulty
            self.jump()
            print("AI decided to jump")
            
        # Decide whether to head
        if (abs(ball.x - (self.x + self.width/2)) < 50 and  # Ball is close horizontally
            abs(ball.y - (self.y + 15)) < 50 and  # Ball is close to head
            random.random() < self.accuracy):  # Random chance based on difficulty
            if self.head():
                print("AI attempting to head the ball")
            
        # Update last ball position
        self.last_ball_pos = current_ball_pos
        
    def update(self, ball):
        # Decide action based on ball position
        self.decide_action(ball)
        
        # Move towards target position
        if self.x + self.width/2 < self.target_x - 10:
            self.move_right()
        elif self.x + self.width/2 > self.target_x + 10:
            self.move_left()
        else:
            self.stop()
            
        # Call parent update method
        super().update()
