"""
Clase base para power-ups del juego Jumpy Game.

Este módulo contiene la clase base PowerUp de la cual heredan
todos los power-ups específicos del juego.
"""

import pygame
from config import GameConfig


class PowerUp(pygame.sprite.Sprite):
    """
    Clase base para power-ups.

    Proporciona funcionalidad común para todos los power-ups
    como movimiento, colisiones y eliminación automática.
    """

    def __init__(self, x, y, image, size=None):
        """
        Inicializa un power-up.

        Args:
            x (int): Posición X
            y (int): Posición Y
            image (pygame.Surface): Imagen del power-up
            size (tuple, optional): Tamaño del power-up (width, height)
        """
        super().__init__()

        # Configurar imagen
        if image and size:
            self.image = pygame.transform.scale(image, size)
        elif image:
            self.image = image
        else:
            # Crear imagen por defecto
            default_size = size if size else GameConfig.POWERUP_SIZE
            self.image = pygame.Surface(default_size)
            self.image.fill(GameConfig.YELLOW)

        # Configurar rectángulo de colisión
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Propiedades del power-up
        self.collected = False
        self.creation_time = pygame.time.get_ticks()

        # Máscara para colisiones precisas
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, scroll):
        """
        Actualiza la posición del power-up.

        Args:
            scroll (int): Cantidad de scroll a aplicar
        """
        # Aplicar scroll vertical
        self.rect.y += scroll

        # Eliminar si sale de la pantalla
        if self.rect.top > GameConfig.SCREEN_HEIGHT:
            self.kill()

        # Actualizar animación si existe
        self._update_animation()

    def _update_animation(self):
        """
        Actualiza la animación del power-up.

        Método base que puede ser sobrescrito por subclases
        para implementar animaciones específicas.
        """
        pass

    def collect(self, player, game_state):
        """
        Maneja la recolección del power-up.

        Args:
            player (Player): Jugador que recolecta el power-up
            game_state (GameState): Estado actual del juego

        Returns:
            bool: True si el power-up fue recolectado exitosamente
        """
        if not self.collected:
            self.collected = True
            success = self.apply_effect(player, game_state)
            if success:
                self.kill()  # Eliminar del grupo de sprites
            return success
        return False

    def apply_effect(self, player, game_state):
        """
        Aplica el efecto del power-up.

        Método base que debe ser sobrescrito por subclases
        para implementar efectos específicos.

        Args:
            player (Player): Jugador que recibe el efecto
            game_state (GameState): Estado actual del juego

        Returns:
            bool: True si el efecto se aplicó correctamente
        """
        return True

    def get_collision_rect(self):
        """
        Obtiene el rectángulo de colisión del power-up.

        Returns:
            pygame.Rect: Rectángulo de colisión
        """
        return self.rect

    def get_collision_mask(self):
        """
        Obtiene la máscara de colisión del power-up.

        Returns:
            pygame.Mask: Máscara para colisiones precisas
        """
        return self.mask

    def is_collected(self):
        """
        Verifica si el power-up ha sido recolectado.

        Returns:
            bool: True si ha sido recolectado
        """
        return self.collected

    def get_age(self):
        """
        Obtiene la edad del power-up en milisegundos.

        Returns:
            int: Tiempo transcurrido desde la creación
        """
        return pygame.time.get_ticks() - self.creation_time

    def get_position(self):
        """
        Obtiene la posición actual del power-up.

        Returns:
            tuple: (x, y) posición del centro del power-up
        """
        return self.rect.center

    def is_on_screen(self):
        """
        Verifica si el power-up está visible en la pantalla.

        Returns:
            bool: True si está en pantalla
        """
        return (0 <= self.rect.right and
                self.rect.left <= GameConfig.SCREEN_WIDTH and
                0 <= self.rect.bottom and
                self.rect.top <= GameConfig.SCREEN_HEIGHT)
