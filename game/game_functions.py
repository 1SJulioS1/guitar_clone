# game/game_functions.py
import pygame
import time

def play_song(song_path):
    """Cargar y reproducir la canción, devolviendo el tiempo de inicio."""
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.play()
    return time.time()

def run_game(notes, song_path):
    """Lógica principal del juego para visualizar las notas y reproducir la canción."""
    # Inicialización de la ventana de juego
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Guitar Hero Clone")

    # Configuración de la línea de acierto
    LINE_Y_POS = 500
    clock = pygame.time.Clock()
    score = 0

    # Reproducir la canción
    start_time = play_song(song_path)

    running = True
    while running:
        screen.fill((255, 255, 255))  # Fondo blanco

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Obtener el tiempo actual en el juego
        current_time = time.time() - start_time

        # Dibujar y actualizar cada nota
        for note in notes:
            note_time = note["time"]
            if current_time >= note_time - 0.5:
                y_pos = int(600 - (current_time - note_time) * 300)
                if 0 < y_pos < 600:
                    pygame.draw.circle(screen, (255, 0, 0), (400, y_pos), 20)

                    # Verificar acierto
                    if LINE_Y_POS - 10 <= y_pos <= LINE_Y_POS + 10:
                        if pygame.key.get_pressed()[pygame.K_SPACE]:
                            score += 100
                            notes.remove(note)

        # Mostrar la puntuación
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)  # FPS

    pygame.quit()
