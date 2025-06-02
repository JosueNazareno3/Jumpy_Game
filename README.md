# Desarrollado por:
1. Cevallos Jamileth
2. Nazareno Josué

# 🐝 Jumpy Game

Un emocionante juego de plataformas vertical donde controlas una abeja que salta automáticamente entre plataformas mientras evita enemigos y recolecta power-ups.

![Jumpy Game](https://img.shields.io/badge/Python-3.7+-blue.svg)
![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Descripción

Jumpy Game es un juego de plataformas con scroll vertical infinito inspirado en juegos clásicos como Doodle Jump. El jugador controla una abeja que salta automáticamente de plataforma en plataforma, tratando de alcanzar la mayor altura posible mientras evita enemigos voladores y recolecta power-ups útiles.

## 🎮 Características

### ✨ Mecánicas de Juego
- **Salto automático**: La abeja salta automáticamente al tocar una plataforma
- **Doble salto**: Capacidad de realizar un segundo salto en el aire presionando ESPACIO
- **Scroll infinito**: El mundo se desplaza verticalmente de forma infinita
- **Sistema de vidas**: Múltiples oportunidades para continuar jugando

### 🚀 Power-ups
- **Boosters** 🚀: Proporcionan un salto súper potente para alcanzar mayor altura
- **Vidas extra** ❤️: Aumentan el número de vidas disponibles (máximo 5)

### 🏗️ Elementos del Juego
- **Plataformas móviles**: Plataformas que se mueven horizontalmente (aparecen después de 1000 puntos)
- **Enemigos voladores**: Pájaros animados que cruzan la pantalla (aparecen después de 2000 puntos)
- **High Score**: Guarda automáticamente tu mejor puntuación

## 🕹️ Controles

| Tecla | Acción |
|-------|--------|
| **N** | Iniciar el juego desde la pantalla principal |
| **A** / **←** | Mover la abeja hacia la izquierda |
| **D** / **→** | Mover la abeja hacia la derecha |
| **ESPACIO** | Realizar doble salto (solo en el aire) |
| **P** | Pausar/reanudar el juego |
| **ESPACIO** | Reiniciar después de Game Over |

## 🎯 Objetivo

- Salta de plataforma en plataforma para alcanzar la mayor altura posible
- Evita caerte de la pantalla
- Esquiva a los enemigos voladores
- Recolecta boosters para saltos más altos
- Recoge vidas extra para tener más oportunidades
- ¡Supera tu high score!

## 📦 Instalación y Ejecución

### 🔧 Requisitos del Sistema

#### Software Necesario
- **Python 3.7 o superior**
- **pygame 2.0 o superior**

#### Sistemas Operativos Compatibles
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+)

### 📥 Instalación

#### Opción 1: Ejecutar desde Código Fuente

1. **Clona o descarga** el proyecto:
   \`\`\`bash
   git clone https://github.com/tu-usuario/jumpy-game.git
   cd jumpy-game
   \`\`\`

2. **Instala las dependencias**:
   \`\`\`bash
   pip install pygame
   \`\`\`

3. **Ejecuta el juego**:
   \`\`\`bash
   python jumpy_game.py
   \`\`\`

#### Opción 2: Crear Ejecutable

1. **Instala PyInstaller**:
   \`\`\`bash
   pip install pyinstaller
   \`\`\`

2. **Ejecuta el script de construcción**:
   \`\`\`bash
   python build_executable.py
   \`\`\`

3. **Encuentra el ejecutable** en la carpeta `JumpyGame_Distribution/`

#### Opción 3: Ejecutable Pre-compilado

Si tienes el ejecutable pre-compilado:
1. Descarga `JumpyGame.exe`
2. Asegúrate de que la carpeta `assets/` esté en el mismo directorio
3. Ejecuta `JumpyGame.exe`

## 📁 Estructura del Proyecto

\`\`\`
jumpy_game/
│
├── jumpy_game.py          # Archivo principal del juego (REDUCIDO)
├── game_config.py         # Configuraciones centralizadas
├── asset_loader.py        # Gestión de recursos
├── game_ui.py            # Interfaz de usuario
├── player.py             # Lógica del jugador
├── platform.py           # Lógica de plataformas
├── powerups.py           # Lógica de power-ups
├── game_state.py         # Estado del juego
├── enemy.py              # Lógica de enemigos
├── spritesheet.py        # Utilidad para sprites
├── build_executable.py   # Script para crear ejecutable
├── README.md             # Este archivo
├── score.txt             # High score (se crea automáticamente)
│
└── assets/               # Carpeta de recursos
    ├── background1.jpg   # Imagen de fondo
    ├── wood.png         # Imagen de plataforma
    ├── bee_rest_l.png   # Sprite de abeja (izquierda)
    ├── bee_rest_r.png   # Sprite de abeja (derecha)
    ├── bird.png         # Sprite sheet de enemigo pájaro
    ├── booster.webp     # Imagen de booster
    ├── extra_life.png   # Imagen de vida extra
    ├── ghost.png        # Icono del juego
    ├── music_game-2d.mp3 # Música de fondo
    ├── jump.mp3         # Sonido de salto
    ├── death.mp3        # Sonido de muerte
    ├── boost.mp3        # Sonido de booster
    └── powerup.wav      # Sonido de power-up
\`\`\`

## 🎮 Mecánicas Detalladas

### Sistema de Salto
- **Salto Automático**: La abeja salta automáticamente al tocar una plataforma
- **Doble Salto**: Presiona ESPACIO para un segundo salto en el aire
- **Boost**: Los boosters proporcionan saltos súper altos que permiten alcanzar plataformas muy lejanas

### Sistema de Puntuación
- La puntuación aumenta según la altura alcanzada
- El scroll hacia arriba genera puntos automáticamente
- El high score se guarda automáticamente en `score.txt`

### Sistema de Vidas
- Comienzas con **3 vidas**
- Máximo de **5 vidas**
- Pierdes una vida al:
  - Caerte de la pantalla
  - Tocar un enemigo
- **Game Over** cuando se acaban las vidas

### Progresión de Dificultad
- **Score 1000+**: Aparecen plataformas móviles y boosters
- **Score 2000+**: Aparecen enemigos voladores

### Power-ups
- **Boosters** 🚀: 8% de probabilidad de aparición, disponibles después de 1000 puntos
- **Vidas Extra** ❤️: 5% de probabilidad de aparición, máximo 1 en pantalla

## 🛠️ Características Técnicas

### Arquitectura del Código
- **Programación Orientada a Objetos**: Clases bien definidas y organizadas
- **Separación de Responsabilidades**: Cada módulo tiene una función específica
- **Código Modular**: Fácil mantenimiento y extensión
- **Manejo de Errores**: Try-catch para operaciones críticas

### Optimizaciones
- **Sprite Groups**: Uso eficiente de grupos de sprites de pygame
- **Collision Detection**: Detección de colisiones optimizada
- **Memory Management**: Limpieza automática de objetos fuera de pantalla
- **Asset Management**: Carga inteligente de recursos con fallbacks

## 🐛 Solución de Problemas

### El juego no inicia
- **Verifica Python**: Asegúrate de tener Python 3.7+
- **Instala pygame**: `pip install pygame`
- **Verifica archivos**: Asegúrate de que todos los archivos .py estén presentes

### No hay sonido
- **Verifica archivos de audio**: Deben estar en la carpeta `assets/`
- **Comprueba el audio del sistema**: Verifica que el volumen esté activado
- **Drivers de audio**: Asegúrate de que los drivers estén actualizados

### Imágenes no aparecen
- **Verifica la carpeta assets**: Debe estar en el mismo directorio que el ejecutable
- **Fallback automático**: El juego creará rectángulos de colores si faltan imágenes

### Rendimiento lento
- **Cierra otras aplicaciones**: Libera memoria RAM
- **Actualiza drivers gráficos**: Especialmente importante para laptops
- **Verifica requisitos del sistema**: Asegúrate de cumplir los requisitos mínimos

### Error al crear ejecutable
- **Instala PyInstaller**: `pip install pyinstaller`
- **Verifica permisos**: Asegúrate de tener permisos de escritura
- **Antivirus**: Algunos antivirus bloquean PyInstaller temporalmente

## 🎨 Personalización

### Modificar Dificultad
Edita las constantes en `game_config.py`:

```python
# Cambiar velocidades de salto
INITIAL_JUMP_VEL = -20    # Salto normal
BOOST_JUMP_VEL = -60      # Salto con boost

# Cambiar probabilidades de power-ups
BOOSTER_SPAWN_CHANCE = 0.08      # 8% para boosters
EXTRA_LIFE_SPAWN_CHANCE = 0.05   # 5% para vidas extra

# Cambiar requisitos de score
MOVING_PLATFORMS_SCORE = 1000    # Plataformas móviles
ENEMY_SCORE = 2000               # Enemigos
