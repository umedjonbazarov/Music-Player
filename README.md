# Music Player

A simple music player application built with Python using Tkinter for the GUI and Pygame for audio playback. This application allows users to browse, play, pause, and navigate through their music tracks, displaying album art when available.

## Features

- Load and play MP3 files from a specified directory.
- Play, pause, stop, skip to the next track, and go back to the previous track.
- Display the current track title and its duration.
- Show album art for the currently playing track.
- A responsive GUI with progress tracking for playback.

## Requirements

To run this application, ensure you have the following dependencies installed:

- Python 3.x
- Pygame
- Mutagen
- Pillow (PIL)
- Tkinter (usually included with Python)

You can install the required packages using pip:

```bash
pip install pygame mutagen pillow
```

## Usage

1. Clone this repository or download the code files to your local machine.
2. Update the `rootpath` variable in the `MusicPlayer` class with the path to your music folder containing MP3 files.
3. Place the image files for the buttons in the `PNG` folder (ensure to rename them accordingly).
4. Run the application:

```bash
python music_player.py
```

5. Select a track from the list to play, and use the control buttons to manage playback.

## Directory Structure

```
Music-Player/
│
├── music_player.py         # Main application file
├── PNG/                     # Directory for button images
│   ├── play_img.png
│   ├── pause_img.png
│   ├── stop_img.png
│   ├── next_img.png
│   └── prev_img.png
└── playlist/                # Directory for your MP3 files
    ├── track1.mp3
    ├── track2.mp3
    └── ...
```

## Contributing

Feel free to contribute to this project by forking the repository, making your changes, and submitting a pull request. 

## Acknowledgments

- This project uses the Pygame library for audio playback.
- Album art extraction is done using the Mutagen library.

## Patterns


1. **Singleton**:
   
2. **Command**:
   
3. **Observer** (to some extent):
   
4. **MVC (Model-View-Controller)**:

5. **Strategy** (to some extent):
