# Guitar Clone

**Guitar Clone** is a game inspired by Guitar Hero, allowing players to play notes in sync with a song's rhythm. It uses signal processing to generate notes based on the song's characteristics, offering an interactive and dynamic experience.

## Features

- **Audio Processing**: Extracts musical features from a song, such as tempo, energy, pitch, and spectrogram.
- **Note Generation**: Creates note events based on the intensity and changes in the audio signal for engaging gameplay.
- **Game Engine**: Provides core game logic, including song playback and note visualization.
- **Graphical Interface**: Visual design for the game, where notes are displayed and player progress is shown.
- **Scoring System**: Evaluates player accuracy in real time.

## Project Structure

- `audio_processing`: Scripts for signal processing and audio feature extraction.
- `note_generator`: Logic to generate notes based on the song’s characteristics.
- `game`: Core game logic.
- `visualization`: Graphical interface for displaying notes and game controls.
- `tests`: Unit and integration tests to verify functionality of the modules.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/1SJulioS1/guitar_clone.git
   cd guitar_clone
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Ensure **FFmpeg** is installed and accessible from the terminal.

4. Run the game:

   ```bash
   python main.py
   ```

## Usage

- **Load a Song**: Select an audio file (.mp3 or .wav) to analyze and generate notes.
- **Gameplay**: Follow the rhythm and press the corresponding keys as notes reach the hit line.
- **Game Controls**: Use the keys `A`, `S`, `K`, and `L` for the four note columns.

## Contributing

Contributions are welcome. If you’d like to improve the project or fix issues, please follow these steps:

1. Fork the repository.
2. Create a branch for your feature or fix (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add a new feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request on GitHub.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
