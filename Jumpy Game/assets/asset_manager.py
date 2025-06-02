"""
Gestor de assets para Jumpy Game.

Este módulo proporciona una interfaz centralizada para cargar
y gestionar todos los recursos del juego (imágenes, sonidos, música).
"""

import pygame
import os
from config import GameConfig


class AssetManager:
    """
    Maneja la carga y gestión de todos los assets del juego.

    Proporciona métodos para cargar imágenes, sonidos y música,
    con manejo de errores y fallbacks para recursos faltantes.
    """

    def __init__(self, assets_directory):
        """
        Inicializa el gestor de assets.

        Args:
            assets_directory (str): Directorio donde están los assets
        """
        self.assets_dir = assets_directory
        self.images = {}
        self.sounds = {}
        self.music_loaded = False

        # Verificar que el directorio de assets existe
        if not os.path.exists(self.assets_dir):
            print(f"Advertencia: Directorio de assets '{self.assets_dir}' no encontrado")
            print("Se crearán assets por defecto")

    def load_image(self, name, filename, scale=None):
        """
        Carga una imagen y la almacena en el diccionario.

        Args:
            name (str): Nombre identificador de la imagen
            filename (str): Nombre del archivo
            scale (tuple, optional): Tamaño para redimensionar (width, height)

        Returns:
            pygame.Surface: La imagen cargada o una superficie por defecto
        """
        try:
            image_path = os.path.join(self.assets_dir, filename)

            if os.path.exists(image_path):
                image = pygame.image.load(image_path).convert_alpha()

                if scale:
                    image = pygame.transform.scale(image, scale)

                self.images[name] = image
                return image
            else:
                raise FileNotFoundError(f"Archivo no encontrado: {image_path}")

        except (pygame.error, FileNotFoundError) as error:
            print(f"Error cargando imagen {filename}: {error}")
            return self._create_default_image(name, scale)

    def _create_default_image(self, name, scale):
        """
        Crea una imagen por defecto cuando falla la carga.

        Args:
            name (str): Nombre de la imagen
            scale (tuple, optional): Tamaño de la imagen

        Returns:
            pygame.Surface: Imagen por defecto
        """
        default_size = scale if scale else (32, 32)
        default_image = pygame.Surface(default_size)

        # Usar diferentes colores según el tipo de asset
        color_map = {
            'background': GameConfig.BLUE,
            'platform': (139, 69, 19),  # Marrón
            'player_left': GameConfig.YELLOW,
            'player_right': GameConfig.YELLOW,
            'booster': GameConfig.RED,
            'extra_life': GameConfig.GREEN,
            'enemy': GameConfig.RED,
            'icon': GameConfig.MAGENTA
        }

        color = color_map.get(name, GameConfig.MAGENTA)
        default_image.fill(color)

        self.images[name] = default_image
        return default_image

    def load_sound(self, name, filename, volume=1.0):
        """
        Carga un sonido y lo almacena en el diccionario.

        Args:
            name (str): Nombre identificador del sonido
            filename (str): Nombre del archivo
            volume (float): Volumen del sonido (0.0 a 1.0)

        Returns:
            pygame.mixer.Sound: El sonido cargado o uno por defecto
        """
        try:
            sound_path = os.path.join(self.assets_dir, filename)

            if os.path.exists(sound_path):
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(volume)
                self.sounds[name] = sound
                return sound
            else:
                raise FileNotFoundError(f"Archivo no encontrado: {sound_path}")

        except (pygame.error, FileNotFoundError) as error:
            print(f"Error cargando sonido {filename}: {error}")
            return self._create_default_sound(name)

    def _create_default_sound(self, name):
        """
        Crea un sonido silencioso por defecto.

        Args:
            name (str): Nombre del sonido

        Returns:
            pygame.mixer.Sound: Sonido silencioso
        """
        default_sound = pygame.mixer.Sound(pygame.sndarray.make_sound(b'\x00' * 100))
        self.sounds[name] = default_sound
        return default_sound

    def load_music(self, filename, volume=0.9):
        """
        Carga y reproduce música de fondo.

        Args:
            filename (str): Nombre del archivo de música
            volume (float): Volumen de la música (0.0 a 1.0)
        """
        try:
            music_path = os.path.join(self.assets_dir, filename)

            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1, 0.0)  # Loop infinito
                self.music_loaded = True
            else:
                raise FileNotFoundError(f"Archivo no encontrado: {music_path}")

        except (pygame.error, FileNotFoundError) as error:
            print(f"Error cargando música {filename}: {error}")
            self.music_loaded = False

    def get_image(self, name):
        """
        Obtiene una imagen por su nombre.

        Args:
            name (str): Nombre de la imagen

        Returns:
            pygame.Surface: La imagen solicitada o None si no existe
        """
        return self.images.get(name)

    def get_sound(self, name):
        """
        Obtiene un sonido por su nombre.

        Args:
            name (str): Nombre del sonido

        Returns:
            pygame.mixer.Sound: El sonido solicitado o None si no existe
        """
        return self.sounds.get(name)

    def load_all_game_assets(self):
        """
        Carga todos los assets necesarios para el juego.

        Este método centraliza la carga de todos los recursos
        para facilitar la inicialización del juego.
        """
        # Cargar imágenes
        self.load_image('background', GameConfig.BACKGROUND_IMAGE)
        self.load_image('platform', GameConfig.PLATFORM_IMAGE)
        self.load_image('player_left', GameConfig.PLAYER_LEFT_IMAGE, GameConfig.PLAYER_IMAGE_SIZE)
        self.load_image('player_right', GameConfig.PLAYER_RIGHT_IMAGE, GameConfig.PLAYER_IMAGE_SIZE)
        self.load_image('booster', GameConfig.BOOSTER_IMAGE)
        self.load_image('extra_life', GameConfig.EXTRA_LIFE_IMAGE)
        self.load_image('enemy_bird', GameConfig.ENEMY_BIRD_IMAGE)
        self.load_image('icon', GameConfig.ICON_IMAGE)

        # Cargar sonidos
        self.load_sound('jump', GameConfig.JUMP_SOUND, GameConfig.SOUND_VOLUME)
        self.load_sound('death', GameConfig.DEATH_SOUND, GameConfig.SOUND_VOLUME)
        self.load_sound('boost', GameConfig.BOOST_SOUND, GameConfig.POWERUP_SOUND_VOLUME)
        self.load_sound('extra_life', GameConfig.EXTRA_LIFE_SOUND, GameConfig.POWERUP_SOUND_VOLUME)

        # Cargar música
        self.load_music(GameConfig.BACKGROUND_MUSIC, GameConfig.MUSIC_VOLUME)

    def get_asset_count(self):
        """
        Obtiene el número total de assets cargados.

        Returns:
            dict: Diccionario con el conteo de cada tipo de asset
        """
        return {
            'images': len(self.images),
            'sounds': len(self.sounds),
            'music_loaded': self.music_loaded
        }

    def cleanup(self):
        """Limpia todos los assets cargados."""
        self.images.clear()
        self.sounds.clear()
        if self.music_loaded:
            pygame.mixer.music.stop()
            self.music_loaded = False
