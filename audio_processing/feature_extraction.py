import librosa
import numpy as np

def extract_tempo(audio_data, sample_rate):
    onset_env = librosa.onset.onset_strength(y=audio_data, sr=sample_rate)
    tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sample_rate)
    # Asegurarnos de que tempo sea un escalar
    return float(tempo[0]) if isinstance(tempo, np.ndarray) else float(tempo)


def extract_energy(audio_data):
    return sum(audio_data**2) / len(audio_data)

def extract_pitch(audio_data, sample_rate):
    pitches, magnitudes = librosa.core.piptrack(y=audio_data, sr=sample_rate)
    pitch_values = [pitches[index, t] for t in range(pitches.shape[1]) if (index := magnitudes[:, t].argmax()) and pitches[index, t] > 0]
    return sum(pitch_values) / len(pitch_values) if pitch_values else 0

# Nuevas características
def extract_onsets(audio_data, sample_rate):
    onset_frames = librosa.onset.onset_detect(y=audio_data, sr=sample_rate)
    onset_times = librosa.frames_to_time(onset_frames, sr=sample_rate)
    return onset_times

def extract_mfcc(audio_data, sample_rate, n_mfcc=13):
    mfcc = librosa.feature.mfcc(y=audio_data, sr=sample_rate, n_mfcc=n_mfcc)
    return mfcc

def extract_chroma(audio_data, sample_rate):
    chroma = librosa.feature.chroma_stft(y=audio_data, sr=sample_rate)
    return chroma

def extract_spectral_contrast(audio_data, sample_rate):
    spectral_contrast = librosa.feature.spectral_contrast(y=audio_data, sr=sample_rate)
    return spectral_contrast
