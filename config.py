# config.py

# Screen dimensions
WIDTH, HEIGHT = 800, 650
FPS = 60
TILE_SIZE = 64

# Player settings
PLAYER_SPEED = 5
PLAYER_RADIUS = 16
PLAYER_HEALTH = 100

# Zombie settings
ZOMBIE_SPEED = 2
ZOMBIE_RADIUS = 12
ZOMBIE_HEALTH = 100

# Bullet settings
BULLET_SPEED = 15

# Weapon settings
RELOAD_TIME = 2000  # 2 seconds

MAX_AMMO = {
    "pistol": 30,
    "shotgun": 8,
    "assault_rifle": 100,
    "sniper_rifle": 10,
    "submachine_gun": 150,
    "grenade_launcher": 5,
}

WEAPON_STATS = {
    "pistol": {
        "fire_rate": 500,
        "damage": 20,
        "spread": 0.05,
    },
    "shotgun": {
        "fire_rate": 1000,
        "damage": 50,
        "spread": 0.2,
    },
    "assault_rifle": {
        "fire_rate": 150,
        "damage": 15,
        "spread": 0.03,
    },
    "sniper_rifle": {
        "fire_rate": 1500,
        "damage": 100,
        "spread": 0.01,
    },
    "submachine_gun": {
        "fire_rate": 100,
        "damage": 10,
        "spread": 0.08,
    },
    "grenade_launcher": {
        "fire_rate": 2000,
        "damage": 50,
        "spread": 0.1,
    },
}

# Map settings
MAP_WIDTH = 100
MAP_HEIGHT = 100
VIEW_RADIUS_TILES = 8
MAP_SIZE = 2048

# Spawn settings
SPAWN_DISTANCE = 600
SPAWN_INTERVAL = 3000  # 3 seconds

# Colors
COLORS = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "dark_red": (139, 0, 0),
    "ammo": (255, 255, 0),
}
