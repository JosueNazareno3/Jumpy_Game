"""
Clase Player para Jumpy Game.
Maneja toda la lógica del jugador.
"""

import pygame
from game_config import *


class Player:
    """Clase que representa al jugador (abeja)."""

    def __init__(self, x, y, asset_loader):
        # Configuración de imagen
        self.image_width = PLAYER_IMAGE_SIZE[0]
        self.image_height = PLAYER_IMAGE_SIZE[1]

        # Cargar imágenes del jugador
        self.bee_images = {
            'left': asset_loader.get_image('player_left'),
            'right': asset_loader.get_image('player_right')
        }

        # Estado visual
        self.current_direction = 'right'
        self.image = self.bee_images[self.current_direction]

        # Configuración de colisión
        self.collision_width = int(self.image_width * PLAYER_COLLISION_SCALE)
        self.collision_height = int(self.image_height * PLAYER_COLLISION_SCALE)
        self.rect = pygame.Rect(0, 0, self.collision_width, self.collision_height)
        self.rect.center = (x, y)

        # Estado de movimiento
        self.vel_y = 0
        self.in_air = True
        self.has_double_jump = False
        self.can_auto_jump = True
        self.current_jump_vel = INITIAL_JUMP_VEL

        # Referencias a sonidos
        self.jump_sound = asset_loader.get_sound('jump')
        self.boost_sound = asset_loader.get_sound('boost')
        self.extra_life_sound = asset_loader.get_sound('extra_life')

    def move(self, platform_group, booster_group, extra_life_group):
        """Actualiza el movimiento del jugador."""
        scroll = 0
        dx = 0
        dy = 0

        key = pygame.key.get_pressed()

        # Movimiento horizontal
        if key[pygame.K_a]:
            dx = -PLAYER_SPEED
            self.current_direction = 'left'
        if key[pygame.K_d]:
            dx = PLAYER_SPEED
            self.current_direction = 'right'

        # Salto automático
        if not self.in_air and self.can_auto_jump:
            self.vel_y = self.current_jump_vel
            if self.jump_sound:
                self.jump_sound.play()
            self.in_air = True
            self.can_auto_jump = False

        # Doble salto
        if key[pygame.K_SPACE] and self.in_air and self.has_double_jump:
            self.vel_y = self.current_jump_vel
            if self.jump_sound:
                self.jump_sound.play()
            self.has_double_jump = False

        # Aplicar gravedad
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Límites de pantalla
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        # Colisión con plataformas
        self.in_air = True
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.collision_width, self.collision_height):
                if self.vel_y > 0:
                    self.rect.bottom = platform.rect.top
                    dy = 0
                    self.in_air = False
                    self.can_auto_jump = True
                    self.current_jump_vel = INITIAL_JUMP_VEL
                    self.has_double_jump = True

        # Scroll de pantalla
        if self.rect.top <= SCROLL_THRESH:
            if self.vel_y < 0:
                scroll = -dy

        # Recolectar boosters
        for booster in booster_group:
            if self.rect.colliderect(booster.rect):
                self.vel_y = BOOST_JUMP_VEL
                self.current_jump_vel = BOOST_JUMP_VEL
                self.in_air = True
                if self.boost_sound:
                    self.boost_sound.play()
                booster.kill()

        # Recolectar vidas extra
        for extra_life in extra_life_group:
            if self.rect.colliderect(extra_life.rect):
                if self.extra_life_sound:
                    self.extra_life_sound.play()
                extra_life.kill()
                return scroll, True  # Indica que se recolectó una vida

        # Actualizar posición
        self.image = self.bee_images[self.current_direction]
        self.rect.x += dx
        self.rect.y += dy + scroll

        return scroll, False

    def draw(self, screen):
        """Dibuja el jugador en la pantalla."""
        if self.image:
            draw_x = self.rect.x - (self.image_width - self.collision_width) // 2
            draw_y = self.rect.y - (self.image_height - self.collision_height) // 2
            screen.blit(self.image, (draw_x, draw_y))
            self.mask = pygame.mask.from_surface(self.image)

    def reset_position(self):
        """Reinicia la posición del jugador."""
        self.rect.center = (PLAYER_START_X, PLAYER_START_Y)
        self.vel_y = 0
        self.in_air = False
        self.can_auto_jump = True
        self.has_double_jump = True
        self.current_jump_vel = INITIAL_JUMP_VEL
