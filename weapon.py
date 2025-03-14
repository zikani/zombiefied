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
    
class GrenadeLauncher(Weapon):
    def __init__(self):
        super().__init__(
            name="Grenade Launcher",
            fire_rate=WEAPON_STATS["grenade_launcher"]["fire_rate"],
            damage=WEAPON_STATS["grenade_launcher"]["damage"],
            spread=WEAPON_STATS["grenade_launcher"]["spread"],
            max_ammo=MAX_AMMO["grenade_launcher"]
        )

    def fire(self, start_pos, target_pos, bullets):
        if self.can_shoot():
            self.last_shot = pygame.time.get_ticks()
            grenade = Grenade(start_pos[0], start_pos[1], target_pos, self.damage)
            bullets.append(grenade)
            return True
        return False
    
class SniperRifle(Weapon):
    def __init__(self):
        super().__init__(
            name="Sniper Rifle",
            fire_rate=1500,
            damage=100,
            spread=0.01,
            max_ammo=MAX_AMMO["sniper_rifle"]
        )

    def fire(self, start_pos, target_pos, bullets):
        if super().fire(start_pos, target_pos, bullets):
            bullets[-1].speed *= 2 #make sniper bullets faster.
            return True
        return False
    
class AssaultRifle(Weapon):
    def __init__(self):
        super().__init__(
            name="Assault Rifle",
            fire_rate=150,
            damage=15,
            spread=0.03,
            max_ammo=MAX_AMMO["assault_rifle"]
        )
    def fire(self, start_pos, target_pos, bullets):
        if super().fire(start_pos, target_pos, bullets):
            bullets[-1].speed = 10
            return True
        return False
    
class SubmachineGun(Weapon):
    def __init__(self):
        super().__init__(
            name="Submachine Gun",
            fire_rate=100,
            damage=10,
            spread=0.08,
            max_ammo=MAX_AMMO["submachine_gun"]
        )
    def fire(self, start_pos, target_pos, bullets):
        if super().fire(start_pos, target_pos, bullets):
            bullets[-1].speed = 7
            return True
        return False
    
class Grenade:
    def __init__(self, x, y, target_pos, damage):
        self.x = x
        self.y = y
        self.target_pos = target_pos
        self.damage = damage
        self.speed = 5
        self.explosion_radius = 50
        self.lifetime = 120
        self.radius = 8
        self.color = COLORS["yellow"]
        self.dx = target_pos[0] - x
        self.dy = target_pos[1] - y
        self.angle = math.atan2(self.dy, self.dx)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius * 2, self.radius * 2) #add rect.

    def update(self, game):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.rect.center = (int(self.x),int(self.y)) #update rect.

        if self.lifetime <= 0:
            self.explode(game)

    def draw(self, screen, camera_x=0, camera_y=0):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x - camera_x), int(self.y - camera_y)),
            self.radius
        )

    def explode(self, game):
        game.particle_system.add_explosion(self.x, self.y, count=30)
        for zombie in game.wave_manager.zombies[:]: #use wave_manager.zombies.
            distance = math.sqrt((self.x - zombie.rect.centerx) ** 2 + (self.y - zombie.rect.centery) ** 2)
            if distance <= self.explosion_radius:
                zombie.take_damage(self.damage)
        game.bullets.remove(self)
