# player.py
import pygame
from collections import deque
from config import *
from weapon import *

class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH//2, HEIGHT//2, 32, 32)
        self.color = COLORS["green"]
        self.health = PLAYER_HEALTH
        self.weapons = [Pistol(), Shotgun()]
        self.current_weapon_index = 0
        self.ammo = {  # Store ammo per weapon type
            "Pistol": MAX_AMMO["pistol"],
            "Shotgun": MAX_AMMO["shotgun"]
        }
        self.reloading = False
        self.reload_start_time = 0
        self.score = 0

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

    def update(self, dx, dy, game_map):
        new_x = self.rect.centerx + dx
        new_y = self.rect.centery + dy
        
        # Check collision with new position
        if not game_map.check_collision(new_x, new_y, PLAYER_RADIUS):
            self.rect.centerx = new_x
            self.rect.centery = new_y

    def check_move_valid(self, rect, game_map):
        # Check four corners and center
        points = [
            rect.midleft, rect.midright,
            rect.midtop, rect.midbottom,
            rect.center
        ]
        return all(game_map.is_passable(x, y) for x, y in points)

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def add_to_inventory(self, item):
        self.inventory.append(item)

    @staticmethod
    def handle_input():
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_a]: dx -= PLAYER_SPEED
        if keys[pygame.K_d]: dx += PLAYER_SPEED
        if keys[pygame.K_w]: dy -= PLAYER_SPEED
        if keys[pygame.K_s]: dy += PLAYER_SPEED
        return dx, dy