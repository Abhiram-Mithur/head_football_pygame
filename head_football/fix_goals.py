import pygame
import os
import sys
import random
import math
from config import *

# This is a patch to fix the goal positions in the main game
# It modifies the Goal class to maintain its position

# Monkey patch the Goal class to maintain its position
def apply_goal_fix():
    from main import Goal, ImageGoal
    
    # Store the original __init__ method
    original_goal_init = Goal.__init__
    
    # Create a new __init__ method that stores the initial position
    def new_goal_init(self, x, y, width, height, is_left=True):
        original_goal_init(self, x, y, width, height, is_left)
        # Store the initial position
        self.initial_y = y
    
    # Replace the original __init__ method
    Goal.__init__ = new_goal_init
    
    # Store the original reset_ball method
    from main import Game
    original_reset_ball = Game.reset_ball
    
    # Create a new reset_ball method that maintains goal positions
    def new_reset_ball(self):
        original_reset_ball(self)
        # Restore the goals to their initial positions
        if hasattr(self.left_goal, 'initial_y'):
            self.left_goal.y = self.left_goal.initial_y
            self.left_goal.rect.y = self.left_goal.initial_y
        if hasattr(self.right_goal, 'initial_y'):
            self.right_goal.y = self.right_goal.initial_y
            self.right_goal.rect.y = self.right_goal.initial_y
    
    # Replace the original reset_ball method
    Game.reset_ball = new_reset_ball
    
    print("Goal position fix applied!")

# Apply the fix when this module is imported
apply_goal_fix()
