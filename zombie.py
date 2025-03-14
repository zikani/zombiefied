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

    def draw_health_bar(self, screen, camera_x, camera_y):
        bar_width = self.radius * 3
        bar_height = 5
        bar_x = self.x - bar_width // 2 - camera_x
        bar_y = self.y - self.radius - 10 - camera_y

        ratio = self.health / self.max_health
        fill_width = int(bar_width * ratio)

        outline_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
        fill_rect = pygame.Rect(bar_x, bar_y, fill_width, bar_height)

        pygame.draw.rect(screen, COLORS["black"], outline_rect)
        pygame.draw.rect(screen, COLORS["green"], fill_rect)

    def draw_type_indicator(self, screen, camera_x, camera_y):
        if self.type == "fast":
            pygame.draw.circle(screen, COLORS["yellow"], (int(self.x - camera_x + self.radius // 2), int(self.y - camera_y - self.radius // 2)), 3)
        elif self.type == "tank":
            pygame.draw.rect(screen, COLORS["dark_red"], (int(self.x - camera_x - self.radius // 2), int(self.y - camera_y - self.radius // 2), 5, 5))

    def draw(self, screen, camera_x, camera_y):
        render_radius = self.get_render_radius()
        render_color = self.get_render_color()
        pygame.draw.circle(screen, render_color, (int(self.x - camera_x), int(self.y - camera_y)), render_radius)
        self.draw_health_bar(screen, camera_x, camera_y)
        self.draw_type_indicator(screen, camera_x, camera_y)
