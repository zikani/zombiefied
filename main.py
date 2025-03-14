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
from weapon import *
import math

class Game:
    def __init__(self):
        # Initialize core systems
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Zombie Survival RPG")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_state = "menu"

        # Game systems initialization
        self.game_map = GameMap()
        
        self.player = Player(self.game_map)
        self.wave_manager = WaveManager()
        self.menu = Menu()
        self.particle_system = ParticleSystem()
        self.sound_manager = SoundManager()
        
        # Initialize collections
        self.bullets = []

        # Audio setup
        self.initialize_audio()

    def initialize_audio(self):
        """Load and configure game audio"""
        try:
            self.sound_manager.load_sounds()
            self.sound_manager.play_music("background")
        except Exception as e:
            print(f"Audio initialization error: {e}")

    def handle_events(self):
        """Main event handling loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()

            # State-specific input handling
            if self.game_state == "menu":
                self.handle_menu_input(event)
            elif self.game_state == "playing":
                self.handle_game_input(event)
            elif self.game_state == "game_over":
                self.handle_game_over_input(event)

    def handle_menu_input(self, event):
        """Process menu screen inputs"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.main_menu_select_previous()
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_DOWN:
                self.menu.main_menu_select_next()
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_RETURN:
                self.sound_manager.play_sound("menu_select")
                if self.menu.get_main_menu_selection() == 0:
                    self.game_state = "playing"
                    self.reset_game()
                else:
                    self.quit_game()

    def handle_game_input(self, event):
        """Process in-game inputs."""
        if event.type == pygame.KEYDOWN:
            # Weapon management
            if event.key == pygame.K_1:
                self.safe_weapon_switch(0)
            elif event.key == pygame.K_2:
                self.safe_weapon_switch(1)
            elif event.key == pygame.K_3:
                self.safe_weapon_switch(2)
            elif event.key == pygame.K_4:
                self.safe_weapon_switch(3)
            elif event.key == pygame.K_5:
                self.safe_weapon_switch(4)
            elif event.key == pygame.K_6:
                self.safe_weapon_switch(5)
            elif event.key == pygame.K_r:
                self.initiate_reload()
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"

    def handle_game_over_input(self, event):
        """Process game over screen inputs"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
                self.game_state = "playing"  # Fixed: changed self.state to self.game_state
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"  # Fixed: changed self.state to self.game_state

    def safe_weapon_switch(self, index):
        """Safely switch weapons with validation"""
        if hasattr(self.player, 'weapons') and 0 <= index < len(self.player.weapons):
            self.player.current_weapon_index = index
            weapon_name = self.player.current_weapon.name
            # Initialize ammo if missing
            if self.player.ammo.get(weapon_name, 0) <= 0:
                self.player.ammo[weapon_name] = self.player.current_weapon.max_ammo
            self.sound_manager.play_sound("weapon_switch")

    def initiate_reload(self):
        """Start reload process with validation"""
        if hasattr(self.player, 'reloading') and not self.player.reloading:
            self.player.reload()
            self.sound_manager.play_sound("reload")

    def update_game(self):
        """Main game update loop"""
        # Process player input
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        # Calculate movement direction
        dx = (keys[pygame.K_d] or keys[pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[pygame.K_LEFT])
        dy = (keys[pygame.K_s] or keys[pygame.K_DOWN]) - (keys[pygame.K_w] or keys[pygame.K_UP])
        
        # Handle weapon switching via mouse wheel
        weapon_switch = 0
        
        # Check if shooting
        shoot = mouse_buttons[0]  # Left mouse button
        
        # Get world mouse position
        world_mouse = self.get_world_mouse_position()
        
        # Update player state
        self.player.update(
            dx, dy,
            self.game_map,
            world_mouse[0],
            world_mouse[1],
            weapon_switch,
            shoot
        )
        
        # Handle shooting
        if shoot and hasattr(self.player, 'reloading') and not self.player.reloading:
            self.handle_shooting()

        # Update game systems
        self.update_wave_manager()
        self.update_zombies()
        self.update_bullets()
        self.particle_system.update()

    def get_world_mouse_position(self):
        """Convert screen mouse position to world coordinates"""
        camera_pos = (
            self.player.rect.centerx - WIDTH//2,
            self.player.rect.centery - HEIGHT//2
        )
        screen_mouse = pygame.mouse.get_pos()
        return (
            screen_mouse[0] + camera_pos[0],
            screen_mouse[1] + camera_pos[1]
        )

    def handle_shooting(self):
        """Handle bullet firing mechanics"""
        weapon = self.player.current_weapon
        if self.player.ammo.get(weapon.name, 0) > 0:
            if weapon.fire(self.player.rect.center, self.get_world_mouse_position(), self.bullets):
                self.player.ammo[weapon.name] -= 1
                self.sound_manager.play_sound("shoot")
                self.particle_system.add_explosion(
                    self.player.rect.centerx, 
                    self.player.rect.centery, 
                    COLORS['white'], 
                    5
                )

    def update_wave_manager(self):
        """Update wave spawning system"""
        try:
            self.wave_manager.update(self.player.rect, self.game_map)
        except Exception as e:
            print(f"Wave update error: {e}")

    def update_zombies(self):
        """Update all zombies in the game"""
        for zombie in self.wave_manager.zombies[:]:
            try:
                zombie.move_towards(
                    self.player.rect.centerx,
                    self.player.rect.centery,
                    self.game_map
                )

                # Circle collision check
                distance = math.hypot(zombie.x - self.player.rect.centerx, zombie.y - self.player.rect.centery)
                if distance < zombie.radius + self.player.radius:
                    self.player.take_damage(1)
                    self.sound_manager.play_sound("player_hurt")
                    self.player.apply_knockback(zombie.x, zombie.y)
                    
                    # Do NOT remove the zombie here!

                if zombie.health <= 0:
                    self.wave_manager.zombies.remove(zombie)
                    self.player.score += 100
                    self.particle_system.add_explosion(
                        zombie.x,
                        zombie.y,
                        COLORS['red'],
                        15
                    )
                    self.sound_manager.play_sound("zombie_death")
                    self.try_spawn_pickup((zombie.x, zombie.y))
            except Exception as e:
                print(f"Zombie update error: {e}")
                if zombie in self.wave_manager.zombies:
                    self.wave_manager.zombies.remove(zombie)

    def try_spawn_pickup(self, position):
        """Attempt to spawn a pickup at the given position"""
        import random
        if random.random() < 0.1:  # 10% chance
            pickup_type = random.choice(["health", "ammo"])
            # Implement pickup spawning here
            print(f"Spawned {pickup_type} pickup at {position}")

    def update_bullets(self):
        """Update all bullets in the game."""
        for bullet in self.bullets[:]:
            try:
                if hasattr(bullet, 'update') and callable(bullet.update):
                    if isinstance(bullet, Grenade):
                        bullet.update(self)  # Pass in self, which is the game object
                    else:
                        bullet.update()
                else:
                    print(f"Warning: Bullet object {bullet} does not have an update method.")
                    # Remove bullets without update method to prevent further issues
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    continue  # Skip the rest of the loop for this bullet

                # Safety check for bullet rect
                if not hasattr(bullet, 'rect'):
                    print(f"Warning: Bullet object {bullet} does not have a rect attribute.")
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    continue

                if hasattr(bullet, 'is_off_screen') and callable(bullet.is_off_screen) and bullet.is_off_screen():
                    self.bullets.remove(bullet)
                    continue

                if self.game_map.check_collision(bullet.rect.centerx, bullet.rect.centery, 4):
                    self.bullets.remove(bullet)
                    self.particle_system.add_explosion(
                        bullet.rect.centerx,
                        bullet.rect.centery,
                        COLORS['white'],
                        8
                    )
                    self.sound_manager.play_sound("bullet_impact")
                    continue  # Skip zombie collision check

                for zombie in self.wave_manager.zombies[:]:
                    # Circle-rectangle collision check
                    dx = max(zombie.x - bullet.rect.centerx, 0, bullet.rect.centerx - zombie.x)
                    dy = max(zombie.y - bullet.rect.centery, 0, bullet.rect.centery - zombie.y)
                    distance = math.hypot(dx, dy)
                    if distance <= zombie.radius:
                        if bullet in self.bullets:  # Check if bullet still exists
                            self.bullets.remove(bullet)
                        zombie.take_damage(self.player.current_weapon.damage)
                        # Add hit effects
                        self.particle_system.add_explosion(
                            bullet.rect.centerx,
                            bullet.rect.centery,
                            COLORS['red'],
                            5
                        )
                        self.sound_manager.play_sound("zombie_hit")
                        break  # Break zombie loop

            except Exception as e:
                print(f"Error updating bullet: {e}")
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

    def draw_game(self):
        """Render all game elements"""
        try:
            # Calculate camera position
            camera_x = self.player.rect.centerx - WIDTH//2
            camera_y = self.player.rect.centery - HEIGHT//2
            
            # Draw game world
            self.game_map.draw(self.screen, camera_x, camera_y)
            self.draw_entities(camera_x, camera_y)
            self.particle_system.draw(self.screen, camera_x, camera_y)
            
            # Draw UI elements
            self.menu.draw_hud(self.screen, self.player, self.wave_manager.wave)
            
            pygame.display.flip()
        except Exception as e:
            print(f"Rendering error: {e}")

    def draw_entities(self, camera_x, camera_y):
        """Draw all game entities with camera offset"""

        # Draw zombies first (under player)
        for zombie in self.wave_manager.zombies:
            try:
                # Draw zombie as a circle
                pygame.draw.circle(
                    self.screen,
                    zombie.get_render_color(),
                    (int(zombie.x - camera_x), int(zombie.y - camera_y)),
                    zombie.get_render_radius()
                )

                # Draw health bar
                health_pct = zombie.health / zombie.max_health
                bar_width = zombie.get_render_radius() * 2
                filled_width = int(bar_width * health_pct)

                pygame.draw.rect(
                    self.screen,
                    COLORS['red'],
                    (
                        int(zombie.x - camera_x - bar_width // 2),
                        int(zombie.y - camera_y - zombie.get_render_radius() - 10),
                        filled_width,
                        3
                    )
                )
                
                # Ensure zombie has the draw_type_indicator method
                if hasattr(zombie, 'draw_type_indicator') and callable(zombie.draw_type_indicator):
                    zombie.draw_type_indicator(self.screen, camera_x, camera_y)

            except Exception as e:
                print(f"Zombie drawing error: {e}")

        # Draw player
        try:
            pygame.draw.circle(
                self.screen,
                self.player.color,
                (int(self.player.rect.centerx - camera_x), int(self.player.rect.centery - camera_y)),
                self.player.radius
            )

        except Exception as e:
            print(f"Player drawing error: {e}")

        # Draw bullets
        for bullet in self.bullets:
            try:
                pygame.draw.rect(
                    self.screen,
                    bullet.color,
                    (
                        int(bullet.rect.x - camera_x),
                        int(bullet.rect.y - camera_y),
                        bullet.rect.width,
                        bullet.rect.height
                    )
                )
            except Exception as e:
                print(f"Bullet drawing error: {e}")

    def reset_game(self):
        """Reset game state to initial values"""
        try:
            self.player = Player(self.game_map)
            self.wave_manager = WaveManager()
            self.bullets = []
            self.particle_system = ParticleSystem()
            self.sound_manager.play_sound("game_start")
        except Exception as e:
            print(f"Game reset error: {e}")
            self.quit_game()

    def quit_game(self):
        """Clean up and exit game"""
        pygame.quit()
        sys.exit()

    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            
            if self.game_state == "menu":
                # Draw main menu
                self.screen.fill(COLORS['black'])
                self.menu.draw_main_menu(self.screen)
                pygame.display.flip()
            
            elif self.game_state == "playing":
                # Update and draw game state
                self.update_game()
                
                # Check player survival
                if self.player.health <= 0:
                    self.game_state = "game_over"
                    self.sound_manager.play_sound("game_over")
                    self.sound_manager.stop_music()
                
                self.draw_game()
            
            elif self.game_state == "game_over":
                # Draw game over screen
                self.screen.fill(COLORS['black'])
                self.menu.draw_game_over(self.screen, self.player.score)
                pygame.display.flip()
            
            # Maintain consistent frame rate
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
