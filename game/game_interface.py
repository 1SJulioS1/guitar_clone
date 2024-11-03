import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pygame
import time

# Configuración de la ventana y colores
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LINE_Y_POS = SCREEN_HEIGHT - 100
WHITE = (255, 255, 255)
NOTE_COLOR = (255, 0, 0)
LINE_COLOR = (0, 255, 0)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guitar Hero Clone")

# Fuente para la puntuación
font = pygame.font.Font(None, 36)

# Configuración de teclas y posiciones para las columnas de notas
COLUMNS = 4
COLUMN_POSITIONS = [SCREEN_WIDTH // (COLUMNS + 1) * (i + 1) for i in range(COLUMNS)]
KEYS = [pygame.K_a, pygame.K_s, pygame.K_k, pygame.K_l]  # Teclas A, S, K, L

def draw_score(score):
    """Dibuja la puntuación en la pantalla."""
    score_text = font.render(f"Score: {score}", True, LINE_COLOR)
    screen.blit(score_text, (10, 10))

def draw_line():
    """Dibuja la línea de acierto en la pantalla."""
    pygame.draw.line(screen, LINE_COLOR, (0, LINE_Y_POS), (SCREEN_WIDTH, LINE_Y_POS), 5)

def draw_notes(notes, current_time):
    """Dibuja y actualiza la posición de las notas en la pantalla, distribuídas en columnas."""
    for note in notes:
        note_time = note["time"]
        
        # Asignar columna y posición horizontal
        column = note.get("column", 0)  # Asigna una columna predeterminada si no está especificada
        x_pos = COLUMN_POSITIONS[column]
        
        # Calcular posición vertical de la nota
        y_pos = int((current_time - note_time) * 150)  # Ajustar velocidad aquí
        
        # Dibujar solo si la nota está en la pantalla
        if 0 <= y_pos < LINE_Y_POS:
            pygame.draw.circle(screen, NOTE_COLOR, (x_pos, y_pos), 20)
            note["y_pos"] = y_pos  # Guardar la posición actual de la nota para la verificación de acierto

def check_note_hit(notes, column):
    """Verifica si el jugador ha acertado una nota en una columna específica al presionar la tecla."""
    for note in notes:
        if note.get("column") == column:
            if LINE_Y_POS - 10 <= note.get("y_pos", 0) <= LINE_Y_POS + 10:
                notes.remove(note)  # Eliminar la nota acertada
                return True
    return False

def run_interface(notes, processed_audio, song_name="Canción Procesada"):
    """Ejecuta la interfaz gráfica del juego usando el audio procesado y muestra el nombre de la canción."""
    print(f"Iniciando el juego con {song_name}")
    clock = pygame.time.Clock()
    score = 0
    start_time = time.time()
    
    running = True
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                for i, key in enumerate(KEYS):
                    if event.key == key and check_note_hit(notes, i):
                        score += 100

        current_time = time.time() - start_time

        draw_line()
        draw_notes(notes, current_time)
        draw_score(score)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
