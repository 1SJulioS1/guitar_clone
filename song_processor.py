import os
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from audio_processing.data_preparation import load_audio, preprocess_audio
from note_generator.note_generation import generate_notes
from game.game_interface import run_interface
import random  # To assign notes to random columns


def process_and_save_song():
    """Selects and processes a song, then saves it in processed_songs/."""
    file_path = filedialog.askopenfilename(title="Seleccionar Canción", filetypes=[("Audio Files", "*.mp3 *.wav")])
    if not file_path:
        return

    try:
        audio_data, sr = load_audio(file_path)
        processed_audio = preprocess_audio(audio_data)
        
        output_dir = "processed_songs"
        os.makedirs(output_dir, exist_ok=True)
        
        file_name = os.path.splitext(os.path.basename(file_path))[0] + "_processed.npy"
        output_path = os.path.join(output_dir, file_name)
        np.save(output_path, processed_audio)
        
        messagebox.showinfo("Éxito", f"La canción '{file_name}' ha sido procesada y guardada en '{output_dir}'.")
    except Exception as e:
        messagebox.showerror("Error", f"Hubo un error al procesar la canción: {e}")

def list_processed_songs():
    """Lists all processed songs in the 'processed_songs' directory."""
    output_dir = "processed_songs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    return [f for f in os.listdir(output_dir) if f.endswith("_processed.npy")]

def select_processed_song_and_start_game():
    """Displays a list of processed songs and starts the game with the selected song."""
    # Create the selection window
    selection_window = tk.Toplevel()
    selection_window.title("Seleccionar Canción Procesada")
    
    # List available processed songs
    processed_files = list_processed_songs()
    if not processed_files:
        messagebox.showinfo("Sin canciones", "No se encontraron canciones procesadas en 'processed_songs'.")
        selection_window.destroy()
        return
    
    # Define `selected_song` as a local variable within `select_processed_song_and_start_game`
    selected_song = tk.StringVar(selection_window)
    selected_song.set(processed_files[0])  # Set the first song as default
    
    # Dropdown menu for song selection
    dropdown = tk.OptionMenu(selection_window, selected_song, *processed_files)
    dropdown.pack(pady=20)

    def start_game():
        song_path = os.path.join("processed_songs", selected_song.get())
        processed_audio = np.load(song_path)
        COLUMNS = 4
        
        
        # Generate notes and assign each to a random column
        sample_rate = 22050
        notes = generate_notes(processed_audio, sample_rate)
        for note in notes:
            note["column"] = random.randint(0, COLUMNS - 1)  # Assign each note to one of the columns

        run_interface(notes, processed_audio, song_name=selected_song.get())
        selection_window.destroy()


    # Button to start the game with the selected song
    start_button = tk.Button(selection_window, text="Jugar", command=start_game)
    start_button.pack(pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Procesador de Canciones")
    root.geometry("300x200")
    
    process_button = tk.Button(root, text="Procesar Canción", command=process_and_save_song)
    process_button.pack(pady=20)
    
    select_button = tk.Button(root, text="Seleccionar Canción Procesada y Jugar", command=select_processed_song_and_start_game)
    select_button.pack(pady=20)
    
    root.mainloop()
