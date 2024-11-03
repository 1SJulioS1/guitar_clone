# game/game_engine.py
from audio_processing.data_preparation import load_audio, preprocess_audio
from note_generator.note_generation import generate_notes
from game.game_functions import run_game  # Ya no importamos play_song

if __name__ == "__main__":
    # Cargar el archivo de audio y preparar las notas
    audio_data, sample_rate = load_audio("data/song.mp3")
    preprocessed_audio = preprocess_audio(audio_data)
    notes = generate_notes(preprocessed_audio, sample_rate)
    
    # Ejecutar el juego
    run_game(notes, "data/song.mp3")
