# map.py
import pygame
import random
import math
from config import *

class GameMap:
    def __init__(self, size=MAP_SIZE, tile_size=TILE_SIZE, assets=None):
        self.size = size
        self.tile_size = tile_size
        self.grid_size = size // tile_size
        self.assets = assets
        self.grid = self.generate_map()
        self.load_tile_definitions()

    def load_tile_definitions(self):
        """Load tile types with passability and textures"""
        self.tile_defs = {
            0: {"name": "grass", "passable": True, "color": (34, 139, 34)},
            1: {"name": "wall", "passable": False, "color": (139, 69, 19)},
            2: {"name": "water", "passable": False, "color": (0, 128, 255)},
            3: {"name": "road", "passable": True, "color": (100, 100, 100)}
        }

    def generate_map(self):
        """Hybrid map generation with procedural elements and borders"""
        grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        edge_padding = 3

        # Generate procedural terrain
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # Generate noise-based value (0-1)
                value = math.sin(x/10) + math.sin(y/8) + 1.5 * math.sin(x/15) * math.cos(y/12)
                norm_value = (value + 3) / 6  # Normalize to 0-1 range

                if norm_value < 0.3:
                    grid[y][x] = 2  # Water
                elif norm_value > 0.7:
                    grid[y][x] = 3  # Road

        # Add borders and random walls
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if (x < edge_padding or y < edge_padding or 
                    x >= self.grid_size - edge_padding or 
                    y >= self.grid_size - edge_padding):
                    grid[y][x] = 1  # Border walls
                elif random.random() < 0.08 and grid[y][x] == 0:
                    grid[y][x] = 1  # Random interior walls

        return grid

    def is_passable(self, x, y):
        """Check passability at world coordinates"""
        grid_x = int(x // self.tile_size)
        grid_y = int(y // self.tile_size)
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            return self.tile_defs[self.grid[grid_y][grid_x]]["passable"]
        return False

    def check_collision(self, x, y, radius=PLAYER_RADIUS):
        """Improved collision detection with radius"""
        grid_x = int(x // self.tile_size)
        grid_y = int(y // self.tile_size)
        
        for i in range(max(0, grid_x - 1), min(self.grid_size, grid_x + 2)):
            for j in range(max(0, grid_y - 1), min(self.grid_size, grid_y + 2)):
                if self.grid[j][i] in [1, 2]:  # Walls and water
                    rect_x = i * self.tile_size
                    rect_y = j * self.tile_size
                    
                    # Find closest point on tile
                    closest_x = max(rect_x, min(x, rect_x + self.tile_size))
                    closest_y = max(rect_y, min(y, rect_y + self.tile_size))
                    
                    distance = math.hypot(x - closest_x, y - closest_y)
                    if distance < radius:
                        return True
        return False

    def draw(self, screen, camera_x, camera_y):
        """Optimized drawing with camera view"""
        start_x = max(0, int(camera_x // self.tile_size))
        end_x = min(self.grid_size, int((camera_x + WIDTH) // self.tile_size) + 1)
        start_y = max(0, int(camera_y // self.tile_size))
        end_y = min(self.grid_size, int((camera_y + HEIGHT) // self.tile_size) + 1)

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                tile_type = self.grid[y][x]
                texture = self.get_tile_texture(tile_type)
                
                screen.blit(texture, (
                    x * self.tile_size - camera_x,
                    y * self.tile_size - camera_y
                ))  # Adjust for camera

    def get_tile_texture(self, tile_type):
        """Get tile texture from assets or generate color"""
        if self.assets and f"tile_{self.tile_defs[tile_type]['name']}" in self.assets.textures:
            return self.assets.textures[f"tile_{self.tile_defs[tile_type]['name']}"]
        
        # Fallback to colored surface
        surface = pygame.Surface((self.tile_size, self.tile_size))
        surface.fill(self.tile_defs[tile_type]["color"])
        return surface