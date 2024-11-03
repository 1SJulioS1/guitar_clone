import librosa
import numpy as np

def load_audio(file_path, sample_rate=22050):
    """Loads audio from file, regardless of format."""
    audio_data, sr = librosa.load(file_path, sr=sample_rate)
    return audio_data, sr

def preprocess_audio(audio_data):
    """Normalizes and converts audio to mono if necessary."""
    audio_data = librosa.util.normalize(audio_data)
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)
    return audio_data
