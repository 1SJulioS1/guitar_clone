# test_feature_extraction.py
import unittest
import os
import numpy as np
from backend.audio_processing.data_preparation import DataPreparation
from backend.audio_processing.feature_extraction import FeatureExtraction

class TestFeatureExtraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Ruta al archivo de audio de prueba en el directorio `test_data`
        file_path = os.path.join(os.path.dirname(__file__), "test_data", "test_audio.mp3")
        data_prep = DataPreparation(file_path)
        audio_data, sample_rate = data_prep.load_audio()
        cls.feature_extractor = FeatureExtraction(audio_data, sample_rate)

    def test_extract_tempo(self):
        tempo = self.feature_extractor.extract_tempo()
        self.assertIsInstance(tempo, float)
        self.assertGreater(tempo, 0)

    def test_extract_pitch(self):
        pitch = self.feature_extractor.extract_pitch()
        self.assertIsInstance(pitch, float)
        self.assertGreaterEqual(pitch, 0)

    def test_extract_energy(self):
        energy = self.feature_extractor.extract_energy()
        self.assertIsInstance(energy, float)
        self.assertGreater(energy, 0)

    def test_extract_spectrogram(self):
        spectrogram = self.feature_extractor.extract_spectrogram()
        self.assertIsInstance(spectrogram, np.ndarray)
        self.assertEqual(spectrogram.ndim, 2)

    def test_extract_rhythm_pattern(self):
        rhythm_pattern = self.feature_extractor.extract_rhythm_pattern()
        self.assertIsInstance(rhythm_pattern, float)
        self.assertGreater(rhythm_pattern, 0)

    def test_extract_onsets(self):
        onsets = self.feature_extractor.extract_onsets()
        self.assertIsInstance(onsets, np.ndarray)
        self.assertGreater(len(onsets), 0)

    def test_extract_mfcc(self):
        mfccs = self.feature_extractor.extract_mfcc()
        self.assertIsInstance(mfccs, np.ndarray)
        self.assertEqual(mfccs.shape[0], 13)
        self.assertGreater(mfccs.shape[1], 0)

    def test_extract_chroma(self):
        chroma = self.feature_extractor.extract_chroma()
        self.assertIsInstance(chroma, np.ndarray)
        self.assertEqual(chroma.shape[0], 12)
        self.assertGreater(chroma.shape[1], 0)

    def test_extract_spectral_contrast(self):
        spectral_contrast = self.feature_extractor.extract_spectral_contrast()
        self.assertIsInstance(spectral_contrast, np.ndarray)
        self.assertGreaterEqual(spectral_contrast.shape[0], 2)
        self.assertGreater(spectral_contrast.shape[1], 0)

    def test_extract_tempo_changes(self):
        """Test if tempo changes extraction provides a list of tempos."""
        tempo_changes = self.feature_extractor.extract_tempo_changes()
        self.assertIsInstance(tempo_changes, np.ndarray)
        self.assertGreater(len(tempo_changes), 0)
        for tempo in tempo_changes:
            self.assertIsInstance(tempo, float)
            self.assertGreater(tempo, 0)  # Tempo should be positive

if __name__ == '__main__':
    unittest.main()
