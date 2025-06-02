"""
Configuración global del juego Jumpy Game.

Este módulo contiene todas las constantes y configuraciones
utilizadas a lo largo del juego, centralizando los valores
para facilitar el mantenimiento y la personalización.
"""


class GameConfig:
    """Configuración centralizada del juego."""

    # === CONFIGURACIÓN DE PANTALLA ===
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 600
    FPS = 60

    # === CONFIGURACIÓN DE FÍSICA ===
    GRAVITY = 1
    SCROLL_THRESHOLD = 200

    # === CONFIGURACIÓN DE PLATAFORMAS ===
    MAX_PLATFORMS = 10
    PLATFORM_MIN_WIDTH = 40
    PLATFORM_MAX_WIDTH = 60
    PLATFORM_MIN_GAP = 80
    PLATFORM_MAX_GAP = 120

    # === SISTEMA DE VIDAS ===
    INITIAL_LIVES = 3
    MAX_LIVES = 5

    # === VELOCIDADES DE SALTO ===
    NORMAL_JUMP_VELOCITY = -20
    BOOST_JUMP_VELOCITY = -60

    # === PROBABILIDADES DE SPAWN ===
    BOOSTER_SPAWN_CHANCE = 0.08  # 8%
    EXTRA_LIFE_SPAWN_CHANCE = 0.05  # 5%

    # === REQUISITOS DE SCORE ===
    MOVING_PLATFORMS_SCORE_REQUIREMENT = 1000
    BOOSTER_SCORE_REQUIREMENT = 1000
    ENEMY_SCORE_REQUIREMENT = 2000

    # === CONFIGURACIÓN DE ENEMIGOS ===
    ENEMY_ANIMATION_COOLDOWN = 50  # Milisegundos entre frames
    ENEMY_MOVEMENT_SPEED = 2
    ENEMY_FRAME_COUNT = 8
    ENEMY_FRAME_SIZE = 32

    # === CONFIGURACIÓN DE POWER-UPS ===
    POWERUP_SIZE = (30, 30)
    BOOSTER_Y_OFFSET = -30
    EXTRA_LIFE_Y_OFFSET = -60

    # === CONFIGURACIÓN DE JUGADOR ===
    PLAYER_IMAGE_SIZE = (48, 48)
    PLAYER_COLLISION_SCALE = 0.7
    PLAYER_INITIAL_X = SCREEN_WIDTH // 2
    PLAYER_INITIAL_Y = SCREEN_HEIGHT - 150
    PLAYER_MOVEMENT_SPEED = 10

    # === COLORES ===
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)  # Color para assets faltantes

    # === CONFIGURACIÓN DE AUDIO ===
    MUSIC_VOLUME = 0.9
    SOUND_VOLUME = 1.0
    POWERUP_SOUND_VOLUME = 0.8

    # === ARCHIVOS DE ASSETS ===
    ASSETS_DIR = 'assets'
    SCORE_FILE = 'score.txt'

    # Imágenes
    BACKGROUND_IMAGE = 'background1.jpg'
    PLATFORM_IMAGE = 'wood.png'
    PLAYER_LEFT_IMAGE = 'bee_rest_l.png'
    PLAYER_RIGHT_IMAGE = 'bee_rest_r.png'
    BOOSTER_IMAGE = 'booster.webp'
    EXTRA_LIFE_IMAGE = 'extra_life.png'
    ENEMY_BIRD_IMAGE = 'bird.png'
    ICON_IMAGE = 'ghost.png'

    # Sonidos
    BACKGROUND_MUSIC = 'music_game-2d.mp3'
    JUMP_SOUND = 'jump.mp3'
    DEATH_SOUND = 'death.mp3'
    BOOST_SOUND = 'boost.mp3'
    EXTRA_LIFE_SOUND = 'powerup.wav'


class UIConfig:
    """Configuración específica de la interfaz de usuario."""

    # === FUENTES ===
    FONT_FAMILY = 'Lucida Sans'
    SMALL_FONT_SIZE = 20
    BIG_FONT_SIZE = 24

    # === POSICIONES DE UI ===
    SCORE_POSITION = (0, 0)
    LIVES_POSITION_X = GameConfig.SCREEN_WIDTH - 90
    LIVES_POSITION_Y = 0

    # === CONFIGURACIÓN DE PANTALLAS ===
    TITLE_Y_OFFSET = -80
    START_TEXT_Y_OFFSET = -20
    CONTROLS_Y_OFFSET = 40
    CONTROLS_LINE_SPACING = 30

    PAUSE_TITLE_Y_OFFSET = -20
    PAUSE_TEXT_Y_OFFSET = 20

    GAME_OVER_TITLE_Y = 200
    GAME_OVER_SCORE_Y = 250
    GAME_OVER_RESTART_Y = 300

    # === EFECTOS VISUALES ===
    FADE_SPEED = 5
    HIGH_SCORE_LINE_WIDTH = 3
    HIGH_SCORE_TEXT_OFFSET = -130


class PhysicsConfig:
    """Configuración específica de física del juego."""

    # === CONFIGURACIÓN DE COLISIONES ===
    COLLISION_TOLERANCE = 1

    # === CONFIGURACIÓN DE MOVIMIENTO ===
    HORIZONTAL_BOUNDARY_BUFFER = 0
    VERTICAL_DEATH_BOUNDARY = GameConfig.SCREEN_HEIGHT

    # === CONFIGURACIÓN DE SCROLL ===
    BACKGROUND_SCROLL_RESET = 600
    SCROLL_SCORE_MULTIPLIER = 1

    # === CONFIGURACIÓN DE RESPAWN ===
    RESPAWN_Y_OFFSET = -50
    RESPAWN_VELOCITY = -10


# === CONFIGURACIÓN DE DESARROLLO ===
class DebugConfig:
    """Configuración para debugging y desarrollo."""

    ENABLE_DEBUG_PRINT = False
    SHOW_COLLISION_BOXES = False
    SHOW_FPS = False
    ENABLE_GOD_MODE = False

    # Colores para debugging
    DEBUG_COLLISION_COLOR = (255, 0, 0)
    DEBUG_PLATFORM_COLOR = (0, 255, 0)
    DEBUG_POWERUP_COLOR = (0, 0, 255)
