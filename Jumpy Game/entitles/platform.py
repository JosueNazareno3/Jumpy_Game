"""
Plataformas del juego Jumpy Game.

Este módulo contiene la clase Platform que representa las plataformas
sobre las que salta el jugador.
"""

import pygame
import random
from config import GameConfig


class Platform(pygame.sprite.Sprite):
    """
    Clase que representa una plataforma en el juego.

    Las plataformas pueden ser estáticas o móviles, y proporcionan
    superficies sobre las que el jugador puede saltar.
    """

    def __init__(self, x, y, width, is_moving, asset_manager):
        """
        Inicializa una plataforma.

        Args:
            x (int): Posición X
            y (int): Posición Y
            width (int): Ancho de la plataforma
            is_moving (bool): Si la plataforma se mueve
            asset_manager (AssetManager): Gestor de assets
        """
        super().__init__()

        # Cargar imagen de la plataforma
        platform_image = asset_manager.get_image('platform')
        if platform_image:
            self.image = pygame.transform.scale(platform_image, (width, 10))
        else:
            # Crear plataforma por defecto
            self.image = pygame.Surface((width, 10))
            self.image.fill((139, 69, 19))  # Color marrón

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Configuración de movimiento
        self.is_moving = is_moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.original_width = width

        # Límites de movimiento
        self.left_boundary = 0
        self.right_boundary = GameConfig.SCREEN_WIDTH

    def _update_movement(self):
        """Actualiza el movimiento de la plataforma si es móvil."""
        if not self.is_moving:
            return

        self.move_counter += 1

        # Calcular nueva posición
        new_x = self.rect.x + (self.direction * self.speed)

        # Verificar límites y cambiar dirección si es necesario
        if (self.move_counter >= 100 or
                new_x < self.left_boundary or
                new_x + self.rect.width > self.right_boundary):
            self.direction *= -1
            self.move_counter = 0
        else:
            self.rect.x = new_x

    def update(self, scroll):
        """
        Actualiza la plataforma.

        Args:
            scroll (int): Cantidad de scroll a aplicar
        """
        # Actualizar movimiento horizontal
        self._update_movement()

        # Aplicar scroll vertical
        self.rect.y += scroll

        # Eliminar si sale de la pantalla
        if self.rect.top > GameConfig.SCREEN_HEIGHT:
            self.kill()

    def get_collision_rect(self):
        """
        Obtiene el rectángulo de colisión de la plataforma.

        Returns:
            pygame.Rect: Rectángulo de colisión
        """
        return self.rect

    def get_top_surface(self):
        """
        Obtiene la superficie superior de la plataforma.

        Returns:
            int: Coordenada Y de la superficie superior
        """
        return self.rect.top

    def get_width(self):
        """
        Obtiene el ancho de la plataforma.

        Returns:
            int: Ancho de la plataforma
        """
        return self.rect.width

    def get_center_x(self):
        """
        Obtiene la coordenada X del centro de la plataforma.

        Returns:
            int: Coordenada X del centro
        """
        return self.rect.centerx

    def is_player_on_platform(self, player_rect):
        """
        Verifica si el jugador está sobre esta plataforma.

        Args:
            player_rect (pygame.Rect): Rectángulo del jugador

        Returns:
            bool: True si el jugador está sobre la plataforma
        """
        return (player_rect.bottom <= self.rect.top + 5 and
                player_rect.bottom >= self.rect.top - 5 and
                player_rect.centerx >= self.rect.left and
                player_rect.centerx <= self.rect.right)

    def set_movement_boundaries(self, left, right):
        """
        Establece los límites de movimiento para plataformas móviles.

        Args:
            left (int): Límite izquierdo
            right (int): Límite derecho
        """
        self.left_boundary = left
        self.right_boundary = right

    def stop_movement(self):
        """Detiene el movimiento de la plataforma."""
        self.is_moving = False

    def start_movement(self):
        """Inicia el movimiento de la plataforma."""
        self.is_moving = True

    def get_movement_info(self):
        """
        Obtiene información sobre el movimiento de la plataforma.

        Returns:
            dict: Información de movimiento
        """
        return {
            'is_moving': self.is_moving,
            'direction': self.direction,
            'speed': self.speed,
            'position': self.rect.center
        }
