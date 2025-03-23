from logging import DEBUG
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
import random
import traceback

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
                # Check if game is paused first
                if self.menu.paused:
                    self.handle_pause_input(event)
                else:
                    self.handle_game_input(event)
                    # Handle minimap input if available
                    if hasattr(self.menu, 'handle_minimap_input'):
                        self.menu.handle_minimap_input(event)
            elif self.game_state == "game_over":
                self.handle_game_over_input(event)

    def handle_menu_input(self, event):
        """Process menu screen inputs"""
        if self.menu.show_settings:
            self.handle_settings_input(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.main_menu_selected = (self.menu.main_menu_selected - 1) % len(self.menu.main_menu_options)
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_DOWN:
                self.menu.main_menu_selected = (self.menu.main_menu_selected + 1) % len(self.menu.main_menu_options)
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_RETURN:
                self.sound_manager.play_sound("menu_select")
                selection = self.menu.main_menu_selected
                if selection == 0:  # Start Game
                    self.game_state = "playing"
                    self.reset_game()
                elif selection == 1:  # Settings
                    self.menu.show_settings = True
                    self.menu.settings_selected = 0
                    self.menu.ui_animations["settings_offset"] = HEIGHT
                elif selection == 2:  # Quit
                    self.quit_game()

    def handle_settings_input(self, event):
        """Process settings menu inputs"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.menu.show_settings = False
                self.sound_manager.play_sound("menu_move")
                return
            
            if event.key == pygame.K_UP:
                self.menu.settings_selected = (self.menu.settings_selected - 1) % len(self.menu.settings_options)
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_DOWN:
                self.menu.settings_selected = (self.menu.settings_selected + 1) % len(self.menu.settings_options)
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_RETURN:
                self.sound_manager.play_sound("menu_select")
                selected_option = self.menu.settings_options[self.menu.settings_selected]
                if selected_option == "Back":
                    self.menu.show_settings = False
                elif selected_option == "Show FPS":
                    self.menu.settings["show_fps"] = not self.menu.settings["show_fps"]
                elif selected_option == "Show Minimap":
                    self.menu.settings["show_minimap"] = not self.menu.settings["show_minimap"]
            elif event.key == pygame.K_LEFT:
                self.adjust_setting(-1)
            elif event.key == pygame.K_RIGHT:
                self.adjust_setting(1)

    def adjust_setting(self, direction):
        """Adjust the selected setting value"""
        selected_option = self.menu.settings_options[self.menu.settings_selected]
        
        if selected_option == "Sound Volume":
            new_vol = max(0.0, min(1.0, self.menu.settings["sound_volume"] + direction * 0.1))
            self.menu.settings["sound_volume"] = new_vol
            self.sound_manager.set_sound_volume(new_vol)
            self.sound_manager.play_sound("menu_move")
        elif selected_option == "Music Volume":
            new_vol = max(0.0, min(1.0, self.menu.settings["music_volume"] + direction * 0.1))
            self.menu.settings["music_volume"] = new_vol
            self.sound_manager.set_music_volume(new_vol)
        elif selected_option == "Graphics Quality":
            new_val = max(0, min(2, self.menu.settings["graphics_quality"] + direction))
            self.menu.settings["graphics_quality"] = new_val
            self.sound_manager.play_sound("menu_move")
        elif selected_option == "Difficulty":
            new_val = max(0, min(2, self.menu.settings["difficulty"] + direction))
            self.menu.settings["difficulty"] = new_val
            self.sound_manager.play_sound("menu_move")

    def handle_pause_input(self, event):
        """Process pause menu inputs"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.menu.paused = False
                self.menu.ui_animations["pause_alpha"] = 0
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_UP:
                self.menu.pause_selected = (self.menu.pause_selected - 1) % len(self.menu.pause_options)
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_DOWN:
                self.menu.pause_selected = (self.menu.pause_selected + 1) % len(self.menu.pause_options)
                self.sound_manager.play_sound("menu_move")
            elif event.key == pygame.K_RETURN:
                self.sound_manager.play_sound("menu_select")
                selection = self.menu.pause_selected
                if selection == 0:  # Resume
                    self.menu.paused = False
                    self.menu.ui_animations["pause_alpha"] = 0
                elif selection == 1:  # Settings
                    self.menu.show_settings = True
                    self.menu.settings_selected = 0
                    self.menu.ui_animations["settings_offset"] = HEIGHT
                elif selection == 2:  # Quit to Menu
                    self.game_state = "menu"
                    self.menu.paused = False
                    self.menu.ui_animations["pause_alpha"] = 0

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
                # Toggle pause
                self.menu.paused = True
                self.menu.pause_selected = 0
                self.sound_manager.play_sound("menu_select")
            elif event.key == pygame.K_TAB:
                # Show weapon wheel
                self.menu.show_weapon_wheel = True
                self.menu.wheel_alpha = 0
            elif event.key == pygame.K_q:
                # Show items wheel
                self.menu.show_items_wheel = True
                self.menu.items_alpha = 0
            elif event.key == pygame.K_c:
                # Cycle crosshair style
                if hasattr(self.menu, 'crosshair_style'):
                    self.menu.crosshair_style = (self.menu.crosshair_style + 1) % 4
                    self.sound_manager.play_sound("menu_select")
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:
                # Hide weapon wheel and apply selection
                if self.menu.show_weapon_wheel:
                    self.safe_weapon_switch(self.menu.selected_weapon_index)
                    self.menu.show_weapon_wheel = False
            elif event.key == pygame.K_q:
                # Hide items wheel and use selected item
                if self.menu.show_items_wheel:
                    self.use_selected_item()
                    self.menu.show_items_wheel = False
        
        # Handle wheel input if showing
        if self.menu.show_weapon_wheel:
            if hasattr(self.menu, 'handle_weapon_wheel_input'):
                if self.menu.handle_weapon_wheel_input(event, self.player):
                    self.sound_manager.play_sound("menu_move")
                    
        if self.menu.show_items_wheel:
            if hasattr(self.menu, 'handle_items_wheel_input'):
                if self.menu.handle_items_wheel_input(event, self.player):
                    self.sound_manager.play_sound("menu_move")

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

    def use_selected_item(self):
        """Use the currently selected item from player's inventory"""
        if hasattr(self.player, 'inventory') and self.player.inventory:
            try:
                if 0 <= self.menu.selected_item_index < len(self.player.inventory):
                    item = self.player.inventory[self.menu.selected_item_index]
                    
                    # Apply item effect based on type
                    if item["type"] == "health":
                        # Health item: restore player health
                        self.player.health = min(self.player.max_health, self.player.health + item["value"])
                        self.sound_manager.play_sound("health_pickup")
                    elif item["type"] == "ammo":
                        # Ammo item: add ammo to current weapon
                        weapon_name = self.player.current_weapon.name
                        self.player.ammo[weapon_name] += item["value"]
                        self.sound_manager.play_sound("ammo_pickup")
                    elif item["type"] == "grenade":
                        # Grenade: damage all zombies in radius
                        self.throw_grenade(item["value"])
                        self.sound_manager.play_sound("explosion")
                    elif item["type"] == "speed":
                        # Speed boost: temporarily increase player speed
                        self.player.speed += item["value"]
                        # Schedule speed return after 10 seconds
                        pygame.time.set_timer(pygame.USEREVENT + 1, 10000)
                    
                    # Remove used item
                    self.player.inventory.pop(self.menu.selected_item_index)
                    
                    # Reset selected index if needed
                    if not self.player.inventory:
                        self.menu.selected_item_index = 0
                    elif self.menu.selected_item_index >= len(self.player.inventory):
                        self.menu.selected_item_index = len(self.player.inventory) - 1
            except Exception as e:
                print(f"Error using item: {e}")

    def throw_grenade(self, damage):
        """Throw a grenade that damages zombies in radius"""
        try:
            # Get player position
            center_x, center_y = self.player.rect.centerx, self.player.rect.centery
            
            # Get mouse position for throw direction
            mouse_pos = pygame.mouse.get_pos()
            world_mouse_x = mouse_pos[0] + (self.player.rect.centerx - WIDTH // 2)
            world_mouse_y = mouse_pos[1] + (self.player.rect.centery - HEIGHT // 2)
            
            # Calculate throw direction
            dx = world_mouse_x - center_x
            dy = world_mouse_y - center_y
            distance = max(1, math.hypot(dx, dy))
            dx, dy = dx / distance, dy / distance
            
            # Calculate grenade landing position (throw distance of 200 pixels)
            throw_distance = 200
            grenade_x = center_x + dx * throw_distance
            grenade_y = center_y + dy * throw_distance
            
            # Create explosion particles
            explosion_radius = 150
            self.particle_system.add_explosion(grenade_x, grenade_y, explosion_radius)
            
            # Damage zombies in radius
            for zombie in self.wave_manager.zombies[:]:  # Use a copy to allow removal
                distance = math.hypot(zombie.x - grenade_x, zombie.y - grenade_y)
                if distance < explosion_radius:
                    # Calculate damage based on distance (more damage closer to center)
                    distance_factor = 1 - (distance / explosion_radius)
                    actual_damage = damage * distance_factor
                    
                    # Apply damage with knockback
                    zombie.take_damage(actual_damage)
                    
                    # Add knockback effect
                    knockback_strength = 20 * distance_factor
                    knockback_dx = (zombie.x - grenade_x) / distance * knockback_strength
                    knockback_dy = (zombie.y - grenade_y) / distance * knockback_strength
                    zombie.x += knockback_dx
                    zombie.y += knockback_dy
                    
                    # Add damage indicator
                    self.add_damage_indicator(zombie.x, zombie.y, actual_damage)
                    
                    # Check if zombie died
                    if zombie.health <= 0 and zombie in self.wave_manager.zombies:
                        self.player.score += zombie.score_value
                        self.wave_manager.zombies.remove(zombie)
        except Exception as e:
            print(f"Error throwing grenade: {e}")

    def initiate_reload(self):
        """Start reload process with validation"""
        if hasattr(self.player, 'reloading') and not self.player.reloading:
            self.player.reload()
            self.sound_manager.play_sound("reload")

    def update_game(self):
        """Main game update loop"""
        # Get player input
        keys = pygame.key.get_pressed()
        mouse_press = pygame.mouse.get_pressed()
        
        # Movement directions
        dx, dy = 0, 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1
        
        # Weapon switching via scroll wheel is handled in event processing
        weapon_switch = None
        
        # Get shoot input (left mouse button)
        shoot = mouse_press[0]
        
        # Update player
        self.player.update(
            dx, dy, self.game_map,
            pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1],
            weapon_switch, shoot
        )
        
        # Handle shooting
        if shoot and hasattr(self.player, 'reloading') and not self.player.reloading:
            self.handle_shooting()

        # Update game systems
        self.update_wave_manager()
        self.update_zombies()
        self.update_bullets()
        self.update_pickups()
        self.update_damage_indicators()
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
                
                # Make crosshair pulse when shooting
                if hasattr(self.menu, 'pulse_crosshair'):
                    self.menu.pulse_crosshair()

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
                    
                    # Add damage indicator
                    self.add_damage_indicator(self.player.rect.centerx, self.player.rect.centery, 1, is_player=True)
                    
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
        if random.random() < 0.2:  # Increased to 20% chance for better testing
            pickup_type = random.choice(["health", "ammo"])
            
            # Initialize pickups list if it doesn't exist
            if not hasattr(self, 'pickups'):
                self.pickups = []
                
            # Create a new pickup
            pickup = {
                "type": pickup_type,
                "x": position[0],
                "y": position[1],
                "radius": 15,
                "value": 30 if pickup_type == "health" else 20,  # Health or ammo amount
                "color": COLORS['green'] if pickup_type == "health" else COLORS['gold'],
                "pulse": 0,  # For visual effect
                "lifetime": 600  # 10 seconds at 60 FPS
            }
            
            self.pickups.append(pickup)
            print(f"Spawned {pickup_type} pickup at {position}")
            
            # Add sparkle effect to show pickup appearance
            self.particle_system.add_sparkle(
                position[0],
                position[1],
                COLORS['gold'] if pickup_type == "ammo" else COLORS['green'],
                10
            )
            
    def update_pickups(self):
        """Update and handle pickups"""
        if not hasattr(self, 'pickups'):
            self.pickups = []
            return
            
        # Update each pickup
        for pickup in self.pickups[:]:
            # Update visual effect
            pickup['pulse'] = (pickup['pulse'] + 0.1) % (2 * math.pi)
            
            # Decrease lifetime
            pickup['lifetime'] -= 1
            if pickup['lifetime'] <= 0:
                self.pickups.remove(pickup)
                continue
                
            # Check for player collision
            distance = math.hypot(
                pickup['x'] - self.player.rect.centerx,
                pickup['y'] - self.player.rect.centery
            )
            
            if distance < pickup['radius'] + self.player.radius:
                # Apply pickup effect
                if pickup['type'] == 'health':
                    self.player.health = min(self.player.max_health, self.player.health + pickup['value'])
                    self.sound_manager.play_sound("pickup")
                    print(f"Player picked up health, new health: {self.player.health}")
                elif pickup['type'] == 'ammo':
                    weapon_name = self.player.current_weapon.name
                    self.player.ammo[weapon_name] += pickup['value']
                    self.sound_manager.play_sound("pickup")
                    print(f"Player picked up ammo for {weapon_name}, new ammo: {self.player.ammo[weapon_name]}")
                
                # Add pickup effect
                self.particle_system.add_sparkle(
                    pickup['x'],
                    pickup['y'],
                    pickup['color'],
                    20
                )
                
                # Remove the pickup
                self.pickups.remove(pickup)
                
    def draw_pickups(self, screen, camera_x, camera_y):
        """Draw all pickups with visual effects"""
        if not hasattr(self, 'pickups'):
            self.pickups = []
            return
            
        for pickup in self.pickups:
            # Calculate pulsing size
            pulse_mod = 1 + 0.2 * math.sin(pickup['pulse'])
            size = int(pickup['radius'] * pulse_mod)
            
            # Draw pickup
            pygame.draw.circle(
                screen,
                pickup['color'],
                (int(pickup['x'] - camera_x), int(pickup['y'] - camera_y)),
                size
            )
            
            # Draw icon inside
            if pickup['type'] == 'health':
                # Draw plus sign
                line_color = COLORS['white']
                center_x = int(pickup['x'] - camera_x)
                center_y = int(pickup['y'] - camera_y)
                
                pygame.draw.line(
                    screen,
                    line_color,
                    (center_x, center_y - size // 2),
                    (center_x, center_y + size // 2),
                    3
                )
                pygame.draw.line(
                    screen,
                    line_color,
                    (center_x - size // 2, center_y),
                    (center_x + size // 2, center_y),
                    3
                )
            elif pickup['type'] == 'ammo':
                # Draw ammo icon (bullet shape)
                pygame.draw.rect(
                    screen,
                    COLORS['white'],
                    (
                        int(pickup['x'] - camera_x - size // 4),
                        int(pickup['y'] - camera_y - size // 2),
                        size // 2,
                        size
                    )
                )

    def update_bullets(self):
        """Update all bullets and handle collisions"""
        for bullet in self.bullets[:]:
            try:
                # Check if the bullet is valid
                if bullet is None:
                    print("Warning: Found None bullet in bullets list, removing")
                    self.bullets.remove(bullet)
                    continue
                    
                # Basic attribute checks
                if not hasattr(bullet, 'rect') or bullet.rect is None:
                    print("Warning: Bullet has no rect attribute or rect is None, removing")
                    self.bullets.remove(bullet)
                    continue
                    
                # Debug logging
                bullet_type = type(bullet).__name__
                has_explode = hasattr(bullet, 'explode')
                print(f"Bullet type: {bullet_type}, has explode: {has_explode}")
                
                # Check if this is a Grenade (which needs the game parameter)
                if has_explode:
                    try:
                        print(f"Calling update with game instance for grenade")
                        # Directly handle the case where lifetime is None
                        if hasattr(bullet, 'lifetime') and bullet.lifetime is None:
                            print("Warning: Grenade has None lifetime, fixing...")
                            bullet.lifetime = 120  # Default lifetime value
                        bullet.update(self)
                    except Exception as e:
                        print(f"Grenade update error: {e}")
                        import traceback
                        traceback.print_exc()
                        self.bullets.remove(bullet)
                        continue
                else:
                    try:
                        bullet.update()
                    except Exception as e:
                        print(f"Bullet update error: {e}")
                        import traceback
                        traceback.print_exc()
                        self.bullets.remove(bullet)
                        continue
                
                # Remove bullets that are off-screen
                if hasattr(bullet, 'is_off_screen') and bullet.is_off_screen():
                    self.bullets.remove(bullet)
                    continue
                    
                # Check for collision with map obstacles - with safety checks
                if hasattr(bullet, 'rect') and bullet.rect is not None and hasattr(bullet.rect, 'centerx') and hasattr(bullet.rect, 'centery'):
                    if self.game_map.check_collision(bullet.rect.centerx, bullet.rect.centery, 4):
                        self.particle_system.add_explosion(
                            bullet.rect.centerx,
                            bullet.rect.centery,
                            COLORS["white"],
                            5
                        )
                        self.bullets.remove(bullet)
                        continue
                else:
                    print(f"Warning: Bullet has invalid rect structure, removing")
                    self.bullets.remove(bullet)
                    continue
                    
                # Check for collision with zombies
                for zombie in self.wave_manager.zombies[:]:
                    try:
                        # Make sure zombie has required attributes
                        if not hasattr(zombie, 'x') or not hasattr(zombie, 'y') or not hasattr(zombie, 'radius'):
                            print("Warning: Zombie missing required attributes")
                            continue
                            
                        if not hasattr(bullet, 'rect') or not hasattr(bullet.rect, 'centerx') or not hasattr(bullet.rect, 'centery'):
                            print("Warning: Bullet missing required position attributes")
                            continue
                            
                        distance = math.hypot(
                            zombie.x - bullet.rect.centerx,
                            zombie.y - bullet.rect.centery
                        )
                        
                        # Ensure all values needed for comparison are not None
                        if zombie.radius is not None and hasattr(bullet.rect, 'width'):
                            radius_sum = zombie.radius + (bullet.rect.width // 2)
                            if distance < radius_sum:
                                # Handle bullet hit
                                if hasattr(zombie, 'take_damage'):
                                    damage = getattr(bullet, 'damage', 1)  # Use damage attribute if available, else default to 1
                                    zombie.take_damage(damage)
                                    
                                    # Add blood effect at hit position
                                    self.particle_system.add_blood_effect(zombie.x, zombie.y)
                                    
                                    # Add damage indicator 
                                    self.add_damage_indicator(zombie.x, zombie.y, damage)
                                    
                                    # Remove the bullet if it's not a special penetrating type
                                    if not hasattr(bullet, 'penetrating') or not bullet.penetrating:
                                        if bullet in self.bullets:  # Safety check
                                            self.bullets.remove(bullet)
                                            break
                    except Exception as e:
                        print(f"Zombie bullet collision error: {e}")
            except Exception as e:
                print(f"Bullet update error: {e}")
                # Remove problematic bullets to prevent continuous errors
                if bullet in self.bullets:
                    self.bullets.remove(bullet)

    def add_damage_indicator(self, x, y, damage, is_critical=False, is_player=False):
        """Add floating damage number indicator"""
        try:
            if not hasattr(self, 'damage_indicators'):
                self.damage_indicators = []
            
            # Format: [x, y, damage_text, lifetime, offset_x, offset_y, is_critical]
            color = COLORS["red"] if is_player else (COLORS["yellow"] if is_critical else COLORS["white"])
            damage_str = str(damage)
            if is_critical:
                damage_str = f"CRIT {damage}!"
            
            offset_x = random.randint(-20, 20)
            self.damage_indicators.append([x, y, damage_str, 60, offset_x, 0, color])
        except Exception as e:
            print(f"Damage indicator error: {e}")

    def update_damage_indicators(self):
        """Update floating damage texts"""
        if not hasattr(self, 'damage_indicators'):
            self.damage_indicators = []
            
        for indicator in self.damage_indicators[:]:
            indicator[3] -= 1  # Decrease lifetime
            indicator[5] -= 1  # Move upward
            
            if indicator[3] <= 0:
                self.damage_indicators.remove(indicator)

    def draw_damage_indicators(self, screen, camera_x, camera_y):
        """Draw all floating damage numbers with error handling"""
        if not hasattr(self, 'damage_indicators'):
            self.damage_indicators = []
            return
        
        try:
            # Cache the font to avoid creating it multiple times
            if not hasattr(self, 'damage_font') or self.damage_font is None:
                self.damage_font = pygame.font.Font(None, 20)
            if not hasattr(self, 'damage_font_large') or self.damage_font_large is None:
                self.damage_font_large = pygame.font.Font(None, 25)
                
            for indicator in self.damage_indicators[:]:
                try:
                    x, y, text, lifetime, offset_x, offset_y, color = indicator
                    
                    # Fade out based on lifetime
                    alpha = min(255, int(lifetime * 4.25))
                    
                    # Choose font based on critical hit
                    font = self.damage_font_large if "CRIT" in text else self.damage_font
                    
                    # Create damage text
                    text_surf = font.render(text, True, color)
                    
                    # Create surface with transparency
                    text_surf.set_alpha(alpha)
                    
                    # Calculate position with offsets
                    pos_x = int(x - camera_x + offset_x)
                    pos_y = int(y - camera_y + offset_y)
                    
                    # Draw text
                    screen.blit(text_surf, (pos_x - text_surf.get_width() // 2, pos_y - text_surf.get_height() // 2))
                except Exception as e:
                    print(f"Error drawing damage indicator: {e}")
                    if indicator in self.damage_indicators:
                        self.damage_indicators.remove(indicator)
        except Exception as e:
            print(f"Error in draw_damage_indicators: {e}")
            self.damage_indicators = []  # Reset if there's a critical error

    def draw_game(self):
        """Main game rendering function"""
        try:
            # Clear the screen
            self.screen.fill(COLORS["black"])
            
            # Calculate camera position
            camera_x = self.player.rect.centerx - WIDTH // 2
            camera_y = self.player.rect.centery - HEIGHT // 2
            
            # Draw map
            self.game_map.draw(self.screen, camera_x, camera_y)
            
            # Draw bullets
            for bullet in self.bullets:
                bullet.draw(self.screen, camera_x, camera_y)
            
            # Draw zombies
            self.wave_manager.draw_zombies(self.screen, camera_x, camera_y)
            
            # Draw player
            self.player.draw(self.screen, camera_x, camera_y)
            
            # Draw damage indicators
            self.draw_damage_indicators(self.screen, camera_x, camera_y)
            
            # Draw particles
            self.particle_system.draw(self.screen, camera_x, camera_y)
            
            # Draw HUD
            self.menu.draw_hud(self.screen, self.player, self.wave_manager.current_wave)
            self.menu.draw_crosshair(self.screen, pygame.mouse.get_pos())
            
            # Minimap
            self.menu.draw_enhanced_minimap(self.screen, self.player, self.game_map, self.wave_manager.zombies)
            
            # Draw weapon wheel if showing
            if self.menu.show_weapon_wheel:
                self.menu.draw_weapon_wheel(self.screen, self.player)
                
            # Draw items wheel if showing  
            if self.menu.show_items_wheel:
                self.menu.draw_items_wheel(self.screen, self.player)
            
            # Draw pickups
            self.draw_pickups(self.screen, camera_x, camera_y)
            
            # Draw pause screen if paused
            if self.menu.paused:
                self.draw_pause_menu()
                
                # If settings menu is open, draw it on top of the pause menu
                if self.menu.show_settings:
                    self.draw_settings()
            
            # FPS counter
            if self.menu.settings["show_fps"]:
                fps = str(int(self.clock.get_fps()))
                fps_text = self.menu.small_font.render(f"FPS: {fps}", True, COLORS["white"])
                self.screen.blit(fps_text, (WIDTH - 100, 10))
            
            # Debug information
            if DEBUG:
                debug_info = [
                    f"Player pos: ({self.player.rect.centerx}, {self.player.rect.centery})",
                    f"Zombies: {len(self.wave_manager.zombies)}",
                    f"Bullets: {len(self.bullets)}",
                    f"Wave: {self.wave_manager.current_wave}",
                    f"Score: {self.player.score}"
                ]
                
                for i, info in enumerate(debug_info):
                    debug_text = self.menu.small_font.render(info, True, COLORS["yellow"])
                    self.screen.blit(debug_text, (10, 40 + i * 20))
            
            # Update the display
            pygame.display.flip()
            
        except Exception as e:
            print(f"Error in draw_game: {e}")
            # Continue despite rendering errors

    def draw_pause_menu(self):
        """Draw the pause menu overlay"""
        try:
            # Animate the alpha for fade-in effect
            self.menu.ui_animations["pause_alpha"] = min(180, self.menu.ui_animations["pause_alpha"] + 10)
            alpha = self.menu.ui_animations["pause_alpha"]
            
            # Create overlay surface with alpha
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            self.screen.blit(overlay, (0, 0))
            
            # Draw pause text
            title_text = self.menu.title_font.render("PAUSED", True, COLORS["white"])
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            self.screen.blit(title_text, title_rect)
            
            # Draw pause menu options
            for i, option in enumerate(self.menu.pause_options):
                if i == self.menu.pause_selected:
                    # Highlight selected option
                    color = COLORS["yellow"]
                    # Add indicator arrow
                    pygame.draw.polygon(self.screen, COLORS["yellow"], 
                        [(WIDTH // 2 - 140, HEIGHT // 2 + i * 50), 
                         (WIDTH // 2 - 120, HEIGHT // 2 + i * 50 + 10), 
                         (WIDTH // 2 - 140, HEIGHT // 2 + i * 50 + 20)])
                else:
                    color = COLORS["white"]
                
                option_text = self.menu.menu_font.render(option, True, color)
                option_rect = option_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 50))
                self.screen.blit(option_text, option_rect)
            
            # Draw controls help
            controls_text = self.menu.small_font.render("Use arrow keys to navigate, Enter to select", True, COLORS["white"])
            controls_rect = controls_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            self.screen.blit(controls_text, controls_rect)
            
        except Exception as e:
            print(f"Error drawing pause menu: {e}")

    def draw_settings(self):
        """Draw the settings menu based on current state"""
        try:
            # Check if the menu has the draw_settings method
            if hasattr(self.menu, 'draw_settings'):
                self.menu.draw_settings(self.screen)
            else:
                # Fallback if method doesn't exist
                print("Warning: Menu.draw_settings() method not found")
                
                # Draw a basic settings menu
                overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                self.screen.blit(overlay, (0, 0))
                
                title_text = self.menu.menu_font.render("Settings", True, COLORS["white"])
                title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
                self.screen.blit(title_text, title_rect)
                
                help_text = self.menu.small_font.render("Press ESC to return", True, COLORS["white"])
                help_rect = help_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
                self.screen.blit(help_text, help_rect)
        except Exception as e:
            print(f"Error drawing settings menu: {e}")
            traceback.print_exc()

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
        try:
            while self.running:
                try:
                    self.handle_events()
                    
                    if self.game_state == "menu":
                        # Draw main menu
                        self.screen.fill(COLORS['black'])
                        self.menu.draw_main_menu(self.screen)
                    
                    elif self.game_state == "playing":
                        # Update and draw game state
                        try:
                            self.update_game()
                        except Exception as e:
                            print(f"Error in update_game: {e}")
                            import traceback
                            traceback.print_exc()
                        
                        # Check player survival
                        if self.player.health <= 0:
                            self.game_state = "game_over"
                            self.sound_manager.play_sound("game_over")
                            self.sound_manager.stop_music()
                        
                        try:
                            self.draw_game()
                        except Exception as e:
                            print(f"Error in draw_game: {e}")
                            import traceback
                            traceback.print_exc()
                    
                    elif self.game_state == "game_over":
                        # Draw game over screen
                        self.screen.fill(COLORS['black'])
                        self.menu.draw_game_over(self.screen, self.player.score)
                    
                    # Update display
                    pygame.display.flip()
                    
                    # Maintain consistent frame rate
                    self.clock.tick(FPS)
                    
                except Exception as e:
                    print(f"Error in main game loop: {e}")
                    import traceback
                    traceback.print_exc()
                    
        except Exception as e:
            print(f"Critical error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    game = Game()
    game.run()
