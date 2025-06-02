"""
Interfaz de usuario para Jumpy Game.

Este módulo maneja todo el renderizado de la interfaz del juego,
incluyendo texto, menús, HUD y efectos visuales.
"""

import pygame
from config import GameConfig, UIConfig


class UserInterface:
    """
    Maneja la interfaz de usuario y el renderizado de texto.

    Proporciona métodos para dibujar todos los elementos de la UI
    del juego, desde el HUD hasta las pantallas de menú.
    """

    def __init__(self, screen):
        """
        Inicializa la interfaz de usuario.

        Args:
            screen (pygame.Surface): Superficie de la pantalla
        """
        self.screen = screen
        self.screen_center_x = GameConfig.SCREEN_WIDTH // 2
        self.screen_center_y = GameConfig.SCREEN_HEIGHT // 2

        # Inicializar fuentes
        self._initialize_fonts()

    def _initialize_fonts(self):
        """Inicializa las fuentes del juego."""
        try:
            self.font_small = pygame.font.SysFont(UIConfig.FONT_FAMILY, UIConfig.SMALL_FONT_SIZE)
            self.font_big = pygame.font.SysFont(UIConfig.FONT_FAMILY, UIConfig.BIG_FONT_SIZE)
        except pygame.error:
            # Fallback a fuente por defecto
            self.font_small = pygame.font.Font(None, UIConfig.SMALL_FONT_SIZE)
            self.font_big = pygame.font.Font(None, UIConfig.BIG_FONT_SIZE)

    def draw_text(self, text, font, color, x, y, center=False):
        """
        Dibuja texto en la pantalla.

        Args:
            text (str): Texto a dibujar
            font (pygame.font.Font): Fuente a usar
            color (tuple): Color del texto (R, G, B)
            x (int): Posición X
            y (int): Posición Y
            center (bool): Si centrar el texto horizontalmente
        """
        text_surface = font.render(str(text), True, color)

        if center:
            text_rect = text_surface.get_rect()
            text_rect.center = (self.screen_center_x, y)
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, (x, y))

    def draw_game_panel(self, game_state):
        """
        Dibuja el panel de información del juego (score y vidas).

        Args:
            game_state (GameState): Estado actual del juego
        """
        # Dibujar score
        score_text = f'SCORE: {game_state.score}'
        self.draw_text(score_text, self.font_small, GameConfig.WHITE,
                       UIConfig.SCORE_POSITION[0], UIConfig.SCORE_POSITION[1])

        # Dibujar vidas con color dinámico
        lives_color = self._get_lives_color(game_state.lives)
        lives_text = f'LIVES: {game_state.lives}'
        self.draw_text(lives_text, self.font_small, lives_color,
                       UIConfig.LIVES_POSITION_X, UIConfig.LIVES_POSITION_Y)

    def _get_lives_color(self, lives):
        """
        Obtiene el color para mostrar las vidas según la cantidad.

        Args:
            lives (int): Número de vidas

        Returns:
            tuple: Color RGB
        """
        if lives <= 1:
            return GameConfig.RED
        elif lives <= 2:
            return GameConfig.YELLOW
        else:
            return GameConfig.GREEN

    def draw_start_screen(self):
        """Dibuja la pantalla inicial del juego."""
        self.screen.fill(GameConfig.BLACK)

        # Título principal
        title_y = self.screen_center_y + UIConfig.TITLE_Y_OFFSET
        self.draw_text('JUMPY GAME', self.font_big, GameConfig.WHITE,
                       0, title_y, center=True)

        # Instrucción de inicio
        start_y = self.screen_center_y + UIConfig.START_TEXT_Y_OFFSET
        self.draw_text('PRESIONA "N" PARA COMENZAR', self.font_big, GameConfig.WHITE,
                       0, start_y, center=True)

        # Sección de controles
        self._draw_controls_section()

    def _draw_controls_section(self):
        """Dibuja la sección de controles en la pantalla inicial."""
        controls_start_y = self.screen_center_y + UIConfig.CONTROLS_Y_OFFSET

        controls = [
            'CONTROLES:',
            'A/D - MOVER',
            'ESPACIO - DOBLE SALTO',
            'P - PAUSAR'
        ]

        for i, control_text in enumerate(controls):
            y_position = controls_start_y + (i * UIConfig.CONTROLS_LINE_SPACING)
            color = GameConfig.YELLOW if i == 0 else GameConfig.WHITE
            self.draw_text(control_text, self.font_small, color,
                           0, y_position, center=True)

    def draw_pause_screen(self):
        """Dibuja la pantalla de pausa."""
        # Crear overlay semi-transparente
        overlay = pygame.Surface((GameConfig.SCREEN_WIDTH, GameConfig.SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(GameConfig.BLACK)
        self.screen.blit(overlay, (0, 0))

        # Texto de pausa
        pause_title_y = self.screen_center_y + UIConfig.PAUSE_TITLE_Y_OFFSET
        pause_text_y = self.screen_center_y + UIConfig.PAUSE_TEXT_Y_OFFSET

        self.draw_text('JUEGO EN PAUSA', self.font_big, GameConfig.WHITE,
                       0, pause_title_y, center=True)
        self.draw_text('PRESIONA "P" PARA CONTINUAR', self.font_small, GameConfig.WHITE,
                       0, pause_text_y, center=True)

    def draw_game_over_screen(self, game_state):
        """
        Dibuja la pantalla de game over.

        Args:
            game_state (GameState): Estado actual del juego
        """
        # Efecto de fade
        if game_state.fade_counter < GameConfig.SCREEN_WIDTH:
            self._draw_fade_effect(game_state)
        else:
            self._draw_game_over_text(game_state)

    def _draw_fade_effect(self, game_state):
        """
        Dibuja el efecto de fade para game over.

        Args:
            game_state (GameState): Estado del juego
        """
        game_state.fade_counter += UIConfig.FADE_SPEED

        for y in range(0, 6, 2):
            # Barras desde la izquierda
            pygame.draw.rect(self.screen, GameConfig.BLACK,
                             (0, y * 100, game_state.fade_counter, 100))
            # Barras desde la derecha
            pygame.draw.rect(self.screen, GameConfig.BLACK,
                             (GameConfig.SCREEN_WIDTH - game_state.fade_counter,
                              (y + 1) * 100, GameConfig.SCREEN_WIDTH, 100))

    def _draw_game_over_text(self, game_state):
        """
        Dibuja el texto de game over.

        Args:
            game_state (GameState): Estado del juego
        """
        # Título de game over
        self.draw_text('GAME OVER!', self.font_big, GameConfig.RED,
                       130, UIConfig.GAME_OVER_TITLE_Y)

        # Score final
        score_text = f'SCORE: {game_state.score}'
        self.draw_text(score_text, self.font_big, GameConfig.WHITE,
                       130, UIConfig.GAME_OVER_SCORE_Y)

        # High score si es nuevo récord
        if game_state.score >= game_state.high_score:
            self.draw_text('¡NUEVO RÉCORD!', self.font_small, GameConfig.YELLOW,
                           0, UIConfig.GAME_OVER_SCORE_Y + 30, center=True)

        # Instrucción de reinicio
        self.draw_text('PRESS SPACE TO PLAY AGAIN', self.font_big, GameConfig.WHITE,
                       40, UIConfig.GAME_OVER_RESTART_Y)

    def draw_background(self, background_image, background_scroll):
        """
        Dibuja el fondo con scroll infinito.

        Args:
            background_image (pygame.Surface): Imagen de fondo
            background_scroll (int): Offset del scroll
        """
        if background_image:
            # Dibujar dos copias de la imagen para scroll infinito
            self.screen.blit(background_image, (0, 0 + background_scroll))
            self.screen.blit(background_image, (0, -600 + background_scroll))
        else:
            # Fondo por defecto si no hay imagen
            self.screen.fill(GameConfig.BLUE)

    def draw_high_score_line(self, game_state):
        """
        Dibuja la línea del high score.

        Args:
            game_state (GameState): Estado actual del juego
        """
        line_y = game_state.score - game_state.high_score + GameConfig.SCROLL_THRESHOLD

        # Solo dibujar si la línea está visible
        if 0 <= line_y <= GameConfig.SCREEN_HEIGHT:
            pygame.draw.line(self.screen, GameConfig.WHITE,
                             (0, line_y), (GameConfig.SCREEN_WIDTH, line_y),
                             UIConfig.HIGH_SCORE_LINE_WIDTH)

            # Texto del high score
            text_x = GameConfig.SCREEN_WIDTH + UIConfig.HIGH_SCORE_TEXT_OFFSET
            self.draw_text('HIGH SCORE', self.font_small, GameConfig.WHITE,
                           text_x, line_y)

    def draw_debug_info(self, game_state, fps):
        """
        Dibuja información de debug (solo en modo desarrollo).

        Args:
            game_state (GameState): Estado del juego
            fps (float): FPS actuales
        """
        if hasattr(game_state, 'debug_mode') and game_state.debug_mode:
            debug_y = 30
            debug_info = [
                f'FPS: {fps:.1f}',
                f'Scroll: {game_state.scroll}',
                f'Player Y: {getattr(game_state, "player_y", "N/A")}'
            ]

            for info in debug_info:
                self.draw_text(info, self.font_small, GameConfig.YELLOW,
                               5, debug_y)
                debug_y += 20

    def draw_powerup_indicator(self, powerup_type, duration_left):
        """
        Dibuja un indicador de power-up activo.

        Args:
            powerup_type (str): Tipo de power-up
            duration_left (int): Tiempo restante en milisegundos
        """
        if duration_left > 0:
            indicator_y = 30
            indicator_text = f'{powerup_type.upper()}: {duration_left // 1000}s'
            self.draw_text(indicator_text, self.font_small, GameConfig.YELLOW,
                           GameConfig.SCREEN_WIDTH - 150, indicator_y)

    def clear_screen(self, color=None):
        """
        Limpia la pantalla con un color específico.

        Args:
            color (tuple, optional): Color RGB. Por defecto negro.
        """
        if color is None:
            color = GameConfig.BLACK
        self.screen.fill(color)
