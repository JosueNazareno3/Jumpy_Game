"""
Paquete de entidades para Jumpy Game.

Este paquete contiene todas las entidades del juego como
el jugador, enemigos, plataformas y power-ups.
"""

from .player import Player
from .enemy import Enemy
from .platform import Platform

__all__ = ['Player', 'Enemy', 'Platform']
