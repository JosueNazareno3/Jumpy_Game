"""
Power-up Booster para Jumpy Game.

Este módulo contiene la clase Booster que proporciona
un salto súper potente al jugador.
"""

import pygame
import math
from .powerup import PowerUp
from config import GameConfig


class Booster(PowerUp):
    """
    Power-up que aumenta la altura del salto del jugador.

    Cuando se recolecta, proporciona un impulso inmediato hacia arriba
    y modifica temporalmente la velocidad de salto.
    """

    def __init__(self, x, y, asset_manager):
        """
        Inicializa un booster.

        Args:
            x (int): Posición X
            y (int): Posición Y
            asset_manager (AssetManager): Gestor de assets
        """
        booster_image = asset_manager.get_image('booster')
        super().__init__(x, y, booster_image, GameConfig.POWERUP_SIZE)

        # Propiedades específicas del booster
        self.boost_power = GameConfig.BOOST_JUMP_VELOCITY
        self.sound = asset_manager.get_sound('boost')

        # Animación de flotación
        self.float_offset = 0
        self.float_speed = 0.1
        self.original_y = y

    def _update_animation(self):
        """Actualiza la animación de flotación del booster."""
        # Efecto de flotación suave
        self.float_offset += self.float_speed
        float_y = self.original_y + math.sin(self.float_offset) * 3
        self.rect.centery = int(float_y)

    def apply_effect(self, player, game_state):
        """
        Aplica el efecto del booster al jugador.

        Args:
            player (Player): Jugador que recibe el efecto
            game_state (GameState): Estado actual del juego

        Returns:
            bool: True si el efecto se aplicó correctamente
        """
        try:
            # Aplicar impulso inmediato hacia arriba
            player.velocity_y = self.boost_power
            player.current_jump_velocity = self.boost_power
            player.is_in_air = True

            # Reproducir sonido
            if self.sound:
                self.sound.play()

            return True

        except Exception as error:
            print(f"Error aplicando efecto de booster: {error}")
            return False

    def update(self, scroll):
        """
        Actualiza el booster con animación especial.

        Args:
            scroll (int): Cantidad de scroll a aplicar
        """
        # Actualizar posición original para el scroll
        self.original_y += scroll

        # Llamar al update base
        super().update(scroll)
