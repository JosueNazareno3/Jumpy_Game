"""
Clase Platform para Jumpy Game.
Maneja las plataformas del juego.
"""

import pygame
import random
from game_config import *


class Platform(pygame.sprite.Sprite):
    """Clase que representa una plataforma."""

    def __init__(self, x, y, width, moving, asset_loader):
        pygame.sprite.Sprite.__init__(self)

        platform_image = asset_loader.get_image('platform')
        if platform_image:
            self.image = pygame.transform.scale(platform_image, (width, 10))
        else:
            self.image = pygame.Surface((width, 10))
            self.image.fill((139, 69, 19))  # Marrón

        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 2)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, scroll):
        """Actualiza la plataforma."""
        if self.moving:
            self.move_counter += 1
            self.rect.x += self.direction * self.speed

        if self.move_counter >= 100 or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1
            self.move_counter = 0

        self.rect.y += scroll

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
