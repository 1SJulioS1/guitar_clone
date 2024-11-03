import numpy as np
from audio_processing.feature_extraction import extract_tempo, extract_onsets, extract_energy, extract_pitch, extract_chroma

def generate_notes(audio_data, sample_rate):
    # Extraer características clave para la generación de notas
    tempo = extract_tempo(audio_data, sample_rate)
    onsets = extract_onsets(audio_data, sample_rate)
    onsets = [float(onset) for onset in onsets]  # Convertir cada onset a float
    energy = extract_energy(audio_data)
    pitch = float(extract_pitch(audio_data, sample_rate))  # Convertir pitch a float
    chroma = extract_chroma(audio_data, sample_rate)
    
    notes = []
    onset_index = 0

    # Convertir el tempo a un intervalo de tiempo entre notas en segundos como float
    interval = float(60 / tempo)

    # Generar notas en intervalos basados en el tempo y en los onsets detectados
    current_time = 0.0
    while current_time < onsets[-1]:  # Ahora onsets[-1] es un float escalar
        if onset_index < len(onsets) and current_time >= onsets[onset_index]:
            tone_class = np.argmax(chroma[:, int(onset_index % chroma.shape[1])])
            note_type = map_tone_to_note_type(tone_class)

            intensity = "high" if energy > 0.5 else "normal"

            # Crear la nota asegurándonos de que current_time es un float
            note = {
                "time": current_time,  # current_time es un float escalar
                "type": note_type,
                "intensity": intensity,
                "pitch": pitch  # pitch ya está asegurado como float
            }
            notes.append(note)
            onset_index += 1
        
        # Incremento y forzado a float para current_time
        current_time = float(current_time + interval)

    return notes

def map_tone_to_note_type(tone_class):
    """Mapea el valor de croma a un tipo de nota del juego."""
    note_types = ["red", "green", "blue", "yellow", "purple"]
    return note_types[tone_class % len(note_types)]
