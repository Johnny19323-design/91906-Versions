import pygame
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import threading
import os
from mutagen.mp3 import MP3
from tkinter import Tk

# Gets the name of the current song file
song_folder = os.path.basename(os.getcwd())
song_name = song_folder.capitalize()

# Music directory path
music_directory = "main_homepage/upload_page/userdata" 

# List all music files in the directory
music_files = []
for file in os.listdir(music_directory):
    if file.endswith(".mp3"):
        music_files.append(os.path.join(music_directory, file))

# Initialize Pygame mixer
pygame.mixer.init()

# Create variables to track the music playing and paused states
is_playing = False
is_paused = False
current_music_index = 0

# Create Tkinter window
root = Tk()
root.title("Music Player Software - {}".format(song_name)) 


# Set window size
window_width = 1000
window_height = 650
root.geometry(f"{window_width}x{window_height}")


# Load images
play_image = PhotoImage(file="assets/play_icon.png")
pause_image = PhotoImage(file="assets/pause_icon.png")
forward_image = PhotoImage(file="assets/next_icon.png")
backward_image = PhotoImage(file="assets/previous_icon.png")
forward_10s_image = PhotoImage(file="assets/forward.png")
backward_10s_image = PhotoImage(file="assets/backward.png")

# Create style
style = ttk.Style()
style.configure("TButton", background="white", relief="flat")

# Create a label to display the song name
song_name_label = Label(root, text=song_name, font=("Arial", 38))
song_name_label.pack(pady=10)

# Create a frame for the image label
image_frame = Frame(root)
image_frame.pack(pady=10)

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return "{:02d}:{:02d}".format(minutes, seconds)

# Create an initial image label
initial_image_path = "assets/tape_small.png"
initial_image = Image.open(initial_image_path)
initial_photo = ImageTk.PhotoImage(initial_image)
image_label = Label(image_frame, image=initial_photo)
image_label.pack()

# Create a frame for the buttons
button_frame = Frame(root)
button_frame.pack()


 # Update the size of the window
def center_window(window):
    window.update_idletasks() 
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# Control the play and pause of music, update the image of the play/pause button.
def toggle_play_pause():
    global is_playing, is_paused, current_position, paused_position
    if is_playing:
        pygame.mixer.music.pause()  # Pause music
        play_pause_button.config(image=play_image)  # Change to "Play" image
        rotation_stop_event.set()  # Stop image rotation
        is_paused = True
        paused_position = current_position  # Store the current position
    else:
        if is_paused:
            pygame.mixer.music.unpause()  # Resume music
            start_image_rotation()  # Start image rotation
            is_paused = False
            current_position = paused_position  # Set the current position to the paused position
            
        else:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.play()  # Resume music from current position
            else:
                pygame.mixer.music.load(music_files[current_music_index])
                pygame.mixer.music.play(start=current_position)
                
            start_image_rotation()  # Start image rotation
        play_pause_button.config(image=pause_image)  # Change to "Pause" image
    is_playing = not is_playing

# Move the music forward 10 seconds
def skip_forward_10s():
    global current_position, paused_position
    if is_playing or is_paused:
        current_position += 10
        if current_position > current_music.info.length:
            current_position = current_music.info.length
        if is_paused:
            paused_position = current_position
        set_song_position(current_position)
        progress_bar.set((current_position / current_music.info.length) * 100)

# Move the music backward 10 seconds
def skip_backward_10s():
    global current_position, paused_position
    if is_playing or is_paused:
        current_position -= 10
        if current_position < 0:
            current_position = 0
        if is_paused:
            paused_position = current_position
        set_song_position(current_position)
        progress_bar.set((current_position / current_music.info.length) * 100)

# Play button
play_pause_button = ttk.Button(button_frame, image=play_image, style="TButton", command=toggle_play_pause)
play_pause_button.grid(row=0, column=2, padx=10)
# Forward button
forward_10s_button = ttk.Button(button_frame, image=forward_10s_image, style="TButton", command=skip_forward_10s)
forward_10s_button.grid(row=0, column=3, padx=10)
# Backward button
backward_10s_button = ttk.Button(button_frame, image=backward_10s_image, style="TButton", command=skip_backward_10s)
backward_10s_button.grid(row=0, column=1, padx=10)
# Event to control image rotation
rotation_stop_event = threading.Event()

# Picture tape turning
def start_image_rotation():
    rotation_stop_event.clear()  # Clear the stop event flag
    rotation_thread = threading.Thread(target=rotate_image)  # Create a new thread
    rotation_thread.start()  # Start the rotation thread

# Picture tape upload
def rotate_image():
    rotation_angle = 0
    image_path = "assets/tape_small.png"  # Replace with the actual path to your image
    image = Image.open(image_path)
    while not rotation_stop_event.is_set():
        rotated_image = image.rotate(rotation_angle)
        photo = ImageTk.PhotoImage(rotated_image)
        image_label.config(image=photo)
        image_label.image = photo
        rotation_angle += 1

