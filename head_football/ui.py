"""
UI module for the Head Football game.
"""
import pygame
from config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, RED, GREEN, BLUE, SKY_BLUE,
    PLAYER_PROFILES, DIFFICULTY_SETTINGS, PLAYERS_DIR
)
import os

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=BLACK, border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.border_radius = border_radius
        self.selected = False
        
    def draw(self, screen, font):
        # Draw button background
        color = self.hover_color if self.is_hovered else self.color
        
        # For selected buttons, use a different effect
        if self.selected:
            # Draw a glow effect for selected buttons
            glow_rect = self.rect.inflate(10, 10)
            pygame.draw.rect(screen, self.color, glow_rect, border_radius=self.border_radius)
            # Use a brighter color for the button itself
            pygame.draw.rect(screen, (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)), 
                            self.rect, border_radius=self.border_radius)
        else:
            # Draw the button with rounded corners
            pygame.draw.rect(screen, color, self.rect, border_radius=self.border_radius)
            
        # Always draw border
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=self.border_radius)
        
        # Draw text if there is any
        if self.text:
            text_surface = font.render(self.text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)
        
    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered
        
    def check_click(self, mouse_pos, mouse_clicked):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        return self.is_hovered and mouse_clicked

class UI:
    def __init__(self):
        # Fonts
        self.title_font = pygame.font.SysFont('Arial', 60, bold=True)
        self.menu_font = pygame.font.SysFont('Arial', 36)
        self.button_font = pygame.font.SysFont('Arial', 28)
        self.info_font = pygame.font.SysFont('Arial', 22)
        
        # Menu buttons
        self.menu_buttons = [
            Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 - 50, 300, 60, "Play Game", GREEN, (100, 255, 100), WHITE),
            Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 40, 300, 60, "Quit", RED, (255, 100, 100), WHITE)
        ]
        
        # Player selection buttons
        self.player_buttons = []
        x_pos = 100
        for i, name in enumerate(PLAYER_PROFILES):
            # Calculate position for a horizontal layout
            button_x = x_pos + i * 120
            self.player_buttons.append(
                Button(button_x, SCREEN_HEIGHT//2 - 100, 100, 100, name, PLAYER_PROFILES[name]["color"], WHITE)
            )
            
        # Difficulty buttons
        self.difficulty_buttons = []
        y_pos = SCREEN_HEIGHT//2 + 100
        for i, name in enumerate(DIFFICULTY_SETTINGS):
            color = GREEN if name == "Easy" else BLUE if name == "Medium" else RED
            # All text in black now
            text_color = BLACK
            self.difficulty_buttons.append(
                Button(SCREEN_WIDTH//2 - 300 + i * 200, y_pos, 180, 50, name, color, WHITE, text_color)
            )
            
        # Game over buttons
        self.game_over_buttons = [
            Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 50, 300, 60, "Play Again", GREEN, (100, 255, 100), WHITE),
            Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2 + 130, 300, 60, "Main Menu", BLUE, (100, 100, 255), WHITE)
        ]
        
        # Selected options
        self.selected_player = None
        self.selected_difficulty = None
        
        # Load player preview images
        self.player_previews = {}
        for name, profile in PLAYER_PROFILES.items():
            sprite_name = profile.get("sprite", None)
            if sprite_name:
                sprite_path = os.path.join(PLAYERS_DIR, f"{sprite_name}.png")
                head_path = os.path.join(PLAYERS_DIR, f"{sprite_name}_head.png")
                try:
                    if os.path.exists(sprite_path):
                        sprite = pygame.image.load(sprite_path)
                        sprite = pygame.transform.scale(sprite, (80, 160))
                        self.player_previews[name] = sprite
                except pygame.error:
                    print(f"Could not load preview for: {sprite_path}")
        
    def draw_menu(self, screen):
        # Draw background
        self.draw_background(screen)
        
        # Draw title with shadow effect
        self.draw_title(screen, "HEAD FOOTBALL", SCREEN_WIDTH//2, 120)
        
        # Draw subtitle
        subtitle = self.menu_font.render("Single Player Game", True, BLACK)
        screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 190))
        
        # Draw buttons
        for button in self.menu_buttons:
            button.draw(screen, self.button_font)
            
    def draw_player_select(self, screen):
        # Draw background
        self.draw_background(screen)
        
        # Draw title with shadow
        self.draw_title(screen, "Select Player", SCREEN_WIDTH//2, 80)
        
        # Draw player selection area - make it taller to accommodate player names
        selection_bg = pygame.Rect(50, SCREEN_HEIGHT//2 - 220, SCREEN_WIDTH - 100, 280)
        pygame.draw.rect(screen, (240, 240, 240), selection_bg, border_radius=15)
        pygame.draw.rect(screen, BLACK, selection_bg, 2, border_radius=15)
        
        # Calculate equal spacing for player buttons
        button_width = 100
        total_width = len(self.player_buttons) * button_width + (len(self.player_buttons) - 1) * 30  # 30px spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        # Draw player buttons with equal spacing
        for i, button in enumerate(self.player_buttons):
            # Update button position for equal spacing
            button.rect.x = start_x + i * (button_width + 30)
            button.rect.y = SCREEN_HEIGHT//2 - 180
            
            # Update selected state
            button.selected = (button.text == self.selected_player)
            
            # Don't draw text inside the button
            original_text = button.text
            button.text = ""
            button.draw(screen, self.button_font)
            button.text = original_text
            
            # Draw player preview if available
            if button.text in self.player_previews:
                preview = self.player_previews[button.text]
                preview_x = button.rect.x + (button.rect.width - preview.get_width()) // 2
                preview_y = button.rect.y - 100
                screen.blit(preview, (preview_x, preview_y))
                
                # Draw player name below character
                name_text = self.info_font.render(button.text, True, BLACK)
                name_x = button.rect.x + (button.rect.width - name_text.get_width()) // 2
                name_y = button.rect.y + button.rect.height + 10
                screen.blit(name_text, (name_x, name_y))
        
        # Draw player stats if one is selected
        if self.selected_player:
            profile = PLAYER_PROFILES[self.selected_player]
            
            # Draw stats box with proper spacing - made taller to fit all stats
            stats_rect = pygame.Rect(SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 20, 400, 140)
            pygame.draw.rect(screen, WHITE, stats_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, stats_rect, 2, border_radius=10)
            
            # Draw player description based on type
            description = ""
            if self.selected_player == "Speedy":
                description = "Fast player with excellent acceleration"
            elif self.selected_player == "Powerful":
                description = "Strong player with powerful headers"
            elif self.selected_player == "Balanced":
                description = "Well-rounded player with no weaknesses"
            elif self.selected_player == "Technical":
                description = "Precise player with excellent control"
            elif self.selected_player == "Jumper":
                description = "Acrobatic player with incredible jump"
                
            desc_text = self.info_font.render(description, True, BLACK)
            screen.blit(desc_text, (stats_rect.centerx - desc_text.get_width()//2, stats_rect.y + 15))
            
            # Draw stats as bars - reduced spacing between bars
            stats = [
                ("Speed", profile['speed'], 12),
                ("Jump", profile['jump'], 15),
                ("Power", profile['power'], 15),
                ("Control", profile['control'], 15)
            ]
            
            y_offset = 45
            for stat_name, stat_value, max_value in stats:
                # Draw stat name
                stat_text = self.info_font.render(f"{stat_name}:", True, BLACK)
                screen.blit(stat_text, (stats_rect.x + 20, stats_rect.y + y_offset))
                
                # Draw stat bar background
                bar_bg_rect = pygame.Rect(stats_rect.x + 120, stats_rect.y + y_offset + 5, 250, 15)
                pygame.draw.rect(screen, (200, 200, 200), bar_bg_rect, border_radius=7)
                
                # Draw stat bar fill
                bar_fill_width = int((stat_value / max_value) * 250)
                bar_fill_rect = pygame.Rect(stats_rect.x + 120, stats_rect.y + y_offset + 5, bar_fill_width, 15)
                pygame.draw.rect(screen, profile["color"], bar_fill_rect, border_radius=7)
                
                y_offset += 22  # Reduced from 25 to 22
            
        # Draw continue button if player is selected
        if self.selected_player:
            continue_button = Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 60, 300, 50, 
                                "Continue", GREEN, (100, 255, 100), WHITE)
            continue_button.draw(screen, self.button_font)
            return continue_button
        return None
        
    def draw_difficulty_select(self, screen):
        # Draw background
        self.draw_background(screen)
        
        # Draw title with shadow
        self.draw_title(screen, "Select Difficulty", SCREEN_WIDTH//2, 80)
        
        # Draw selected player info
        if self.selected_player:
            profile = PLAYER_PROFILES[self.selected_player]
            
            # Draw player preview
            if self.selected_player in self.player_previews:
                preview = self.player_previews[self.selected_player]
                preview_x = 100
                preview_y = SCREEN_HEIGHT//2 - 200
                screen.blit(preview, (preview_x, preview_y))
                
                # Draw player name
                name_text = self.menu_font.render(self.selected_player, True, profile["color"])
                name_x = preview_x + preview.get_width() // 2 - name_text.get_width() // 2
                name_y = preview_y + preview.get_height() + 10
                screen.blit(name_text, (name_x, name_y))
        
        # Draw difficulty selection area
        selection_bg = pygame.Rect(50, SCREEN_HEIGHT//2 - 100, SCREEN_WIDTH - 100, 200)
        pygame.draw.rect(screen, (240, 240, 240), selection_bg, border_radius=15)
        pygame.draw.rect(screen, BLACK, selection_bg, 2, border_radius=15)
        
        # Calculate equal spacing for difficulty buttons
        button_width = 180
        total_width = len(self.difficulty_buttons) * button_width + (len(self.difficulty_buttons) - 1) * 30  # 30px spacing
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        # Draw difficulty buttons with equal spacing
        for i, button in enumerate(self.difficulty_buttons):
            # Update button position for equal spacing
            button.rect.x = start_x + i * (button_width + 30)
            button.rect.y = SCREEN_HEIGHT//2 - 50
            
            # Update selected state
            button.selected = (button.text == self.selected_difficulty)
            button.draw(screen, self.button_font)
        
        # Draw difficulty description if one is selected
        if self.selected_difficulty:
            # Draw description box
            desc_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 + 50, 500, 100)
            pygame.draw.rect(screen, WHITE, desc_rect, border_radius=10)
            pygame.draw.rect(screen, BLACK, desc_rect, 2, border_radius=10)
            
            # Draw difficulty description
            if self.selected_difficulty == "Easy":
                title = "Easy Mode"
                desc = "Slower AI with poor reaction time and accuracy."
                desc2 = "Recommended for beginners."
                color = GREEN
            elif self.selected_difficulty == "Medium":
                title = "Medium Mode"
                desc = "Balanced AI with moderate reactions and accuracy."
                desc2 = "Recommended for casual players."
                color = BLUE
            else:  # Hard
                title = "Hard Mode"
                desc = "Fast AI with quick reactions and high accuracy."
                desc2 = "Recommended for experienced players."
                color = RED
                
            # Draw title
            title_text = self.menu_font.render(title, True, color)
            screen.blit(title_text, (desc_rect.centerx - title_text.get_width()//2, desc_rect.y + 15))
            
            # Draw descriptions
            desc_text = self.info_font.render(desc, True, BLACK)
            screen.blit(desc_text, (desc_rect.centerx - desc_text.get_width()//2, desc_rect.y + 50))
            
            desc2_text = self.info_font.render(desc2, True, BLACK)
            screen.blit(desc2_text, (desc_rect.centerx - desc2_text.get_width()//2, desc_rect.y + 75))
        
        # Draw back button
        back_button = Button(100, SCREEN_HEIGHT - 80, 150, 60, "Back", BLUE, (100, 100, 255), WHITE)
        back_button.draw(screen, self.button_font)
        
        # Draw start button if difficulty is selected
        if self.selected_difficulty:
            start_button = Button(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 80, 150, 60, 
                                "Start Game", GREEN, (100, 255, 100), WHITE)
            start_button.draw(screen, self.button_font)
            return start_button, back_button
        return None, back_button
            
    def draw_game_hud(self, screen, player_score, ai_score, time_left):
        # Draw HUD background - make it shorter again since timer will be in game field
        hud_rect = pygame.Rect(0, 0, SCREEN_WIDTH, 60)
        pygame.draw.rect(screen, (0, 0, 0, 128), hud_rect)
        pygame.draw.line(screen, WHITE, (0, 60), (SCREEN_WIDTH, 60), 2)
        
        # Draw score with shadow effect - centered at the top
        score_text = self.title_font.render(f"{player_score} - {ai_score}", True, WHITE)
        # Add shadow for better visibility
        score_shadow = self.title_font.render(f"{player_score} - {ai_score}", True, (50, 50, 50))
        screen.blit(score_shadow, (SCREEN_WIDTH//2 - score_text.get_width()//2 + 2, 12))
        screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, 10))
        
        # Draw player names with team colors - moved to the sides
        player_name = self.info_font.render(f"You ({self.selected_player})", True, WHITE)
        ai_name = self.info_font.render(f"AI ({self.selected_difficulty})", True, WHITE)
        
        # Add colored indicators for player sides
        pygame.draw.rect(screen, PLAYER_PROFILES[self.selected_player]["color"], (10, 30, 5, 20))
        pygame.draw.rect(screen, (255, 50, 50), (SCREEN_WIDTH - 15, 30, 5, 20))  # AI color (red)
        
        screen.blit(player_name, (20, 30))
        screen.blit(ai_name, (SCREEN_WIDTH - 20 - ai_name.get_width(), 30))
        
        # Draw time with a semi-transparent box in the game field
        minutes = time_left // 60
        seconds = time_left % 60
        time_text = self.menu_font.render(f"{minutes:02d}:{seconds:02d}", True, WHITE)
        time_rect = time_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        
        # Create a semi-transparent surface for the timer background
        timer_surface = pygame.Surface((time_rect.width + 30, time_rect.height + 10), pygame.SRCALPHA)
        timer_surface.fill((0, 0, 0, 128))  # Black with 50% transparency
        
        # Draw the timer background and text
        screen.blit(timer_surface, (time_rect.x - 15, time_rect.y - 5))
        screen.blit(time_text, time_rect)
        
    def draw_game_over(self, screen, player_score, ai_score):
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Draw game over panel
        panel_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 - 200, 500, 400)
        pygame.draw.rect(screen, WHITE, panel_rect, border_radius=20)
        pygame.draw.rect(screen, BLACK, panel_rect, 3, border_radius=20)
        
        # Determine winner
        if player_score > ai_score:
            result_text = "You Win!"
            result_color = GREEN
        elif ai_score > player_score:
            result_text = "You Lose!"
            result_color = RED
        else:
            result_text = "It's a Draw!"
            result_color = BLUE
            
        # Draw result with shadow
        result = self.title_font.render(result_text, True, result_color)
        result_shadow = self.title_font.render(result_text, True, (50, 50, 50))
        screen.blit(result_shadow, (panel_rect.centerx - result.get_width()//2 + 3, 120 + 3))
        screen.blit(result, (panel_rect.centerx - result.get_width()//2, 120))
        
        # Draw final score
        score_text = self.menu_font.render(f"Final Score: {player_score} - {ai_score}", True, BLACK)
        screen.blit(score_text, (panel_rect.centerx - score_text.get_width()//2, 200))
        
        # Draw buttons
        for button in self.game_over_buttons:
            button.draw(screen, self.button_font)
            
    def handle_menu_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.menu_buttons:
                button.check_hover(mouse_pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.menu_buttons):
                if button.check_click(mouse_pos, True):
                    return i  # Return button index
        return -1
        
    def handle_player_select_events(self, event):
        # Create continue button if player is selected
        continue_button = None
        if self.selected_player:
            continue_button = Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 60, 300, 50, 
                                "Continue", GREEN, (100, 255, 100), WHITE)
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            # Calculate equal spacing for player buttons
            button_width = 100
            total_width = len(self.player_buttons) * button_width + (len(self.player_buttons) - 1) * 30  # 30px spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            
            # Update player button positions
            for i, button in enumerate(self.player_buttons):
                button.rect.x = start_x + i * (button_width + 30)
                button.rect.y = SCREEN_HEIGHT//2 - 180
                button.check_hover(mouse_pos)
                
            # Check continue button if visible
            if continue_button:
                continue_button.check_hover(mouse_pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check player buttons
            for i, button in enumerate(self.player_buttons):
                if button.check_click(mouse_pos, True):
                    self.selected_player = button.text
                    print(f"Selected player: {self.selected_player}")
                    return None
                    
            # Check continue button if visible
            if continue_button and continue_button.rect.collidepoint(mouse_pos):
                print(f"Continue to difficulty selection with player: {self.selected_player}")
                return "continue"
                    
        return None
        
    def handle_difficulty_select_events(self, event):
        # Create buttons
        start_button = None
        if self.selected_difficulty:
            start_button = Button(SCREEN_WIDTH - 250, SCREEN_HEIGHT - 80, 150, 60, 
                                "Start Game", GREEN, (100, 255, 100), WHITE)
                                
        back_button = Button(100, SCREEN_HEIGHT - 80, 150, 60, "Back", BLUE, (100, 100, 255), WHITE)
        
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            
            # Calculate equal spacing for difficulty buttons
            button_width = 180
            total_width = len(self.difficulty_buttons) * button_width + (len(self.difficulty_buttons) - 1) * 30  # 30px spacing
            start_x = (SCREEN_WIDTH - total_width) // 2
            
            # Update difficulty button positions
            for i, button in enumerate(self.difficulty_buttons):
                button.rect.x = start_x + i * (button_width + 30)
                button.rect.y = SCREEN_HEIGHT//2 - 50
                button.check_hover(mouse_pos)
                
            # Check back button
            back_button.check_hover(mouse_pos)
            
            # Check start button if visible
            if start_button:
                start_button.check_hover(mouse_pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            
            # Check difficulty buttons
            for i, button in enumerate(self.difficulty_buttons):
                if button.check_click(mouse_pos, True):
                    self.selected_difficulty = button.text
                    print(f"Selected difficulty: {self.selected_difficulty}")
                    return None
            
            # Check back button
            if back_button.rect.collidepoint(mouse_pos):
                print("Going back to player selection")
                return "back"
                    
            # Check start button if visible
            if start_button and start_button.rect.collidepoint(mouse_pos):
                print(f"Start button clicked! Player: {self.selected_player}, Difficulty: {self.selected_difficulty}")
                return "start"
                    
        return None
        
    def handle_game_over_events(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.game_over_buttons:
                button.check_hover(mouse_pos)
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            for i, button in enumerate(self.game_over_buttons):
                if button.check_click(mouse_pos, True):
                    return i  # Return button index
        return -1
        
    def draw_background(self, screen):
        # Draw gradient background
        for y in range(0, SCREEN_HEIGHT, 2):
            color_value = int(200 - y / SCREEN_HEIGHT * 100)
            color = (color_value, color_value + 30, 255)
            pygame.draw.line(screen, color, (0, y), (SCREEN_WIDTH, y))
            
        # Draw ground
        pygame.draw.rect(screen, (34, 139, 34), 
                        (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
                        
        # Draw decorative elements
        pygame.draw.circle(screen, WHITE, (100, 100), 40, 2)
        pygame.draw.circle(screen, WHITE, (SCREEN_WIDTH - 100, 100), 40, 2)
        
    def draw_title(self, screen, text, x, y):
        # Draw shadow
        title_shadow = self.title_font.render(text, True, (50, 50, 50))
        screen.blit(title_shadow, (x - title_shadow.get_width()//2 + 3, y + 3))
        
        # Draw text
        title = self.title_font.render(text, True, BLACK)
        screen.blit(title, (x - title.get_width()//2, y))
