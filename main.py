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
                self.game_state = "playing"
            elif event.key == pygame.K_ESCAPE:
                self.game_state = "menu"

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
                
                # Add muzzle flash effect
                angle = math.atan2(
                    self.get_world_mouse_position()[1] - self.player.rect.centery,
                    self.get_world_mouse_position()[0] - self.player.rect.centerx
                )
                muzzle_x = self.player.rect.centerx + math.cos(angle) * (self.player.radius + 5)
                muzzle_y = self.player.rect.centery + math.sin(angle) * (self.player.radius + 5)
                
                self.particle_system.add_explosion(
                    muzzle_x, 
                    muzzle_y, 
                    COLORS['yellow'], 
                    8
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
                    
                    # Add blood particle effect for player
                    self.particle_system.add_blood_effect(
                        self.player.rect.centerx,
                        self.player.rect.centery,
                        count=10
                    )
                    
                    # Do NOT remove the zombie here!

                if zombie.health <= 0:
                    self.wave_manager.zombies.remove(zombie)
                    self.player.score += 100
                    
                    # Add blood splatter and explosion effects
                    self.particle_system.add_blood_effect(
                        zombie.x,
                        zombie.y,
                        count=15
                    )
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
            
            # Add sparkle effect to show pickup appearance
            self.particle_system.add_sparkle(
                position[0],
                position[1],
                COLORS['gold'] if pickup_type == "ammo" else COLORS['green'],
                10
            )

    def update_bullets(self):
        """Update all bullets in the game."""
        for bullet in self.bullets[:]:
            try:
                if hasattr(bullet, 'update') and callable(bullet.update):
                    if isinstance(bullet, Grenade):
                        bullet.update(self)  # Pass in self, which is the game object
                    else:
                        bullet.update()
                        
                        # Add trail for fast bullets (like from sniper rifles)
                        if hasattr(bullet, 'speed') and bullet.speed > 10:
                            self.particle_system.add_trail(
                                bullet.rect.centerx,
                                bullet.rect.centery,
                                bullet.color,
                                3
                            )
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
                    
                    # Add impact particle effect
                    self.particle_system.add_impact(
                        bullet.rect.centerx,
                        bullet.rect.centery,
                        COLORS['white'],
                        12
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
                        
                        # Add blood splatter on hit
                        self.particle_system.add_blood_effect(
                            bullet.rect.centerx,
                            bullet.rect.centery,
                            count=8
                        )
                        # Add hit impact
                        self.particle_system.add_impact(
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
                # Draw zombie with shadow effect
                shadow_radius = zombie.get_render_radius() * 1.2
                pygame.draw.circle(
                    self.screen,
                    COLORS["black"],
                    (int(zombie.x - camera_x + 4), int(zombie.y - camera_y + 4)),
                    int(shadow_radius * 0.9),
                    0
                )
                
                # Draw zombie body
                pygame.draw.circle(
                    self.screen,
                    zombie.get_render_color(),
                    (int(zombie.x - camera_x), int(zombie.y - camera_y)),
                    zombie.get_render_radius()
                )
                
                # Draw zombie eyes
                eye_radius = max(2, zombie.get_render_radius() // 5)
                eye_offset = zombie.get_render_radius() // 3
                
                # Direction to player for eyes
                dx = self.player.rect.centerx - zombie.x
                dy = self.player.rect.centery - zombie.y
                dist = max(1, math.hypot(dx, dy))
                dx, dy = dx / dist, dy / dist
                
                # Left eye
                left_eye_x = int(zombie.x - camera_x - eye_offset + dx * eye_offset * 0.5)
                left_eye_y = int(zombie.y - camera_y - eye_offset + dy * eye_offset * 0.5)
                pygame.draw.circle(self.screen, COLORS["black"], (left_eye_x, left_eye_y), eye_radius)
                
                # Right eye
                right_eye_x = int(zombie.x - camera_x + eye_offset + dx * eye_offset * 0.5)
                right_eye_y = int(zombie.y - camera_y - eye_offset + dy * eye_offset * 0.5)
                pygame.draw.circle(self.screen, COLORS["black"], (right_eye_x, right_eye_y), eye_radius)
                
                # Visual zombie type indicator
                if zombie.type == "fast":
                    speed_indicator_x = int(zombie.x - camera_x)
                    speed_indicator_y = int(zombie.y - camera_y + zombie.get_render_radius() - 5)
                    # Draw speed lines
                    for i in range(3):
                        offset = (i - 1) * 5
                        pygame.draw.line(
                            self.screen, 
                            COLORS["yellow"], 
                            (speed_indicator_x + offset - 5, speed_indicator_y), 
                            (speed_indicator_x + offset - 12, speed_indicator_y),
                            2
                        )
                elif zombie.type == "tank":
                    # Draw armor plates
                    for angle in range(0, 360, 60):
                        rad = math.radians(angle)
                        armor_x = int(zombie.x - camera_x + math.cos(rad) * zombie.get_render_radius() * 0.7)
                        armor_y = int(zombie.y - camera_y + math.sin(rad) * zombie.get_render_radius() * 0.7)
                        pygame.draw.circle(self.screen, COLORS["dark_gray"], (armor_x, armor_y), 4)

                # Draw health bar with fancy styling
                health_pct = zombie.health / zombie.max_health
                bar_width = zombie.get_render_radius() * 2
                bar_height = 4
                bar_bg_rect = (
                    int(zombie.x - camera_x - bar_width // 2),
                    int(zombie.y - camera_y - zombie.get_render_radius() - 8),
                    bar_width,
                    bar_height
                )
                
                # Draw health bar background and border
                pygame.draw.rect(self.screen, COLORS["black"], 
                                (bar_bg_rect[0]-1, bar_bg_rect[1]-1, bar_width+2, bar_height+2))
                
                # Calculate health bar color based on remaining health
                if health_pct > 0.6:
                    health_color = COLORS["green"]
                elif health_pct > 0.3:
                    health_color = COLORS["yellow"]
                else:
                    health_color = COLORS["red"]
                
                # Draw the filled portion
                filled_width = int(bar_width * health_pct)
                pygame.draw.rect(
                    self.screen,
                    health_color,
                    (bar_bg_rect[0], bar_bg_rect[1], filled_width, bar_height)
                )

            except Exception as e:
                print(f"Zombie drawing error: {e}")

        # Draw player with visual enhancements
        try:
            # Draw player shadow
            pygame.draw.circle(
                self.screen,
                COLORS["black"],
                (int(self.player.rect.centerx - camera_x + 3), int(self.player.rect.centery - camera_y + 3)),
                self.player.radius,
                0
            )
            
            # Draw player body
            pygame.draw.circle(
                self.screen,
                self.player.color,
                (int(self.player.rect.centerx - camera_x), int(self.player.rect.centery - camera_y)),
                self.player.radius
            )
            
            # Draw weapon direction indicator
            mouse_pos = pygame.mouse.get_pos()
            world_mouse_x = mouse_pos[0] + camera_x
            world_mouse_y = mouse_pos[1] + camera_y
            
            # Calculate direction to mouse
            dx = world_mouse_x - self.player.rect.centerx
            dy = world_mouse_y - self.player.rect.centery
            angle = math.atan2(dy, dx)
            
            # Draw weapon indicator (gun barrel)
            barrel_length = self.player.radius + 10
            end_x = self.player.rect.centerx + math.cos(angle) * barrel_length
            end_y = self.player.rect.centery + math.sin(angle) * barrel_length
            
            pygame.draw.line(
                self.screen,
                COLORS["dark_gray"],
                (int(self.player.rect.centerx - camera_x), int(self.player.rect.centery - camera_y)),
                (int(end_x - camera_x), int(end_y - camera_y)),
                4
            )
            
            # Draw eyes
            eye_radius = 3
            eye_offset = self.player.radius // 3
            
            # Adjust eye position based on mouse direction
            look_x = math.cos(angle) * eye_offset * 0.5
            look_y = math.sin(angle) * eye_offset * 0.5
            
            # Left eye
            pygame.draw.circle(
                self.screen,
                COLORS["black"],
                (int(self.player.rect.centerx - camera_x - eye_offset + look_x), 
                 int(self.player.rect.centery - camera_y - eye_offset + look_y)),
                eye_radius
            )
            
            # Right eye
            pygame.draw.circle(
                self.screen,
                COLORS["black"],
                (int(self.player.rect.centerx - camera_x + eye_offset + look_x), 
                 int(self.player.rect.centery - camera_y - eye_offset + look_y)),
                eye_radius
            )
            
            # Show player invulnerability effect
            if self.player.invulnerable:
                # Draw shield effect
                shield_radius = self.player.radius + 5
                shield_thickness = 2
                shield_alpha = 128 + int(127 * math.sin(pygame.time.get_ticks() / 100))
                
                # Create a surface with per-pixel alpha
                shield_surface = pygame.Surface((shield_radius*2 + 4, shield_radius*2 + 4), pygame.SRCALPHA)
                pygame.draw.circle(
                    shield_surface,
                    (100, 100, 255, shield_alpha),
                    (shield_radius + 2, shield_radius + 2),
                    shield_radius,
                    shield_thickness
                )
                
                self.screen.blit(
                    shield_surface,
                    (int(self.player.rect.centerx - camera_x - shield_radius - 2),
                     int(self.player.rect.centery - camera_y - shield_radius - 2))
                )

        except Exception as e:
            print(f"Player drawing error: {e}")

        # Draw bullets with effects
        for bullet in self.bullets:
            try:
                if isinstance(bullet, Grenade):
                    # Draw grenade with shadow
                    pygame.draw.circle(
                        self.screen,
                        COLORS["black"],
                        (int(bullet.x - camera_x + 2), int(bullet.y - camera_y + 2)),
                        bullet.radius
                    )
                    
                    # Draw grenade body
                    pygame.draw.circle(
                        self.screen,
                        bullet.color,
                        (int(bullet.x - camera_x), int(bullet.y - camera_y)),
                        bullet.radius
                    )
                    
                    # Draw grenade details (safety pin, etc)
                    pygame.draw.line(
                        self.screen,
                        COLORS["dark_gray"],
                        (int(bullet.x - camera_x - 3), int(bullet.y - camera_y - 3)),
                        (int(bullet.x - camera_x + 3), int(bullet.y - camera_y - 3)),
                        1
                    )
                    
                    # Add trail effect based on lifetime
                    if bullet.lifetime < 60: # Add more trail as it's about to explode
                        trail_intensity = max(0, 60 - bullet.lifetime) / 30
                        for i in range(3):
                            trail_alpha = int(200 * trail_intensity * (3-i)/3)
                            trail_offset = i * 3
                            
                            # Calculate trail position opposite to movement direction
                            trail_x = int(bullet.x - bullet.vx * trail_offset - camera_x) 
                            trail_y = int(bullet.y - bullet.vy * trail_offset - camera_y)
                            
                            # Create a surface with per-pixel alpha
                            trail_surf = pygame.Surface((bullet.radius*2, bullet.radius*2), pygame.SRCALPHA)
                            pygame.draw.circle(
                                trail_surf,
                                (255, 255, 0, trail_alpha),
                                (bullet.radius, bullet.radius),
                                max(1, bullet.radius - i)
                            )
                            
                            self.screen.blit(
                                trail_surf,
                                (trail_x - bullet.radius, trail_y - bullet.radius)
                            )
                else:
                    # Draw regular bullet with trail
                    # Bullet body
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
                    
                    # Add bullet trail
                    if hasattr(bullet, 'vx') and hasattr(bullet, 'vy'):
                        # Draw trail in opposite direction of movement
                        trail_length = 8
                        trail_x = int(bullet.rect.centerx - bullet.vx * trail_length - camera_x)
                        trail_y = int(bullet.rect.centery - bullet.vy * trail_length - camera_y)
                        
                        pygame.draw.line(
                            self.screen,
                            (bullet.color[0]//2, bullet.color[1]//2, bullet.color[2]//2),
                            (int(bullet.rect.centerx - camera_x), int(bullet.rect.centery - camera_y)),
                            (trail_x, trail_y),
                            max(1, bullet.rect.width // 2)
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
