import os
import librosa
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from game.game_interface import run_interface  # Importar la función de juego para iniciar el juego

def load_audio(file_path, sample_rate=22050):
    """Carga el archivo de audio sin importar el formato (.mp3, .wav, etc.)."""
    audio_data, sr = librosa.load(file_path, sr=sample_rate)
    return audio_data, sr

def preprocess_audio(audio_data):
    """Normaliza el audio y lo convierte a mono si es necesario."""
    audio_data = librosa.util.normalize(audio_data)
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)
    return audio_data

def process_and_save_song():
    """Permite al usuario seleccionar una canción, procesa el audio y lo guarda en un directorio de salida."""
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
    """Lista las canciones procesadas en el directorio 'processed_songs'."""
    output_dir = "processed_songs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Obtener los archivos .npy en el directorio de canciones procesadas
    processed_files = [f for f in os.listdir(output_dir) if f.endswith("_processed.npy")]
    return processed_files

def select_processed_song_and_start_game():
    """Permite seleccionar una canción procesada de una lista y luego inicia el juego con esa canción."""
    # Crear ventana de selección de canciones
    selection_window = tk.Toplevel()
    selection_window.title("Seleccionar Canción Procesada")
    
    # Lista de canciones procesadas
    processed_files = list_processed_songs()
    if not processed_files:
        messagebox.showinfo("Sin canciones", "No se encontraron canciones procesadas en 'processed_songs'.")
        selection_window.destroy()
        return
    
    # Variable para almacenar la canción seleccionada
    selected_song = tk.StringVar(selection_window)
    selected_song.set(processed_files[0])  # Seleccionar la primera canción por defecto

    # Menú desplegable para seleccionar una canción
    dropdown = tk.OptionMenu(selection_window, selected_song, *processed_files)
    dropdown.pack(pady=20)

    def start_game():
        song_path = os.path.join("processed_songs", selected_song.get())
        processed_audio = np.load(song_path)
        run_interface(processed_audio, song_name=selected_song.get())  # Usar `song_name` si `run_interface` está modificado
        selection_window.destroy()

    # Botón para iniciar el juego con la canción seleccionada
    start_button = tk.Button(selection_window, text="Jugar", command=start_game)
    start_button.pack(pady=10)

# Interfaz de `song_processor.py` para pruebas
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Procesador de Canciones")
    root.geometry("300x200")
    
    # Botón para procesar una nueva canción
    process_button = tk.Button(root, text="Procesar Canción", command=process_and_save_song)
    process_button.pack(pady=20)
    
    # Botón para seleccionar una canción procesada y jugar
    select_button = tk.Button(root, text="Seleccionar Canción Procesada y Jugar", command=select_processed_song_and_start_game)
    select_button.pack(pady=20)
    
    root.mainloop()
