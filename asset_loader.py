"""
Cargador de assets para Jumpy Game.
Maneja la carga de imágenes, sonidos y música.
"""

import pygame
import os
from game_config import *


class AssetLoader:
    """Maneja la carga de todos los assets del juego."""

    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.music_loaded = False

    def load_image(self, name, filename, scale=None):
        """Carga una imagen con manejo de errores."""
        try:
            image_path = os.path.join(ASSETS_DIR, filename)
            image = pygame.image.load(image_path).convert_alpha()

            if scale:
                image = pygame.transform.scale(image, scale)

            self.images[name] = image
            return image

        except pygame.error as e:
            print(f"Error cargando imagen {filename}: {e}")
            # Crear imagen por defecto
            default_size = scale if scale else (32, 32)
            default_image = pygame.Surface(default_size)
            default_image.fill(YELLOW)
            self.images[name] = default_image
            return default_image

    def load_sound(self, name, filename, volume=1.0):
        """Carga un sonido con manejo de errores."""
        try:
            sound_path = os.path.join(ASSETS_DIR, filename)
            sound = pygame.mixer.Sound(sound_path)
            sound.set_volume(volume)
            self.sounds[name] = sound
            return sound

        except pygame.error as e:
            print(f"Error cargando sonido {filename}: {e}")
            # Crear sonido silencioso por defecto
            default_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(b'\x00' * 100))
            self.sounds[name] = default_sound
            return default_sound

    def load_music(self, filename, volume=0.9):
        """Carga música de fondo."""
        try:
            music_path = os.path.join(ASSETS_DIR, filename)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(-1, 0.0)
            self.music_loaded = True
        except pygame.error as e:
            print(f"Error cargando música {filename}: {e}")
            self.music_loaded = False

    def load_all_assets(self):
        """Carga todos los assets del juego."""
        # Cargar imágenes
        self.load_image('background', 'background1.jpg')
        self.load_image('platform', 'wood.png')
        self.load_image('player_left', 'bee_rest_l.png', PLAYER_IMAGE_SIZE)
        self.load_image('player_right', 'bee_rest_r.png', PLAYER_IMAGE_SIZE)
        self.load_image('booster', 'booster.webp')
        self.load_image('extra_life', 'extra_life.png')
        self.load_image('bird_enemy', 'bird.png')
        self.load_image('icon', 'ghost.png')

        # Cargar sonidos
        self.load_sound('jump', 'jump.mp3', 1.0)
        self.load_sound('death', 'death.mp3', 1.0)
        self.load_sound('boost', 'boost.mp3', 0.8)
        self.load_sound('extra_life', 'powerup.wav', 0.8)

        # Cargar música
        self.load_music('music_game-2d.mp3', 0.9)

    def get_image(self, name):
        """Obtiene una imagen por nombre."""
        return self.images.get(name)

    def get_sound(self, name):
        """Obtiene un sonido por nombre."""
        return self.sounds.get(name)
