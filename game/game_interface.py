import pygame
import time
import random  # To assign notes to random columns

from audio_processing.data_preparation import load_audio, preprocess_audio
from note_generator.note_generation import generate_notes

# Screen and color configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LINE_Y_POS = SCREEN_HEIGHT - 100
WHITE = (255, 255, 255)
NOTE_COLOR = (255, 0, 0)
LINE_COLOR = (0, 255, 0)

pygame.init()
pygame.mixer.init()  # Initialize the mixer for audio playback
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Guitar Hero Clone")

font = pygame.font.Font(None, 36)
COLUMNS = 4
COLUMN_POSITIONS = [SCREEN_WIDTH // (COLUMNS + 1) * (i + 1) for i in range(COLUMNS)]
KEYS = [pygame.K_a, pygame.K_s, pygame.K_k, pygame.K_l]  # Map each column to a specific key

def draw_score(score):
    """Draw the current score on the screen."""
    score_text = font.render(f"Score: {score}", True, LINE_COLOR)
    screen.blit(score_text, (10, 10))

def draw_line():
    """Draw the hit line on the screen."""
    pygame.draw.line(screen, LINE_COLOR, (0, LINE_Y_POS), (SCREEN_WIDTH, LINE_Y_POS), 5)

def draw_notes(notes, current_time):
    """Draw and update the position of notes on the screen, distributed across columns."""
    for note in notes:
        note_time = note["time"]
        
        # Assign column position and x-coordinate
        column = note.get("column", random.randint(0, COLUMNS - 1))
        x_pos = COLUMN_POSITIONS[column]
        
        # Calculate y-coordinate based on time elapsed
        y_pos = int((current_time - note_time) * 150)  # Adjust speed if necessary

        # Draw the note only if it's on screen
        if 0 <= y_pos < LINE_Y_POS:
            pygame.draw.circle(screen, NOTE_COLOR, (x_pos, y_pos), 20)
            note["y_pos"] = y_pos  # Save y-position for hit detection

def check_note_hit(notes, column):
    """Check if the player has hit a note in a specific column when pressing a key."""
    for note in notes:
        if note.get("column") == column:
            if LINE_Y_POS - 10 <= note.get("y_pos", 0) <= LINE_Y_POS + 10:
                notes.remove(note)  # Remove the note if hit successfully
                return True
    return False

def run_interface(notes, processed_audio, song_name="Canción Procesada"):
    """Run the game interface with audio playback and note interaction."""
    pygame.mixer.music.load("data/song.mp3")  # Ensure this points to the correct audio file
    pygame.mixer.music.play()

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
                # Check if the pressed key corresponds to a column
                for i, key in enumerate(KEYS):
                    if event.key == key and check_note_hit(notes, i):
                        score += 100  # Increase score on hit

        current_time = time.time() - start_time

        draw_line()
        draw_notes(notes, current_time)
        draw_score(score)

        pygame.display.flip()
        clock.tick(60)

    pygame.mixer.music.stop()
    pygame.quit()
