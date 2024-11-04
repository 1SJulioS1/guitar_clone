# data_preparation.py
import librosa

class DataPreparation:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio_data = None
        self.sample_rate = None

    def load_audio(self):
        """Load audio data from a file."""
        self.audio_data, self.sample_rate = librosa.load(self.file_path, sr=None)
        return self.audio_data, self.sample_rate

    def normalize_audio(self):
        """Normalize audio data to ensure consistency."""
        if self.audio_data is not None:
            max_val = max(abs(self.audio_data))
            self.audio_data = self.audio_data / max_val if max_val != 0 else self.audio_data
        return self.audio_data
