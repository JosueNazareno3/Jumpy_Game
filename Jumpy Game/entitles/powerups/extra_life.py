"""
Power-up Vida Extra para Jumpy Game.

Este módulo contiene la clase ExtraLife que otorga
una vida adicional al jugador.
"""

import pygame
import math
from .powerup import PowerUp
from config import GameConfig


class ExtraLife(PowerUp):
    """
    Power-up que otorga una vida extra al jugador.

    Aumenta el contador de vidas del jugador hasta el máximo permitido.
    """

    def __init__(self, x, y, asset_manager):
        """
        Inicializa una vida extra.

        Args:
            x (int): Posición X
            y (int): Posición Y
            asset_manager (AssetManager): Gestor de assets
        """
        extra_life_image = asset_manager.get_image('extra_life')
        super().__init__(x, y, extra_life_image, GameConfig.POWERUP_SIZE)

        # Propiedades específicas de vida extra
        self.sound = asset_manager.get_sound('extra_life')

        # Animación de pulsación
        self.pulse_offset = 0
        self.pulse_speed = 0.15
        self.original_size = GameConfig.POWERUP_SIZE
        self.pulse_range = 5

    def _update_animation(self):
        """Actualiza la animación de pulsación de la vida extra."""
        # Efecto de pulsación
        self.pulse_offset += self.pulse_speed
        scale_factor = 1 + (math.sin(self.pulse_offset) * 0.1)

        new_width = int(self.original_size[0] * scale_factor)
        new_height = int(self.original_size[1] * scale_factor)

        # Redimensionar imagen manteniendo el centro
        if hasattr(self, '_original_image'):
            center = self.rect.center
            self.image = pygame.transform.scale(self._original_image, (new_width, new_height))
            self.rect = self.image.get_rect()
            self.rect.center = center
        else:
            # Guardar imagen original en la primera ejecución
            self._original_image = self.image.copy()

    def apply_effect(self, player, game_state):
        """
        Aplica el efecto de vida extra al jugador.

        Args:
            player (Player): Jugador que recibe el efecto
            game_state (GameState): Estado actual del juego

        Returns:
            bool: True si el efecto se aplicó correctamente
        """
        try:
            # Verificar si se puede agregar una vida
            if game_state.lives < GameConfig.MAX_LIVES:
                game_state.lives += 1

                # Reproducir sonido
                if self.sound:
                    self.sound.play()

                return True
            else:
                # No se puede agregar más vidas, pero el power-up se consume
                if self.sound:
                    self.sound.play()
                return True

        except Exception as error:
            print(f"Error aplicando efecto de vida extra: {error}")
            return False
