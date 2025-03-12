import pygame
import random
import math
from bullet import Bullet
from config import *

class Weapon:
    def __init__(self, name, fire_rate, damage, spread, max_ammo):
        self.name = name  # This is the crucial fix
        self.fire_rate = fire_rate
        self.damage = damage
        self.spread = spread
        self.max_ammo = max_ammo
        self.last_shot = 0

    def can_shoot(self):
        return pygame.time.get_ticks() - self.last_shot > self.fire_rate

    def fire(self, start_pos, target_pos, bullets):
        if self.can_shoot():
            self.last_shot = pygame.time.get_ticks()
            dx = target_pos[0] - start_pos[0]
            dy = target_pos[1] - start_pos[1]
            angle = math.atan2(dy, dx)
            angle += random.uniform(-self.spread, self.spread)
            bullets.append(Bullet(start_pos[0], start_pos[1], angle))
            return True
        return False

class Pistol(Weapon):
    def __init__(self):
        super().__init__(
            name="Pistol",
            fire_rate=500,
            damage=25,
            spread=0.05,
            max_ammo=MAX_AMMO["pistol"]
        )

class Shotgun(Weapon):
    def __init__(self):
        super().__init__(
            name="Shotgun",
            fire_rate=1000,
            damage=8,
            spread=0.2,
            max_ammo=MAX_AMMO["shotgun"]
        )
    
    def fire(self, start_pos, target_pos, bullets):
        if super().fire(start_pos, target_pos, bullets):
            for _ in range(7):
                dx = target_pos[0] - start_pos[0]
                dy = target_pos[1] - start_pos[1]
                angle = math.atan2(dy, dx) + random.uniform(-0.3, 0.3)
                bullets.append(Bullet(start_pos[0], start_pos[1], angle))
            return True
        return False