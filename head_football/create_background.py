"""
Script to create improved background assets for Head Football game.
"""
import pygame
import os
import random
import math

def create_background_assets():
    """Create improved background assets for the game"""
    # Initialize pygame
    pygame.init()
    
    # Ensure directory exists
    os.makedirs('assets/background', exist_ok=True)
    
    # Create stadium background with crowd
    create_stadium_background()
    
    # Create field with markings
    create_field()
    
    # Create goal posts with nets
    create_goal_posts()
    
    print('Created improved background assets successfully!')

def create_stadium_background():
    """Create a stadium background with crowd"""
    # Create a large surface for the stadium background
    width, height = 800, 600
    stadium = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Fill the sky
    sky_gradient(stadium, width, height)
    
    # Draw stadium structure
    draw_stadium_structure(stadium, width, height)
    
    # Draw crowd
    draw_crowd(stadium, width, height)
    
    # Fill the gap between crowd and field with a gradient
    fill_stadium_gap(stadium, width, height)
    
    # Add credits footer
    add_credits_footer(stadium, width, height)
    
    # Save the background
    pygame.image.save(stadium, 'assets/background/stadium.png')

def fill_stadium_gap(surface, width, height):
    """Fill the gap between crowd and field with a gradient to prevent glitches"""
    stand_height = height // 3
    stand_y = height // 4
    gap_start = stand_y + stand_height
    gap_end = height - 100  # Where the field starts
    
    # Create a gradient from stadium color to field color
    for y in range(gap_start, gap_end):
        # Calculate gradient progress (0 to 1)
        progress = (y - gap_start) / (gap_end - gap_start)
        # Blend from stadium gray (100,100,100) to field green (34,139,34)
        r = int(100 - progress * (100 - 34))
        g = int(100 + progress * (139 - 100))
        b = int(100 - progress * (100 - 34))
        pygame.draw.line(surface, (r, g, b), (0, y), (width, y))

def add_credits_footer(surface, width, height):
    """Add a credits footer at the bottom of the screen"""
    # Create font
    try:
        font = pygame.font.SysFont('Arial', 16)
        credits_text = "Made with ❤️ by Abhiram Mithur"
        text_surface = font.render(credits_text, True, (255, 255, 255))
        
        # Add a semi-transparent background for the text
        footer_height = 25
        footer_y = height - footer_height
        footer_surface = pygame.Surface((width, footer_height), pygame.SRCALPHA)
        footer_surface.fill((0, 0, 0, 150))  # Semi-transparent black
        
        # Position text in the center of the footer
        text_x = (width - text_surface.get_width()) // 2
        text_y = footer_y + (footer_height - text_surface.get_height()) // 2
        
        # Blit footer background and text
        surface.blit(footer_surface, (0, footer_y))
        surface.blit(text_surface, (text_x, text_y))
    except Exception as e:
        print(f"Could not add credits: {e}")

