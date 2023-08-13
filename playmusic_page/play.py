import pygame
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import threading
import os
from mutagen.mp3 import MP3
import sys
import time

# Class for the Play music page
class MusicPlayer:
    def __init__(self, genres, music_files):
        pygame.mixer.init()  # Initialize the Pygame mixer
        # Initialize class variables
        self.genres = genres
        self.genre_index = 0
        self.current_music_index = 0
        self.current_position = 0
        self.paused_position = 0
        self.music_files = music_files
        self.is_playing = False
        self.is_paused = False
        self.is_completed = False
        self.is_dragging = False
        self.music_directory = None
        self.current_music = None
        self.root = None
        self.song_name_label = None
        self.image_frame = None
        self.image_label = None
        self.button_frame = None
        self.play_pause_button = None
        self.forward_10s_button = None
        self.backward_10s_button = None
        self.progress_frame = None
        self.progress_bar = None
        self.duration_label = None
        self.previous_button = None
        self.next_button = None
        self.song_name_update_thread = None
        self.rotation_stop_event = threading.Event()
    
    # Convert seconds into minutes and seconds format
    def format_time(self, seconds):
        minutes = int(seconds // 60)
        seconds = int(seconds % 60)
        return "{:02d}:{:02d}".format(minutes, seconds)
    
    # Toggle between play and pause
    def toggle_play_pause(self):
        if self.is_playing:
            pygame.mixer.music.pause()  # Pause the music
            self.play_pause_button.config(image=self.play_image)
            self.rotation_stop_event.set()
            self.is_paused = True
            self.paused_position = self.current_position
        else:
            if self.is_paused:
                pygame.mixer.music.unpause()  # Unpause the music
                self.start_image_rotation()
                self.is_paused = False
                self.current_position = self.paused_position
            else:
                if pygame.mixer.music.get_busy():
                   pygame.mixer.music.play()  # Resume playing from where it was paused
                else:
                    pygame.mixer.music.load(self.music_files[self.current_music_index])  # Load and play the music from the current position
                    pygame.mixer.music.play(start=self.current_position)
                self.start_image_rotation()
            self.play_pause_button.config(image=self.pause_image)
        self.is_playing = not self.is_playing

    # Skip forward by 10 seconds
    def skip_forward_10s(self):
        if self.is_playing or self.is_paused:
            self.current_position += 10
            if self.current_position > self.current_music.info.length:
                self.current_position = self.current_music.info.length
            if self.is_paused:
                self.paused_position = self.current_position
            self.set_song_position(self.current_position)
            self.progress_bar.set((self.current_position / self.current_music.info.length) * 100)

    # Skip backward by 10 seconds
    def skip_backward_10s(self):
        if self.is_playing or self.is_paused:
            self.current_position -= 10
            if self.current_position < 0:
               self.current_position = 0
            if self.is_paused:
               self.paused_position = self.current_position
            self.set_song_position(self.current_position)
            self.progress_bar.set((self.current_position / self.current_music.info.length) * 100)
    
    # Start rotating the image on a separate thread
    def start_image_rotation(self):
        self.rotation_stop_event.clear()
        rotation_thread = threading.Thread(target=self.rotate_image)
        rotation_thread.start()

    # Rotate the image continuously while the rotation_stop_event is not set
    def rotate_image(self):
        rotation_angle = 0
        image_path = "assets/tape_small.png"  
        image = Image.open(image_path)
        while not self.rotation_stop_event.is_set():
            rotated_image = image.rotate(rotation_angle)
            photo = ImageTk.PhotoImage(rotated_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo
            rotation_angle += 1

    # Start dragging the progress bar
    def start_dragging(self, event):
        self.is_dragging = True
        self.progress_bar.set(event.x / self.progress_bar.winfo_width() * 100)

    # Stop dragging and set the song position accordingly
    def stop_dragging(self, event):
        if self.is_playing or self.is_paused:
            position = event.x / self.progress_bar.winfo_width() * 100
            self.current_position = float(position) / 100 * self.current_music.info.length
            if self.is_paused:
                self.paused_position = self.current_position
                self.set_song_position(self.current_position)
            else:
                self.set_song_position(self.current_position)
                pygame.mixer.music.unpause()
        self.is_dragging = False

    # Set the playback position of the music
    def set_song_position(self, position):
        pygame.mixer.music.set_pos(position)

    # Update the progress bar while playing
    def update_progress_bar(self):
        if self.is_playing:
            if self.current_position < self.current_music.info.length:
                self.current_position += 0.1
            else:
                if not self.is_completed:
                    # If the music is completed, reset and load the next song
                    self.is_completed = True
                    self.stop_playing()
                    self.current_position = 0
                    self.progress_bar.set(0)
                    self.duration_label.config(text="00:00/" + self.format_time(self.current_music.info.length))
                    self.load_music()
                    self.update_progress_bar()
                    return
        if not self.is_completed:
            progress = (self.current_position / self.current_music.info.length) * 100
            self.progress_bar.set(progress)
            self.duration_label.config(
                text=self.format_time(self.current_position) + "/" + self.format_time(self.current_music.info.length))
        self.root.after(100, self.update_progress_bar)

    # Stop the music playback
    def stop_playing(self):
        pygame.mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.play_pause_button.config(image=self.play_image)
        self.rotation_stop_event.set()
        self.reset_progress_bar()

    # Reset the progress bar when not playing or dragging
    def reset_progress_bar(self):
        if not self.is_playing and not self.is_dragging:
            self.progress_bar.set(0)
            self.duration_label.config(text="00:00/" + self.format_time(self.current_music.info.length))

    # Play the next song in the playlist
    def next_song(self):
        if self.current_music_index < len(self.music_files) - 1:
            self.current_music_index += 1
            self.load_music()

    # Play the previous song in the playlist
    def previous_song(self):
        if self.current_music_index > 0:
            self.current_music_index -= 1
            self.load_music()

    # Update the song name label continuously
    def update_song_name_label(self):
        while True:
            song_filename = os.path.splitext(os.path.basename(self.music_files[self.current_music_index]))[0]
            self.song_name_label.config(text=song_filename)
            self.root.update()
            time.sleep(1)

    # Refreash music
    def load_music(self):
        pygame.mixer.music.stop()
        self.rotation_stop_event.set()
        self.is_completed = False

        if self.current_music_index >= len(self.music_files):
            self.current_music_index = 0

        self.current_music = MP3(self.music_files[self.current_music_index])
        pygame.mixer.music.load(self.music_files[self.current_music_index])
        self.is_playing = False
        self.is_paused = False
        self.play_pause_button.config(image=self.play_image)
        self.duration_label.config(text="00:00/" + self.format_time(self.current_music.info.length))
        self.current_position = 0
        self.reset_progress_bar()
        song_filename = os.path.splitext(os.path.basename(self.music_files[self.current_music_index]))[0]
        self.song_name_label.config(text=song_filename)
    
    # Close window 
    def on_close(self):
        self.toggle_play_pause()
        self.root.destroy()
        os._exit(0)
        
    # Create Tkinter window    
    def initialize(self):
        self.root = Tk()
        genre = self.genres[self.genre_index]
        self.root.title("Music Player Software - {}".format(genre))
        self.root.resizable(False, False)
        window_width = 1150
        window_height = 700
        self.root.geometry(f"{window_width}x{window_height}")

        if not self.music_files:
            print("No music files found in the music directory.")
            return

        # Set the initial current_music to the first music file
        self.current_music = MP3(self.music_files[self.current_music_index])
        pygame.mixer.music.load(self.music_files[self.current_music_index])   # Load a new music file

        # Load images
        self.play_image = PhotoImage(file="assets/play_icon.png")
        self.pause_image = PhotoImage(file="assets/pause_icon.png")
        forward_image = PhotoImage(file="assets/next_icon.png")
        backward_image = PhotoImage(file="assets/previous_icon.png")
        forward_10s_image = PhotoImage(file="assets/forward.png")
        backward_10s_image = PhotoImage(file="assets/backward.png")

        # Create style
        style = ttk.Style()
        style.configure("TButton", background="white", relief="flat")

        # Create a label to display the song name without the file extension
        self.song_name_label = Label(self.root, text="", font=("Arial", 38))
        self.song_name_label.pack(pady=10)
 
        # Create a frame for the image label
        self.image_frame = Frame(self.root)
        self.image_frame.pack(pady=10)

        # Create an initial image label
        initial_image_path = "assets/tape_small.png"
        initial_image = Image.open(initial_image_path)
        initial_photo = ImageTk.PhotoImage(initial_image)
        self.image_label = Label(self.image_frame, image=initial_photo)
        self.image_label.pack()

        # Create a frame for the buttons
        self.button_frame = Frame(self.root)
        self.button_frame.pack()

        # Play button
        self.play_pause_button = ttk.Button(self.button_frame, image=self.play_image, style="TButton", command=self.toggle_play_pause)
        self.play_pause_button.grid(row=0, column=2, padx=10)

        # Forward button
        self.forward_10s_button = ttk.Button(self.button_frame, image=forward_10s_image, style="TButton", command=self.skip_forward_10s)
        self.forward_10s_button.grid(row=0, column=3, padx=10)

        # Backward button
        self.backward_10s_button = ttk.Button(self.button_frame, image=backward_10s_image, style="TButton", command=self.skip_backward_10s)
        self.backward_10s_button.grid(row=0, column=1, padx=10)

        # Create a frame for the progress bar
        self.progress_frame = Frame(self.root)
        self.progress_frame.pack(pady=10)

        # Create a progress bar
        self.progress_bar = ttk.Scale(self.progress_frame, from_=0, to=100, orient=HORIZONTAL, length=800)
        self.progress_bar.pack()

        # Bind progress bar events
        self.progress_bar.bind("<ButtonPress-1>", self.start_dragging)
        self.progress_bar.bind("<ButtonRelease-1>", self.stop_dragging)

        # Create a label to display music duration with initial text
        initial_duration_text = "00:00/{}".format(self.format_time(self.current_music.info.length))
        self.duration_label = Label(self.root, text=initial_duration_text)
        self.duration_label.pack()

        # Create previous button
        self.previous_button = ttk.Button(self.button_frame, image=backward_image, style="TButton", command=self.previous_song)
        self.previous_button.grid(row=0, column=0, padx=10)
        
        # Create next button
        self.next_button = ttk.Button(self.button_frame, image=forward_image, style="TButton", command=self.next_song)
        self.next_button.grid(row=0, column=4, padx=10)

        # Start the thread to update the song name label
        self.song_name_update_thread = threading.Thread(target=self.update_song_name_label)
        self.song_name_update_thread.daemon = True
        self.song_name_update_thread.start()
        
        # Start updating the progress bar
        self.update_progress_bar()
        
         # Center the window
        self.center_window()

        # Bind window close event to on_close function
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Start the Tkinter event loop
        self.root.mainloop()
        
    # Set window to center
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

# Read user name
with open('username.txt', 'r') as file:
    username = file.read().strip()  # Assuming the username is a single line of text in the file

# Genres
genres = ["rock", "pop", "jazz", "classical", "hip_hop", "country", "userfile"]
genres = [genre.replace("userfile", f"userdata/{username}") for genre in genres]
# Get the genre index from the command-line arguments
genre_index = int(sys.argv[1])

# Use the genre index to load the corresponding music folder and files
genre = genres[genre_index]
music_directory = f"playmusic_page/{genre}"

# List all music files in the directory
music_files = []
for file in os.listdir(music_directory):
    if file.endswith(".mp3"):
        music_files.append(os.path.join(music_directory, file))

# Create the MusicPlayer object with the required arguments
player = MusicPlayer(genres, music_files)
player.initialize()
