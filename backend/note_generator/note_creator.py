# note_creator.py
import random
import numpy as np

class NoteCreator:
    def __init__(self, audio_features):
        """
        Initialize with extracted audio features.

        Parameters:
            audio_features (dict): Dictionary containing all extracted features.
        """
        self.tempo = audio_features.get("tempo", 120)  # Base tempo in BPM
        self.tempo_changes = audio_features.get("tempo_changes", [])
        self.onsets = audio_features.get("onsets", [])
        self.energy = audio_features.get("energy", 1.0)
        self.pitch = audio_features.get("pitch", 0.0)
        self.spectrogram = np.array(audio_features.get("spectrogram", []))  # Convert to NumPy array
        self.rhythm_pattern = audio_features.get("rhythm_pattern", 0.0)
        self.mfcc = np.array(audio_features.get("mfcc", []))  # Convert to NumPy array
        self.chroma = np.array(audio_features.get("chroma", []))  # Convert to NumPy array
        self.spectral_contrast = np.array(audio_features.get("spectral_contrast", []))  # Convert to NumPy array
        self.notes = []

    def generate_notes(self):
        """
        Generate a sequence of notes based on multiple song characteristics.

        Returns:
            list of dicts: Each dict represents a note event with timing, lane, intensity, and other properties.
        """
        lane_count = 4
        beat_interval = 60.0 / self.tempo if self.tempo else 0.5  # Initial beat interval
        current_time = 0.0

        # Generate notes based on onsets, rhythm, and energy
        for onset_time in self.onsets:
            # Adjust beat interval based on tempo changes if available
            if self.tempo_changes:
                beat_interval = 60.0 / random.choice(self.tempo_changes)

            # Determine the lane using pitch, chroma, and mfcc
            note_lane = self._determine_lane(self.pitch, self.chroma, self.mfcc)

            # Determine intensity using energy and spectral contrast
            intensity = self._determine_intensity(self.energy, self.spectral_contrast)

            # Conditionally add note based on energy level
            if random.random() < self.energy:  # Higher energy increases likelihood of note creation
                self.notes.append({
                    "time": onset_time,
                    "lane": note_lane,
                    "intensity": intensity,
                    "spectral_band": self._determine_spectral_band(self.spectrogram, onset_time)
                })

            current_time = onset_time + beat_interval

        return self.notes

    def _determine_lane(self, pitch, chroma, mfcc):
        """Determine the lane based on pitch, chroma, and MFCC information."""
        if chroma.size > 0:
            chroma_mean = chroma.mean(axis=1)
            lane = int((chroma_mean.argmax() % 4) + 1)
        elif mfcc.size > 0:
            lane = int((np.mean(mfcc) % 4) + 1)  # Mapping MFCC average to lanes
        else:
            lane = min(4, max(1, int(pitch / 200)))  # Basic mapping based on pitch
        return lane

    def _determine_intensity(self, energy, spectral_contrast):
        """Determine the intensity of a note based on energy and spectral contrast."""
        if spectral_contrast.size > 0:
            contrast_mean = spectral_contrast.mean()
            if contrast_mean > 20 and energy > 0.8:
                return "high"
            elif contrast_mean > 10 and energy > 0.5:
                return "medium"
            else:
                return "low"
        return "medium"  # Default intensity if no spectral contrast available

    def _determine_spectral_band(self, spectrogram, time):
        """Determine the primary spectral band at a given time."""
        if spectrogram.size > 0:
            index = min(int(time * spectrogram.shape[1]), spectrogram.shape[1] - 1)
            band_energy = spectrogram[:, index]
            primary_band = np.argmax(band_energy) + 1  # Spectral band with highest energy
            return primary_band
        return 1  # Default to band 1 if no spectrogram available

    def get_notes(self):
        """Return the generated notes."""
        return self.notes
