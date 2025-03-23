# bullet.py
import pygame
import math
from config import *

class Bullet:
    def __init__(self, x, y, angle):
        self.rect = pygame.Rect(x, y, 8, 8)
        self.color = COLORS["white"]
        self.speed = BULLET_SPEED
        self.angle = angle  # Store the angle as an attribute
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed

    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def is_off_screen(self):
        """Check if bullet is outside map boundaries"""
        return not (0 <= self.rect.x <= MAP_SIZE and 0 <= self.rect.y <= MAP_SIZE)
        
    def draw(self, screen, camera_x, camera_y):
        """Draw bullet with trail effect"""
        # Draw bullet body
        pygame.draw.rect(
            screen,
            self.color,
            (
                int(self.rect.x - camera_x),
                int(self.rect.y - camera_y),
                self.rect.width,
                self.rect.height
            )
        )
        
        # Add bullet trail
        trail_length = 8
        trail_x = int(self.rect.centerx - self.vx * trail_length - camera_x)
        trail_y = int(self.rect.centery - self.vy * trail_length - camera_y)
        
        pygame.draw.line(
            screen,
            (self.color[0]//2, self.color[1]//2, self.color[2]//2),
            (int(self.rect.centerx - camera_x), int(self.rect.centery - camera_y)),
            (trail_x, trail_y),
            max(1, self.rect.width // 2)
        )
