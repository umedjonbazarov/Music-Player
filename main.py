import tkinter as tk
from tkinter import ttk
import fnmatch
import os
from pygame import mixer
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from PIL import Image, ImageTk
import io

class MusicPlayer:
    _instance = None

    @staticmethod
    def get_instance():
        if MusicPlayer._instance is None:
            MusicPlayer._instance = MusicPlayer()
        return MusicPlayer._instance

    def __init__(self):
        if MusicPlayer._instance is not None:
            raise Exception("This class is a singleton!")
        self.current_track_index = 0
        self.tracks = []
        self.is_paused = False
        self.rootpath = "/home/umed/python_Music_Player/Music-Player/playlist"
        self.pattern = "*.mp3"
        self.track_duration = 0
        self.correct_time = 0
        self.new_time = 0
        self.init_gui()

    def init_gui(self):
        mixer.init()
        self.convas = tk.Tk()
        self.convas.title("Music Player")
        self.convas.geometry("600x800")
        self.convas.config(bg='black')
        self.prev_img = tk.PhotoImage(file="PNG/prev_img.png")
        self.stop_img = tk.PhotoImage(file="PNG/stop_img.png")
        self.play_img = tk.PhotoImage(file="PNG/play_img.png")
        self.pause_img = tk.PhotoImage(file="PNG/pause_img.png")
        self.next_img = tk.PhotoImage(file="PNG/next_img.png")
        self.album_label = tk.Label(self.convas, bg="black", text="No Album Art", font=('ds-digital', 14), fg="yellow", compound="center")
        self.album_label.pack(pady=20)
        self.label = tk.Label(self.convas, text='', bg='black', fg='yellow', font=('ds-digital', 18), pady=10)
        self.label.pack()
        self.init_controls()
        self.time_frame = tk.Frame(self.convas, bg="black")
        self.time_frame.pack(pady=10)
        self.current_time_label = tk.Label(self.time_frame, text="0:00", bg="black", fg="yellow", font=('ds-digital', 14))
        self.current_time_label.pack(side="left")
        self.progress = ttk.Progressbar(self.time_frame, orient='horizontal', length=400, mode='determinate')
        self.progress.pack(side="left", padx=10)
        self.duration_label = tk.Label(self.time_frame, text="0:00", bg="black", fg="yellow", font=('ds-digital', 14))
        self.duration_label.pack(side="left")
        self.listBox = tk.Listbox(self.convas, fg="cyan", bg="black", width=50, height=10, font=('ds-digital', 14), selectbackground="gray20", selectforeground="cyan")
        self.listBox.pack(side='bottom', padx=20, pady=20)
        self.listBox.bind("<<ListboxSelect>>", self.on_select_track)
        self.progress.bind("<Button-1>", self.on_progress_click)
        self.load_tracks()
        self.convas.mainloop()

    def init_controls(self):
        top = tk.Frame(self.convas, bg="black")
        top.pack(pady=20, anchor='center')
        button_style = {'bg': 'black', 'borderwidth': 0, 'highlightthickness': 0, 'activebackground': 'gray20'}
        self.prevButton = tk.Button(top, image=self.prev_img, **button_style, command=PreviousCommand(self))
        self.prevButton.pack(side='left', padx=10)
        self.stopButton = tk.Button(top, image=self.stop_img, **button_style, command=StopCommand(self))
        self.stopButton.pack(side='left', padx=10)
        self.playButton = tk.Button(top, image=self.play_img, **button_style, command=PlayCommand(self))
        self.playButton.pack(side='left', padx=10)
        self.pauseButton = tk.Button(top, image=self.pause_img, **button_style, command=PauseCommand(self))
        self.pauseButton.pack(side='left', padx=10)
        self.nextButton = tk.Button(top, image=self.next_img, **button_style, command=NextCommand(self))
        self.nextButton.pack(side='left', padx=10)

    def load_tracks(self):
        for root, dirs, files in os.walk(self.rootpath):
            for filename in fnmatch.filter(files, self.pattern):
                self.tracks.append(filename)
                self.listBox.insert('end', filename)

    def on_select_track(self, event):
        selected_index = self.listBox.curselection()
        if selected_index:
            self.current_track_index = selected_index[0]

    def play_track(self):
        if not self.tracks:
            return
        track_name = self.tracks[self.current_track_index]
        self.label.config(text=track_name)
        mixer.music.load(os.path.join(self.rootpath, track_name))
        mixer.music.set_volume(1.0)
        mixer.music.play()
        self.correct_time = 0
        self.new_time = 0
        audio = MP3(os.path.join(self.rootpath, track_name))
        self.track_duration = audio.info.length
        self.progress['maximum'] = self.track_duration
        self.duration_label.config(text=self.format_time(self.track_duration))
        self.update_progress_bar()
        self.show_album_art(track_name)

    def update_progress_bar(self):
        if mixer.music.get_busy() or self.is_paused:
            current_time = (mixer.music.get_pos() + self.new_time - self.correct_time) / 1000
            self.progress['value'] = current_time
            self.current_time_label.config(text=self.format_time(current_time))
            self.convas.after(1000, self.update_progress_bar)

    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return f"{minutes}:{seconds:02}"

    def stop_track(self):
        mixer.music.stop()
        self.progress['value'] = 0
        self.current_time_label.config(text="0:00")
        self.correct_time = 0
        self.new_time = 0

    def toggle_pause(self):
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
        else:
            mixer.music.pause()
            self.is_paused = True

    def on_progress_click(self, event):
        x = event.x
        bar_width = self.progress.winfo_width()
        new_position = (x / bar_width) * self.track_duration
        mixer.music.set_pos(new_position)
        self.progress['value'] = new_position
        self.current_time_label.config(text=self.format_time(new_position))
        self.correct_time = mixer.music.get_pos()
        self.new_time = new_position * 1000

    def next_track(self):
        self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
        self.select_track()
        self.correct_time = 0
        self.new_time = 0

    def prev_track(self):
        self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
        self.select_track()
        self.correct_time = 0
        self.new_time = 0

    def select_track(self):
        self.listBox.select_clear(0, tk.END)
        self.listBox.select_set(self.current_track_index)
        self.listBox.activate(self.current_track_index)
        self.play_track()

    def show_album_art(self, track_name):
        try:
            audio = MP3(os.path.join(self.rootpath, track_name), ID3=ID3)
            for tag in audio.tags.values():
                if isinstance(tag, APIC):
                    album_art_data = tag.data
                    image = Image.open(io.BytesIO(album_art_data))
                    image = image.resize((300, 300), Image.LANCZOS)
                    album_art = ImageTk.PhotoImage(image)
                    self.album_label.config(image=album_art, text="")
                    self.album_label.image = album_art
                    return
            raise ValueError("No album art found")
        except Exception as e:
            print(f"No album art for {track_name}: {e}")
            self.album_label.config(image='', text="No Album Art Available", font=('ds-digital', 14), fg="yellow")

class Command:
    def __init__(self, player):
        self.player = player

class PlayCommand(Command):
    def __call__(self):
        self.player.play_track()

class StopCommand(Command):
    def __call__(self):
        self.player.stop_track()

class PauseCommand(Command):
    def __call__(self):
        self.player.toggle_pause()

class NextCommand(Command):
    def __call__(self):
        self.player.next_track()

class PreviousCommand(Command):
    def __call__(self):
        self.player.prev_track()

if __name__ == "__main__":
    MusicPlayer.get_instance()
