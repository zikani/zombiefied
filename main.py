import pygame
import sys
from config import *
from map import GameMap
from player import Player
from zombie import Zombie
from bullet import Bullet
from wave_manager import WaveManager
from menu import Menu
from particle_collision import ParticleSystem
from sound_manager import SoundManager
from weapon import Pistol, Shotgun

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Survival RPG")
        self.clock = pygame.time.Clock()
        
        # Initialize game systems
        self.game_map = GameMap()
        self.player = Player()
        self.wave_manager = WaveManager()
        self.menu = Menu()
        self.particle_system = ParticleSystem()
        self.sound_manager = SoundManager()
        
        # Game state
        self.state = "menu"
        self.running = True
        self.bullets = []

        # Initialize audio
        self.sound_manager.load_sounds()
        self.sound_manager.play_music("background")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
                
            if self.state == "menu":
                self.handle_menu_input(event)
            elif self.state == "playing":
                self.handle_game_input(event)
            elif self.state == "game_over":
                self.handle_game_over_input(event)

    def handle_menu_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.selected = max(0, self.menu.selected-1)
            elif event.key == pygame.K_DOWN:
                self.menu.selected = min(len(self.menu.options)-1, self.menu.selected+1)
            elif event.key == pygame.K_RETURN:
                if self.menu.selected == 0:
                    self.state = "playing"
                elif self.menu.selected == 1:
                    self.quit_game()

    def handle_game_input(self, event):
        if event.type == pygame.KEYDOWN:
            # Weapon switching
            if event.key == pygame.K_1:
                self.player.current_weapon_index = 0
            elif event.key == pygame.K_2:
                self.player.current_weapon_index = 1
                weapon_name = self.player.current_weapon.name
                if self.player.ammo.get(weapon_name, 0) <= 0:
                    self.player.ammo[weapon_name] = self.player.current_weapon.max_ammo
            # Reloading
            elif event.key == pygame.K_r:
                self.player.reload()
                self.sound_manager.play_sound("reload")
        
        if event.type == pygame.MOUSEBUTTONDOWN and not self.player.reloading:
            self.fire_bullet()

    def handle_game_over_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
                self.state = "playing"
            elif event.key == pygame.K_ESCAPE:
                self.state = "menu"

    def fire_bullet(self):
        current_weapon = self.player.current_weapon
        weapon_name = current_weapon.name
        
        if self.player.ammo.get(weapon_name, 0) > 0:
            # Get camera-adjusted mouse position
            camera_x = self.player.rect.centerx - WIDTH // 2
            camera_y = self.player.rect.centery - HEIGHT // 2
            mouse_x, mouse_y = pygame.mouse.get_pos()
            world_mouse_x = mouse_x + camera_x
            world_mouse_y = mouse_y + camera_y
            
            if current_weapon.fire(
                self.player.rect.center, 
                (world_mouse_x, world_mouse_y), 
                self.bullets
            ):
                self.player.ammo[weapon_name] -= 1
                self.sound_manager.play_sound("shoot")
                self.particle_system.add_explosion(*self.player.rect.center, COLORS['white'], 5)

    def update_game(self):
        # Update reload status
        self.player.update_reload()
        
        # Player movement
        dx, dy = self.player.handle_input()
        self.player.update(dx, dy, self.game_map)

        # Wave updates
        self.wave_manager.update(self.player.rect, self.game_map)

        # Zombie updates
        for zombie in self.wave_manager.zombies[:]:
            zombie.move_towards(
                self.player.rect.centerx,
                self.player.rect.centery,
                self.game_map
            )
            
            if zombie.rect.colliderect(self.player.rect):
                self.player.take_damage(1)
                self.sound_manager.play_sound("player_hurt")
            
            if zombie.health <= 0:
                self.wave_manager.zombies.remove(zombie)
                self.player.score += 100
                self.particle_system.add_explosion(*zombie.rect.center, COLORS['red'], 15)
                self.sound_manager.play_sound("zombie_death")

        # Bullet updates
        for bullet in self.bullets[:]:
            bullet.update()
            
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                continue
                
            if self.game_map.check_collision(bullet.rect.centerx, bullet.rect.centery, 4):
                self.bullets.remove(bullet)
                self.particle_system.add_explosion(*bullet.rect.center, COLORS['white'], 8)
            
            for zombie in self.wave_manager.zombies[:]:
                if bullet.rect.colliderect(zombie.rect):
                    self.bullets.remove(bullet)
                    zombie.take_damage(self.player.current_weapon.damage)
                    break

        self.particle_system.update()

    def draw_game(self):
        # Calculate camera position
        camera_x = self.player.rect.centerx - WIDTH // 2
        camera_y = self.player.rect.centery - HEIGHT // 2
        
        # Draw map
        self.game_map.draw(self.screen, camera_x, camera_y)
        
        # Draw all entities
        entities = [
            (self.player.rect, self.player.color),
            *[(z.rect, z.color) for z in self.wave_manager.zombies],
            *[(b.rect, b.color) for b in self.bullets]
        ]
        
        for rect, color in entities:
            pygame.draw.rect(
                self.screen,
                color,
                (
                    rect.x - camera_x,
                    rect.y - camera_y,
                    rect.width,
                    rect.height
                )
            )
        
        # Draw particles and HUD
        self.particle_system.draw(self.screen)
        self.menu.draw_hud(self.screen, self.player, self.wave_manager.wave)
        pygame.display.flip()

    def reset_game(self):
        self.player = Player()
        self.wave_manager = WaveManager()
        self.bullets = []
        self.particle_system = ParticleSystem()

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while self.running:
            self.handle_events()
            
            if self.state == "menu":
                self.menu.draw_main_menu(self.screen)
                pygame.display.flip()
            elif self.state == "playing":
                self.update_game()
                self.draw_game()
                
                if self.player.health <= 0:
                    self.state = "game_over"
            elif self.state == "game_over":
                self.menu.draw_game_over(self.screen, self.player.score)
                pygame.display.flip()
            
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()