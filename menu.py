import pygame
from config import *

class Menu:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 72)
        self.menu_font = pygame.font.Font(None, 48)
        self.hud_font = pygame.font.Font(None, 32)

        self.main_menu_options = ["Start Game", "Quit"]
        self.main_menu_selected = 0

    def draw_main_menu(self, screen):
        """Draws the main menu."""
        screen.fill(COLORS["black"])

        title_text = self.title_font.render("Zombie Survival", True, COLORS["green"])
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        for index, option in enumerate(self.main_menu_options):
            color = COLORS["green"] if index == self.main_menu_selected else COLORS["white"]
            option_text = self.menu_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + index * 60))
            screen.blit(option_text, option_rect)

    def draw_hud(self, screen, player, wave):
        """Draws the in-game HUD."""
        health_text = self.hud_font.render(f"Health: {player.health}", True, COLORS["white"])
        screen.blit(health_text, (20, 20))

        weapon = player.current_weapon
        ammo_text = self.hud_font.render(
            f"{weapon.name} ({player.ammo.get(weapon.name, 0)}/{weapon.max_ammo})",
            True, COLORS["ammo"]
        )
        screen.blit(ammo_text, (20, 60))

        wave_text = self.hud_font.render(f"Wave: {wave}", True, COLORS["white"])
        wave_rect = wave_text.get_rect(topright=(WIDTH - 20, 20))
        screen.blit(wave_text, wave_rect)

        score_text = self.hud_font.render(f"Score: {player.score:,}", True, COLORS["white"]) #added commas to score.
        score_rect = score_text.get_rect(topright=(WIDTH - 20, 60))
        screen.blit(score_text, score_rect)

        if player.reloading:
            reload_text = self.hud_font.render("Reloading...", True, COLORS["red"])
            screen.blit(reload_text, (WIDTH // 2 - 50, 60))

    def draw_game_over(self, screen, score):
        """Draws the game over screen."""
        screen.fill(COLORS["black"])

        game_over_text = self.title_font.render("Game Over", True, COLORS["red"])
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(game_over_text, game_over_rect)

        score_text = self.menu_font.render(f"Final Score: {score:,}", True, COLORS["white"]) #added commas to score.
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(score_text, score_rect)

        restart_text = self.menu_font.render("Press R to Restart", True, COLORS["white"])
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT * 2 // 3))
        screen.blit(restart_text, restart_rect)

    def main_menu_select_next(self):
        """Selects the next main menu option."""
        self.main_menu_selected = (self.main_menu_selected + 1) % len(self.main_menu_options)

    def main_menu_select_previous(self):
        """Selects the previous main menu option."""
        self.main_menu_selected = (self.main_menu_selected - 1) % len(self.main_menu_options)

    def get_main_menu_selection(self):
        """Returns the currently selected main menu option's index."""
        return self.main_menu_selected
