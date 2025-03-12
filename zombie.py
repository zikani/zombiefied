# zombie.py
import pygame
import math
from config import *

class Zombie:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 32, 32)
        self.health = 100
        self.color = COLORS["red"]
        self.speed = ZOMBIE_SPEED

    def move_towards(self, target_x, target_y, game_map):
        # Calculate base direction
        dx = target_x - self.rect.x
        dy = target_y - self.rect.y
        dist = math.hypot(dx, dy)
        
        if dist == 0:
            return

        # Normalize direction
        move_x = self.speed * dx/dist
        move_y = self.speed * dy/dist

        # Check proposed position
        new_rect = self.rect.copy()
        new_rect.x += move_x
        new_rect.y += move_y

        if self.check_move_valid(new_rect, game_map):
            self.rect.x += move_x
            self.rect.y += move_y
        else:
            # Obstacle avoidance - try perpendicular directions
            self.rect.x += move_y  # Swap x/y components
            self.rect.y += move_x
            if not self.check_move_valid(self.rect, game_map):
                self.rect.x -= 2*move_y
                self.rect.y -= 2*move_x

    def check_move_valid(self, rect, game_map):
        return game_map.is_passable(rect.centerx, rect.centery)


    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0