# Desarrollado por:
1. Cevallos Jamileth
2. Nazareno Josué
   
# Jumpy Game 🐝

Un emocionante juego de plataformas vertical donde controlas una abeja que salta automáticamente entre plataformas mientras evita enemigos y recolecta power-ups.

## 📋 Descripción

Jumpy Game es un juego de plataformas con scroll vertical infinito. El jugador controla una abeja que salta automáticamente de plataforma en plataforma, tratando de alcanzar la mayor altura posible mientras evita enemigos voladores y recolecta power-ups útiles.

## 🎮 Características

- **Salto automático**: La abeja salta automáticamente al tocar una plataforma
- **Doble salto**: Capacidad de realizar un segundo salto en el aire
- **Power-ups**:
  - 🚀 **Boosters**: Proporcionan un salto súper potente
  - ❤️ **Vidas extra**: Aumentan el número de vidas disponibles
- **Plataformas móviles**: Plataformas que se mueven horizontalmente
- **Enemigos voladores**: Pájaros que cruzan la pantalla
- **Sistema de vidas**: Múltiples oportunidades para continuar jugando
- **High Score**: Guarda automáticamente tu mejor puntuación

## 🕹️ Controles

| Tecla | Acción |
|-------|--------|
| **N** | Iniciar el juego desde la pantalla principal |
| **A** | Mover la abeja hacia la izquierda |
| **D** | Mover la abeja hacia la derecha |
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

## 📦 Requisitos

### Software Necesario
- Python 3.7 o superior
- pygame 2.0 o superior

### Instalación de Dependencias

\`\`\`bash
pip install pygame
\`\`\`

## 📁 Estructura del Proyecto

\`\`\`
jumpy_game/
│
├── jumpy_game.py          # Archivo principal del juego
├── enemy.py               # Clase Enemy para enemigos
├── spritesheet.py         # Clase SpriteSheet para manejo de sprites
├── README.md              # Este archivo
├── score.txt              # Archivo de high score (se crea automáticamente)
│
└── assets/                # Carpeta de recursos
    ├── background1.jpg    # Imagen de fondo
    ├── wood.png          # Imagen de plataforma
    ├── bee_rest_l.png    # Sprite de abeja (izquierda)
    ├── bee_rest_r.png    # Sprite de abeja (derecha)
    ├── bird.png          # Sprite sheet de enemigo pájaro
    ├── booster.webp      # Imagen de booster
    ├── extra_life.png    # Imagen de vida extra
    ├── ghost.png         # Icono del juego
    ├── music_game-2d.mp3 # Música de fondo
    ├── jump.mp3          # Sonido de salto
    ├── death.mp3         # Sonido de muerte
    ├── boost.mp3         # Sonido de booster
    └── powerup.wav       # Sonido de power-up
\`\`\`

## 🚀 Cómo Ejecutar

1. **Clona o descarga** el proyecto
2. **Asegúrate** de tener Python y pygame instalados
3. **Navega** al directorio del juego
4. **Ejecuta** el juego:

\`\`\`bash
python jumpy_game.py
\`\`\`

## 🎮 Mecánicas del Juego

### Sistema de Salto
- **Salto Automático**: La abeja salta automáticamente al tocar una plataforma
- **Doble Salto**: Presiona ESPACIO para un segundo salto en el aire
- **Boost**: Los boosters proporcionan saltos súper altos

### Sistema de Puntuación
- La puntuación aumenta según la altura alcanzada
- El scroll hacia arriba genera puntos
- El high score se guarda automáticamente

### Sistema de Vidas
- Comienzas con 3 vidas
- Máximo de 5 vidas
- Pierdes una vida al:
  - Caerte de la pantalla
  - Tocar un enemigo
- Game Over cuando se acaban las vidas

### Power-ups
- **Boosters** (🚀): 8% de probabilidad, aparecen después de 1000 puntos
- **Vidas Extra** (❤️): 5% de probabilidad, máximo 1 en pantalla

### Progresión de Dificultad
- **Score 1000+**: Aparecen plataformas móviles y boosters
- **Score 2000+**: Aparecen enemigos voladores

## 🛠️ Características Técnicas

### Arquitectura del Código
- **Programación Orientada a Objetos**: Clases bien definidas y organizadas
- **Separación de Responsabilidades**: Cada clase tiene una función específica
- **Gestión de Assets**: Sistema centralizado para cargar recursos
- **Manejo de Errores**: Try-catch para operaciones de archivo y carga de assets

### Optimizaciones
- **Sprite Groups**: Uso eficiente de grupos de sprites de pygame
- **Object Pooling**: Reutilización de objetos para mejor rendimiento
- **Collision Detection**: Detección de colisiones optimizada
- **Memory Management**: Limpieza automática de objetos fuera de pantalla

## 🐛 Solución de Problemas

### El juego no inicia
- Verifica que pygame esté instalado: \`pip install pygame\`
- Asegúrate de tener Python 3.7+

### No hay sonido
- Verifica que los archivos de audio estén en la carpeta \`assets/\`
- Comprueba que tu sistema tenga audio habilitado

### Imágenes no aparecen
- Verifica que todos los archivos de imagen estén en \`assets/\`
- El juego creará rectángulos de colores si faltan imágenes

### Rendimiento lento
- Cierra otras aplicaciones que consuman recursos
- Verifica que tu sistema cumpla los requisitos mínimos

## 🎨 Personalización

### Modificar Dificultad
Edita las constantes en la clase \`GameConfig\`:

\`\`\`python
# Cambiar velocidades de salto
NORMAL_JUMP_VELOCITY = -20  # Salto normal
BOOST_JUMP_VELOCITY = -60   # Salto con boost

# Cambiar probabilidades de power-ups
BOOSTER_SPAWN_CHANCE = 0.08      # 8% para boosters
EXTRA_LIFE_SPAWN_CHANCE = 0.05   # 5% para vidas extra
\`\`\`

### Agregar Nuevos Power-ups
1. Crea una nueva clase heredando de \`PowerUp\`
2. Agrega la lógica en \`Player.handle_power_up_collection()\`
3. Incluye la generación en \`GameManager._generate_power_ups()\`

## 📝 Créditos

- **Desarrollado con**: Python y pygame
- **Inspirado en**: Juegos clásicos de plataformas como Doodle Jump
- **Assets**: [Especifica aquí la fuente de tus assets si no son propios]

## 📄 Licencia

Este proyecto es de código abierto. Siéntete libre de modificarlo y distribuirlo.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar el juego:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Soporte

Si encuentras algún problema o tienes preguntas:
- Abre un issue en el repositorio
- Revisa la sección de solución de problemas
- Verifica que tengas todas las dependencias instaladas

¡Disfruta jugando Jumpy Game! 🐝🎮
\`\`\`
