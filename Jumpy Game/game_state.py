"""
Estado del juego Jumpy Game.
Maneja puntuación, vidas y persistencia.
"""

import os
from game_config import *


class GameState:
    """Maneja el estado del juego."""

    def __init__(self):
        # Estados de pantalla
        self.waiting_for_start = True
        self.paused = False
        self.game_over = False

        # Puntuación y vidas
        self.score = 0
        self.lives = LIVES
        self.high_score = self.load_high_score()

        # Variables de scroll
        self.scroll = 0
        self.bg_scroll = 0
        self.fade_counter = 0

    def load_high_score(self):
        """Carga el high score desde archivo."""
        try:
            if os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, 'r') as file:
                    return int(file.read().strip())
        except (ValueError, IOError):
            pass
        return 0

    def save_high_score(self):
        """Guarda el high score actual."""
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                with open(SCORE_FILE, 'w') as file:
                    file.write(str(self.high_score))
            except IOError:
                pass

    def reset_game(self):
        """Reinicia el estado para una nueva partida."""
        self.game_over = False
        self.score = 0
        self.lives = LIVES
        self.scroll = 0
        self.bg_scroll = 0
        self.fade_counter = 0

    def lose_life(self):
        """Hace perder una vida al jugador."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
            return True
        return False

    def gain_life(self):
        """Otorga una vida extra."""
        if self.lives < MAX_LIVES:
            self.lives += 1
            return True
        return False
