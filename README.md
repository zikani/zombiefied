# zombiefied
A simple zombie survival game built with Pygame.

## Features
- **Player Mechanics**:
  - Movement with collision detection.
  - Multiple weapons with unique stats (Pistol, Shotgun, Assault Rifle, etc.).
  - Reloading and ammo management.
  - Health system with visual indicators.
  - Inventory system for items like health packs and grenades.

- **Zombie AI**:
  - Different zombie types (Regular, Fast, Tank) with unique behaviors.
  - Pathfinding and movement towards the player.
  - Health and damage system with visual effects.

- **Weapons and Combat**:
  - Variety of weapons with different fire rates, damage, and spread.
  - Bullet mechanics with collision detection and trails.
  - Grenade launcher with area-of-effect damage.

- **Game Systems**:
  - Wave-based enemy spawning with increasing difficulty.
  - Minimap with fog of war and zoom functionality.
  - Particle effects for explosions, blood splatter, and sparkles.
  - HUD displaying health, ammo, score, and wave information.

- **Menus and UI**:
  - Main menu with animated title and options.
  - Pause menu with settings and controls.
  - Weapon and item selection wheels.
  - Game over screen with final score and restart option.

- **Audio**:
  - Background music and sound effects for actions like shooting, reloading, and zombie deaths.
  - Adjustable sound and music volume.

- **Map**:
  - Procedurally generated map with terrain types (grass, water, road, walls).
  - Collision detection for obstacles.

## Known Errors
- **Grenade Lifetime**: Occasionally, grenade lifetime is set to `None`, causing errors during updates.
- **Zombie Collision**: Rare cases where zombies get stuck in map obstacles.
- **Sound Loading**: Missing sound files are replaced with silent placeholders, which may cause confusion.
- **Performance**: High particle counts can cause performance drops on lower-end systems.

## Future Implementations
- **Multiplayer Mode**: Add support for cooperative multiplayer gameplay.
- **Boss Zombies**: Introduce boss enemies with unique abilities.
- **Weapon Upgrades**: Allow players to upgrade weapons during gameplay.
- **Achievements**: Add an achievement system for milestones like high scores or zombie kills.
- **Story Mode**: Implement a campaign mode with missions and objectives.
- **Improved AI**: Enhance zombie pathfinding and add more complex behaviors.
- **Dynamic Weather**: Introduce weather effects like rain and fog.
- **Save System**: Allow players to save and load their progress.
- **Custom Maps**: Add support for user-created maps.
- **Localization**: Translate the game into multiple languages.

#game/
├── main.py              # Entry point of the game
├── config.py            # Game settings and constants
├── assets/              # Graphics, sounds, and Image assets, Sound effects and music
├── player.py        # Player class and related logic
├── zombie.py        # Zombie class and behavior
├── weapon.py        # Weapon mechanics and shooting logic
├── bullet.py        # Bullet movement and collisions
|── wave_manager.py  # Handles enemy waves and progression
├── menu.py          # Main menu and pause menu Heads-up display (health, ammo, score),Game over screen logic           
├── particle_collision.py      # Particle effects for visuals
|-- map.py              # random map generator
