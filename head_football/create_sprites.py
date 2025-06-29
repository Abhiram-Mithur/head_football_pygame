"""
Script to create improved player sprites for Head Football game.
"""
import pygame
import os
import math

def create_improved_player_sprites():
    """Create more human-like player sprites"""
    # Initialize pygame
    pygame.init()
    
    # Create player sprites
    player_types = ['speedy_player', 'powerful_player', 'balanced_player', 'technical_player', 'jumper_player']
    player_names = ['Speedy', 'Powerful', 'Balanced', 'Technical', 'Jumper']
    colors = [(255, 50, 50), (50, 50, 255), (50, 255, 50), (255, 255, 50), (255, 50, 255)]
    
    # Ensure directory exists
    os.makedirs('assets/players', exist_ok=True)
    
    # Create each player sprite
    for i, player_type in enumerate(player_types):
        # Create player body
        player_surface = pygame.Surface((80, 160), pygame.SRCALPHA)
        color = colors[i]
        skin_color = (255, 213, 170)  # Basic skin tone
        
        # Draw body (torso)
        pygame.draw.ellipse(player_surface, color, (25, 50, 30, 50))  # Torso
        
        # Draw head
        pygame.draw.circle(player_surface, skin_color, (40, 30), 15)  # Head
        
        # Draw limbs
        # Legs
        pygame.draw.line(player_surface, color, (30, 95), (25, 140), 8)  # Left leg
        pygame.draw.line(player_surface, color, (50, 95), (55, 140), 8)  # Right leg
        
        # Feet
        pygame.draw.ellipse(player_surface, (0, 0, 0), (20, 135, 10, 5))  # Left foot
        pygame.draw.ellipse(player_surface, (0, 0, 0), (50, 135, 10, 5))  # Right foot
        
        # Arms
        pygame.draw.line(player_surface, color, (25, 60), (15, 90), 6)  # Left arm
        pygame.draw.line(player_surface, color, (55, 60), (65, 90), 6)  # Right arm
        
        # Hands
        pygame.draw.circle(player_surface, skin_color, (15, 90), 4)  # Left hand
        pygame.draw.circle(player_surface, skin_color, (65, 90), 4)  # Right hand
        
        # Draw face
        pygame.draw.circle(player_surface, (255, 255, 255), (35, 25), 3)  # Left eye
        pygame.draw.circle(player_surface, (255, 255, 255), (45, 25), 3)  # Right eye
        pygame.draw.circle(player_surface, (0, 0, 0), (35, 25), 1.5)  # Left pupil
        pygame.draw.circle(player_surface, (0, 0, 0), (45, 25), 1.5)  # Right pupil
        
        # Draw mouth
        pygame.draw.arc(player_surface, (0, 0, 0), (30, 30, 20, 15), 0, math.pi, 2)
        
        # Add hair based on player type
        if player_type == 'speedy_player':
            # Short spiky hair
            hair_color = (30, 30, 30)  # Black hair
            for x in range(25, 55, 4):
                pygame.draw.line(player_surface, hair_color, (x, 20), (x, 10), 2)
                pygame.draw.line(player_surface, hair_color, (x-1, 20), (x-2, 12), 2)
            # Add some hair volume
            pygame.draw.ellipse(player_surface, hair_color, (25, 12, 30, 10))
        elif player_type == 'powerful_player':
            # Bald with beard
            hair_color = (60, 40, 20)  # Brown beard
            pygame.draw.arc(player_surface, hair_color, (25, 35, 30, 20), 0, math.pi, 3)
            # Add some stubble on top
            pygame.draw.ellipse(player_surface, hair_color, (30, 15, 20, 5), 1)
        elif player_type == 'balanced_player':
            # Medium hair
            hair_color = (80, 50, 20)  # Brown hair
            pygame.draw.ellipse(player_surface, hair_color, (25, 10, 30, 18))
            # Add some hair strands
            pygame.draw.line(player_surface, hair_color, (30, 15), (28, 10), 2)
            pygame.draw.line(player_surface, hair_color, (40, 12), (40, 8), 2)
            pygame.draw.line(player_surface, hair_color, (50, 15), (52, 10), 2)
        elif player_type == 'technical_player':
            # Neat hair with side part
            hair_color = (20, 20, 20)  # Dark hair
            pygame.draw.ellipse(player_surface, hair_color, (25, 10, 30, 15))
            # Add side part
            pygame.draw.line(player_surface, hair_color, (35, 10), (35, 5), 3)
            pygame.draw.line(player_surface, hair_color, (45, 10), (48, 5), 3)
            pygame.draw.line(player_surface, hair_color, (50, 12), (55, 8), 3)
        elif player_type == 'jumper_player':
            # Long flowing hair
            hair_color = (120, 80, 40)  # Light brown hair
            # Hair top
            pygame.draw.ellipse(player_surface, hair_color, (25, 10, 30, 18))
            # Hair sides
            pygame.draw.line(player_surface, hair_color, (25, 20), (20, 35), 3)
            pygame.draw.line(player_surface, hair_color, (55, 20), (60, 35), 3)
            # Hair back
            pygame.draw.line(player_surface, hair_color, (30, 20), (25, 40), 3)
            pygame.draw.line(player_surface, hair_color, (40, 20), (40, 40), 3)
            pygame.draw.line(player_surface, hair_color, (50, 20), (55, 40), 3)
        
        # Add jersey number
        font = pygame.font.SysFont('Arial', 20)
        number = font.render(str(i+1), True, (255, 255, 255))
        player_surface.blit(number, (35, 65))
        
        # Add some shading for depth
        pygame.draw.ellipse(player_surface, (color[0]//1.5, color[1]//1.5, color[2]//1.5), (25, 50, 15, 50))
        
        # Save player sprite
        pygame.image.save(player_surface, f'assets/players/{player_type}.png')
        
        # Create head sprite separately for heading animations
        head_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(head_surface, skin_color, (20, 20), 15)  # Head
        pygame.draw.circle(head_surface, (255, 255, 255), (15, 15), 3)  # Left eye
        pygame.draw.circle(head_surface, (255, 255, 255), (25, 15), 3)  # Right eye
        pygame.draw.circle(head_surface, (0, 0, 0), (15, 15), 1.5)  # Left pupil
        pygame.draw.circle(head_surface, (0, 0, 0), (25, 15), 1.5)  # Right pupil
        pygame.draw.arc(head_surface, (0, 0, 0), (10, 20, 20, 15), 0, math.pi, 2)  # Mouth
        
        # Add hair based on player type
        if player_type == 'speedy_player':
            # Short spiky hair
            hair_color = (30, 30, 30)  # Black hair
            for x in range(10, 30, 4):
                pygame.draw.line(head_surface, hair_color, (x, 10), (x, 5), 2)
                pygame.draw.line(head_surface, hair_color, (x-1, 10), (x-2, 6), 2)
            # Add some hair volume
            pygame.draw.ellipse(head_surface, hair_color, (5, 5, 30, 8))
        elif player_type == 'powerful_player':
            # Bald with beard
            hair_color = (60, 40, 20)  # Brown beard
            pygame.draw.arc(head_surface, hair_color, (5, 25, 30, 20), 0, math.pi, 3)
            # Add some stubble on top
            pygame.draw.ellipse(head_surface, hair_color, (10, 5, 20, 5), 1)
        elif player_type == 'balanced_player':
            # Medium hair
            hair_color = (80, 50, 20)  # Brown hair
            pygame.draw.ellipse(head_surface, hair_color, (5, 2, 30, 15))
            # Add some hair strands
            pygame.draw.line(head_surface, hair_color, (10, 8), (8, 3), 2)
            pygame.draw.line(head_surface, hair_color, (20, 5), (20, 1), 2)
            pygame.draw.line(head_surface, hair_color, (30, 8), (32, 3), 2)
        elif player_type == 'technical_player':
            # Neat hair with side part
            hair_color = (20, 20, 20)  # Dark hair
            pygame.draw.ellipse(head_surface, hair_color, (5, 2, 30, 12))
            # Add side part
            pygame.draw.line(head_surface, hair_color, (15, 5), (15, 1), 3)
            pygame.draw.line(head_surface, hair_color, (25, 5), (28, 1), 3)
            pygame.draw.line(head_surface, hair_color, (30, 7), (35, 3), 3)
        elif player_type == 'jumper_player':
            # Long flowing hair
            hair_color = (120, 80, 40)  # Light brown hair
            # Hair top
            pygame.draw.ellipse(head_surface, hair_color, (5, 2, 30, 15))
            # Hair sides
            pygame.draw.line(head_surface, hair_color, (5, 10), (2, 20), 3)
            pygame.draw.line(head_surface, hair_color, (35, 10), (38, 20), 3)
            # Hair back
            pygame.draw.line(head_surface, hair_color, (10, 10), (5, 25), 3)
            pygame.draw.line(head_surface, hair_color, (20, 10), (20, 25), 3)
            pygame.draw.line(head_surface, hair_color, (30, 10), (35, 25), 3)
        
        # Save head sprite
        pygame.image.save(head_surface, f'assets/players/{player_type}_head.png')
        
    # Create player profiles file
    with open('assets/players/profiles.txt', 'w') as f:
        f.write("# Player Profiles\n\n")
        
        for i, name in enumerate(player_names):
            f.write(f"## {name}\n")
            if name == "Speedy":
                f.write("The fastest player on the field. Has excellent acceleration and top speed, but lacks power in headers.\n")
                f.write("- Speed: ★★★★★\n")
                f.write("- Jump: ★★★★☆\n")
                f.write("- Power: ★★☆☆☆\n")
                f.write("- Control: ★★☆☆☆\n\n")
            elif name == "Powerful":
                f.write("A strong player with powerful headers. Can send the ball flying across the field but moves slowly.\n")
                f.write("- Speed: ★★☆☆☆\n")
                f.write("- Jump: ★★★☆☆\n")
                f.write("- Power: ★★★★★\n")
                f.write("- Control: ★★★☆☆\n\n")
            elif name == "Balanced":
                f.write("A well-rounded player with no major weaknesses. Good at everything but not exceptional in any area.\n")
                f.write("- Speed: ★★★☆☆\n")
                f.write("- Jump: ★★★★☆\n")
                f.write("- Power: ★★★☆☆\n")
                f.write("- Control: ★★★☆☆\n\n")
            elif name == "Technical":
                f.write("A technical player with excellent ball control. Can place headers with precision but lacks raw power.\n")
                f.write("- Speed: ★★★☆☆\n")
                f.write("- Jump: ★★★☆☆\n")
                f.write("- Power: ★★★☆☆\n")
                f.write("- Control: ★★★★★\n\n")
            elif name == "Jumper":
                f.write("An acrobatic player with incredible jumping ability. Can reach balls that others can't.\n")
                f.write("- Speed: ★★★☆☆\n")
                f.write("- Jump: ★★★★★\n")
                f.write("- Power: ★★★☆☆\n")
                f.write("- Control: ★★☆☆☆\n\n")
    
    print('Created improved player sprites and profiles successfully!')

if __name__ == "__main__":
    create_improved_player_sprites()
