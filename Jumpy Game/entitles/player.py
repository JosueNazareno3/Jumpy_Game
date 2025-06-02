"""
Jugador del juego Jumpy Game.

Este módulo contiene la clase Player que maneja toda la lógica
del personaje controlado por el usuario (la abeja).
"""

import pygame
from config import GameConfig, PhysicsConfig


class Player:
    """
    Clase que representa al jugador (abeja).

    Maneja el movimiento, saltos, colisiones y recolección
    de power-ups del personaje principal del juego.
    """

    def __init__(self, x, y, asset_manager):
        """
        Inicializa el jugador.

        Args:
            x (int): Posición inicial X
            y (int): Posición inicial Y
            asset_manager (AssetManager): Gestor de assets
        """
        # Configuración de imagen
        self.image_width = GameConfig.PLAYER_IMAGE_SIZE[0]
        self.image_height = GameConfig.PLAYER_IMAGE_SIZE[1]

        # Cargar imágenes del jugador
        self.bee_images = {
            'left': asset_manager.get_image('player_left'),
            'right': asset_manager.get_image('player_right')
        }

        # Estado visual
        self.current_direction = 'right'
        self.image = self.bee_images[self.current_direction]

        # Configuración de colisión
        self.collision_width = int(self.image_width * GameConfig.PLAYER_COLLISION_SCALE)
        self.collision_height = int(self.image_height * GameConfig.PLAYER_COLLISION_SCALE)
        self.rect = pygame.Rect(0, 0, self.collision_width, self.collision_height)
        self.rect.center = (x, y)

        # Estado de movimiento
        self.velocity_y = 0
        self.is_in_air = True
        self.has_double_jump = False
        self.can_auto_jump = True
        self.current_jump_velocity = GameConfig.NORMAL_JUMP_VELOCITY

        # Referencias a sonidos
        self.jump_sound = asset_manager.get_sound('jump')
        self.boost_sound = asset_manager.get_sound('boost')
        self.extra_life_sound = asset_manager.get_sound('extra_life')

        # Máscara para colisiones precisas
        self.mask = None
        self._update_mask()

    def _update_mask(self):
        """Actualiza la máscara de colisión del jugador."""
        if self.image:
            self.mask = pygame.mask.from_surface(self.image)

    def handle_input(self):
        """
        Maneja la entrada del usuario.

        Returns:
            int: Movimiento horizontal calculado
        """
        keys = pygame.key.get_pressed()
        horizontal_movement = 0

        # Movimiento horizontal
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            horizontal_movement = -GameConfig.PLAYER_MOVEMENT_SPEED
            self.current_direction = 'left'
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            horizontal_movement = GameConfig.PLAYER_MOVEMENT_SPEED
            self.current_direction = 'right'

        return horizontal_movement

    def handle_jumping(self, keys):
        """
        Maneja la lógica de salto.

        Args:
            keys (pygame.key): Estado de las teclas
        """
        # Salto automático al tocar plataforma
        if not self.is_in_air and self.can_auto_jump:
            self._perform_jump()
            self.can_auto_jump = False

        # Doble salto con espacio
        if (keys[pygame.K_SPACE] and self.is_in_air and
                self.has_double_jump):
            self._perform_jump()
            self.has_double_jump = False

    def _perform_jump(self):
        """Ejecuta un salto con el sonido correspondiente."""
        self.velocity_y = self.current_jump_velocity
        self.is_in_air = True
        if self.jump_sound:
            self.jump_sound.play()

    def apply_gravity(self):
        """Aplica la gravedad al jugador."""
        self.velocity_y += GameConfig.GRAVITY

    def handle_platform_collision(self, platform_group):
        """
        Maneja las colisiones con plataformas.

        Args:
            platform_group (pygame.sprite.Group): Grupo de plataformas
        """
        self.is_in_air = True

        for platform in platform_group:
            # Verificar colisión futura
            future_rect = pygame.Rect(
                self.rect.x,
                self.rect.y + self.velocity_y,
                self.collision_width,
                self.collision_height
            )

            if platform.rect.colliderect(future_rect):
                if self.velocity_y > 0:  # Cayendo
                    self._land_on_platform(platform)
                    break

    def _land_on_platform(self, platform):
        """
        Maneja el aterrizaje en una plataforma.

        Args:
            platform (Platform): Plataforma en la que aterriza
        """
        self.rect.bottom = platform.rect.top
        self.velocity_y = 0
        self.is_in_air = False
        self.can_auto_jump = True
        self.current_jump_velocity = GameConfig.NORMAL_JUMP_VELOCITY
        self.has_double_jump = True

    def handle_power_up_collection(self, booster_group, extra_life_group, game_state):
        """
        Maneja la recolección de power-ups.

        Args:
            booster_group (pygame.sprite.Group): Grupo de boosters
            extra_life_group (pygame.sprite.Group): Grupo de vidas extra
            game_state (GameState): Estado del juego
        """
        # Recolectar boosters
        collected_boosters = pygame.sprite.spritecollide(
            self, booster_group, True, self._check_powerup_collision
        )

        for booster in collected_boosters:
            self._apply_boost_effect()

        # Recolectar vidas extra
        collected_lives = pygame.sprite.spritecollide(
            self, extra_life_group, True, self._check_powerup_collision
        )

        for extra_life in collected_lives:
            self._apply_extra_life_effect(game_state)

    def _check_powerup_collision(self, powerup):
        """
        Verifica colisión con power-up usando rectángulos.

        Args:
            powerup: Power-up a verificar

        Returns:
            bool: True si hay colisión
        """
        return self.rect.colliderect(powerup.rect)

    def _apply_boost_effect(self):
        """Aplica el efecto del booster."""
        # Impulso inmediato hacia arriba
        self.velocity_y = GameConfig.BOOST_JUMP_VELOCITY
        self.current_jump_velocity = GameConfig.BOOST_JUMP_VELOCITY
        self.is_in_air = True

        if self.boost_sound:
            self.boost_sound.play()

    def _apply_extra_life_effect(self, game_state):
        """
        Aplica el efecto de vida extra.

        Args:
            game_state (GameState): Estado del juego
        """
        if game_state.lives < GameConfig.MAX_LIVES:
            game_state.lives += 1
            if self.extra_life_sound:
                self.extra_life_sound.play()

    def calculate_screen_scroll(self):
        """
        Calcula el scroll de la pantalla basado en la posición del jugador.

        Returns:
            int: Cantidad de scroll a aplicar
        """
        if (self.rect.top <= GameConfig.SCROLL_THRESHOLD and
                self.velocity_y < 0):
            return -self.velocity_y
        return 0

    def apply_horizontal_boundaries(self, horizontal_movement):
        """
        Aplica los límites horizontales de la pantalla.

        Args:
            horizontal_movement (int): Movimiento horizontal deseado

        Returns:
            int: Movimiento horizontal ajustado
        """
        # Límite izquierdo
        if self.rect.left + horizontal_movement < PhysicsConfig.HORIZONTAL_BOUNDARY_BUFFER:
            horizontal_movement = PhysicsConfig.HORIZONTAL_BOUNDARY_BUFFER - self.rect.left

        # Límite derecho
        if self.rect.right + horizontal_movement > GameConfig.SCREEN_WIDTH - PhysicsConfig.HORIZONTAL_BOUNDARY_BUFFER:
            horizontal_movement = GameConfig.SCREEN_WIDTH - PhysicsConfig.HORIZONTAL_BOUNDARY_BUFFER - self.rect.right

        return horizontal_movement

    def update(self, platform_group, booster_group, extra_life_group, game_state):
        """
        Actualiza el estado del jugador.

        Args:
            platform_group (pygame.sprite.Group): Grupo de plataformas
            booster_group (pygame.sprite.Group): Grupo de boosters
            extra_life_group (pygame.sprite.Group): Grupo de vidas extra
            game_state (GameState): Estado del juego

        Returns:
            int: Cantidad de scroll aplicado
        """
        keys = pygame.key.get_pressed()

        # Manejar entrada y movimiento
        horizontal_movement = self.handle_input()
        horizontal_movement = self.apply_horizontal_boundaries(horizontal_movement)

        self.handle_jumping(keys)
        self.apply_gravity()

        # Aplicar movimiento vertical
        vertical_movement = self.velocity_y

        # Colisiones y power-ups
        self.handle_platform_collision(platform_group)
        self.handle_power_up_collection(booster_group, extra_life_group, game_state)

        # Calcular scroll
        scroll = self.calculate_screen_scroll()

        # Actualizar imagen y posición
        self.image = self.bee_images[self.current_direction]
        self._update_mask()

        self.rect.x += horizontal_movement
        self.rect.y += vertical_movement + scroll

        return scroll

    def draw(self, screen):
        """
        Dibuja el jugador en la pantalla.

        Args:
            screen (pygame.Surface): Superficie donde dibujar
        """
        if self.image:
            draw_x = self.rect.x - (self.image_width - self.collision_width) // 2
            draw_y = self.rect.y - (self.image_height - self.collision_height) // 2
            screen.blit(self.image, (draw_x, draw_y))

    def reset_position(self):
        """Reinicia la posición del jugador."""
        self.rect.center = (GameConfig.PLAYER_INITIAL_X, GameConfig.PLAYER_INITIAL_Y)
        self.velocity_y = 0
        self.is_in_air = False
        self.can_auto_jump = True
        self.has_double_jump = True
        self.current_jump_velocity = GameConfig.NORMAL_JUMP_VELOCITY
        self.current_direction = 'right'

    def is_off_screen(self):
        """
        Verifica si el jugador cayó de la pantalla.

        Returns:
            bool: True si el jugador está fuera de la pantalla
        """
        return self.rect.top > PhysicsConfig.VERTICAL_DEATH_BOUNDARY

    def get_collision_rect(self):
        """
        Obtiene el rectángulo de colisión del jugador.

        Returns:
            pygame.Rect: Rectángulo de colisión
        """
        return self.rect

    def get_position(self):
        """
        Obtiene la posición actual del jugador.

        Returns:
            tuple: (x, y) posición del centro del jugador
        """
        return self.rect.center
