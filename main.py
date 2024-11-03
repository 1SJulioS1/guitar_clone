import sys
import os
import tkinter as tk
from song_processor import process_and_save_song, select_processed_song_and_start_game

# Asegurarse de que el directorio raíz esté en el PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

def start_song_processor():
    """Inicia la interfaz para procesar y seleccionar canciones usando song_processor."""
    root = tk.Tk()
    root.title("Procesador de Canciones")
    root.geometry("300x200")
    
    # Botón para procesar una nueva canción
    process_button = tk.Button(root, text="Procesar Canción", command=process_and_save_song)
    process_button.pack(pady=20)
    
    # Botón para seleccionar una canción procesada y abrir el juego
    select_button = tk.Button(root, text="Seleccionar Canción Procesada y Jugar", command=select_processed_song_and_start_game)
    select_button.pack(pady=20)
    
    root.mainloop()

if __name__ == "__main__":
    # Inicia la interfaz del procesador de canciones
    start_song_processor()