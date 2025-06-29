"""
Player class for the Head Football game.
"""
import pygame
import os
from config import GRAVITY, GROUND_HEIGHT, SCREEN_WIDTH, USE_PLACEHOLDER_GRAPHICS, PLAYERS_DIR

class Player:
    def __init__(self, x, y, profile, is_player=True):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 100
        self.profile = profile
        self.is_player = is_player
        
        # Extract profile attributes
        self.speed = profile["speed"]
        self.jump_power = profile["jump"]
        self.heading_power = profile["power"]
        self.control = profile["control"]
        self.color = profile["color"]
        self.sprite_name = profile.get("sprite", None)
        
        # Store initial position for reset
        self.initial_x = x
        self.initial_y = y
        
        # Load sprite if available
        self.sprite = None
        self.head_sprite = None
        if not USE_PLACEHOLDER_GRAPHICS and self.sprite_name:
            sprite_path = os.path.join(PLAYERS_DIR, f"{self.sprite_name}.png")
            head_path = os.path.join(PLAYERS_DIR, f"{self.sprite_name}_head.png")
            try:
                if os.path.exists(sprite_path):
                    self.sprite = pygame.image.load(sprite_path)
                    self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
                if os.path.exists(head_path):
                    self.head_sprite = pygame.image.load(head_path)
                    self.head_sprite = pygame.transform.scale(self.head_sprite, (30, 30))
            except pygame.error:
                print(f"Could not load sprite: {sprite_path}")
                self.sprite = None
                self.head_sprite = None
        
        # Physics
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.is_heading = False
        self.heading_cooldown = 0
        
        # Celebration state
        self.is_celebrating = False
        self.celebration_frames = 0
        self.celebration_jump_count = 0
        
        # Create a simple rectangle for collision detection
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
    def move_left(self):
        self.vel_x = -self.speed
        
    def move_right(self):
        self.vel_x = self.speed
        
    def stop(self):
        self.vel_x = 0
        
    def jump(self):
        if not self.is_jumping:
            self.vel_y = -self.jump_power
            self.is_jumping = True
            
    def head(self):
        if self.heading_cooldown <= 0:
            self.is_heading = True
            
            # Different cooldown for human vs AI
            if self.is_player:
                self.heading_cooldown = 15  # Increased cooldown for human player
                self.heading_frames = 8  # Keep heading state active for 8 frames
            else:
                self.heading_cooldown = 15  # Normal cooldown for AI
                self.heading_frames = 5  # Keep heading state active for 5 frames
                
            print(f"{'Player' if self.is_player else 'AI'} attempting to head the ball")
            
            # Add a small upward boost when heading to help reach the ball
            if self.is_player:  # More powerful boost for human player
                if self.is_jumping:
                    self.vel_y -= 2  # Reduced boost when already jumping
                else:
                    self.vel_y -= 4  # Reduced boost when on ground
                    self.is_jumping = True  # Consider this a mini-jump
            else:  # Normal boost for AI
                if self.is_jumping:
                    self.vel_y -= 1.5  # Small boost when already jumping
                else:
                    self.vel_y -= 3  # Reduced boost when on ground
                    self.is_jumping = True  # Consider this a mini-jump
            return True
        return False
            
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Boundary checks
        if self.x < 0:
            self.x = 0
        elif self.x > SCREEN_WIDTH - self.width:
            self.x = SCREEN_WIDTH - self.width
            
        # Ground collision
        if self.y > GROUND_HEIGHT - self.height:
            self.y = GROUND_HEIGHT - self.height
            self.vel_y = 0
            self.is_jumping = False
            
        # Update heading state
        if self.is_heading:
            # For both human player and AI, use heading_frames
            if hasattr(self, 'heading_frames'):
                self.heading_frames -= 1
                if self.heading_frames <= 0:
                    self.is_heading = False
                    self.heading_frames = 0
            else:
                # Fallback in case heading_frames is not set
                self.heading_frames = 0
                self.is_heading = False
            
        # Update cooldown
        if self.heading_cooldown > 0:
            self.heading_cooldown -= 1
            
        # Update celebration if celebrating
        if self.is_celebrating:
            self.update_celebration()
            
        # Update rectangle position
        self.rect.x = self.x
        self.rect.y = self.y
        
    def reset_position(self):
        """Reset player to initial position"""
        self.x = self.initial_x
        self.y = self.initial_y
        self.vel_x = 0
        self.vel_y = 0
        self.is_jumping = False
        self.is_heading = False
        self.is_celebrating = False
        
    def draw(self, screen):
        if self.sprite:
            # Draw player sprite
            # Add shadow beneath player for better grounding effect
            shadow_radius = self.width // 3
            shadow_y = GROUND_HEIGHT - 5  # Just above the ground
            shadow_x = self.x + self.width // 2
            
            # Draw oval shadow with transparency
            shadow_surface = pygame.Surface((shadow_radius * 2, shadow_radius), pygame.SRCALPHA)
            pygame.draw.ellipse(shadow_surface, (0, 0, 0, 80), (0, 0, shadow_radius * 2, shadow_radius))
            screen.blit(shadow_surface, (shadow_x - shadow_radius, shadow_y - shadow_radius // 2))
            
            # Draw player sprite (but not the head part if heading)
            if self.is_heading and self.head_sprite:
                # If we're heading and have a head sprite, we'll draw it separately
                # For now, just draw the body sprite
                screen.blit(self.sprite, (self.x, self.y))
                
                # Draw the separate head sprite above the body
                head_x = self.x + self.width // 2 - 15  # Center the head
                head_y = self.y - 15  # Position above body
                screen.blit(self.head_sprite, (head_x, head_y))
            else:
                # Just draw the normal sprite which includes the head
                screen.blit(self.sprite, (self.x, self.y))
        else:
            # Draw shadow beneath player
            shadow_radius = 15
            shadow_y = GROUND_HEIGHT - 5
            shadow_x = self.x + self.width // 2
            pygame.draw.ellipse(screen, (0, 0, 0, 80), (shadow_x - shadow_radius, shadow_y - shadow_radius // 2, shadow_radius * 2, shadow_radius))
            
            # Draw player body (simple rectangle as fallback)
            pygame.draw.rect(screen, self.color, self.rect)
            
            # Draw only one head
            head_radius = 15
            head_x = self.x + self.width // 2
            
            # Adjust head position when heading
            if self.is_heading:
                head_y = self.y - 5  # Move head up when heading
            else:
                head_y = self.y + head_radius
                
            # Draw the head
            pygame.draw.circle(screen, self.color, (head_x, head_y), head_radius)
            
            # Draw eyes
            eye_color = (255, 255, 255)
            if self.is_player:
                pygame.draw.circle(screen, eye_color, (head_x - 5, head_y - 5), 4)
                pygame.draw.circle(screen, eye_color, (head_x + 5, head_y - 5), 4)
                pygame.draw.circle(screen, (0, 0, 0), (head_x - 5, head_y - 5), 2)
                pygame.draw.circle(screen, (0, 0, 0), (head_x + 5, head_y - 5), 2)
            else:
                # AI eyes
                pygame.draw.circle(screen, eye_color, (head_x - 5, head_y - 5), 4)
                pygame.draw.circle(screen, eye_color, (head_x + 5, head_y - 5), 4)
                pygame.draw.circle(screen, (255, 0, 0), (head_x - 5, head_y - 5), 2)
                pygame.draw.circle(screen, (255, 0, 0), (head_x + 5, head_y - 5), 2)
            
    def get_head_position(self):
        """Return the position of the player's head for collision detection"""
        if self.sprite:
            return (self.x + self.width // 2, self.y)
        else:
            # Adjust head position when heading
            if self.is_heading:
                return (self.x + self.width // 2, self.y - 5)  # Higher position when heading
            else:
                return (self.x + self.width // 2, self.y + 15)
    def celebrate(self):
        """Make the player celebrate a goal"""
        # Set celebration state
        self.is_celebrating = True
        self.celebration_frames = 60  # Celebrate for 60 frames (1 second at 60 FPS)
        self.celebration_jump_count = 0
        
        # Make the player jump in celebration
        self.vel_y = -self.jump_power * 0.7
        self.is_jumping = True
        
        print(f"{'Player' if self.is_player else 'AI'} celebrating!")
        
    def update_celebration(self):
        """Update the celebration animation"""
        if self.is_celebrating:
            self.celebration_frames -= 1
            
            # Jump every 20 frames during celebration
            self.celebration_jump_count += 1
            if self.celebration_jump_count >= 20 and self.celebration_frames > 10:
                self.celebration_jump_count = 0
                self.vel_y = -self.jump_power * 0.7
                self.is_jumping = True
            
            # End celebration when frames run out
            if self.celebration_frames <= 0:
                self.is_celebrating = False
