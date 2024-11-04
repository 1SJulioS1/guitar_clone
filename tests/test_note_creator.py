# test_note_creator.py
import unittest
from backend.note_generator.note_creator import NoteCreator
import numpy as np

class TestNoteCreator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Simulated audio features for testing
        cls.audio_features = {
            "tempo": 120,
            "tempo_changes": [100, 120, 140],
            "onsets": [0.5, 1.0, 1.5, 2.0],  # Verifica que onsets tenga valores
            "energy": 0.8,
            "pitch": 440,
            "spectrogram": np.random.rand(10, 100),  # Simulated spectrogram data
            "rhythm_pattern": 128,
            "mfcc": np.random.rand(13, 20),  # Simulated MFCC data
            "chroma": np.random.rand(12, 20),  # Simulated Chroma data
            "spectral_contrast": np.random.rand(7, 20) * 20  # Simulated Spectral Contrast
        }
        cls.note_creator = NoteCreator(cls.audio_features)

    def test_generate_notes(self):
        """Test if notes are generated with correct structure and timing."""
        notes = self.note_creator.generate_notes()
        # Debugging message if no notes generated
        if len(notes) == 0:
            print("Debug: No notes generated, audio features:", self.audio_features)
        self.assertGreater(len(notes), 0, "No notes were generated")

        for note in notes:
            self.assertIsInstance(note, dict)
            self.assertIn("time", note)
            self.assertIn("lane", note)
            self.assertIn("intensity", note)
            self.assertIn("spectral_band", note)

    def test_timing_alignment_with_onsets(self):
        """Check that the note times match the onsets provided."""
        notes = self.note_creator.generate_notes()
        onset_times = self.audio_features["onsets"]

        # Verify each note time corresponds to an onset time
        for i, note in enumerate(notes):
            if i < len(onset_times):
                self.assertAlmostEqual(note["time"], onset_times[i], delta=0.1,
                                       msg=f"Note time {note['time']} does not match onset time {onset_times[i]}")

    def test_lane_assignment(self):
        """Test if lane assignment is influenced by chroma, pitch, or mfcc features."""
        notes = self.note_creator.generate_notes()

        for note in notes:
            self.assertGreaterEqual(note["lane"], 1)
            self.assertLessEqual(note["lane"], 4)

    def test_intensity_assignment(self):
        """Check if note intensity is correctly assigned based on energy and spectral contrast."""
        notes = self.note_creator.generate_notes()

        for note in notes:
            self.assertIn(note["intensity"], ["high", "medium", "low"])

    def test_spectral_band_assignment(self):
        """Verify that spectral_band is determined correctly based on the spectrogram."""
        notes = self.note_creator.generate_notes()
        for note in notes:
            self.assertGreaterEqual(note["spectral_band"], 1)
            self.assertLessEqual(note["spectral_band"], self.audio_features["spectrogram"].shape[0])

    def test_variability_with_different_energy_levels(self):
        """Ensure that different energy levels affect the note generation density."""
        low_energy_features = self.audio_features.copy()
        low_energy_features["energy"] = 0.3
        high_energy_features = self.audio_features.copy()
        high_energy_features["energy"] = 1.0

        low_energy_note_creator = NoteCreator(low_energy_features)
        high_energy_note_creator = NoteCreator(high_energy_features)

        low_energy_notes = low_energy_note_creator.generate_notes()
        high_energy_notes = high_energy_note_creator.generate_notes()

        self.assertGreater(len(high_energy_notes), len(low_energy_notes), 
                           "High energy did not produce more notes than low energy")

if __name__ == '__main__':
    unittest.main()
