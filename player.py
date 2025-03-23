#sound_manager.py
import pygame
import os
from pathlib import Path

class SoundManager:
    def __init__(self):
        self.sounds = {}  # Sound effects
        self.music = {}   # Music tracks
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.current_music = None # Track the currently playing music
        self.sound_enabled = True
        self.music_enabled = True
        self.sound_volume = 0.7
        self.music_volume = 0.5

    def load_sounds(self, sound_dir="assets/sounds"):
        """Load all game sounds with error handling"""
        try:
            # Initialize pygame mixer if not already
            if not pygame.mixer.get_init():
                try:
                    pygame.mixer.init()
                except Exception as e:
                    print(f"Could not initialize mixer: {e}")
                    return
                
            # Create directory if it doesn't exist
            sound_path = Path(sound_dir)
            os.makedirs(sound_path, exist_ok=True)
                
            # Define sound files
            sound_files = {
                "shoot": "shoot.wav",
                "reload": "reload.wav",
                "bullet_impact": "bullet_impact.wav",
                "zombie_death": "zombie_death.wav",
                "player_hurt": "player_hurt.wav",
                "menu_move": "menu_move.wav",
                "menu_select": "menu_select.wav",
                "game_start": "game_start.wav",
                "game_over": "game_over.wav",
                "pickup": "pickup.wav",
                "weapon_switch": "weapon_switch.wav",
            }
            
            # Load each sound with warning but don't crash
            for name, file in sound_files.items():
                try:
                    path = Path(sound_dir) / file
                    if path.exists():
                        self.sounds[name] = pygame.mixer.Sound(str(path))
                        self.sounds[name].set_volume(self.sfx_volume)
                    else:
                        # Create a silent dummy sound for missing files
                        buffer = pygame.mixer.Sound(buffer=bytearray(44))  # Empty sound buffer
                        self.sounds[name] = buffer
                        print(f"Created silent placeholder for missing sound: {path}")
                except Exception as e:
                    # Create a silent dummy sound on error
                    buffer = pygame.mixer.Sound(buffer=bytearray(44)) 
                    self.sounds[name] = buffer
                    print(f"Error loading sound {name}: {e}, using silent placeholder")
            
            # Define music files
            music_files = {
                "background": "background_music.mp3",
                "menu": "menu_music.mp3",
                "game_over": "game_over_music.mp3"
            }
            
            # Only add music entries if files exist, otherwise warn
            for name, file in music_files.items():
                path = Path(sound_dir) / file
                if path.exists():
                    self.music[name] = str(path)
                else:
                    print(f"Music file not found: {path}")
                    
        except Exception as e:
            print(f"Error initializing sound manager: {e}")

    def play_sound(self, name):
        """Play a sound effect with error handling"""
        try:
            if self.sound_enabled and name in self.sounds:
                self.sounds[name].set_volume(self.sfx_volume)
                self.sounds[name].play()
        except Exception as e:
            print(f"Error playing sound {name}: {e}")

    def play_music(self, name):
        """Play background music with error handling"""
        try:
            if self.music_enabled and name in self.music:
                if self.current_music != name:
                    self.current_music = name
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load(self.music[name])
                    pygame.mixer.music.set_volume(self.music_volume)
                    pygame.mixer.music.play(-1)  # Loop infinitely
            else:
                # Silently ignore missing music to prevent game disruption
                pass
        except Exception as e:
            print(f"Error playing music {name}: {e}")

    def stop_music(self):
        """Stop currently playing music with error handling"""
        try:
            pygame.mixer.music.stop()
            self.current_music = None
        except Exception as e:
            print(f"Error stopping music: {e}")

    def set_sound_volume(self, volume):
        """Set volume for sound effects with error handling"""
        try:
            volume = max(0.0, min(1.0, volume))
            self.sfx_volume = volume
            for sound in self.sounds.values():
                sound.set_volume(self.sfx_volume)
            return True
        except Exception as e:
            print(f"Error setting sound volume: {e}")
            return False

    def set_music_volume(self, volume):
        """Set volume for music with error handling"""
        try:
            volume = max(0.0, min(1.0, volume))
            self.music_volume = volume
            pygame.mixer.music.set_volume(self.music_volume)
            return True
        except Exception as e:
            print(f"Error setting music volume: {e}")
            return False

    def toggle_sound(self):
        """Toggle sound effects on/off"""
        try:
            self.sound_enabled = not self.sound_enabled
            return self.sound_enabled
        except Exception as e:
            print(f"Error toggling sound: {e}")
            return self.sound_enabled

    def toggle_music(self):
        """Toggle music on/off"""
        try:
            self.music_enabled = not self.music_enabled
            if self.music_enabled and self.current_music:
                self.play_music(self.current_music)
            else:
                pygame.mixer.music.stop()
            return self.music_enabled
        except Exception as e:
            print(f"Error toggling music: {e}")
            return self.music_enabled
