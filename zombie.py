import pygame
import math
import random
from config import *

class Zombie:
    def __init__(self, x, y, zombie_type="regular"):
        self.radius = 16  # Zombie radius
        self.x, self.y = x, y  # Center coordinates
        self.zombie_types = {
            "regular": {"health": 100, "color": COLORS["red"], "speed": ZOMBIE_SPEED, "damage": 10},
            "fast": {"health": 60, "color": COLORS["yellow"], "speed": ZOMBIE_SPEED * 1.5, "damage": 5},
            "tank": {"health": 200, "color": COLORS["dark_red"], "speed": ZOMBIE_SPEED * 0.7, "damage": 20}
        }
        self.type = zombie_type
        self.health = self.zombie_types[zombie_type]["health"]
        self.max_health = self.health
        self.color = self.zombie_types[zombie_type]["color"]
        self.speed = self.zombie_types[zombie_type]["speed"]
        self.damage = self.zombie_types[zombie_type]["damage"]
        self.path_timer = 0
        self.path_timer_max = random.randint(30, 60)
        self.path_offset_x = 0
        self.path_offset_y = 0
        self.animation_frame = 0
        self.hit_flash = 0
        self.size_pulse = 0

    def move_towards(self, target_x, target_y, game_map):
        self.path_timer += 1
        if self.path_timer >= self.path_timer_max:
            self.path_timer = 0
            self.path_timer_max = random.randint(30, 60)
            self.path_offset_x = random.randint(-50, 50)
            self.path_offset_y = random.randint(-50, 50)
        dx = (target_x + self.path_offset_x) - self.x
        dy = (target_y + self.path_offset_y) - self.y
        dist = math.hypot(dx, dy)
        if dist == 0:
            return
        dx /= dist
        dy /= dist
        move_x = self.speed * dx
        new_x = self.x + move_x
        if self.check_position_valid(new_x, self.y, game_map):
            self.x = new_x
        else:
            diag_x = self.x + (move_x * 0.5)
            if self.check_position_valid(diag_x, self.y, game_map):
                self.x = diag_x
        move_y = self.speed * dy
        new_y = self.y + move_y
        if self.check_position_valid(self.x, new_y, game_map):
            self.y = new_y
        else:
            diag_y = self.y + (move_y * 0.5)
            if self.check_position_valid(self.x, diag_y, game_map):
                self.y = diag_y
        self.animation_frame = (self.animation_frame + 1) % 30
        if self.hit_flash > 0:
            self.hit_flash -= 1
        self.size_pulse = 2 * math.sin(self.animation_frame / 5)

    def check_position_valid(self, x, y, game_map):
        points = [(x, y)]
        return any(game_map.is_passable(px, py) for px, py in points)

    def take_damage(self, damage):
        self.health -= damage
        self.hit_flash = 5
        return self.health <= 0

    def get_render_radius(self):
        return self.radius + int(self.size_pulse)

    def get_render_color(self):
        if self.hit_flash > 0:
            return COLORS["white"]
        return self.color

    def draw(self, screen, camera_x, camera_y):
        """Draw zombie with enhanced visuals"""
        render_radius = self.get_render_radius()
        render_color = self.get_render_color()
        
        # Draw shadow
        pygame.draw.circle(
            screen, 
            COLORS["black"], 
            (int(self.x - camera_x + 3), int(self.y - camera_y + 3)), 
            render_radius, 
            0
        )
        
        # Draw zombie body
        pygame.draw.circle(
            screen,
            render_color,
            (int(self.x - camera_x), int(self.y - camera_y)),
            render_radius
        )
        
        # Draw eyes based on direction to player
        eye_radius = max(2, render_radius // 5)
        eye_offset = render_radius // 3
        
        # Direction vector to player
        player_pos = pygame.mouse.get_pos()  
        dx = (player_pos[0] + camera_x) - self.x
        dy = (player_pos[1] + camera_y) - self.y
        dist = max(1, math.hypot(dx, dy))
        dx, dy = dx / dist, dy / dist
        
        # Left eye
        left_eye_x = int(self.x - camera_x - eye_offset + dx * eye_offset * 0.5)
        left_eye_y = int(self.y - camera_y - eye_offset + dy * eye_offset * 0.5)
        pygame.draw.circle(screen, COLORS["black"], (left_eye_x, left_eye_y), eye_radius)
        
        # Right eye
        right_eye_x = int(self.x - camera_x + eye_offset + dx * eye_offset * 0.5)
        right_eye_y = int(self.y - camera_y - eye_offset + dy * eye_offset * 0.5)
        pygame.draw.circle(screen, COLORS["black"], (right_eye_x, right_eye_y), eye_radius)
        
        # Draw zombie-type specific visual enhancements
        if self.type == "fast":
            # Draw speed lines
            for i in range(3):
                offset = (i - 1) * 5
                pygame.draw.line(
                    screen, 
                    COLORS["yellow"], 
                    (int(self.x - camera_x + offset - 5), int(self.y - camera_y + render_radius - 5)), 
                    (int(self.x - camera_x + offset - 15), int(self.y - camera_y + render_radius - 5)),
                    2
                )
        elif self.type == "tank":
            # Draw armor plates
            for angle in range(0, 360, 60):
                rad = math.radians(angle)
                armor_x = int(self.x - camera_x + math.cos(rad) * render_radius * 0.7)
                armor_y = int(self.y - camera_y + math.sin(rad) * render_radius * 0.7)
                pygame.draw.circle(screen, COLORS["dark_gray"], (armor_x, armor_y), 4)
        
        # Draw health bar
        self.draw_health_bar(screen, camera_x, camera_y)
        
        # Draw damage text if hit recently
        if self.hit_flash > 0:
            # Create a damage text that floats upward
            damage_color = COLORS["white"]
            damage_text = pygame.font.Font(None, 24).render("!", True, damage_color)
            offset_y = self.hit_flash * 2  
            screen.blit(damage_text, 
                     (int(self.x - camera_x - damage_text.get_width() // 2),
                      int(self.y - camera_y - render_radius - 15 - offset_y)))

    def draw_health_bar(self, screen, camera_x, camera_y):
        """Draw enhanced health bar with gradient color"""
        bar_width = self.radius * 2
        bar_height = 4
        bar_x = self.x - bar_width // 2 - camera_x
        bar_y = self.y - self.radius - 10 - camera_y
        
        # Draw background/border
        pygame.draw.rect(screen, COLORS["black"], 
                       (bar_x - 1, bar_y - 1, bar_width + 2, bar_height + 2))
        
        # Calculate health percentage and color
        health_pct = self.health / self.max_health
        
        if health_pct > 0.6:
            health_color = COLORS["green"]
        elif health_pct > 0.3:
            health_color = COLORS["yellow"]
        else:
            health_color = COLORS["red"]
        
        # Draw filled portion
        filled_width = int(bar_width * health_pct)
        pygame.draw.rect(screen, health_color, (bar_x, bar_y, filled_width, bar_height))

    def draw_type_indicator(self, screen, camera_x, camera_y):
        if self.type == "fast":
            pygame.draw.circle(screen, COLORS["yellow"], (int(self.x - camera_x + self.radius // 2), int(self.y - camera_y - self.radius // 2)), 3)
        elif self.type == "tank":
            pygame.draw.rect(screen, COLORS["dark_red"], (int(self.x - camera_x - self.radius // 2), int(self.y - camera_y - self.radius // 2), 5, 5))
