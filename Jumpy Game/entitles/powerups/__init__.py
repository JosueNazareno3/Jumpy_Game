"""
Paquete de power-ups para Jumpy Game.

Este paquete contiene todas las clases de power-ups disponibles
en el juego, incluyendo boosters y vidas extra.
"""

from .powerup import PowerUp
from .booster import Booster
from .extra_life import ExtraLife

__all__ = ['PowerUp', 'Booster', 'ExtraLife']
