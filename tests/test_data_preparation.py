import unittest
import os
import numpy as np
from audio_processing.data_preparation import load_audio, preprocess_audio

# Definir el directorio del proyecto y el archivo de audio para pruebas
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
audio_file_path = os.path.join(project_root, 'data', 'song.mp3')

class TestDataPreparation(unittest.TestCase):

    def test_load_audio(self):
        """Prueba la carga del archivo de audio y verifica los datos básicos."""
        audio_data, sr = load_audio(audio_file_path)
        self.assertIsInstance(audio_data, np.ndarray, "El audio cargado no es un array de numpy")
        self.assertGreater(len(audio_data), 0, "El archivo de audio debería contener datos")
        self.assertIsInstance(sr, int, "El sample rate debería ser un entero")

    def test_sample_rate(self):
        """Verifica si el sample rate es el esperado al cargar el archivo."""
        expected_sr = 22050
        _, sr = load_audio(audio_file_path, sample_rate=expected_sr)
        self.assertEqual(sr, expected_sr, "El sample rate no coincide con el valor esperado")

    def test_preprocess_audio(self):
        audio_data, _ = load_audio(audio_file_path)
        processed_audio = preprocess_audio(audio_data)
        
        # Verificar que los datos estén en el rango [-1, 1]
        self.assertTrue(np.max(processed_audio) <= 1 and np.min(processed_audio) >= -1,
                        "El audio no está normalizado en el rango [-1, 1]")
        
        # Verificar que los datos sean mono
        self.assertEqual(processed_audio.ndim, 1, "El audio no es mono")
        
if __name__ == '__main__':
    unittest.main()
