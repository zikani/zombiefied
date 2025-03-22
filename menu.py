import pygame
from config import *
import math

class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.hud_font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)  # Added small font

        self.main_menu_options = ["Start Game", "Quit"]
        self.main_menu_selected = 0
        
        # Crosshair properties
        self.crosshair_size = 20
        self.crosshair_thickness = 2
        self.crosshair_color = COLORS["white"]
        self.crosshair_pulse = 0
        
        # Tutorial tip index for in-game tips
        self.current_tip = 0
        self.tip_display_time = 5000  # Display each tip for 5 seconds
        self.last_tip_change = 0
        self.tips = [
            "Press R to reload your weapon",
            "Use keys 1-6 to switch weapons",
            "Shotgun is effective at close range",
            "Sniper Rifle deals high damage",
            "Watch your ammo count!"
        ]

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

    def draw_hud(self, screen, player, wave):
        """Draws the in-game HUD."""
        # Health bar with background
        health_percentage = player.health / player.max_health
        health_bar_width = 200
        health_bar_height = 25
        
        # Background
        pygame.draw.rect(screen, COLORS["black"], 
                        (20, 20, health_bar_width, health_bar_height))
        
        # Health bar with dynamic color
        health_color = (
            min(255, 255 * (1 - health_percentage) * 2),  # Red component increases as health decreases
            min(255, 255 * health_percentage * 2),  # Green component increases as health increases
            0
        )
        pygame.draw.rect(screen, health_color, 
                        (20, 20, health_bar_width * health_percentage, health_bar_height))
        
        # Health text overlay
        health_text = self.hud_font.render(f"Health: {player.health}", True, COLORS["white"])
        health_text_rect = health_text.get_rect(center=(20 + health_bar_width//2, 20 + health_bar_height//2))
        screen.blit(health_text, health_text_rect)

        # Weapon info with icon indicator
        weapon = player.current_weapon
        ammo_text = self.hud_font.render(
            f"{weapon.name} ({player.ammo.get(weapon.name, 0)}/{weapon.max_ammo})",
            True, COLORS["ammo"]
        )
        screen.blit(ammo_text, (20, 60))
        
        # Draw weapon selector UI
        self.draw_weapon_selector(screen, player)

        # Wave indicator with visual enhancement
        wave_text = self.hud_font.render(f"Wave: {wave}", True, COLORS["white"])
        wave_rect = wave_text.get_rect(topright=(WIDTH - 20, 20))
        
        # Add wave background
        pygame.draw.rect(screen, COLORS["red"], 
                        (wave_rect.left - 10, wave_rect.top - 5, 
                         wave_rect.width + 20, wave_rect.height + 10))
        
        screen.blit(wave_text, wave_rect)

        # Score with background
        score_text = self.hud_font.render(f"Score: {player.score:,}", True, COLORS["white"])
        score_rect = score_text.get_rect(topright=(WIDTH - 20, 60))
        pygame.draw.rect(screen, (0, 0, 100), 
                        (score_rect.left - 10, score_rect.top - 5, 
                         score_rect.width + 20, score_rect.height + 10))
        screen.blit(score_text, score_rect)

        # Reload indicator
        if player.reloading:
            # Calculate reload progress
            reload_progress = min(1.0, (pygame.time.get_ticks() - player.reload_start_time) / RELOAD_TIME)
            
            # Draw reload progress bar
            bar_width = 200
            pygame.draw.rect(screen, COLORS["black"], (WIDTH // 2 - bar_width//2, 90, bar_width, 20))
            pygame.draw.rect(screen, COLORS["red"], (WIDTH // 2 - bar_width//2, 90, int(bar_width * reload_progress), 20))
            
            reload_text = self.hud_font.render("Reloading...", True, COLORS["red"])
            reload_rect = reload_text.get_rect(center=(WIDTH // 2, 70))
            screen.blit(reload_text, reload_rect)

        # Draw minimap
        self.draw_minimap(screen, player)
        
        # Draw game tips
        self.draw_tips(screen)
        
        # Draw crosshair at mouse position
        mouse_pos = pygame.mouse.get_pos()
        self.draw_crosshair(screen, mouse_pos)

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
