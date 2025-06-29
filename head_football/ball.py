"""
Ball class for the Head Football game.
"""
import pygame
import math
import random
from config import GRAVITY, GROUND_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.color = (255, 165, 0)  # Orange
        
        # Physics - adjusted values for more moderate football physics
        self.vel_x = 0
        self.vel_y = 0
        self.bounce_factor = 0.6  # Reduced bounce
        self.air_resistance = 0.98  # Increased air resistance to slow down the ball
        self.ground_friction = 0.94  # Increased ground friction to slow down rolling
        
        # Create a simple circle for now (will be replaced with sprites later)
        self.rect = pygame.Rect(x - self.radius, y - self.radius, 
                               self.radius * 2, self.radius * 2)
        
        # Collision cooldown to prevent multiple collisions in a single frame
        self.collision_cooldown = 0
        self.last_collision_entity = None
        
    def apply_force(self, force_x, force_y):
        """Apply a force to the ball"""
        self.vel_x += force_x
        self.vel_y += force_y
        
    def reset(self, x, y):
        """Reset the ball to a specific position"""
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.collision_cooldown = 0
        self.last_collision_entity = None
        
        # Update rectangle position
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        
    def update(self):
        # Apply gravity
        self.vel_y += GRAVITY
        
        # Apply air resistance (more realistic values)
        self.vel_x *= self.air_resistance
        self.vel_y *= self.air_resistance
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Boundary checks - X axis
        if self.x - self.radius < 0:
            self.x = self.radius
            self.vel_x = -self.vel_x * self.bounce_factor
        elif self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.vel_x = -self.vel_x * self.bounce_factor
            
        # Boundary check - Ground
        if self.y + self.radius > GROUND_HEIGHT:
            self.y = GROUND_HEIGHT - self.radius
            
            # More realistic bounce - reduce bounce height over time
            if abs(self.vel_y) > 2.0:
                self.vel_y = -self.vel_y * self.bounce_factor
            else:
                self.vel_y = 0  # Stop bouncing when velocity is low
            
            # Apply ground friction to x velocity - more realistic
            self.vel_x *= self.ground_friction
            
            # Gradually slow down the ball on ground
            if abs(self.vel_x) < 0.5:
                self.vel_x *= 0.8  # Slow down faster when moving slowly
        
        # Update collision cooldown
        if self.collision_cooldown > 0:
            self.collision_cooldown -= 1
            
        # Boundary check - Ceiling
        if self.y - self.radius < 0:
            self.y = self.radius
            self.vel_y = -self.vel_y * self.bounce_factor
            
        # Update rectangle position
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
        
    def check_player_collision(self, player):
        """Check if the ball collides with a player's head or body"""
        # Special handling for human player to make it easier
        is_human = player.is_player
        
        # Skip collision check if on cooldown with this player
        if self.collision_cooldown > 0 and self.last_collision_entity == player:
            return False
            
        # Check head collision
        head_x, head_y = player.get_head_position()
        
        # Reasonable collision radius
        head_radius = 25 if is_human else 20
        
        # Calculate distance between ball center and player's head
        head_distance = math.sqrt((self.x - head_x)**2 + (self.y - head_y)**2)
        
        # More realistic body collision box
        body_padding = 5 if is_human else 0
        body_collision = (self.x + self.radius > player.x - body_padding and 
                         self.x - self.radius < player.x + player.width + body_padding and
                         self.y + self.radius > player.y - body_padding and
                         self.y - self.radius < player.y + player.height + body_padding)
        
        # Only check for head collision when player is actively heading
        head_collision_check = player.is_heading
        
        # If distance is less than sum of radii, head collision occurred
        if (head_distance < (self.radius + head_radius)) and head_collision_check:
            # Calculate collision angle
            angle = math.atan2(self.y - head_y, self.x - head_x)
            
            # Apply force based on player's heading power (reduced force)
            force = player.heading_power * (0.8 if is_human else 0.7)
            
            # Add slight randomness to make it feel more natural
            angle_randomness = 0.05
            angle += random.uniform(-angle_randomness, angle_randomness)
            
            # Calculate new velocities
            self.vel_x = math.cos(angle) * force
            self.vel_y = math.sin(angle) * force - 1.5  # Reduced upward force
            
            # Move ball outside of collision to prevent sticking
            self.x = head_x + math.cos(angle) * (self.radius + head_radius + 2)
            self.y = head_y + math.sin(angle) * (self.radius + head_radius + 2)
            
            # Set collision cooldown
            self.collision_cooldown = 10
            self.last_collision_entity = player
            
            # Print collision info for debugging
            print(f"{'HUMAN' if is_human else 'AI'} Ball head collision! Force: {force}, New velocity: ({self.vel_x}, {self.vel_y})")
            
            return True
            
        # Body collision - more moderate physics
        elif body_collision:
            # Skip if on cooldown
            if self.collision_cooldown > 0:
                return False
                
            # Calculate collision point and angle
            collision_x = max(min(self.x, player.x + player.width), player.x)
            collision_y = max(min(self.y, player.y + player.height), player.y)
            
            # Calculate collision normal
            normal_x = self.x - collision_x
            normal_y = self.y - collision_y
            
            # Normalize the normal vector
            length = math.sqrt(normal_x**2 + normal_y**2)
            if length > 0:
                normal_x /= length
                normal_y /= length
            else:
                # If ball is exactly at collision point, use a default normal
                normal_x = 0
                normal_y = -1
                
            # Calculate relative velocity (reduced effect)
            rel_vel_x = self.vel_x - player.vel_x * 0.7
            rel_vel_y = self.vel_y - player.vel_y * 0.7
            
            # Calculate impulse (reduced)
            impulse = 1.5 * (rel_vel_x * normal_x + rel_vel_y * normal_y)
            
            # Apply impulse to ball velocity (reduced effect)
            self.vel_x -= impulse * normal_x * 0.6
            self.vel_y -= impulse * normal_y * 0.6
            
            # Add player's velocity influence (reduced effect)
            self.vel_x += player.vel_x * 0.2
            
            # Ensure the ball doesn't get stuck
            if abs(self.vel_x) < 0.8:
                direction = 1 if player.vel_x >= 0 else -1
                self.vel_x += direction * 0.8
                
            # Add a slight upward velocity to make the ball bounce
            if self.vel_y > 0:  # Only if ball is moving downward
                self.vel_y = -self.vel_y * 0.4 - 0.8
                
            # Move ball outside of collision to prevent sticking
            overlap = self.radius + 2 - length
            if overlap > 0:
                self.x += normal_x * overlap
                self.y += normal_y * overlap
                
            # Set collision cooldown
            self.collision_cooldown = 5
            self.last_collision_entity = player
                
            print(f"{'HUMAN' if is_human else 'AI'} Ball body collision! New velocity: ({self.vel_x}, {self.vel_y})")
            return True
                
        return False
        
    def check_goal_collision(self, left_goal, right_goal):
        """Check if the ball enters either goal"""
        # Check left goal
        if (self.x - self.radius < left_goal.x + left_goal.width and
            self.x + self.radius > left_goal.x and
            self.y - self.radius < left_goal.y + left_goal.height and
            self.y + self.radius > left_goal.y):
            print("Ball entered left goal!")
            return "right"  # Right player scores
            
        # Check right goal
        if (self.x - self.radius < right_goal.x + right_goal.width and
            self.x + self.radius > right_goal.x and
            self.y - self.radius < right_goal.y + right_goal.height and
            self.y + self.radius > right_goal.y):
            print("Ball entered right goal!")
            return "left"  # Left player scores
            
        return None  # No goal
        
    def draw(self, screen):
        # Draw ball
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Draw pattern on ball (simple lines for now)
        pygame.draw.line(screen, (0, 0, 0), 
                        (self.x - self.radius, self.y), 
                        (self.x + self.radius, self.y), 2)
        pygame.draw.line(screen, (0, 0, 0), 
                        (self.x, self.y - self.radius), 
                        (self.x, self.y + self.radius), 2)
