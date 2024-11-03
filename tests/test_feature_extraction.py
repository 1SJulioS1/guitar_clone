import unittest
import os
import numpy as np
from audio_processing.data_preparation import load_audio, preprocess_audio
from audio_processing.feature_extraction import (
    extract_tempo,
    extract_energy,
    extract_pitch,
    extract_onsets,
    extract_mfcc,
    extract_chroma,
    extract_spectral_contrast
)

# Definir el directorio del proyecto y el archivo de audio para pruebas
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
audio_file_path = os.path.join(project_root, 'data', 'song.mp3')

class TestFeatureExtraction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        audio_data, sample_rate = load_audio(audio_file_path)
        cls.audio_data = preprocess_audio(audio_data)
        cls.sample_rate = sample_rate

    def test_extract_tempo(self):
        tempo = extract_tempo(self.audio_data, self.sample_rate)
        self.assertGreater(tempo, 0, "El tempo debería ser mayor que 0")

    def test_extract_energy(self):
        energy = extract_energy(self.audio_data)
        self.assertGreater(energy, 0, "La energía debería ser mayor que 0")

    def test_extract_pitch(self):
        pitch = extract_pitch(self.audio_data, self.sample_rate)
        self.assertGreaterEqual(pitch, 0, "El pitch debería ser 0 o positivo")

    def test_extract_onsets(self):
        onsets = extract_onsets(self.audio_data, self.sample_rate)
        self.assertIsInstance(onsets, np.ndarray, "Los onsets deberían ser un array de numpy")
        self.assertGreater(len(onsets), 0, "Debería haber al menos un onset detectado")

    def test_extract_mfcc(self):
        mfcc = extract_mfcc(self.audio_data, self.sample_rate)
        self.assertIsInstance(mfcc, np.ndarray, "Los MFCC deberían ser un array de numpy")
        self.assertEqual(mfcc.shape[0], 13, "El array MFCC debería tener 13 coeficientes")

    def test_extract_chroma(self):
        chroma = extract_chroma(self.audio_data, self.sample_rate)
        self.assertIsInstance(chroma, np.ndarray, "El perfil de croma debería ser un array de numpy")
        self.assertEqual(chroma.shape[0], 12, "El array de croma debería tener 12 valores (una por cada clase de tono)")

    def test_extract_spectral_contrast(self):
        spectral_contrast = extract_spectral_contrast(self.audio_data, self.sample_rate)
        self.assertIsInstance(spectral_contrast, np.ndarray, "El contraste espectral debería ser un array de numpy")
        self.assertGreater(spectral_contrast.shape[0], 0, "El array de contraste espectral debería tener al menos una banda de frecuencias")

if __name__ == '__main__':
    unittest.main()
