# menu.py
import pygame
from config import *
from weapon import *

class Menu:
    def __init__(self):
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
        self.hud_font = pygame.font.Font(None, 32)
        self.options = ["Start Game", "Quit"]
        self.selected = 0

    def draw_main_menu(self, screen):
        """Draw the main menu screen"""
        screen.fill(COLORS["black"])
        
        # Draw title
        title = self.title_font.render("Zombie Survival", True, COLORS["green"])
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
        screen.blit(title, title_rect)

        # Draw menu options
        for i, text in enumerate(self.options):
            color = COLORS["white"] if i != self.selected else COLORS["green"]
            text_surf = self.font.render(text, True, color)
            text_rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2 + i*60))
            screen.blit(text_surf, text_rect)

    def draw_hud(self, screen, player, wave):
        """Draw in-game heads-up display"""
        # Health display
        health_text = self.hud_font.render(f"Health: {player.health}", True, COLORS["white"])
        screen.blit(health_text, (20, 20))

        # Ammo display
        weapon = player.current_weapon
        ammo_text = self.hud_font.render(
            f"{weapon.name} ({player.ammo.get(weapon.name, 0)}/{weapon.max_ammo})", 
            True, 
            COLORS["ammo"]
        )
        screen.blit(ammo_text, (20, 60))

        # Wave display
        wave_text = self.hud_font.render(f"Wave: {wave}", True, COLORS["white"])
        wave_rect = wave_text.get_rect(topright=(WIDTH-20, 20))
        screen.blit(wave_text, wave_rect)

        # Score display
        score_text = self.hud_font.render(f"Score: {player.score}", True, COLORS["white"])
        score_rect = score_text.get_rect(topright=(WIDTH-20, 60))
        screen.blit(score_text, score_rect)

        # Weapon display
        weapon_text = self.hud_font.render(
            f"{player.current_weapon.name} ({player.ammo}/{player.current_weapon.max_ammo})", 
            True, 
            COLORS["white"]
        )
        screen.blit(weapon_text, (WIDTH//2 - 100, 20))
        
        # Reload indicator
        if player.reloading:
            reload_text = self.hud_font.render("Reloading...", True, COLORS["red"])
            screen.blit(reload_text, (WIDTH//2 - 50, 60))

    def draw_game_over(self, screen, score):
        """Draw game over screen"""
        screen.fill(COLORS["black"])
        
        # Game over text
        title = self.title_font.render("Game Over", True, COLORS["red"])
        title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//3))
        screen.blit(title, title_rect)

        # Score display
        score_text = self.font.render(f"Final Score: {score}", True, COLORS["white"])
        score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(score_text, score_rect)

        # Restart prompt
        restart_text = self.font.render("Press R to restart", True, COLORS["white"])
        restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT*2//3))
        screen.blit(restart_text, restart_rect)