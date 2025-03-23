import pygame
from config import *
import math

class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.hud_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)  # Added small font

        self.main_menu_options = ["Start Game", "Settings", "Quit"]
        self.main_menu_selected = 0
        
        # Settings
        self.settings = {
            "sound_volume": 0.7,
            "music_volume": 0.5,
            "graphics_quality": 1,  # 0: Low, 1: Medium, 2: High
            "difficulty": 1,  # 0: Easy, 1: Normal, 2: Hard
            "show_fps": False,
            "show_minimap": True
        }
        
        # UI States
        self.show_settings = False
        self.settings_selected = 0
        self.settings_options = ["Sound Volume", "Music Volume", "Graphics Quality", 
                                "Difficulty", "Show FPS", "Show Minimap", "Back"]
        
        # Weapon wheel variables
        self.show_weapon_wheel = False
        self.wheel_alpha = 0  # For fade in/out effect
        self.wheel_radius = 150
        self.selected_weapon_index = 0
        
        # Items wheel variables
        self.show_items_wheel = False
        self.items_alpha = 0
        self.items_wheel_radius = 120
        self.selected_item_index = 0
        
        # Pause screen variables
        self.paused = False
        self.pause_options = ["Resume", "Settings", "Quit to Menu"]
        self.pause_selected = 0
        
        # Crosshair properties
        self.crosshair_size = 20
        self.crosshair_thickness = 2
        self.crosshair_color = COLORS["white"]
        self.crosshair_pulse = 0
        self.crosshair_style = 0  # 0: Default, 1: Dot, 2: Circle, 3: Dynamic
        self.crosshair_hit_confirm = False
        self.crosshair_hit_time = 0
        
        # Tutorial tip index for in-game tips
        self.current_tip = 0
        self.tip_display_time = 5000  # Display each tip for 5 seconds
        self.last_tip_change = 0
        self.tips = [
            "Press R to reload your weapon",
            "Use keys 1-6 to switch weapons",
            "Hold TAB to open the weapon wheel",
            "Hold Q to open the items wheel",
            "Press ESC to pause the game",
            "Shotgun is effective at close range",
            "Sniper Rifle deals high damage",
            "Watch your ammo count!"
        ]
        
        # UI animation variables
        self.ui_animations = {
            "settings_offset": HEIGHT,  # For slide-in effect
            "pause_alpha": 0,  # For fade-in effect
            "wheel_rotation": 0,  # For rotation effect
        }

    def draw_main_menu(self, screen):
        """Draws the main menu."""
        screen.fill(COLORS["black"])

        # Draw animated title
        title_color = (
            0, 
            200 + int(55 * math.sin(pygame.time.get_ticks() / 500)), 
            0
        )
        title_text = self.title_font.render("Zombie Survival", True, title_color)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        # Draw subtitle
        subtitle = self.small_font.render("Survive the undead apocalypse", True, COLORS["white"])
        subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 50))
        screen.blit(subtitle, subtitle_rect)

        # Draw menu options with hover effect
        for index, option in enumerate(self.main_menu_options):
            if index == self.main_menu_selected:
                # Draw selection indicator
                indicator_x = WIDTH // 2 - 120
                indicator_y = HEIGHT // 2 + index * 60
                pygame.draw.polygon(screen, COLORS["green"], 
                    [(indicator_x, indicator_y), 
                     (indicator_x + 15, indicator_y + 8), 
                     (indicator_x, indicator_y + 16)])
                
                color = COLORS["green"]
                # Add pulsing effect to selected item
                size = 52 + int(4 * math.sin(pygame.time.get_ticks() / 200))
                option_font = pygame.font.Font(None, size)
            else:
                color = COLORS["white"]
                option_font = self.menu_font
                
            option_text = option_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 60))
            screen.blit(option_text, option_rect)

        # Draw controls help
        controls_text = self.small_font.render("Use arrow keys to navigate, Enter to select", True, COLORS["white"])
        controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        screen.blit(controls_text, controls_rect)

        # Draw version number
        version_text = self.small_font.render("v1.0", True, COLORS["white"])
        version_rect = version_text.get_rect(bottomright=(WIDTH - 10, HEIGHT - 10))
        screen.blit(version_text, version_rect)

    def draw_settings(self, screen):
        """Draw the settings menu with animations"""
        # Update settings menu slide animation
        if "settings_offset" in self.ui_animations:
            target = 0
            current = self.ui_animations["settings_offset"]
            # Animate slide-in effect
            if current > target:
                self.ui_animations["settings_offset"] = max(target, current - 30)
            
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Calculate vertical offset for slide-in animation
        offset_y = self.ui_animations.get("settings_offset", 0)
        
        # Draw title
        title_text = self.menu_font.render("Settings", True, COLORS["white"])
        title_rect = title_text.get_rect(center=(WIDTH // 2, 100 + offset_y))
        screen.blit(title_text, title_rect)
        
        # Draw settings options
        start_y = 180 + offset_y
        for i, option in enumerate(self.settings_options):
            # Determine if this option is selected
            is_selected = i == self.settings_selected
            
            # Choose text color based on selection
            if is_selected:
                color = COLORS["yellow"]
                # Draw selection indicator
                pygame.draw.polygon(screen, COLORS["yellow"], 
                    [(WIDTH // 2 - 150, start_y + i * 50), 
                     (WIDTH // 2 - 130, start_y + i * 50 + 10), 
                     (WIDTH // 2 - 150, start_y + i * 50 + 20)])
            else:
                color = COLORS["white"]
            
            # Draw option text
            option_text = self.menu_font.render(option, True, color)
            option_rect = option_text.get_rect(midleft=(WIDTH // 2 - 120, start_y + i * 50 + 10))
            screen.blit(option_text, option_rect)
            
            # Draw current value/state for each setting
            if option == "Sound Volume":
                self.draw_slider(screen, WIDTH // 2 + 120, start_y + i * 50 + 10, 
                               self.settings["sound_volume"], color)
            elif option == "Music Volume":
                self.draw_slider(screen, WIDTH // 2 + 120, start_y + i * 50 + 10, 
                               self.settings["music_volume"], color)
            elif option == "Graphics Quality":
                quality_labels = ["Low", "Medium", "High"]
                quality = quality_labels[self.settings["graphics_quality"]]
                value_text = self.small_font.render(quality, True, color)
                screen.blit(value_text, (WIDTH // 2 + 120, start_y + i * 50 + 5))
            elif option == "Difficulty":
                difficulty_labels = ["Easy", "Normal", "Hard"]
                difficulty = difficulty_labels[self.settings["difficulty"]]
                value_text = self.small_font.render(difficulty, True, color)
                screen.blit(value_text, (WIDTH // 2 + 120, start_y + i * 50 + 5))
            elif option == "Show FPS":
                state = "ON" if self.settings["show_fps"] else "OFF"
                value_text = self.small_font.render(state, True, color)
                screen.blit(value_text, (WIDTH // 2 + 120, start_y + i * 50 + 5))
            elif option == "Show Minimap":
                state = "ON" if self.settings["show_minimap"] else "OFF"
                value_text = self.small_font.render(state, True, color)
                screen.blit(value_text, (WIDTH // 2 + 120, start_y + i * 50 + 5))
        
        # Draw controls help
        controls_text = self.small_font.render("↑↓: Navigate   ←→: Adjust   Enter: Toggle   Esc: Back", True, COLORS["white"])
        controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT - 50 + offset_y))
        screen.blit(controls_text, controls_rect)

    def draw_slider(self, screen, x, y, value, color):
        """Draw a slider for volume settings"""
        # Draw slider track
        slider_width = 150
        slider_height = 8
        pygame.draw.rect(screen, (50, 50, 50), 
                       (x, y - slider_height // 2, slider_width, slider_height))
        
        # Draw filled portion based on value (0.0 to 1.0)
        filled_width = int(slider_width * value)
        pygame.draw.rect(screen, color, 
                       (x, y - slider_height // 2, filled_width, slider_height))
        
        # Draw slider handle
        handle_x = x + filled_width
        pygame.draw.circle(screen, COLORS["white"], (handle_x, y), 8)
        
        # Draw percentage
        percent_text = self.small_font.render(f"{int(value * 100)}%", True, color)
        screen.blit(percent_text, (x + slider_width + 10, y - 8))

    def draw_hud(self, screen, player, wave):
        """Draw the heads-up display with enhanced visuals"""
        # Health bar with gradient effect
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = HEIGHT - 40
        health_pct = player.health / player.max_health
        
        # Health bar background
        pygame.draw.rect(screen, COLORS["dark_gray"], 
                       (health_x - 2, health_y - 2, health_width + 4, health_height + 4))
        
        # Health bar gradient
        if health_pct > 0:
            for i in range(int(health_width * health_pct)):
                if health_pct > 0.7:
                    # Green to yellow gradient
                    g = 255
                    r = int(255 * (1 - (health_pct - 0.7) / 0.3))
                elif health_pct > 0.3:
                    # Yellow to orange gradient
                    r = 255
                    g = int(255 * (health_pct - 0.3) / 0.4)
                else:
                    # Orange to red gradient
                    r = 255
                    g = int(255 * health_pct / 0.3)
                b = 0
                
                pygame.draw.rect(screen, (r, g, b), 
                              (health_x + i, health_y, 1, health_height))
        
        # Health text
        health_text = self.small_font.render(f"{int(player.health)}/{player.max_health} HP", True, COLORS["white"])
        screen.blit(health_text, (health_x + health_width // 2 - health_text.get_width() // 2, 
                               health_y + health_height // 2 - health_text.get_height() // 2))
        
        # Weapon info
        weapon_x = health_x + health_width + 30
        weapon_y = HEIGHT - 40
        
        # Current weapon display
        if hasattr(player, 'current_weapon'):
            weapon_name = player.current_weapon.name
            weapon_text = self.small_font.render(weapon_name, True, COLORS["white"])
            screen.blit(weapon_text, (weapon_x, weapon_y - 20))
            
            # Ammo display with dynamic coloring
            ammo = player.ammo.get(weapon_name, 0)
            max_ammo = player.current_weapon.max_ammo
            ammo_pct = ammo / max_ammo
            
            if ammo_pct < 0.25:
                ammo_color = COLORS["red"]
            elif ammo_pct < 0.5:
                ammo_color = COLORS["yellow"]
            else:
                ammo_color = COLORS["white"]
                
            ammo_text = self.small_font.render(f"Ammo: {ammo}/{max_ammo}", True, ammo_color)
            screen.blit(ammo_text, (weapon_x, weapon_y))
            
            # Reload indicator
            if player.reloading:
                reload_progress = min(1.0, (pygame.time.get_ticks() - player.reload_start_time) / RELOAD_TIME)
                reload_width = 100 * reload_progress
                pygame.draw.rect(screen, COLORS["yellow"], (weapon_x, weapon_y + 20, reload_width, 5))
                reload_text = self.small_font.render("RELOADING", True, COLORS["yellow"])
                screen.blit(reload_text, (weapon_x + 110, weapon_y + 15))
        
        # Score and wave info
        score_x = WIDTH - 150
        score_y = 20
        
        # Wave display with pulse effect on wave change
        pulse_amount = 0
        if hasattr(self, 'last_wave') and self.last_wave != wave:
            if not hasattr(self, 'wave_pulse_time'):
                self.wave_pulse_time = pygame.time.get_ticks()
            pulse_time = pygame.time.get_ticks() - self.wave_pulse_time
            if pulse_time < 1000:  # Pulse for 1 second
                pulse_amount = 10 * math.sin(pulse_time / 100.0)
            else:
                self.wave_pulse_time = 0
        self.last_wave = wave
        
        wave_text = self.menu_font.render(f"Wave: {wave}", True, COLORS["red"])
        wave_text_rect = wave_text.get_rect(topright=(WIDTH - 20, 20 + pulse_amount))
        screen.blit(wave_text, wave_text_rect)
        
        # Score with animated increase effect
        if not hasattr(self, 'displayed_score'):
            self.displayed_score = 0
        
        if self.displayed_score < player.score:
            self.displayed_score += max(1, (player.score - self.displayed_score) // 10)
        elif self.displayed_score > player.score:  # Just in case
            self.displayed_score = player.score
            
        score_text = self.small_font.render(f"Score: {self.displayed_score}", True, COLORS["white"])
        screen.blit(score_text, (score_x, score_y + 40))
        
        # Draw tutorial tip
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tip_change > self.tip_display_time:
            self.current_tip = (self.current_tip + 1) % len(self.tips)
            self.last_tip_change = current_time
            
        tip_alpha = min(255, (self.tip_display_time - (current_time - self.last_tip_change)) // 10)
        tip_text = self.small_font.render(self.tips[self.current_tip], True, COLORS["white"])
        tip_surface = pygame.Surface((tip_text.get_width() + 20, tip_text.get_height() + 10), pygame.SRCALPHA)
        tip_surface.fill((0, 0, 0, 150))
        tip_surface.blit(tip_text, (10, 5))
        tip_surface.set_alpha(tip_alpha)
        
        tip_x = WIDTH // 2 - tip_surface.get_width() // 2
        tip_y = HEIGHT - 80
        screen.blit(tip_surface, (tip_x, tip_y))
        
        # Dynamic crosshair (changes size on shoot)
        mouse_pos = pygame.mouse.get_pos()
        crosshair_radius = self.crosshair_size // 2 + self.crosshair_pulse
        if self.crosshair_pulse > 0:
            self.crosshair_pulse -= 0.5
            
        # Draw crosshair lines
        pygame.draw.line(screen, self.crosshair_color, 
                      (mouse_pos[0] - crosshair_radius, mouse_pos[1]), 
                      (mouse_pos[0] - crosshair_radius // 2, mouse_pos[1]), 
                      self.crosshair_thickness)
        pygame.draw.line(screen, self.crosshair_color, 
                      (mouse_pos[0] + crosshair_radius // 2, mouse_pos[1]), 
                      (mouse_pos[0] + crosshair_radius, mouse_pos[1]), 
                      self.crosshair_thickness)
        pygame.draw.line(screen, self.crosshair_color, 
                      (mouse_pos[0], mouse_pos[1] - crosshair_radius), 
                      (mouse_pos[0], mouse_pos[1] - crosshair_radius // 2), 
                      self.crosshair_thickness)
        pygame.draw.line(screen, self.crosshair_color, 
                      (mouse_pos[0], mouse_pos[1] + crosshair_radius // 2), 
                      (mouse_pos[0], mouse_pos[1] + crosshair_radius), 
                      self.crosshair_thickness)

    def pulse_crosshair(self):
        """Make crosshair pulse when shooting"""
        self.crosshair_pulse = 5

    def draw_weapon_selector(self, screen, player):
        """Draw weapon selection UI"""
        # Start position for weapon slots
        start_x = 20
        start_y = HEIGHT - 70
        slot_width = 100
        slot_height = 50
        spacing = 10
        
        for i, weapon in enumerate(player.weapons):
            # Determine slot color based on selection
            slot_color = COLORS["blue"] if i == player.current_weapon_index else (50, 50, 50)
            
            # Draw weapon slot box
            pygame.draw.rect(screen, slot_color, 
                           (start_x + i * (slot_width + spacing), start_y, 
                            slot_width, slot_height))
            
            # Draw weapon name
            name_text = self.small_font.render(weapon.name.split()[0], True, COLORS["white"])
            name_rect = name_text.get_rect(center=(
                start_x + i * (slot_width + spacing) + slot_width // 2,
                start_y + 15
            ))
            screen.blit(name_text, name_rect)
            
            # Draw key number
            key_text = self.small_font.render(f"{i+1}", True, COLORS["yellow"])
            key_rect = key_text.get_rect(center=(
                start_x + i * (slot_width + spacing) + slot_width // 2,
                start_y + 35
            ))
            screen.blit(key_text, key_rect)
            
            # Draw ammo counter
            ammo_text = self.small_font.render(f"{player.ammo.get(weapon.name, 0)}", True, COLORS["white"])
            ammo_rect = ammo_text.get_rect(bottomright=(
                start_x + i * (slot_width + spacing) + slot_width - 5,
                start_y + slot_height - 5
            ))
            screen.blit(ammo_text, ammo_rect)

    def draw_minimap(self, screen, player):
        """Draw a minimap in the corner"""
        minimap_size = 150
        minimap_x = WIDTH - minimap_size - 20
        minimap_y = HEIGHT - minimap_size - 20
        
        # Draw minimap background
        pygame.draw.rect(screen, (0, 0, 0, 128), (minimap_x, minimap_y, minimap_size, minimap_size))
        pygame.draw.rect(screen, COLORS["white"], (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Draw player position on minimap
        # Scale coordinates down to fit minimap
        map_scale = minimap_size / MAP_SIZE
        player_minimap_x = minimap_x + int(player.rect.centerx * map_scale)
        player_minimap_y = minimap_y + int(player.rect.centery * map_scale)
        
        # Draw player as a pulsing dot
        pulse_size = 5 + int(2 * math.sin(pygame.time.get_ticks() / 200))
        pygame.draw.circle(screen, COLORS["green"], (player_minimap_x, player_minimap_y), pulse_size)
        
        # Map title
        map_text = self.small_font.render("MINIMAP", True, COLORS["white"])
        map_rect = map_text.get_rect(center=(minimap_x + minimap_size//2, minimap_y - 10))
        screen.blit(map_text, map_rect)

    def draw_tips(self, screen):
        """Draw game tips that change periodically"""
        current_time = pygame.time.get_ticks()
        
        # Change tip if needed
        if current_time - self.last_tip_change > self.tip_display_time:
            self.current_tip = (self.current_tip + 1) % len(self.tips)
            self.last_tip_change = current_time
        
        # Draw tip with fade-in/fade-out effect
        time_in_tip = (current_time - self.last_tip_change) / self.tip_display_time
        
        # Calculate alpha (transparency) for fade effect
        alpha = 255
        if time_in_tip < 0.2:  # Fade in
            alpha = int(255 * (time_in_tip / 0.2))
        elif time_in_tip > 0.8:  # Fade out
            alpha = int(255 * (1 - (time_in_tip - 0.8) / 0.2))
        
        # Create a surface for the text with an alpha channel
        tip_text = self.small_font.render(self.tips[self.current_tip], True, COLORS["yellow"])
        tip_alpha_surface = pygame.Surface(tip_text.get_size(), pygame.SRCALPHA)
        tip_alpha_surface.fill((255, 255, 255, alpha))
        tip_text.blit(tip_alpha_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        
        # Draw the tip at the bottom of the screen
        tip_rect = tip_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(tip_text, tip_rect)

    def draw_crosshair(self, screen, position):
        """Draw dynamic crosshair at the mouse position"""
        x, y = position
        size = self.crosshair_size
        thickness = self.crosshair_thickness
        
        # Pulse the crosshair size
        self.crosshair_pulse = (self.crosshair_pulse + 0.1) % (2 * math.pi)
        pulse_mod = 1 + 0.2 * math.sin(self.crosshair_pulse)
        actual_size = int(size * pulse_mod)
        
        # Draw crosshair lines
        pygame.draw.line(screen, self.crosshair_color, (x - actual_size, y), (x - 5, y), thickness)
        pygame.draw.line(screen, self.crosshair_color, (x + 5, y), (x + actual_size, y), thickness)
        pygame.draw.line(screen, self.crosshair_color, (x, y - actual_size), (x, y - 5), thickness)
        pygame.draw.line(screen, self.crosshair_color, (x, y + 5), (x, y + actual_size), thickness)
        
        # Draw center dot
        pygame.draw.circle(screen, self.crosshair_color, (x, y), 2)

    def draw_game_over(self, screen, score):
        """Draws the game over screen."""
        screen.fill(COLORS["black"])

        # Draw animated game over text
        pulse = math.sin(pygame.time.get_ticks() / 200) * 5
        game_over_size = 72 + int(pulse)
        game_over_font = pygame.font.Font(None, game_over_size)
        
        game_over_text = game_over_font.render("Game Over", True, COLORS["red"])
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)

        # Draw stats with labels
        score_text = self.menu_font.render(f"Final Score: {score:,}", True, COLORS["white"])
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(score_text, score_rect)

        # Add more visual elements to game over screen
        pygame.draw.line(screen, COLORS["red"], (WIDTH//4, HEIGHT//2 + 50), (WIDTH*3//4, HEIGHT//2 + 50), 3)

        # Option buttons with highlight effect
        restart_text = self.menu_font.render("Press R to Restart", True, COLORS["green"])
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3))
        
        # Draw button background that pulses
        pulse_width = int(restart_rect.width + 20 + 10 * math.sin(pygame.time.get_ticks() / 300))
        pygame.draw.rect(screen, (30, 70, 30), 
                       (restart_rect.centerx - pulse_width//2, 
                        restart_rect.centery - restart_rect.height//2 - 5,
                        pulse_width, restart_rect.height + 10))
        
        screen.blit(restart_text, restart_rect)

        menu_text = self.menu_font.render("Press ESC for Menu", True, COLORS["blue"])
        menu_rect = menu_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3 + 60))
        screen.blit(menu_text, menu_rect)

    def main_menu_select_next(self):
        """Selects the next main menu option."""
        self.main_menu_selected = (self.main_menu_selected + 1) % len(self.main_menu_options)

    def main_menu_select_previous(self):
        """Selects the previous main menu option."""
        self.main_menu_selected = (self.main_menu_selected - 1) % len(self.main_menu_options)

    def get_main_menu_selection(self):
        """Returns the currently selected main menu option's index."""
        return self.main_menu_selected

    def draw_enhanced_minimap(self, screen, player, game_map, zombies):
        """Draw an enhanced minimap with zombie positions and fog of war"""
        if not self.settings["show_minimap"]:
            return
            
        minimap_x = WIDTH - 150 - 20
        minimap_y = HEIGHT - 150 - 20
        minimap_size = 150
        
        # Initialize minimap surface if needed
        if not hasattr(self, 'minimap_surface'):
            self.minimap_surface = pygame.Surface((minimap_size, minimap_size))
            self.minimap_overlay = pygame.Surface((minimap_size, minimap_size), pygame.SRCALPHA)
            self.fog_of_war = set()  # Store explored coordinates
            self.minimap_zoom = 1.0
        
        # Clear surfaces
        self.minimap_surface.fill(COLORS["black"])
        self.minimap_overlay.fill((0, 0, 0, 0))
        
        # Calculate visible area based on zoom
        visible_size = MAP_SIZE / self.minimap_zoom
        map_scale = minimap_size / visible_size
        
        # Calculate minimap boundaries
        player_x = player.rect.centerx
        player_y = player.rect.centery
        min_x = max(0, player_x - visible_size // 2)
        min_y = max(0, player_y - visible_size // 2)
        max_x = min(MAP_SIZE, min_x + visible_size)
        max_y = min(MAP_SIZE, min_y + visible_size)
        
        # Update fog of war
        view_radius = 300  # Visible radius around player
        for x in range(int(player_x - view_radius), int(player_x + view_radius), 32):
            for y in range(int(player_y - view_radius), int(player_y + view_radius), 32):
                if 0 <= x < MAP_SIZE and 0 <= y < MAP_SIZE:
                    dist = math.hypot(x - player_x, y - player_y)
                    if dist <= view_radius:
                        self.fog_of_war.add((x // 32, y // 32))
        
        # Draw map terrain (only revealed areas)
        for tile_x in range(int(min_x) // 32, int(max_x) // 32 + 1):
            for tile_y in range(int(min_y) // 32, int(max_y) // 32 + 1):
                if (tile_x, tile_y) in self.fog_of_war:
                    map_x = int((tile_x * 32 - min_x) * map_scale)
                    map_y = int((tile_y * 32 - min_y) * map_scale)
                    tile_size = max(1, int(32 * map_scale))
                    
                    if 0 <= tile_x < game_map.grid_size and 0 <= tile_y < game_map.grid_size:
                        tile_type = game_map.grid[tile_y][tile_x]
                        color = COLORS["dark_gray"]  # Default color
                        if hasattr(game_map, 'tile_defs') and tile_type in game_map.tile_defs:
                            color = game_map.tile_defs[tile_type]["color"]
                        pygame.draw.rect(self.minimap_surface, color,
                                      (map_x, map_y, tile_size, tile_size))
        
        # Draw zombies
        for zombie in zombies:
            if min_x <= zombie.x <= max_x and min_y <= zombie.y <= max_y:
                map_x = int((zombie.x - min_x) * map_scale)
                map_y = int((zombie.y - min_y) * map_scale)
                # Draw zombie dot with type-specific color
                if zombie.type == "fast":
                    color = COLORS["yellow"]
                elif zombie.type == "tank":
                    color = COLORS["dark_red"]
                else:
                    color = COLORS["red"]
                pygame.draw.circle(self.minimap_overlay, color, (map_x, map_y), 3)
        
        # Draw player
        player_map_x = int((player_x - min_x) * map_scale)
        player_map_y = int((player_y - min_y) * map_scale)
        # Draw player view cone
        mouse_pos = pygame.mouse.get_pos()
        view_angle = math.atan2(mouse_pos[1] - HEIGHT//2, mouse_pos[0] - WIDTH//2)
        pygame.draw.polygon(self.minimap_overlay, (0, 255, 0, 64),
                          [(player_map_x, player_map_y),
                           (player_map_x + math.cos(view_angle - 0.5) * 30,
                            player_map_y + math.sin(view_angle - 0.5) * 30),
                           (player_map_x + math.cos(view_angle + 0.5) * 30,
                            player_map_y + math.sin(view_angle + 0.5) * 30)])
        # Draw player dot
        pygame.draw.circle(self.minimap_overlay, COLORS["green"], 
                         (player_map_x, player_map_y), 5)
        
        # Draw minimap frame
        pygame.draw.rect(screen, COLORS["black"], 
                        (minimap_x - 2, minimap_y - 2,
                         minimap_size + 4, minimap_size + 4))
        
        # Blit minimap surfaces
        screen.blit(self.minimap_surface, (minimap_x, minimap_y))
        screen.blit(self.minimap_overlay, (minimap_x, minimap_y))
        
        # Draw border
        pygame.draw.rect(screen, COLORS["white"], 
                        (minimap_x, minimap_y, minimap_size, minimap_size), 2)
        
        # Draw zoom level indicator
        zoom_text = self.small_font.render(f"Zoom: {self.minimap_zoom:.1f}x", True, COLORS["white"])
        screen.blit(zoom_text, (minimap_x, minimap_y - 20))

    def handle_minimap_input(self, event):
        """Handle minimap zoom and interaction"""
        if not hasattr(self, 'minimap_zoom'):
            self.minimap_zoom = 1.0
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                self.minimap_zoom = min(4.0, self.minimap_zoom + 0.2)
                return True
            elif event.button == 5:  # Mouse wheel down
                self.minimap_zoom = max(1.0, self.minimap_zoom - 0.2)
                return True
        return False

    def draw_weapon_wheel(self, screen, player):
        """Draw the weapon selection wheel when TAB is held"""
        if not self.show_weapon_wheel:
            return
            
        # Update alpha for fade-in effect
        self.wheel_alpha = min(200, self.wheel_alpha + 15)
        
        # Create a transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Setup wheel parameters
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        mouse_pos = pygame.mouse.get_pos()
        mouse_dx = mouse_pos[0] - center_x
        mouse_dy = mouse_pos[1] - center_y
        mouse_angle = math.atan2(mouse_dy, mouse_dx)
        
        # Determine selected weapon based on mouse position
        if math.hypot(mouse_dx, mouse_dy) > 20:  # Only select if mouse is away from center
            segments = len(player.weapons)
            segment_angle = 2 * math.pi / segments
            # Adjust angle to start from the top
            adjusted_angle = (mouse_angle + math.pi/2) % (2 * math.pi)
            self.selected_weapon_index = int(adjusted_angle / segment_angle) % segments
        
        # Draw the wheel background
        pygame.draw.circle(screen, (50, 50, 50, self.wheel_alpha), 
                         (center_x, center_y), self.wheel_radius)
        pygame.draw.circle(screen, (30, 30, 30, self.wheel_alpha), 
                         (center_x, center_y), self.wheel_radius, 3)
        
        # Draw weapon segments
        segments = len(player.weapons)
        segment_angle = 2 * math.pi / segments
        
        for i, weapon in enumerate(player.weapons):
            angle = i * segment_angle - math.pi/2  # Start from top
            
            # Calculate segment points
            x1 = center_x + math.cos(angle) * 50  # Inner radius
            y1 = center_y + math.sin(angle) * 50
            x2 = center_x + math.cos(angle) * self.wheel_radius  # Outer radius
            y2 = center_y + math.sin(angle) * self.wheel_radius
            
            # Draw segment divider lines
            pygame.draw.line(screen, COLORS["white"], (x1, y1), (x2, y2), 2)
            
            # Draw weapon names at the appropriate positions
            name_x = center_x + math.cos(angle + segment_angle/2) * (self.wheel_radius * 0.7)
            name_y = center_y + math.sin(angle + segment_angle/2) * (self.wheel_radius * 0.7)
            
            # Determine color based on selection and ammo
            if i == self.selected_weapon_index:
                color = COLORS["yellow"]
            else:
                color = COLORS["white"]
                
            name_text = self.small_font.render(weapon.name.split()[0], True, color)
            name_rect = name_text.get_rect(center=(name_x, name_y))
            screen.blit(name_text, name_rect)
            
            # Draw ammo count
            ammo = player.ammo.get(weapon.name, 0)
            ammo_text = self.small_font.render(f"{ammo}", True, color)
            ammo_rect = ammo_text.get_rect(center=(name_x, name_y + 20))
            screen.blit(ammo_text, ammo_rect)
            
            # Highlight selected segment
            if i == self.selected_weapon_index:
                start_angle = angle
                end_angle = angle + segment_angle
                points = [(center_x, center_y)]
                
                for a in [start_angle + segment_angle * j / 10 for j in range(11)]:
                    points.append((
                        center_x + math.cos(a) * self.wheel_radius,
                        center_y + math.sin(a) * self.wheel_radius
                    ))
                
                pygame.draw.polygon(screen, (255, 255, 0, 30), points)
        
        # Draw center circle with current weapon
        pygame.draw.circle(screen, COLORS["blue"], (center_x, center_y), 40)
        current_text = self.small_font.render("Current", True, COLORS["white"])
        current_rect = current_text.get_rect(center=(center_x, center_y - 10))
        screen.blit(current_text, current_rect)
        
        weapon_text = self.small_font.render(player.current_weapon.name.split()[0], True, COLORS["white"])
        weapon_rect = weapon_text.get_rect(center=(center_x, center_y + 10))
        screen.blit(weapon_text, weapon_rect)
        
        # Draw instruction text
        instruction = self.small_font.render("Release TAB to select", True, COLORS["white"])
        instruction_rect = instruction.get_rect(center=(center_x, center_y + self.wheel_radius + 30))
        screen.blit(instruction, instruction_rect)

    def draw_items_wheel(self, screen, player):
        """Draw the items selection wheel when Q is held"""
        if not self.show_items_wheel:
            return
            
        # Update alpha for fade-in effect
        self.items_alpha = min(200, self.items_alpha + 15)
        
        # Create a transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        screen.blit(overlay, (0, 0))
        
        # Setup wheel parameters
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        mouse_pos = pygame.mouse.get_pos()
        mouse_dx = mouse_pos[0] - center_x
        mouse_dy = mouse_pos[1] - center_y
        mouse_angle = math.atan2(mouse_dy, mouse_dx)
        
        # Draw the wheel background
        pygame.draw.circle(screen, (50, 50, 50, self.items_alpha), 
                         (center_x, center_y), self.items_wheel_radius)
        pygame.draw.circle(screen, (30, 30, 30, self.items_alpha), 
                         (center_x, center_y), self.items_wheel_radius, 3)
        
        # Determine selected item based on mouse position
        if math.hypot(mouse_dx, mouse_dy) > 20 and player.inventory:  # Only select if mouse is away from center
            segments = len(player.inventory)
            segment_angle = 2 * math.pi / segments
            # Adjust angle to start from the top
            adjusted_angle = (mouse_angle + math.pi/2) % (2 * math.pi)
            self.selected_item_index = int(adjusted_angle / segment_angle) % segments
        
        # Draw items if player has any
        if player.inventory:
            segments = len(player.inventory)
            segment_angle = 2 * math.pi / segments
            
            for i, item in enumerate(player.inventory):
                angle = i * segment_angle - math.pi/2  # Start from top
                
                # Calculate segment points
                x1 = center_x + math.cos(angle) * 30  # Inner radius
                y1 = center_y + math.sin(angle) * 30
                x2 = center_x + math.cos(angle) * self.items_wheel_radius  # Outer radius
                y2 = center_y + math.sin(angle) * self.items_wheel_radius
                
                # Draw segment divider lines
                pygame.draw.line(screen, COLORS["white"], (x1, y1), (x2, y2), 2)
                
                # Draw item names at the appropriate positions
                name_x = center_x + math.cos(angle + segment_angle/2) * (self.items_wheel_radius * 0.7)
                name_y = center_y + math.sin(angle + segment_angle/2) * (self.items_wheel_radius * 0.7)
                
                # Determine color based on selection
                if i == self.selected_item_index:
                    color = COLORS["yellow"]
                else:
                    color = COLORS["white"]
                    
                name_text = self.small_font.render(item["name"], True, color)
                name_rect = name_text.get_rect(center=(name_x, name_y))
                screen.blit(name_text, name_rect)
                
                # Highlight selected segment
                if i == self.selected_item_index:
                    start_angle = angle
                    end_angle = angle + segment_angle
                    points = [(center_x, center_y)]
                    
                    for a in [start_angle + segment_angle * j / 10 for j in range(11)]:
                        points.append((
                            center_x + math.cos(a) * self.items_wheel_radius,
                            center_y + math.sin(a) * self.items_wheel_radius
                        ))
                    
                    pygame.draw.polygon(screen, (255, 255, 0, 30), points)
        else:
            # Show "No items" message if inventory is empty
            no_items_text = self.small_font.render("No items", True, COLORS["white"])
            no_items_rect = no_items_text.get_rect(center=(center_x, center_y))
            screen.blit(no_items_text, no_items_rect)
        
        # Draw instruction text
        instruction = self.small_font.render("Release Q to use item", True, COLORS["white"])
        instruction_rect = instruction.get_rect(center=(center_x, center_y + self.items_wheel_radius + 30))
        screen.blit(instruction, instruction_rect)

    def handle_weapon_wheel_input(self, event, player):
        """Handle selection on the weapon wheel"""
        if not self.show_weapon_wheel:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            # Calculate wheel center and mouse position
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            mouse_pos = pygame.mouse.get_pos()
            mouse_dx = mouse_pos[0] - center_x
            mouse_dy = mouse_pos[1] - center_y
            
            # Determine selected weapon based on angle
            if math.hypot(mouse_dx, mouse_dy) > 20:  # Only select if mouse is away from center
                mouse_angle = math.atan2(mouse_dy, mouse_dx)
                segments = len(player.weapons)
                segment_angle = 2 * math.pi / segments
                # Adjust angle to start from the top
                adjusted_angle = (mouse_angle + math.pi/2) % (2 * math.pi)
                new_index = int(adjusted_angle / segment_angle) % segments
                
                # Play sound if selection changed
                if new_index != self.selected_weapon_index:
                    self.selected_weapon_index = new_index
                    return True  # Selection changed
        
        return False

    def handle_items_wheel_input(self, event, player):
        """Handle selection on the items wheel"""
        if not self.show_items_wheel or not player.inventory:
            return False
            
        if event.type == pygame.MOUSEMOTION:
            # Calculate wheel center and mouse position
            center_x, center_y = WIDTH // 2, HEIGHT // 2
            mouse_pos = pygame.mouse.get_pos()
            mouse_dx = mouse_pos[0] - center_x
            mouse_dy = mouse_pos[1] - center_y
            
            # Determine selected item based on angle
            if math.hypot(mouse_dx, mouse_dy) > 20:  # Only select if mouse is away from center
                mouse_angle = math.atan2(mouse_dy, mouse_dx)
                segments = len(player.inventory)
                segment_angle = 2 * math.pi / segments
                # Adjust angle to start from the top
                adjusted_angle = (mouse_angle + math.pi/2) % (2 * math.pi)
                new_index = int(adjusted_angle / segment_angle) % segments
                
                # Play sound if selection changed
                if new_index != self.selected_item_index:
                    self.selected_item_index = new_index
                    return True  # Selection changed
        
        return False
