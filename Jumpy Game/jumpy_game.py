"""
Jumpy Game - Un juego de plataformas vertical donde controlas una abeja
que salta automáticamente entre plataformas mientras evita enemigos y
recolecta power-ups.

Autor: 
    1. Nazareno Josué
    2. Cevallos Jamileth
Versión: 2.0
Fecha: 2024
"""

import pygame
import random
import os
from pygame import mixer
from spritesheet import SpriteSheet
from enemy import Enemy
from game_config import *
from asset_loader import AssetLoader
from game_ui import GameUI
from game_state import GameState
from player import Player
from platform import Platform
from powerups import Booster, ExtraLife

class JumpyGame:
    """Clase principal del juego."""

    def __init__(self):
        """Inicializa el juego."""
        # Inicializar pygame
        mixer.init()
        pygame.init()

        # Configurar pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Jumpy Game')
        self.clock = pygame.time.Clock()

        # Inicializar componentes
        self.asset_loader = AssetLoader()
        self.ui = GameUI(self.screen)
        self.game_state = GameState()

        # Cargar assets
        self.asset_loader.load_all_assets()

        # Configurar icono
        icon = self.asset_loader.get_image('icon')
        if icon:
            pygame.display.set_icon(icon)

        # Crear grupos de sprites
        self.platform_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.booster_group = pygame.sprite.Group()
        self.extra_life_group = pygame.sprite.Group()

        # Crear jugador
        self.player = Player(PLAYER_START_X, PLAYER_START_Y, self.asset_loader)

        # Crear plataforma inicial
        self.create_initial_platform()

    def create_initial_platform(self):
        """Crea la plataforma inicial."""
        platform = Platform(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 50, 100, False, self.asset_loader)
        self.platform_group.add(platform)
        self.last_platform = platform

    def generate_platforms(self):
        """Genera nuevas plataformas."""
        if len(self.platform_group) < MAX_PLATFORMS:
            p_w = random.randint(40, 60)
            p_x = random.randint(0, SCREEN_WIDTH - p_w)
            p_y = self.last_platform.rect.y - random.randint(80, 120)
            p_type = random.randint(1, 2)
            p_moving = p_type == 1 and self.game_state.score > MOVING_PLATFORMS_SCORE

            platform = Platform(p_x, p_y, p_w, p_moving, self.asset_loader)
            self.platform_group.add(platform)
            self.last_platform = platform

            # Generar power-ups
            self.generate_powerups(p_x, p_y, p_w)

    def generate_powerups(self, p_x, p_y, p_w):
        """Genera power-ups en las plataformas."""
        center_x = p_x + p_w // 2

        # Generar booster
        if random.random() < BOOSTER_SPAWN_CHANCE and self.game_state.score > BOOSTER_SCORE:
            booster = Booster(center_x, p_y - 30, self.asset_loader)
            self.booster_group.add(booster)

        # Generar vida extra
        if random.random() < EXTRA_LIFE_SPAWN_CHANCE and len(self.extra_life_group) < 1:
            extra_life = ExtraLife(center_x, p_y - 60, self.asset_loader)
            self.extra_life_group.add(extra_life)

    def generate_enemies(self):
        """Genera enemigos."""
        if len(self.enemy_group) == 0 and self.game_state.score > ENEMY_SCORE:
            bird_image = self.asset_loader.get_image('bird_enemy')
            if bird_image:
                bird_sheet = SpriteSheet(bird_image)
                enemy = Enemy(SCREEN_WIDTH, 100, bird_sheet, 1.5)
                self.enemy_group.add(enemy)

    def handle_events(self):
        """Maneja los eventos del juego."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state.save_high_score()
                return False

            if event.type == pygame.KEYDOWN:
                if self.game_state.waiting_for_start and event.key == pygame.K_n:
                    self.game_state.waiting_for_start = False
                elif event.key == pygame.K_p and not self.game_state.waiting_for_start and not self.game_state.game_over:
                    self.game_state.paused = not self.game_state.paused
                elif self.game_state.game_over and event.key == pygame.K_SPACE and self.game_state.fade_counter >= SCREEN_WIDTH:
                    self.restart_game()

        return True

    def restart_game(self):
        """Reinicia el juego."""
        self.game_state.reset_game()
        self.player.reset_position()

        # Limpiar grupos
        self.enemy_group.empty()
        self.platform_group.empty()
        self.booster_group.empty()
        self.extra_life_group.empty()

        # Crear plataforma inicial
        self.create_initial_platform()

    def update_game(self):
        """Actualiza la lógica del juego."""
        # Actualizar jugador
        scroll, life_collected = self.player.move(self.platform_group, self.booster_group, self.extra_life_group)

        # Manejar vida extra recolectada
        if life_collected:
            self.game_state.gain_life()

        # Actualizar scroll de fondo
        self.game_state.bg_scroll += scroll
        if self.game_state.bg_scroll >= 600:
            self.game_state.bg_scroll = 0

        # Generar contenido
        self.generate_platforms()
        self.generate_enemies()

        # Actualizar sprites
        self.platform_group.update(scroll)
        self.booster_group.update(scroll)
        self.extra_life_group.update(scroll)
        self.enemy_group.update(scroll, SCREEN_WIDTH)

        # Actualizar score
        if scroll > 0:
            self.game_state.score += scroll

        # Verificar muerte del jugador
        self.check_player_death()

    def check_player_death(self):
        """Verifica si el jugador murió."""
        death_sound = self.asset_loader.get_sound('death')

        # Caída de pantalla
        if self.player.rect.top > SCREEN_HEIGHT:
            if self.game_state.lose_life():
                if death_sound:
                    death_sound.play()
            else:
                self.player.reset_position()
                if death_sound:
                    death_sound.play()

        # Colisión con enemigos
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
            collided = pygame.sprite.spritecollide(self.player, self.enemy_group, True, pygame.sprite.collide_mask)
            if collided:
                if self.game_state.lose_life():
                    if death_sound:
                        death_sound.play()
                else:
                    self.player.rect.center = (SCREEN_WIDTH // 2, self.player.rect.y - 50)
                    self.player.vel_y = -10
                    self.player.in_air = True
                    self.player.has_double_jump = True
                    if death_sound:
                        death_sound.play()

    def render_game(self):
        """Renderiza el juego."""
        # Dibujar fondo
        bg_image = self.asset_loader.get_image('background')
        self.ui.draw_background(bg_image, self.game_state.bg_scroll)

        # Dibujar línea de high score
        self.ui.draw_high_score_line(self.game_state.score, self.game_state.high_score)

        # Dibujar sprites
        self.platform_group.draw(self.screen)
        self.enemy_group.draw(self.screen)
        self.booster_group.draw(self.screen)
        self.extra_life_group.draw(self.screen)
        self.player.draw(self.screen)

        # Dibujar UI
        self.ui.draw_panel(self.game_state.score, self.game_state.lives)

    def run(self):
        """Ejecuta el bucle principal del juego."""
        running = True

        while running:
            self.clock.tick(FPS)

            # Manejar eventos
            running = self.handle_events()
            if not running:
                break

            # Pantalla de inicio
            if self.game_state.waiting_for_start:
                self.ui.draw_start_screen()
                pygame.display.update()
                continue

            # Pausa
            if self.game_state.paused:
                self.render_game()
                self.ui.draw_pause_screen()
                pygame.display.update()
                continue

            # Juego activo
            if not self.game_state.game_over:
                self.update_game()
                self.render_game()
            else:
                # Game over
                self.ui.draw_game_over(self.game_state.score, self.game_state.fade_counter)
                self.game_state.fade_counter += 5
                self.game_state.save_high_score()

            pygame.display.update()

        pygame.quit()

def main():
    """Función principal."""
    try:
        game = JumpyGame()
        game.run()
    except Exception as e:
        print(f"Error ejecutando el juego: {e}")

if __name__ == "__main__":
    main()
