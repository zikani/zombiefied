import pygame
from config import *
import math
from weapon import Pistol, Shotgun, AssaultRifle, SniperRifle, SubmachineGun, GrenadeLauncher  # Import all weapons

class Player:
    def __init__(self, game_map):
        self.rect = pygame.Rect(WIDTH // 2, HEIGHT // 2, 32, 32)
        self.game_map = game_map
        self.color = COLORS["green"]
        self.radius = PLAYER_RADIUS
        self.health = PLAYER_HEALTH
        self.max_health = PLAYER_HEALTH
        self.weapons = [Pistol(), Shotgun(), AssaultRifle(), SniperRifle(), SubmachineGun(), GrenadeLauncher()] #add all weapons.
        self.current_weapon_index = 0
        self.ammo = {  # Store ammo per weapon type
            "Pistol": MAX_AMMO["pistol"],
            "Shotgun": MAX_AMMO["shotgun"],
            "Assault Rifle": MAX_AMMO["assault_rifle"],
            "Sniper Rifle": MAX_AMMO["sniper_rifle"],
            "Submachine Gun": MAX_AMMO["submachine_gun"],
            "Grenade Launcher": MAX_AMMO["grenade_launcher"]
        }
        self.reloading = False
        self.reload_start_time = 0
        self.score = 0
        self.speed = PLAYER_SPEED
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.inventory = []  # Initialize the inventory list
        self.knockback = [0, 0]

    @property
    def current_weapon(self):
        return self.weapons[self.current_weapon_index]
    
    def reload(self):
        if not self.reloading:
            weapon_name = self.current_weapon.name
            max_ammo = self.current_weapon.max_ammo
            if self.ammo[weapon_name] < max_ammo:
                self.reloading = True
                self.reload_start_time = pygame.time.get_ticks()

    def update_reload(self):
        if self.reloading and pygame.time.get_ticks() - self.reload_start_time > RELOAD_TIME:
            weapon_name = self.current_weapon.name
            self.ammo[weapon_name] = self.current_weapon.max_ammo
            self.reloading = False

    def update(self, dx, dy, game_map, mouse_x, mouse_y, weapon_switch, shoot):
        """Updates player position, weapon, and shooting."""
        # Apply movement speed
        dx *= self.speed
        dy *= self.speed
        
        # Move the player
        self.move(dx, dy, game_map)
        
        # Handle weapon switching
        if weapon_switch != 0:  # Changed from is not None to != 0
            self.switch_weapon(weapon_switch)
        
        # Update invulnerability status
        if self.invulnerable:
            if pygame.time.get_ticks() - self.invulnerable_timer > 1000:  # 1 second of invulnerability
                self.invulnerable = False
        
        # Update reload status
        self.update_reload()
        
        # No need to handle shooting here, it's handled in the Game class

    def move(self, dx, dy, game_map):
        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.7071  # 1/sqrt(2)
            dy *= 0.7071
        
        # Try moving on X axis
        new_x = self.rect.centerx + dx
        if not game_map.check_collision(new_x, self.rect.centery, PLAYER_RADIUS):
            self.rect.centerx = new_x
        
        # Try moving on Y axis
        new_y = self.rect.centery + dy
        if not game_map.check_collision(self.rect.centerx, new_y, PLAYER_RADIUS):
            self.rect.centery = new_y

    def switch_weapon(self, index):
        if index is not None and 0 <= index < len(self.weapons):
            self.current_weapon_index = index

    def shoot(self, mouse_x, mouse_y, bullets):
        weapon_name = self.current_weapon.name
        if self.ammo[weapon_name] > 0 and not self.reloading:
            new_bullets = self.current_weapon.fire(self.rect.center, (mouse_x, mouse_y), bullets)
            if new_bullets:  # Only reduce ammo if bullets were actually fired
                self.ammo[weapon_name] -= 1
            return new_bullets
        return []

    def check_move_valid(self, rect, game_map):
        # Check four corners and center
        points = [
            (rect.left, rect.top), (rect.right, rect.top),
            (rect.left, rect.bottom), (rect.right, rect.bottom),
            (rect.centerx, rect.centery)
        ]
        return all(game_map.is_passable(x, y) for x, y in points)

    def take_damage(self, amount):
        if not self.invulnerable:
            self.health = max(0, self.health - amount)
            self.invulnerable = True
            self.invulnerable_timer = pygame.time.get_ticks()

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def apply_knockback(self, source_x, source_y):
        """Apply knockback effect when hit by an enemy with collision check"""
        knockback_strength = 20  # Adjust as needed

        dx = self.rect.centerx - source_x
        dy = self.rect.centery - source_y

        dist = math.hypot(dx, dy)
        if dist == 0:
            return

        dx /= dist
        dy /= dist

        knockback_x = dx * knockback_strength
        knockback_y = dy * knockback_strength

        # Apply knockback in steps with collision checks
        steps = int(knockback_strength)
        for _ in range(steps):
            new_x = self.rect.centerx + dx
            new_y = self.rect.centery + dy
            if self.game_map.check_collision(new_x, new_y, self.radius):
                break  # Stop knockback if collision
            else:
                self.rect.centerx = new_x
                self.rect.centery = new_y

    def handle_input():
        """Handles player input (movement, weapon switching, shooting)."""
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        weapon_switch = None
        shoot = False

        # Movement
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy += 1

        # Weapon switching
        if keys[pygame.K_1]:
            weapon_switch = 0
        if keys[pygame.K_2]:
            weapon_switch = 1
        if keys[pygame.K_3]:
            weapon_switch = 2
        if keys[pygame.K_4]:
            weapon_switch = 3
        if keys[pygame.K_5]:
            weapon_switch = 4
        if keys[pygame.K_6]:
            weapon_switch = 5

        # Shooting
        shoot = pygame.mouse.get_pressed()[0]

        return dx, dy, weapon_switch, shoot

    def draw(self, screen, camera_x, camera_y):
        """Draw player with visual enhancements"""
        # Draw player shadow
        pygame.draw.circle(
            screen,
            COLORS["black"],
            (int(self.rect.centerx - camera_x + 3), int(self.rect.centery - camera_y + 3)),
            self.radius,
            0
        )
        
        # Draw player body
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.rect.centerx - camera_x), int(self.rect.centery - camera_y)),
            self.radius
        )
        
        # Draw weapon direction indicator
        mouse_pos = pygame.mouse.get_pos()
        world_mouse_x = mouse_pos[0] + camera_x
        world_mouse_y = mouse_pos[1] + camera_y
        
        # Calculate direction to mouse
        dx = world_mouse_x - self.rect.centerx
        dy = world_mouse_y - self.rect.centery
        angle = math.atan2(dy, dx)
        
        # Draw weapon indicator (gun barrel)
        barrel_length = self.radius + 10
        end_x = self.rect.centerx + math.cos(angle) * barrel_length
        end_y = self.rect.centery + math.sin(angle) * barrel_length
        
        pygame.draw.line(
            screen,
            COLORS["dark_gray"],
            (int(self.rect.centerx - camera_x), int(self.rect.centery - camera_y)),
            (int(end_x - camera_x), int(end_y - camera_y)),
            4
        )
        
        # Draw eyes
        eye_radius = 3
        eye_offset = self.radius // 3
        
        # Adjust eye position based on mouse direction
        look_x = math.cos(angle) * eye_offset * 0.5
        look_y = math.sin(angle) * eye_offset * 0.5
        
        # Left eye
        pygame.draw.circle(
            screen,
            COLORS["black"],
            (int(self.rect.centerx - camera_x - eye_offset + look_x), 
             int(self.rect.centery - camera_y - eye_offset + look_y)),
            eye_radius
        )
        
        # Right eye
        pygame.draw.circle(
            screen,
            COLORS["black"],
            (int(self.rect.centerx - camera_x + eye_offset + look_x), 
             int(self.rect.centery - camera_y - eye_offset + look_y)),
            eye_radius
        )
        
        # Show player invulnerability effect
        if self.invulnerable:
            # Draw shield effect
            shield_radius = self.radius + 5
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
            
            screen.blit(
                shield_surface,
                (int(self.rect.centerx - camera_x - shield_radius - 2),
                 int(self.rect.centery - camera_y - shield_radius - 2))
            )
