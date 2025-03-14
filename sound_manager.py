#sound_manager.py
import pygame
from pathlib import Path

class SoundManager:
    def __init__(self):
        self.sounds = {}  # Sound effects
        self.music = {}   # Music tracks
        self.music_volume = 0.5
        self.sfx_volume = 0.7
        self.current_music = None # Track the currently playing music

    def load_sounds(self, sound_dir="assets/sounds"):
        sound_files = {
            "shoot": "shoot.wav",
            "zombie_death": "zombie_death.wav",
            "player_hurt": "player_hurt.wav",
            "reload": "reload.wav",
            "menu_move": "menu_move.wav",
            "menu_select": "menu_select.wav",
            "game_start": "game_start.wav",
            "game_over": "game_over.wav",
            "weapon_switch": "weapon_switch.wav",
            "bullet_impact": "bullet_impact.wav"
        }

        music_files = {
            "background": "background_music.mp3"
        }

        for name, file in sound_files.items():
            path = Path(sound_dir) / file
            if path.exists():
                self.sounds[name] = pygame.mixer.Sound(str(path)) #Convert path object to string.

        for name, file in music_files.items():
            path = Path(sound_dir) / file
            if path.exists():
                self.music[name] = str(path) #Store the path as a string.

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].set_volume(self.sfx_volume)
            self.sounds[name].play()

    def play_music(self, name):
        if name in self.music:
            pygame.mixer.music.load(self.music[name])
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)
            self.current_music = name #Store the music name.

    def stop_music(self):
        pygame.mixer.music.stop()
        self.current_music = None
