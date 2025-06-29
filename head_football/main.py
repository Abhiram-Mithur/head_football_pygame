"""
Main game file for Head Football.
"""
import pygame
import os
import sys
import random
import math
from config import *
from player import Player
from ai import AIOpponent
from ball import Ball
from ui import UI

# Initialize pygame
pygame.init()
pygame.display.set_caption("Head Football")

class Goal(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, is_left=True):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_left = is_left
        
        # Create a simple rectangle for the goal
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (255, 255, 255, 100), (0, 0, width, height), 2)
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class ImageGoal(Goal):
    def __init__(self, x, y, width, height, image, is_left=True):
        super().__init__(x, y, width, height, is_left)
        
        # Use the provided image
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = MENU
        
        # Load background assets
        self.stadium_bg = None
        self.field_bg = None
        self.goal_left_img = None
        self.goal_right_img = None
        self.load_background_assets()
        
        # Fallback background if assets couldn't be loaded
        if not self.stadium_bg:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill(SKY_BLUE)
            # Draw ground
            pygame.draw.rect(self.background, GREEN, (0, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_HEIGHT))
        
        # Game objects
        self.player = None
        self.ai_opponent = None
        self.ball = None
        self.left_goal = None
        self.right_goal = None
        
        # Game state variables
        self.player_score = 0
        self.ai_score = 0
        self.game_time = GAME_TIME
        self.start_time = 0
        
        # Goal cooldown to prevent multiple goals
        self.goal_cooldown = 0
        
        # UI
        self.ui = UI()
        
        # Selected options
        self.selected_player = "Balanced"
        self.selected_difficulty = "Medium"
    
    def load_background_assets(self):
        """Load background assets if they exist"""
        try:
            # Load stadium background
            if os.path.exists("assets/background/stadium.png"):
                self.stadium_bg = pygame.image.load("assets/background/stadium.png").convert_alpha()
                self.stadium_bg = pygame.transform.scale(self.stadium_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
                print("Loaded stadium background")
            
            # Load field
            if os.path.exists("assets/background/field.png"):
                self.field_bg = pygame.image.load("assets/background/field.png").convert_alpha()
                self.field_bg = pygame.transform.scale(self.field_bg, (SCREEN_WIDTH, 200))
                print("Loaded field background")
            
            # Load goal posts
            if os.path.exists("assets/background/goal_left.png"):
                self.goal_left_img = pygame.image.load("assets/background/goal_left.png").convert_alpha()
                self.goal_left_img = pygame.transform.scale(self.goal_left_img, (GOAL_WIDTH, GOAL_HEIGHT))
                print("Loaded left goal image")
            
            if os.path.exists("assets/background/goal_right.png"):
                self.goal_right_img = pygame.image.load("assets/background/goal_right.png").convert_alpha()
                self.goal_right_img = pygame.transform.scale(self.goal_right_img, (GOAL_WIDTH, GOAL_HEIGHT))
                print("Loaded right goal image")
        except Exception as e:
            print(f"Error loading background assets: {e}")
            self.stadium_bg = None
            self.field_bg = None
            self.goal_left_img = None
            self.goal_right_img = None
    
    def fix_goal_positions(self):
        """Ensure goals are at the correct fixed position"""
        # Calculate the correct goal position
        field_height = 200  # Height of the field surface
        goal_area_height = 80  # Match the goal area height from field markings
        field_y = GROUND_HEIGHT - 100
        
        # Calculate goal area position - position it higher in the field
        # Move it up by 30 pixels from the center
        goal_area_y = field_y + (field_height - goal_area_height) // 2 - 30
        
        # Force goals to this position
        if hasattr(self, 'left_goal') and hasattr(self, 'right_goal'):
            self.left_goal.y = goal_area_y
            self.left_goal.rect.y = goal_area_y
            
            self.right_goal.y = goal_area_y
            self.right_goal.rect.y = goal_area_y
            
        # Store this position for future reference
        self.goal_area_y = goal_area_y
    
    def setup_game(self):
        # Create player
        player_profile = PLAYER_PROFILES[self.selected_player]
        self.player = Player(SCREEN_WIDTH // 4, GROUND_HEIGHT - 100, player_profile, is_player=True)
        
        # Create AI opponent with different color than player
        # Get all available profiles
        available_profiles = list(PLAYER_PROFILES.values())
        
        # Filter out profiles with the same color as the player
        different_color_profiles = [profile for profile in available_profiles 
                                   if profile["color"] != player_profile["color"]]
        
        # If all profiles have the same color (unlikely), modify one slightly
        if not different_color_profiles:
            ai_profile = random.choice(available_profiles)
            # Modify the color slightly to make it different
            r, g, b = ai_profile["color"]
            ai_profile = ai_profile.copy()  # Create a copy to avoid modifying the original
            ai_profile["color"] = ((r + 100) % 256, (g + 100) % 256, (b + 100) % 256)
        else:
            ai_profile = random.choice(different_color_profiles)
        
        self.ai_opponent = AIOpponent(3 * SCREEN_WIDTH // 4, GROUND_HEIGHT - 100, ai_profile, 
                             difficulty=DIFFICULTY_SETTINGS[self.selected_difficulty])
        
        # Create ball
        self.ball = Ball(SCREEN_WIDTH // 2, GROUND_HEIGHT - 200)
        
        # Create goals
        goal_y = GROUND_HEIGHT - GOAL_HEIGHT - 30  # Position goals 30 pixels higher
        if self.goal_left_img and self.goal_right_img:
            self.left_goal = ImageGoal(0, goal_y, GOAL_WIDTH, GOAL_HEIGHT, self.goal_left_img, is_left=True)
            self.right_goal = ImageGoal(SCREEN_WIDTH - GOAL_WIDTH, goal_y, GOAL_WIDTH, GOAL_HEIGHT, self.goal_right_img, is_left=False)
            print("Using image goals")
        else:
            self.left_goal = Goal(0, goal_y, GOAL_WIDTH, GOAL_HEIGHT, is_left=True)
            self.right_goal = Goal(SCREEN_WIDTH - GOAL_WIDTH, goal_y, GOAL_WIDTH, GOAL_HEIGHT, is_left=False)
            print("Using placeholder goals")
        
        # Fix goal positions to ensure they're at the correct position
        self.fix_goal_positions()
        
        # Reset scores and time
        self.player_score = 0
        self.ai_score = 0
        self.game_time = GAME_TIME
        self.start_time = pygame.time.get_ticks()
        
        # Reset goal cooldown
        self.goal_cooldown = 0
        
        # Change state to playing
        self.state = PLAYING
    
    def reset_ball(self):
        """Reset the ball to the center of the field"""
        self.ball.reset(SCREEN_WIDTH // 2, GROUND_HEIGHT - 200)
        
        # Fix goal positions to ensure they don't move
        self.fix_goal_positions()
    
    def check_goal(self):
        """Check if a goal has been scored"""
        # Skip goal check if on cooldown
        if self.goal_cooldown > 0:
            return False
            
        # Left goal (AI scores)
        if self.ball.x < GOAL_WIDTH and self.ball.y > self.left_goal.y and self.ball.y < self.left_goal.y + GOAL_HEIGHT:
            # Increment score by exactly 1
            self.ai_score += 1
            print(f"AI GOAL! Score: {self.player_score}-{self.ai_score}")
            
            # Create goal celebration effect
            self.create_goal_celebration(is_left_goal=True)
            
            # Set a flag to reset positions after celebration
            self.reset_pending = True
            self.reset_timer = 60  # Reset after 60 frames (1 second at 60 FPS)
            
            # Set goal cooldown to prevent multiple goals
            self.goal_cooldown = 120  # 2 seconds at 60 FPS
            
            return True
        
        # Right goal (Player scores)
        if self.ball.x > SCREEN_WIDTH - GOAL_WIDTH and self.ball.y > self.right_goal.y and self.ball.y < self.right_goal.y + GOAL_HEIGHT:
            # Increment score by exactly 1
            self.player_score += 1
            print(f"PLAYER GOAL! Score: {self.player_score}-{self.ai_score}")
            
            # Create goal celebration effect
            self.create_goal_celebration(is_left_goal=False)
            
            # Set a flag to reset positions after celebration
            self.reset_pending = True
            self.reset_timer = 60  # Reset after 60 frames (1 second at 60 FPS)
            
            # Set goal cooldown to prevent multiple goals
            self.goal_cooldown = 120  # 2 seconds at 60 FPS
            
            return True
        
        return False
        
    def create_goal_celebration(self, is_left_goal):
        """Create celebration effects at the goal"""
        # Create confetti particles
        self.goal_particles = []
        
        # Determine which goal to create particles for
        if is_left_goal:
            goal_x = GOAL_WIDTH // 2
        else:
            goal_x = SCREEN_WIDTH - GOAL_WIDTH // 2
            
        goal_y = self.left_goal.y + GOAL_HEIGHT // 2
        
        # Create 100 particles
        for _ in range(100):
            # Random position near the goal
            x = goal_x + random.randint(-GOAL_WIDTH, GOAL_WIDTH)
            y = goal_y + random.randint(-GOAL_HEIGHT//2, GOAL_HEIGHT//2)
            
            # Random velocity
            vel_x = random.uniform(-5, 5)
            vel_y = random.uniform(-8, -2)  # Upward velocity
            
            # Random color
            color = (
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            )
            
            # Random size
            size = random.randint(3, 8)
            
            # Random lifetime
            lifetime = random.randint(30, 60)  # frames
            
            # Add particle
            self.goal_particles.append({
                'x': x,
                'y': y,
                'vel_x': vel_x,
                'vel_y': vel_y,
                'color': color,
                'size': size,
                'lifetime': lifetime
            })
            
        # Set celebration time
        self.celebration_time = 60  # 1 second at 60 FPS
        
    def update_goal_celebration(self):
        """Update goal celebration particles"""
        if hasattr(self, 'celebration_time') and self.celebration_time > 0:
            self.celebration_time -= 1
            
            # Update particles
            for particle in self.goal_particles[:]:
                # Apply gravity
                particle['vel_y'] += 0.2
                
                # Update position
                particle['x'] += particle['vel_x']
                particle['y'] += particle['vel_y']
                
                # Decrease lifetime
                particle['lifetime'] -= 1
                
                # Remove if lifetime is over
                if particle['lifetime'] <= 0:
                    self.goal_particles.remove(particle)
                    
    def draw_goal_celebration(self):
        """Draw goal celebration particles"""
        if hasattr(self, 'goal_particles'):
            for particle in self.goal_particles:
                pygame.draw.rect(
                    self.screen, 
                    particle['color'], 
                    (particle['x'], particle['y'], particle['size'], particle['size'])
                )
        
    def reset_after_goal(self):
        """Reset ball and players after a goal"""
        # Reset ball to center
        self.ball.reset(SCREEN_WIDTH // 2, GROUND_HEIGHT - 200)
        
        # Reset players to their initial positions
        self.player.reset_position()
        self.ai_opponent.reset_position()
        
        # Fix goal positions to ensure they don't move
        self.fix_goal_positions()
    
    def update(self):
        """Update game state"""
        if self.state == PLAYING:
            # Update goal cooldown
            if self.goal_cooldown > 0:
                self.goal_cooldown -= 1
                
            # Handle reset after goal celebration
            if hasattr(self, 'reset_pending') and self.reset_pending:
                self.reset_timer -= 1
                if self.reset_timer <= 0:
                    self.reset_after_goal()
                    self.reset_pending = False
            
            # Update player
            keys = pygame.key.get_pressed()
            
            # Only move when keys are pressed (not continuous)
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            elif keys[pygame.K_RIGHT]:
                self.player.move_right()
            else:
                self.player.stop()
                
            if keys[pygame.K_SPACE]:
                self.player.jump()
            if keys[pygame.K_UP]:
                if self.player.head():
                    # Check for collision with the ball when heading
                    self.ball.check_player_collision(self.player)
            
            # Update AI
            self.ai_opponent.update(self.ball)
            
            # Check for collision with the ball for AI
            self.ball.check_player_collision(self.ai_opponent)
            
            # Update ball
            self.ball.update()
            
            # Update player
            self.player.update()
            
            # Always check for collision with human player (makes it much easier to hit the ball)
            self.ball.check_player_collision(self.player)
            
            # Check for goals
            self.check_goal()
            
            # Update goal celebration if active
            if hasattr(self, 'celebration_time') and self.celebration_time > 0:
                self.update_goal_celebration()
            
            # Only fix goal positions if they've moved from the expected position
            if hasattr(self, 'goal_area_y'):
                if (self.left_goal.y != self.goal_area_y or 
                    self.left_goal.rect.y != self.goal_area_y or
                    self.right_goal.y != self.goal_area_y or
                    self.right_goal.rect.y != self.goal_area_y):
                    self.fix_goal_positions()
            
            # Update game time
            elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
            self.game_time = max(0, GAME_TIME - elapsed)
            
            # Check for game over
            if self.game_time <= 0 or self.player_score >= MAX_SCORE or self.ai_score >= MAX_SCORE:
                self.state = GAME_OVER
    
    def render(self):
        """Render the game"""
        # Draw background
        if self.stadium_bg:
            self.screen.blit(self.stadium_bg, (0, 0))
        else:
            self.screen.blit(self.background, (0, 0))
        
        # Draw field
        if self.field_bg:
            self.screen.blit(self.field_bg, (0, GROUND_HEIGHT - 100))
        
        if self.state == MENU:
            self.ui.draw_menu(self.screen)
            # Draw credits only in menu
            self.draw_credits()
        elif self.state == PLAYER_SELECT:
            self.ui.draw_player_select(self.screen)
            # Draw credits in selection screens
            self.draw_credits()
        elif self.state == DIFFICULTY_SELECT:
            self.ui.draw_difficulty_select(self.screen)
            # Draw credits in selection screens
            self.draw_credits()
        elif self.state == PLAYING:
            # Draw goals
            self.screen.blit(self.left_goal.image, (self.left_goal.x, self.left_goal.y))
            self.screen.blit(self.right_goal.image, (self.right_goal.x, self.right_goal.y))
            
            # Draw players
            self.player.draw(self.screen)
            self.ai_opponent.draw(self.screen)
            
            # Draw ball
            self.ball.draw(self.screen)
            
            # Draw goal celebration if active
            if hasattr(self, 'celebration_time') and self.celebration_time > 0:
                self.draw_goal_celebration()
            
            # Draw UI elements
            self.ui.draw_game_hud(self.screen, self.player_score, self.ai_score, self.game_time)
        elif self.state == GAME_OVER:
            self.ui.draw_game_over(self.screen, self.player_score, self.ai_score)
            # Draw credits in game over screen
            self.draw_credits()
        
        pygame.display.flip()
    
    def draw_credits(self):
        """Draw credits at the bottom of the screen"""
        # Create a semi-transparent background for the credits
        footer_height = 25
        footer_y = SCREEN_HEIGHT - footer_height
        
        # Create a semi-transparent surface
        footer_surface = pygame.Surface((SCREEN_WIDTH, footer_height), pygame.SRCALPHA)
        footer_surface.fill((0, 0, 0, 150))  # Black with 60% opacity
        
        # Add text
        font = pygame.font.SysFont('Arial', 16)
        credits_text = font.render("Made with ❤️ by Abhiram Mithur", True, (255, 255, 255))
        
        # Position text in the center of the footer
        text_x = (SCREEN_WIDTH - credits_text.get_width()) // 2
        text_y = footer_y + (footer_height - credits_text.get_height()) // 2
        
        # Blit footer and text
        self.screen.blit(footer_surface, (0, footer_y))
        self.screen.blit(credits_text, (text_x, text_y))
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Handle menu navigation
            if self.state == MENU:
                button_index = self.ui.handle_menu_events(event)
                if button_index == 0:  # Play Game button
                    self.state = PLAYER_SELECT
            elif self.state == PLAYER_SELECT:
                result = self.ui.handle_player_select_events(event)
                if result == "continue" and self.ui.selected_player:
                    self.selected_player = self.ui.selected_player
                    self.state = DIFFICULTY_SELECT
            elif self.state == DIFFICULTY_SELECT:
                result = self.ui.handle_difficulty_select_events(event)
                if result == "start" and self.ui.selected_difficulty:
                    self.selected_difficulty = self.ui.selected_difficulty
                    self.setup_game()
                elif result == "back":
                    self.state = PLAYER_SELECT
            elif self.state == GAME_OVER:
                result = self.ui.handle_game_over_events(event)
                if result == 1:  # Main Menu button (index 1)
                    self.state = MENU
                elif result == 0:  # Play Again button (index 0)
                    self.setup_game()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
