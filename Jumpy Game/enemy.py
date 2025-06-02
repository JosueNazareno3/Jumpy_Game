"""
Módulo Enemy - Maneja los enemigos del juego Jumpy Game.

Este módulo contiene la clase Enemy que representa a los enemigos
voladores (pájaros) que aparecen en el juego.
"""

import pygame
import random


class Enemy(pygame.sprite.Sprite):
    """
    Clase que representa un enemigo volador en el juego.

    Los enemigos se mueven horizontalmente a través de la pantalla
    con animaciones de sprite y pueden aparecer desde cualquier lado.
    """

    def __init__(self, screen_width, y_position, sprite_sheet, scale_factor):
        """
        Inicializa un nuevo enemigo.

        Args:
            screen_width (int): Ancho de la pantalla del juego
            y_position (int): Posición Y donde aparecerá el enemigo
            sprite_sheet (SpriteSheet): Hoja de sprites para la animación
            scale_factor (float): Factor de escala para el tamaño del enemigo
        """
        super().__init__()

        # Configuración de animación
        self.animation_frames = []
        self.current_frame_index = 0
        self.last_update_time = pygame.time.get_ticks()
        self.animation_cooldown = 50  # Milisegundos entre frames

        # Configuración de movimiento
        self.movement_direction = random.choice([-1, 1])  # -1 = izquierda, 1 = derecha
        self.movement_speed = 2
        self.is_flipped = self.movement_direction == 1

        # Cargar frames de animación
        self._load_animation_frames(sprite_sheet, scale_factor)

        # Configurar sprite inicial
        self.image = self.animation_frames[self.current_frame_index]
        self.rect = self.image.get_rect()

        # Posicionar enemigo según dirección
        self._set_initial_position(screen_width, y_position)

    def _load_animation_frames(self, sprite_sheet, scale_factor):
        """
        Carga todos los frames de animación del enemigo.

        Args:
            sprite_sheet (SpriteSheet): Hoja de sprites para extraer frames
            scale_factor (float): Factor de escala para redimensionar
        """
        total_animation_frames = 8
        frame_width = 32
        frame_height = 32
        transparent_color = (0, 0, 0)  # Negro como color transparente

        for frame_index in range(total_animation_frames):
            # Extraer frame de la sprite sheet
            frame_image = sprite_sheet.get_image(
                frame_index, frame_width, frame_height,
                scale_factor, transparent_color
            )

            # Voltear imagen si es necesario
            if self.is_flipped:
                frame_image = pygame.transform.flip(frame_image, True, False)

            # Configurar transparencia
            frame_image.set_colorkey(transparent_color)

            # Agregar frame a la lista
            self.animation_frames.append(frame_image)

    def _set_initial_position(self, screen_width, y_position):
        """
        Establece la posición inicial del enemigo según su dirección.

        Args:
            screen_width (int): Ancho de la pantalla
            y_position (int): Posición Y del enemigo
        """
        if self.movement_direction == 1:  # Moviéndose hacia la derecha
            self.rect.x = 0  # Empezar desde el lado izquierdo
        else:  # Moviéndose hacia la izquierda
            self.rect.x = screen_width  # Empezar desde el lado derecho

        self.rect.y = y_position

    def _update_animation(self):
        """Actualiza la animación del enemigo."""
        current_time = pygame.time.get_ticks()

        # Verificar si es tiempo de cambiar frame
        if current_time - self.last_update_time > self.animation_cooldown:
            self.last_update_time = current_time
            self.current_frame_index += 1

            # Reiniciar animación si llegó al final
            if self.current_frame_index >= len(self.animation_frames):
                self.current_frame_index = 0

        # Actualizar imagen actual
        self.image = self.animation_frames[self.current_frame_index]

    def _update_movement(self, scroll_amount):
        """
        Actualiza el movimiento del enemigo.

        Args:
            scroll_amount (int): Cantidad de scroll vertical a aplicar
        """
        # Movimiento horizontal
        self.rect.x += self.movement_direction * self.movement_speed

        # Movimiento vertical (scroll del juego)
        self.rect.y += scroll_amount

    def _check_if_off_screen(self, screen_width):
        """
        Verifica si el enemigo salió de la pantalla y lo elimina si es necesario.

        Args:
            screen_width (int): Ancho de la pantalla
        """
        if self.rect.right < 0 or self.rect.left > screen_width:
            self.kill()  # Eliminar sprite del grupo

    def update(self, scroll_amount, screen_width):
        """
        Actualiza el estado completo del enemigo.

        Este método se llama en cada frame del juego para actualizar
        la animación, posición y verificar si debe ser eliminado.

        Args:
            scroll_amount (int): Cantidad de scroll vertical del juego
            screen_width (int): Ancho de la pantalla del juego
        """
        self._update_animation()
        self._update_movement(scroll_amount)
        self._check_if_off_screen(screen_width)

    def get_collision_mask(self):
        """
        Obtiene la máscara de colisión del enemigo.

        Returns:
            pygame.Mask: Máscara para detección de colisiones precisas
        """
        return pygame.mask.from_surface(self.image)
