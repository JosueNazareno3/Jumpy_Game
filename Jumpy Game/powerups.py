"""
Clases de Power-ups para Jumpy Game.
Maneja boosters y vidas extra.
"""

import pygame
from game_config import *


class Booster(pygame.sprite.Sprite):
    """Power-up que aumenta la altura del salto."""

    def __init__(self, x, y, asset_loader):
        pygame.sprite.Sprite.__init__(self)

        booster_image = asset_loader.get_image('booster')
        if booster_image:
            self.image = pygame.transform.scale(booster_image, (30, 30))
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(YELLOW)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, scroll):
        """Actualiza la posición del booster."""
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class ExtraLife(pygame.sprite.Sprite):
    """Power-up que otorga una vida extra."""

    def __init__(self, x, y, asset_loader):
        pygame.sprite.Sprite.__init__(self)

        extra_life_image = asset_loader.get_image('extra_life')
        if extra_life_image:
            self.image = pygame.transform.scale(extra_life_image, (30, 30))
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(RED)

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self, scroll):
        """Actualiza la posición de la vida extra."""
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
