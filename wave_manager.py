import random
import math
import pygame
from zombie import Zombie
from config import ZOMBIE_RADIUS, SPAWN_DISTANCE

class WaveManager:
    def __init__(self):
        self.wave = 1
        self.zombies = []
        self.last_spawn = pygame.time.get_ticks()
        self.zombies_per_wave = 5
        self.spawn_interval = 3000
        self.max_spawn_attempts = 20  # Prevent infinite loops

    def update(self, player_rect, game_map):
        current_time = pygame.time.get_ticks()
        
        if (len(self.zombies) < self.zombies_per_wave and 
            current_time - self.last_spawn > self.spawn_interval):
            self.spawn_zombie(player_rect, game_map)
            self.last_spawn = current_time

    def spawn_zombie(self, player_rect, game_map):
        for _ in range(self.max_spawn_attempts):
            # Generate random spawn position around player
            angle = random.uniform(0, 2 * math.pi)
            x = player_rect.centerx + math.cos(angle) * SPAWN_DISTANCE
            y = player_rect.centery + math.sin(angle) * SPAWN_DISTANCE
            
            # Check valid spawn position
            if (game_map.is_passable(x, y) and 
               not game_map.check_collision(x, y, ZOMBIE_RADIUS)):
                self.zombies.append(Zombie(x, y))
                return
        
        print("Failed to find valid spawn position after attempts")

    def next_wave(self):
        self.wave += 1
        self.zombies_per_wave = int(self.zombies_per_wave * 1.5)
        self.spawn_interval = max(500, self.spawn_interval - 200)
