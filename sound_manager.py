# sound_manager.py
import pygame
from pathlib import Path

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_volume = 0.5
        self.sfx_volume = 0.7

    def load_sounds(self, sound_dir="assets/sounds"):
        sound_files = {
            "shoot": "shoot.wav",
            "zombie_death": "zombie_death.wav",
            "player_hurt": "player_hurt.wav",
            "background": "background_music.mp3",
            "reload":"reload.wav"
        }

        for name, file in sound_files.items():
            path = Path(sound_dir) / file
            if path.exists():
                self.sounds[name] = pygame.mixer.Sound(path)

    def play_sound(self, name):
        if name in self.sounds:
            self.sounds[name].set_volume(self.sfx_volume)
            self.sounds[name].play()

    def play_music(self, name):
        if name in self.sounds:
            self.sounds[name].set_volume(self.music_volume)
            self.sounds[name].play(-1)