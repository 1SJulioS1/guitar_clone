# test_game_engine.py

import unittest
import numpy as np
from backend.game_engine.game_engine import GameEngine
from backend.note_generator.note_creator import NoteCreator

class TestGameEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        audio_features = {
            "tempo": 120,
            "onsets": [0.5, 1.0, 1.5, 2.0],  # Onsets específicos para las notas
            "energy": 1.0,
            "pitch": 440.0,
            "spectrogram": np.random.rand(5, 100)
        }
        cls.note_creator = NoteCreator(audio_features)
        cls.notes = cls.note_creator.generate_notes()
        cls.engine = GameEngine(cls.notes, tolerance=0.2)

    def test_register_hit(self):
        """Test if note is registered as a hit within tolerance."""
        self.engine.start_game()
        
        # Ajustamos el tiempo y el lane para que coincidan con los valores generados
        hit_time = 0.6  # Dentro de la tolerancia ±0.2 alrededor de 0.5
        result = self.engine.register_note_hit(hit_time, lane=2)
        
        # Verificamos que el golpe sea registrado como "hit" y el puntaje sea incrementado
        self.assertEqual(result, "hit")
        self.assertEqual(self.engine.score, 100)

    def test_register_miss(self):
        """Test if note is registered as a miss outside of tolerance."""
        self.engine.start_game()
        
        # Usamos un tiempo de golpe fuera de la tolerancia para asegurar que sea "miss"
        hit_time = 1.5  # Este tiempo debería estar fuera de la tolerancia de 0.5
        result = self.engine.register_note_hit(hit_time, lane=2)
        
        # Verificamos que el golpe sea registrado como "miss" y que el puntaje no cambie
        self.assertEqual(result, "miss")
        self.assertEqual(self.engine.score, 0)

if __name__ == '__main__':
    unittest.main()
