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
   - The Singleton pattern ensures that only one instance of a class is created. In your code, this is implemented through the static method `get_instance()` in the `MusicPlayer` class, which guarantees that only one instance of the player will be created.

2. **Command**:
   - The Command pattern encapsulates requests as objects, allowing you to parameterize objects with queues, log them, and support undo operations. In your code, the classes `PlayCommand`, `StopCommand`, `PauseCommand`, `NextCommand`, and `PreviousCommand` implement this pattern, enabling control over actions in the music player through their invocation.

3. **Observer** (to some extent):
   - Although implemented implicitly, there are elements of the observer pattern in your code. For example, when a track is selected in the `Listbox`, the `on_select_track` method updates the current state of the player. If there were additional subscribers, they could respond to changes in the player's state.

4. **MVC (Model-View-Controller)**:
   - Your code exhibits elements of the MVC pattern. The `MusicPlayer` can be seen as the controller that manages the application's logic (playing music, managing tracks), while the Tkinter interface represents the view. The data (model) is stored in the form of a list of tracks and their metadata.

5. **Strategy** (to some extent):
   - If you had multiple methods for managing playback (for instance, different ways to control track playback), you could apply the Strategy pattern to encapsulate those algorithms. In the current version, this is not explicitly expressed, but the concept could be applied if you need to change the ways playback is managed.
