# feature_extraction.py
import librosa
import numpy as np
from librosa.feature import rhythm

class FeatureExtraction:
    def __init__(self, audio_data, sample_rate):
        self.audio_data = audio_data
        self.sample_rate = sample_rate

    def extract_tempo(self):
        """Extract tempo from audio data."""
        tempo, _ = librosa.beat.beat_track(y=self.audio_data, sr=self.sample_rate)
        return float(tempo) if isinstance(tempo, (float, int)) else float(tempo[0])

    def extract_pitch(self):
        """Calculate general pitch tuning."""
        pitches, _ = librosa.core.piptrack(y=self.audio_data, sr=self.sample_rate)
        pitch = np.mean(pitches[np.nonzero(pitches)])  # Average pitch
        return float(pitch)

    def extract_energy(self):
        """Calculate the average energy of the audio signal."""
        energy = np.sum(self.audio_data**2) / len(self.audio_data)
        return energy

    def extract_spectrogram(self):
        """Generate a spectrogram from the audio data."""
        spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(self.audio_data)), ref=np.max)
        return spectrogram

    def extract_rhythm_pattern(self):
        """Extract rhythmic pattern or beats."""
        onset_env = librosa.onset.onset_strength(y=self.audio_data, sr=self.sample_rate)
        rhythm_pattern = rhythm.tempo(onset_envelope=onset_env, sr=self.sample_rate)
        return float(rhythm_pattern[0]) if rhythm_pattern.size > 0 else 0.0

    def extract_onsets(self):
        """Detect onset events in the audio."""
        onsets = librosa.onset.onset_detect(y=self.audio_data, sr=self.sample_rate)
        return onsets

    def extract_mfcc(self):
        """Extract Mel-frequency cepstral coefficients."""
        mfccs = librosa.feature.mfcc(y=self.audio_data, sr=self.sample_rate, n_mfcc=13)
        return mfccs

    def extract_chroma(self):
        """Calculate chroma features."""
        chroma = librosa.feature.chroma_stft(y=self.audio_data, sr=self.sample_rate)
        return chroma

    def extract_spectral_contrast(self):
        """Calculate spectral contrast."""
        spectral_contrast = librosa.feature.spectral_contrast(y=self.audio_data, sr=self.sample_rate)
        return spectral_contrast

    def extract_all_features(self):
        """Extract all features into a dictionary."""
        return {
            "tempo": self.extract_tempo(),
            "pitch": self.extract_pitch(),
            "energy": self.extract_energy(),
            "spectrogram": self.extract_spectrogram(),
            "rhythm_pattern": self.extract_rhythm_pattern(),
            "onsets": self.extract_onsets(),
            "mfcc": self.extract_mfcc(),
            "chroma": self.extract_chroma(),
            "spectral_contrast": self.extract_spectral_contrast()
        }
