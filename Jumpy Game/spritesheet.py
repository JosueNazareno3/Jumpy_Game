"""
Módulo SpriteSheet - Maneja la extracción de sprites de hojas de sprites.

Este módulo proporciona la funcionalidad para extraer sprites individuales
de una imagen que contiene múltiples sprites organizados en una cuadrícula.
"""

import pygame


class SpriteSheet:
    """
    Clase para manejar hojas de sprites (sprite sheets).

    Permite extraer sprites individuales de una imagen más grande
    que contiene múltiples sprites organizados en filas y columnas.
    """

    def __init__(self, sprite_sheet_image):
        """
        Inicializa la hoja de sprites.

        Args:
            sprite_sheet_image (pygame.Surface): Imagen que contiene los sprites
        """
        if not isinstance(sprite_sheet_image, pygame.Surface):
            raise TypeError("sprite_sheet_image debe ser una pygame.Surface")

        self.sprite_sheet = sprite_sheet_image
        self.sheet_width = sprite_sheet_image.get_width()
        self.sheet_height = sprite_sheet_image.get_height()

    def get_image(self, frame_index, frame_width, frame_height,
                  scale_factor=1, transparent_color=(0, 0, 0)):
        """
        Extrae un sprite específico de la hoja de sprites.

        Args:
            frame_index (int): Índice del frame a extraer (empezando desde 0)
            frame_width (int): Ancho de cada frame en píxeles
            frame_height (int): Alto de cada frame en píxeles
            scale_factor (float, optional): Factor de escala para redimensionar.
                                          Por defecto es 1 (sin escalar)
            transparent_color (tuple, optional): Color a hacer transparente (R, G, B).
                                                Por defecto es negro (0, 0, 0)

        Returns:
            pygame.Surface: Sprite extraído y procesado

        Raises:
            ValueError: Si los parámetros de frame son inválidos
            ZeroDivisionError: Si frame_width es 0
        """
        # Validar parámetros
        if frame_width <= 0 or frame_height <= 0:
            raise ValueError("frame_width y frame_height deben ser mayores que 0")

        if frame_index < 0:
            raise ValueError("frame_index debe ser mayor o igual a 0")

        if scale_factor <= 0:
            raise ValueError("scale_factor debe ser mayor que 0")

        # Calcular número de columnas en la hoja de sprites
        columns_count = self.sheet_width // frame_width

        if columns_count == 0:
            raise ValueError("frame_width es mayor que el ancho de la hoja de sprites")

        # Calcular posición del frame en la cuadrícula
        row = frame_index // columns_count
        column = frame_index % columns_count

        # Calcular coordenadas del frame
        frame_x = column * frame_width
        frame_y = row * frame_height

        # Verificar que el frame esté dentro de los límites de la imagen
        if (frame_x + frame_width > self.sheet_width or
            frame_y + frame_height > self.sheet_height):
            raise ValueError(f"Frame {frame_index} está fuera de los límites de la hoja de sprites")

        # Crear superficie para el frame extraído
        extracted_frame = pygame.Surface((frame_width, frame_height)).convert_alpha()

        # Copiar la porción correspondiente de la hoja de sprites
        source_rect = pygame.Rect(frame_x, frame_y, frame_width, frame_height)
        extracted_frame.blit(self.sprite_sheet, (0, 0), source_rect)

        # Aplicar escala si es necesario
        if scale_factor != 1:
            new_width = int(frame_width * scale_factor)
            new_height = int(frame_height * scale_factor)
            extracted_frame = pygame.transform.scale(extracted_frame, (new_width, new_height))

        # Configurar color transparente
        extracted_frame.set_colorkey(transparent_color)

        return extracted_frame

    def get_frame_count(self, frame_width, frame_height):
        """
        Calcula el número total de frames disponibles en la hoja de sprites.

        Args:
            frame_width (int): Ancho de cada frame
            frame_height (int): Alto de cada frame

        Returns:
            int: Número total de frames disponibles

        Raises:
            ValueError: Si los parámetros de frame son inválidos
        """
        if frame_width <= 0 or frame_height <= 0:
            raise ValueError("frame_width y frame_height deben ser mayores que 0")

        columns = self.sheet_width // frame_width
        rows = self.sheet_height // frame_height

        return columns * rows

    def get_sheet_dimensions(self):
        """
        Obtiene las dimensiones de la hoja de sprites.

        Returns:
            tuple: (ancho, alto) de la hoja de sprites
        """
        return (self.sheet_width, self.sheet_height)

    def extract_all_frames(self, frame_width, frame_height, scale_factor=1,
                          transparent_color=(0, 0, 0)):
        """
        Extrae todos los frames de la hoja de sprites.

        Args:
            frame_width (int): Ancho de cada frame
            frame_height (int): Alto de cada frame
            scale_factor (float, optional): Factor de escala. Por defecto es 1
            transparent_color (tuple, optional): Color transparente. Por defecto es negro

        Returns:
            list: Lista de pygame.Surface con todos los frames extraídos
        """
        total_frames = self.get_frame_count(frame_width, frame_height)
        frames_list = []

        for frame_index in range(total_frames):
            frame = self.get_image(frame_index, frame_width, frame_height,
                                 scale_factor, transparent_color)
            frames_list.append(frame)

        return frames_list
