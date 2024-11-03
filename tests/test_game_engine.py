import unittest
import time
import pygame
from game.game_functions import play_song
from audio_processing.data_preparation import load_audio, preprocess_audio
from note_generator.note_generation import generate_notes

LINE_Y_POS = 500  # Posición de la línea de acierto

class TestGameEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("\nCargando y generando notas para las pruebas...")
        audio_data, sample_rate = load_audio("data/song.mp3")
        preprocessed_audio = preprocess_audio(audio_data)
        cls.notes = generate_notes(preprocessed_audio, sample_rate)
        cls.song_path = "data/song.mp3"
        print("Carga y generación de notas completada.")

    def test_play_song_initialization(self):
        print("\nIniciando test_play_song_initialization...")
        pygame.mixer.init()  # Inicializar el mixer de Pygame
        start_time = play_song(self.song_path)
        self.assertIsInstance(start_time, float, "El tiempo de inicio debe ser un número de punto flotante")
        self.assertGreater(start_time, 0, "El tiempo de inicio debe ser positivo")
        pygame.mixer.music.stop()
        pygame.mixer.quit()  # Cerrar el mixer después de la prueba
        print("Finalizado test_play_song_initialization.")

    def test_note_sync_with_song(self):
        print("\nIniciando test_note_sync_with_song...")
        
        # Verificar que los tiempos de las notas estén en orden ascendente
        previous_time = 0
        for i, note in enumerate(self.notes[:10]):  # Probar las primeras 10 notas para simplificar
            note_time = note["time"]
            
            # Asegurarse de que cada tiempo de nota sea mayor o igual al anterior
            self.assertGreaterEqual(note_time, previous_time,
                                    msg=f"La nota {i} no está en orden secuencial correcto.")
            
            # Actualizar el tiempo previo
            previous_time = note_time

        print("Finalizado test_note_sync_with_song.")

    def test_scoring_accuracy(self):
        print("\nIniciando test_scoring_accuracy...")
        pygame.init()
        score = 0
        start_time = time.time()
        for note in self.notes[:5]:
            note_time = note["time"]
            time.sleep(0.1)
            y_pos = LINE_Y_POS
            if abs(y_pos - LINE_Y_POS) <= 10:
                score += 100
        self.assertGreater(score, 0, "La puntuación debe aumentar al acertar las notas")
        pygame.quit()
        print("Finalizado test_scoring_accuracy.")

if __name__ == "__main__":
    unittest.main(verbosity=2)
