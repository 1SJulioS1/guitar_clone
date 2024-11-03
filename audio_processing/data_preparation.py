import librosa
import numpy as np

def load_audio(file_path, sample_rate=22050):
    # Cargar el archivo de audio sin importar el formato (.mp3, .wav, etc.)
    audio_data, sr = librosa.load(file_path, sr=sample_rate)
    return audio_data, sr

def preprocess_audio(audio_data):
    """Preprocesa el audio: normalización y conversión a mono."""
    # Normalización de amplitud para que los valores estén en el rango [-1, 1]
    audio_data = librosa.util.normalize(audio_data)
    # Verificar si el audio es estéreo y, si es así, convertirlo a mono
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)
    return audio_data
