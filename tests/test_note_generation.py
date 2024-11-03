import unittest
import os
import numpy as np
from audio_processing.data_preparation import load_audio, preprocess_audio
from audio_processing.note_generation import generate_notes

# Definir el directorio del proyecto y el archivo de audio para pruebas
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
audio_file_path = os.path.join(project_root, 'data', 'song.mp3')

class TestNoteGeneration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Cargar y preprocesar el audio una vez para usarlo en las pruebas
        audio_data, sample_rate = load_audio(audio_file_path)
        cls.audio_data = preprocess_audio(audio_data)
        cls.sample_rate = sample_rate
        cls.notes = generate_notes(cls.audio_data, cls.sample_rate)

    def test_generate_notes_not_empty(self):
        """Verificar que la lista de notas generada no esté vacía."""
        self.assertGreater(len(self.notes), 0, "La lista de notas no debería estar vacía")

    def test_note_structure(self):
        """Verificar que cada nota tenga las propiedades correctas."""
        for note in self.notes:
            self.assertIn("time", note, "Cada nota debe tener un 'time'")
            self.assertIn("type", note, "Cada nota debe tener un 'type'")
            self.assertIn("intensity", note, "Cada nota debe tener una 'intensity'")
            self.assertIn("pitch", note, "Cada nota debe tener un 'pitch'")
            self.assertIsInstance(note["time"], (int, float), "'time' debe ser un número")
            self.assertIsInstance(note["type"], str, "'type' debe ser un string")
            self.assertIn(note["intensity"], ["high", "normal"], "'intensity' debe ser 'high' o 'normal'")
            self.assertIsInstance(note["pitch"], (int, float), "'pitch' debe ser un número")

    def test_notes_time_order(self):
        """Verificar que las notas estén en orden de tiempo ascendente."""
        times = [note["time"] for note in self.notes]
        self.assertEqual(times, sorted(times), "Los tiempos de las notas deben estar en orden ascendente")

    def test_note_types_within_defined_set(self):
        """Verificar que los tipos de nota estén dentro del conjunto esperado."""
        expected_types = {"red", "green", "blue", "yellow", "purple"}
        for note in self.notes:
            self.assertIn(note["type"], expected_types, "El tipo de nota debe estar en el conjunto definido de tipos")

if __name__ == "__main__":
    unittest.main()