# Create a frame for the progress bar
progress_frame = Frame(root)
progress_frame.pack(pady=10)

# Create a progress bar
progress_bar = ttk.Scale(progress_frame, from_=0, to=100, orient=HORIZONTAL, length=800)
progress_bar.pack()
is_dragging = False
current_position = 0  # Variable to store the current position

# Progress bar is dragging
def start_dragging(event):
    global is_dragging
    is_dragging = True
    progress_bar.set(event.x / progress_bar.winfo_width() * 100)  # Set the progress bar value to the dragged position

# Progress bar stops dragging
def stop_dragging(event):
    global is_dragging, current_position, paused_position
    if is_playing or is_paused:
        position = event.x / progress_bar.winfo_width() * 100
        current_position = float(position) / 100 * current_music.info.length
        if is_paused:
            paused_position = current_position
            set_song_position(current_position)
        else:
            set_song_position(current_position)
            pygame.mixer.music.unpause()  # Resume music
    is_dragging = False

progress_bar.bind("<ButtonPress-1>", start_dragging)
progress_bar.bind("<ButtonRelease-1>", stop_dragging)

# Set the music position
def set_song_position(position):
    pygame.mixer.music.set_pos(position)  
is_completed = False

# Progress bar
def update_progress_bar():
    global current_position, is_completed
    if is_playing:
        if current_position < current_music.info.length:
            current_position += 0.1  # Increment the current position by 0.1 seconds
        else:
            if not is_completed:
                is_completed = True
                stop_playing()  # Music playback completed, stop playing and reset the interface
                current_position = 0  # Reset the position to 0
                progress_bar.set(0)  # Reset the progress bar
                duration_label.config(text="00:00/" + format_time(current_music.info.length))  # Reset the duration label
                load_music()  # Load the next music and start playing from the beginning
                update_progress_bar()  # Start updating the progress bar immediately
                return  # Return to avoid updating progress bar and duration label prematurely
    if not is_completed:
        progress = (current_position / current_music.info.length) * 100  # Calculate the progress percentage
        progress_bar.set(progress)
        duration_label.config(
            text=format_time(current_position) + "/" + format_time(current_music.info.length))  # Update the duration label

    root.after(100, update_progress_bar)  # Update the progress bar every 100 milliseconds

# Play/pause
def stop_playing():
    global is_playing, is_paused
    pygame.mixer.music.stop()  # Stop music
    is_playing = False
    is_paused = False
    play_pause_button.config(image=play_image)  # Change to "Play" image
    rotation_stop_event.set()  # Stop image rotation
    reset_progress_bar()  # Reset progress bar only if the music has ended

# Dragging progress bar
def reset_progress_bar():
    if not is_playing and not is_dragging:
        progress_bar.set(0)
        duration_label.config(
            text="00:00/" + format_time(current_music.info.length))  # Reset the duration label

# Next song
def next_song():
    global current_music_index
    if current_music_index < len(music_files) - 1:
        current_music_index += 1
        load_music()

# Previous song
def previous_song():
    global current_music_index
    if current_music_index > 0:
        current_music_index -= 1
        load_music()

# Refreash music
def load_music():
    global current_music, is_playing, is_paused, current_position, is_completed
    pygame.mixer.music.stop()  # Stop the currently playing music
    rotation_stop_event.set() # Stop the image rotation
    is_completed = False  # Reset the completion flag
    current_music = MP3(music_files[current_music_index])  # Load the new music file
    pygame.mixer.music.load(music_files[current_music_index])  # Load the new music file
    is_playing = False   # Reset the play/pause button to "Play" state
    is_paused = False    # Reset the play/pause button to "Play" state
    play_pause_button.config(image=play_image)
    duration_label.config(text="00:00/" + format_time(current_music.info.length))   # Update the duration label
    current_position = 0   # Reset current position
    reset_progress_bar()  # Reset the progress bar
    file_name_without_extension = os.path.splitext(os.path.basename(music_files[current_music_index]))[0]   # Update the song name label
    song_name_label.config(text=file_name_without_extension)   # Update the song name label


# Create a label to display music duration with initial text
current_music = MP3(music_files[0])  # Load the first music file
initial_duration_text = "00:00/{}".format(format_time(current_music.info.length))
duration_label = Label(root, text=initial_duration_text)
duration_label.pack()

# Create previous and next buttons
previous_button = ttk.Button(button_frame, image=backward_image, style="TButton", command=previous_song)
previous_button.grid(row=0, column=0, padx=10)

next_button = ttk.Button(button_frame, image=forward_image, style="TButton", command=next_song)
next_button.grid(row=0, column=4, padx=10)

# Start updating the progress bar
update_progress_bar()

# Load the initial music
load_music()

# Center the window
center_window(root)

# Start the Tkinter event loop
root.mainloop()
