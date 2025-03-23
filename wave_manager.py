import random
import math
import pygame
from zombie import Zombie
from config import ZOMBIE_RADIUS, SPAWN_DISTANCE, MAP_SIZE

class WaveManager:
    def __init__(self):
        self.zombies = []
        self.current_wave = 1
        self.zombies_per_wave = 5
        self.spawned_count = 0
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between spawns
        self.wave_complete = False

    def update(self, player_rect, game_map):
        """Update wave status and spawn zombies as needed"""
        try:
            # Check if wave is complete
            if not self.zombies and self.spawned_count >= self.zombies_per_wave:
                self.wave_complete = True
                self.start_next_wave()
            
            # Spawn zombies with delay
            if self.spawned_count < self.zombies_per_wave:
                self.spawn_timer += 1
                if self.spawn_timer >= self.spawn_delay:
                    self.spawn_timer = 0
                    self.spawn_zombie(player_rect, game_map)
        except Exception as e:
            print(f"Wave manager update error: {e}")
    
    def start_next_wave(self):
        """Prepare the next wave of zombies"""
        try:
            self.current_wave += 1
            self.zombies_per_wave = 5 + (self.current_wave * 2)  # Increase zombies per wave
            self.spawned_count = 0
            self.wave_complete = False
            # Make zombies spawn faster in later waves
            self.spawn_delay = max(10, 60 - (self.current_wave * 2))  
        except Exception as e:
            print(f"Error starting next wave: {e}")
            # Ensure we have valid values even on error
            self.current_wave = max(1, self.current_wave)
            self.zombies_per_wave = max(5, self.zombies_per_wave)
            self.spawned_count = 0
            self.spawn_delay = max(10, self.spawn_delay)
    
    def spawn_zombie(self, player_rect, game_map):
        """Spawn a zombie at a valid location"""
        try:
            # Choose a zombie type based on wave progress
            zombie_type = self.choose_zombie_type()
            
            # Attempt to find a valid spawn location
            spawn_attempts = 0
            max_attempts = 20
            
            while spawn_attempts < max_attempts:
                # Generate potential spawn location away from player
                min_distance = 300
                max_distance = 600
                
                angle = random.uniform(0, 2 * 3.14159)
                distance = random.uniform(min_distance, max_distance)
                
                spawn_x = player_rect.centerx + distance * math.cos(angle)
                spawn_y = player_rect.centery + distance * math.sin(angle)
                
                # Keep within map bounds
                spawn_x = max(50, min(MAP_SIZE - 50, spawn_x))
                spawn_y = max(50, min(MAP_SIZE - 50, spawn_y))
                
                # Check if spawn location is valid
                if game_map.is_passable(spawn_x, spawn_y):
                    zombie = Zombie(spawn_x, spawn_y, zombie_type)
                    self.zombies.append(zombie)
                    self.spawned_count += 1
                    return True
                
                spawn_attempts += 1
            
            # If we failed to find a valid location after max attempts,
            # spawn at a fixed offset from player as fallback
            fallback_x = player_rect.centerx + 400
            fallback_y = player_rect.centery + 400
            zombie = Zombie(fallback_x, fallback_y, zombie_type)
            self.zombies.append(zombie)
            self.spawned_count += 1
            return True
            
        except Exception as e:
            print(f"Error spawning zombie: {e}")
            return False
    
    def choose_zombie_type(self):
        """Choose a zombie type based on wave number"""
        try:
            if self.current_wave >= 5:
                # More variety in later waves
                types = ["regular", "fast", "tank"]
                weights = [0.5, 0.3, 0.2]
            elif self.current_wave >= 3:
                # Introduce fast zombies in wave 3
                types = ["regular", "fast"]
                weights = [0.7, 0.3]
            else:
                # Only regular zombies in early waves
                return "regular"
                
            return random.choices(types, weights=weights, k=1)[0]
        except Exception as e:
            print(f"Error choosing zombie type: {e}")
            return "regular"  # Fall back to regular zombies on error

    def draw_zombies(self, screen, camera_x, camera_y):
        """Draw all zombies in the game with safe iteration"""
        try:
            for zombie in self.zombies[:]:  # Use a copy of the list for safe iteration
                try:
                    zombie.draw(screen, camera_x, camera_y)
                except Exception as e:
                    print(f"Error drawing zombie: {e}")
                    if zombie in self.zombies:
                        self.zombies.remove(zombie)
        except Exception as e:
            print(f"Error in draw_zombies: {e}")
