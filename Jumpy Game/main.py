"""
Jumpy Game - Punto de entrada principal del juego.

Este archivo inicializa y ejecuta el juego Jumpy Game.
Mantiene el código de inicialización separado de la lógica del juego.
"""

import sys
import os

# Agregar el directorio actual al path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.game_manager import GameManager


def main():
    """
    Función principal que inicializa y ejecuta el juego.

    Maneja errores de inicialización y proporciona mensajes
    informativos al usuario en caso de problemas.
    """
    try:
        print("Iniciando Jumpy Game...")
        game = GameManager()
        game.run()

    except ImportError as error:
        print(f"Error de importación: {error}")
        print("Asegúrate de tener pygame instalado: pip install pygame")

    except Exception as error:
        print(f"Error ejecutando el juego: {error}")
        print("Verifica que todos los archivos estén presentes y sean accesibles.")

    finally:
        print("Juego terminado. ¡Gracias por jugar!")


if __name__ == "__main__":
    main()