def sky_gradient(surface, width, height):
    """Create a gradient sky background"""
    for y in range(0, height // 2):
        # Create gradient from light blue to darker blue
        color_value = int(200 - y / (height // 2) * 100)
        color = (color_value, color_value + 30, 255)
        pygame.draw.line(surface, color, (0, y), (width, y))

def draw_stadium_structure(surface, width, height):
    """Draw the stadium structure"""
    # Stadium upper structure (stands)
    stand_height = height // 3
    stand_y = height // 4
    
    # Main stand structure
    pygame.draw.rect(surface, (150, 150, 150), (0, stand_y, width, stand_height))
    pygame.draw.rect(surface, (100, 100, 100), (0, stand_y, width, 10))  # Top edge
    
    # Draw stadium sections with different shades
    section_width = width // 8
    for i in range(8):
        shade = 130 + (i % 3) * 20  # Alternate shades
        pygame.draw.rect(surface, (shade, shade, shade), 
                        (i * section_width, stand_y + 10, section_width, stand_height - 10))
    
    # Draw stadium roof
    roof_points = [
        (0, stand_y),
        (width, stand_y),
        (width - 50, stand_y - 30),
        (50, stand_y - 30)
    ]
    pygame.draw.polygon(surface, (80, 80, 80), roof_points)
    
    # Draw support beams
    for i in range(1, 8):
        x = i * section_width
        pygame.draw.line(surface, (70, 70, 70), (x, stand_y), (x, stand_y + stand_height), 3)
    
    # Draw stadium lights
    draw_stadium_lights(surface, width, stand_y - 30)

def draw_stadium_lights(surface, width, y_pos):
    """Draw stadium floodlights"""
    # Left light
    pygame.draw.rect(surface, (100, 100, 100), (width // 6 - 5, y_pos - 40, 10, 40))
    light_points = [
        (width // 6 - 25, y_pos - 40),
        (width // 6 + 25, y_pos - 40),
        (width // 6 + 15, y_pos - 50),
        (width // 6 - 15, y_pos - 50)
    ]
    pygame.draw.polygon(surface, (200, 200, 200), light_points)
    
    # Right light
    pygame.draw.rect(surface, (100, 100, 100), (width - width // 6 - 5, y_pos - 40, 10, 40))
    light_points = [
        (width - width // 6 - 25, y_pos - 40),
        (width - width // 6 + 25, y_pos - 40),
        (width - width // 6 + 15, y_pos - 50),
        (width - width // 6 - 15, y_pos - 50)
    ]
    pygame.draw.polygon(surface, (200, 200, 200), light_points)
    
    # Draw light beams (semi-transparent)
    light_beam = pygame.Surface((100, 150), pygame.SRCALPHA)
    for i in range(100):
        alpha = 100 - i  # Fade out
        if alpha < 0:
            alpha = 0
        pygame.draw.line(light_beam, (255, 255, 200, alpha), 
                        (50, 0), (i, 150), 1)
    
    # Position and draw the light beams
    surface.blit(light_beam, (width // 6 - 50, y_pos - 40))
    surface.blit(light_beam, (width - width // 6 - 50, y_pos - 40))

def draw_crowd(surface, width, height):
    """Draw a crowd of spectators in the stadium"""
    stand_y = height // 4
    stand_height = height // 3
    
    # Create a crowd pattern
    crowd_colors = [
        (255, 0, 0),    # Red
        (0, 0, 255),    # Blue
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (255, 165, 0),  # Orange
        (128, 0, 128),  # Purple
        (255, 255, 255) # White
    ]
    
    # Draw rows of crowd
    rows = 15
    people_per_row = 80
    
    for row in range(rows):
        y = stand_y + 15 + row * 10
        for i in range(people_per_row):
            x = 10 + i * (width - 20) // people_per_row
            size = random.randint(3, 6)
            color = random.choice(crowd_colors)
            
            # Add slight randomness to position
            x_offset = random.randint(-2, 2)
            y_offset = random.randint(-1, 1)
            
            # Draw a person (simple circle)
            pygame.draw.circle(surface, color, (x + x_offset, y + y_offset), size)
            
            # Occasionally draw a raised arm
            if random.random() < 0.1:
                arm_height = random.randint(5, 8)
                pygame.draw.line(surface, (255, 213, 170), 
                                (x + x_offset, y + y_offset - size), 
                                (x + x_offset, y + y_offset - size - arm_height), 2)

def create_field():
    """Create a football field with markings"""
    width, height = 800, 200
    field = pygame.Surface((width, height), pygame.SRCALPHA)
    
    # Draw grass base
    pygame.draw.rect(field, (34, 139, 34), (0, 0, width, height))
    
    # Add grass texture
    for i in range(1000):
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        size = random.randint(1, 3)
        shade = random.randint(-20, 20)
        color = (34 + shade, 139 + shade, 34 + shade)
        pygame.draw.circle(field, color, (x, y), size)
    
    # Add alternating grass pattern (mowed lines)
    for i in range(0, width, 20):
        if (i // 20) % 2 == 0:
            pygame.draw.rect(field, (44, 149, 44), (i, 0, 10, height))
    
    # Draw field markings with proper dimensions
    line_color = (255, 255, 255)
    
    # Center line
    pygame.draw.line(field, line_color, (width // 2, 0), (width // 2, height), 2)
    
    # Center circle - properly sized and positioned
    pygame.draw.circle(field, line_color, (width // 2, height // 2), 50, 2)
    pygame.draw.circle(field, line_color, (width // 2, height // 2), 5)
    
    # Penalty areas - centered vertically
    # Left penalty area
    penalty_width = 120
    penalty_height = 120
    penalty_y = (height - penalty_height) // 2  # Center vertically
    pygame.draw.rect(field, line_color, (0, penalty_y, penalty_width, penalty_height), 2)
    
    # Right penalty area
    pygame.draw.rect(field, line_color, (width - penalty_width, penalty_y, penalty_width, penalty_height), 2)
    
    # Goal areas - centered vertically
    goal_area_width = 50
    goal_area_height = 80
    goal_area_y = (height - goal_area_height) // 2  # Center vertically
    
    # Left goal area
    pygame.draw.rect(field, line_color, (0, goal_area_y, goal_area_width, goal_area_height), 2)
    
    # Right goal area
    pygame.draw.rect(field, line_color, (width - goal_area_width, goal_area_y, goal_area_width, goal_area_height), 2)
    
    # Penalty spots
    penalty_spot_distance = 80
    pygame.draw.circle(field, line_color, (penalty_spot_distance, height // 2), 3)
    pygame.draw.circle(field, line_color, (width - penalty_spot_distance, height // 2), 3)
    
    # Corner arcs
    corner_radius = 10
    # Top-left corner
    pygame.draw.arc(field, line_color, (0, 0, corner_radius * 2, corner_radius * 2), 
                   math.pi / 2, math.pi, 2)
    # Bottom-left corner
    pygame.draw.arc(field, line_color, (0, height - corner_radius * 2, corner_radius * 2, corner_radius * 2), 
                   0, math.pi / 2, 2)
    # Top-right corner
    pygame.draw.arc(field, line_color, (width - corner_radius * 2, 0, corner_radius * 2, corner_radius * 2), 
                   0, math.pi / 2, 2)
    # Bottom-right corner
    pygame.draw.arc(field, line_color, (width - corner_radius * 2, height - corner_radius * 2, corner_radius * 2, corner_radius * 2), 
                   math.pi * 3 / 2, math.pi * 2, 2)
    
    # Save the field
    pygame.image.save(field, 'assets/background/field.png')

def create_goal_posts():
    """Create goal posts with nets"""
    # Match goal dimensions with field markings exactly
    field_height = 200  # Height of the field surface
    goal_area_width = 50  # Match the goal area width from field markings
    goal_area_height = 80  # Match the goal area height from field markings
    
    # Create goal surface with exact dimensions to match goal area
    goal = pygame.Surface((goal_area_width, goal_area_height), pygame.SRCALPHA)
    
    # Make the background fully transparent
    goal.fill((0, 0, 0, 0))
    
    # Draw goal frame with simpler, cleaner design
    frame_color = (255, 255, 255)  # Pure white for better visibility
    frame_thickness = 5
    
    # Draw the main goal frame (3 sides - top and two sides)
    # Top bar
    pygame.draw.rect(goal, frame_color, (0, 0, goal_area_width, frame_thickness))
    # Left post
    pygame.draw.rect(goal, frame_color, (0, 0, frame_thickness, goal_area_height))
    # Right post
    pygame.draw.rect(goal, frame_color, (goal_area_width - frame_thickness, 0, frame_thickness, goal_area_height))
    
    # Draw net with a simpler pattern
    net_color = (255, 255, 255, 100)  # Very transparent white
    
    # Draw vertical net lines
    for i in range(5, goal_area_width - 5, 5):
        pygame.draw.line(goal, net_color, (i, frame_thickness), (i, goal_area_height), 1)
    
    # Draw horizontal net lines
    for i in range(5, goal_area_height, 5):
        pygame.draw.line(goal, net_color, (frame_thickness, i), (goal_area_width - frame_thickness, i), 1)
    
    # Save left goal
    pygame.image.save(goal, 'assets/background/goal_left.png')
    
    # Flip for right goal
    right_goal = pygame.transform.flip(goal, True, False)
    pygame.image.save(right_goal, 'assets/background/goal_right.png')

if __name__ == "__main__":
    create_background_assets()
