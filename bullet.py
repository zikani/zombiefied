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