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
        "damage": 25,
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
        "damage": 150,
        "spread": 0.01,
    },
    "submachine_gun": {
        "fire_rate": 100,
        "damage": 12,
        "spread": 0.08,
    },
    "grenade_launcher": {
        "fire_rate": 2000,
        "damage": 500,
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
    # Additional colors for UI
    "dark_blue": (0, 0, 139),
    "light_blue": (173, 216, 230),
    "gray": (128, 128, 128),
    "dark_gray": (64, 64, 64),
    "light_gray": (192, 192, 192),
    "brown": (165, 42, 42),
    "orange": (255, 165, 0),
    "purple": (128, 0, 128),
    "cyan": (0, 255, 255),
    "pink": (255, 192, 203),
    "gold": (255, 215, 0),
    "silver": (192, 192, 192),
    "transparent_black": (0, 0, 0, 128),
}

# UI Settings
UI_SETTINGS = {
    "health_bar_width": 200,
    "health_bar_height": 25,
    "ammo_bar_width": 150,
    "minimap_size": 150,
    "crosshair_size": 10,
    "crosshair_thickness": 2,
    "slot_width": 100,
    "slot_height": 50,
    "slot_spacing": 10,
    "tip_display_time": 5000,
}

# Particle Settings
PARTICLE_SETTINGS = {
    "explosion_count": 20,
    "blood_count": 15,
    "impact_count": 8,
    "max_lifetime": 20,
    "min_lifetime": 10,
    "max_size": 5,
    "min_size": 2,
}
