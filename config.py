# config.py
WIDTH, HEIGHT = 800, 650
FPS = 60
TILE_SIZE = 64
PLAYER_SPEED = 5
ZOMBIE_SPEED = 2
BULLET_SPEED = 15
MAX_AMMO = 30
PLAYER_HEALTH = 100
SPAWN_INTERVAL = 3000  # 3 seconds

COLORS = {
    "white": (255, 255, 255),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "black": (0, 0, 0),
    "ammo": (255, 165, 0),
}
# Add these constants
MAX_AMMO = {
    "pistol": 30,
    "shotgun": 8
}
RELOAD_TIME = 2000  # 2 seconds
# Add these to existing constants
MAP_WIDTH = 100
MAP_HEIGHT = 100
VIEW_RADIUS_TILES = 8  # Tiles visible around player
MAP_SIZE = 2048  # Should be divisible by TILE_SIZE
PLAYER_RADIUS = 16  # Collision radius for entities
ZOMBIE_RADIUS = 12
# Add these constants
SPAWN_DISTANCE = 600  # Distance from player to spawn
ZOMBIE_HEALTH = 50
