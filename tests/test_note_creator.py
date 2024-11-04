# test_note_creator.py

import unittest
import numpy as np
from backend.note_generator.note_creator import NoteCreator

class TestNoteCreator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Definimos valores claros y controlados para los onsets
        cls.audio_features = {
            "tempo": 120,
            "onsets": [0.5, 1.0, 1.5, 2.0],  # Onsets específicos para la prueba
            "energy": 1.0,
            "pitch": 440.0,  # Frecuencia de la nota A4
            "spectrogram": np.random.rand(5, 100)  # Espectrograma de ejemplo
        }
        cls.note_creator = NoteCreator(cls.audio_features)
        cls.notes = cls.note_creator.generate_notes()

    def test_timing_alignment_with_onsets(self):
        """Check that the note times match the onsets provided exactly."""
        onset_times = self.audio_features["onsets"]

        # Verificamos que cada tiempo de nota en notes corresponda al onset
        for i, note in enumerate(self.notes):
            self.assertAlmostEqual(
                note["time"], onset_times[i], delta=0.1,
                msg=f"Note time {note['time']} does not match onset time {onset_times[i]}"
            )

if __name__ == "__main__":
    unittest.main()
