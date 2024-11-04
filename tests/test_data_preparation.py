# test_data_preparation.py
import unittest
import os
from backend.audio_processing.data_preparation import DataPreparation

class TestDataPreparation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ruta al archivo de audio de prueba en el directorio `test_data`
        cls.file_path = os.path.join(os.path.dirname(__file__), "test_data", "test_audio.mp3")
        cls.data_prep = DataPreparation(cls.file_path)

    def test_load_audio(self):
        """Test if audio loads correctly and sample rate is set."""
        audio_data, sample_rate = self.data_prep.load_audio()
        self.assertIsNotNone(audio_data, "Audio data should not be None")
        self.assertIsNotNone(sample_rate, "Sample rate should not be None")
        self.assertGreater(len(audio_data), 0, "Audio data should not be empty")

    def test_normalize_audio(self):
        """Test if audio normalization works as expected."""
        normalized_audio = self.data_prep.normalize_audio()
        max_val = max(abs(normalized_audio))
        self.assertAlmostEqual(max_val, 1.0, delta=0.01, msg="Normalized audio should have max amplitude close to 1.0")

if __name__ == '__main__':
    unittest.main()
