"""
Interfaz de usuario para Jumpy Game.
Maneja todo el renderizado de texto y pantallas.
"""

import pygame
from game_config import *


class GameUI:
    """Maneja la interfaz de usuario del juego."""

    def __init__(self, screen):
        self.screen = screen
        self.font_small = pygame.font.SysFont('Lucida Sans', 20)
        self.font_big = pygame.font.SysFont('Lucida Sans', 24)

    def draw_text(self, text, font, color, x, y, center=False):
        """Dibuja texto en la pantalla."""
        img = font.render(text, True, color)
        if center:
            text_rect = img.get_rect()
            text_rect.center = (SCREEN_WIDTH // 2, y)
            self.screen.blit(img, text_rect)
        else:
            self.screen.blit(img, (x, y))

    def draw_panel(self, score, lives):
        """Dibuja el panel de información del juego."""
        self.draw_text('SCORE: ' + str(score), self.font_small, WHITE, 0, 0)
        self.draw_text('LIVES: ' + str(lives), self.font_small, GREEN, SCREEN_WIDTH - 90, 0)

    def draw_background(self, bg_image, bg_scroll):
        """Dibuja el fondo con scroll."""
        if bg_image:
            self.screen.blit(bg_image, (0, 0 + bg_scroll))
            self.screen.blit(bg_image, (0, -600 + bg_scroll))
        else:
            self.screen.fill((0, 100, 200))  # Azul por defecto

    def draw_start_screen(self):
        """Dibuja la pantalla de inicio."""
        self.screen.fill(BLACK)
        self.draw_text('JUMPY GAME', self.font_big, WHITE, 0, SCREEN_HEIGHT // 2 - 80, center=True)
        self.draw_text('PRESIONA "N" PARA COMENZAR', self.font_big, WHITE, 0, SCREEN_HEIGHT // 2 - 20, center=True)
        self.draw_text('CONTROLES:', self.font_small, WHITE, 0, SCREEN_HEIGHT // 2 + 40, center=True)
        self.draw_text('A/D - MOVER', self.font_small, WHITE, 0, SCREEN_HEIGHT // 2 + 70, center=True)
        self.draw_text('ESPACIO - DOBLE SALTO', self.font_small, WHITE, 0, SCREEN_HEIGHT // 2 + 100, center=True)
        self.draw_text('P - PAUSAR', self.font_small, WHITE, 0, SCREEN_HEIGHT // 2 + 130, center=True)

    def draw_pause_screen(self):
        """Dibuja la pantalla de pausa."""
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        self.draw_text('JUEGO EN PAUSA', self.font_big, WHITE, 0, SCREEN_HEIGHT // 2 - 20, center=True)
        self.draw_text('PRESIONA "P" PARA CONTINUAR', self.font_small, WHITE, 0, SCREEN_HEIGHT // 2 + 20, center=True)

    def draw_game_over(self, score, fade_counter):
        """Dibuja la pantalla de game over."""
        if fade_counter < SCREEN_WIDTH:
            for y in range(0, 6, 2):
                pygame.draw.rect(self.screen, BLACK, (0, y * 100, fade_counter, 100))
                pygame.draw.rect(self.screen, BLACK, (SCREEN_WIDTH - fade_counter, (y + 1) * 100, SCREEN_WIDTH, 100))
        else:
            self.draw_text('GAME OVER!', self.font_big, WHITE, 130, 200)
            self.draw_text('SCORE: ' + str(score), self.font_big, WHITE, 130, 250)
            self.draw_text('PRESS SPACE TO PLAY AGAIN', self.font_big, WHITE, 40, 300)

    def draw_high_score_line(self, score, high_score):
        """Dibuja la línea del high score."""
        line_y = score - high_score + SCROLL_THRESH
        if 0 <= line_y <= SCREEN_HEIGHT:
            pygame.draw.line(self.screen, WHITE, (0, line_y), (SCREEN_WIDTH, line_y), 3)
            self.draw_text('HIGH SCORE', self.font_small, WHITE, SCREEN_WIDTH - 130, line_y)
