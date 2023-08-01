import tkinter as tk
from tkinter import filedialog
import os
import subprocess

# Path to the file list where the file is stored
file_list_path = "main_homepage/upload_page/file_list.txt"
# userdata
userdata_folder = os.path.join(os.getcwd(), "playmusic_page", "userdata")

# Select music files to upload
def browse_files():
    filetypes = [("MP3 files", "*.mp3")]
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if filepath:
        # Save to the userdata subfolder of the upload_page folder
        os.makedirs(userdata_folder, exist_ok=True)
        # Copy the file to the userdata folder
        filename = os.path.basename(filepath)
        destination = os.path.join(userdata_folder, filename)

        try:
            # copy file
            with open(filepath, "rb") as source_file, open(destination, "wb") as destination_file:
                destination_file.write(source_file.read())
            # Change the first letter of the filename to lowercase
            new_filename = filename[0].lower() + filename[1:]
            new_filename.lower()
            new_destination = os.path.join(userdata_folder, new_filename)
            # Rename the file to have the first letter in lowercase
            os.rename(destination, new_destination)
            # Check if a song with the same name already exists in the list
            if new_filename not in song_listbox.get(0, tk.END):
                # Add to song list
                song_listbox.insert(tk.END, new_filename)
            else:
                print("The song is already in the list.")
            # Save the list of updated files
            save_file_list()
        except IOError:
            print("Failed to copy the file.")
    else:
        print("No file selected.")


def update_song_list():
    # Empty song list
    song_listbox.delete(0, tk.END)
    # Reload the song file and add it to the list
    if os.path.exists(userdata_folder) and os.path.isdir(userdata_folder):
        songs = os.listdir(userdata_folder)
        for song in songs:
            song_listbox.insert(tk.END, song)
    # Check if the music list is empty
    if len(songs) > 0:
        play_button.config(state=tk.NORMAL)
    else:
        play_button.config(state=tk.DISABLED)


def save_file_list():
    # Save a list of music files to a file
    songs = song_listbox.get(0, tk.END)
    with open(file_list_path, "w") as file:
        file.write("\n".join(songs))

# Update window size information
def center_window(window):
    window.update_idletasks()  
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


def load_file_list():
    # Load a list of music files from a file
    if os.path.exists(file_list_path):
        with open(file_list_path, "r") as file:
            songs = file.read().splitlines()
            for song in songs:
                song_listbox.insert(tk.END, song)
        # Check if the music list is empty
        if len(songs) > 0:
            play_button.config(state=tk.NORMAL)
        else:
            play_button.config(state=tk.DISABLED)


def play_music_list():
    # Get the song list
    songs = song_listbox.get(0, tk.END)

    if len(songs) > 0:
        # Jump to main.py page
        play_py_path = os.path.join(os.getcwd(), "playmusic_page", "play.py")
        if os.path.exists(play_py_path):
            # Run Play.py
            subprocess.run(["python3", play_py_path, str(6)])
        else:
            print("play_user.py file not found.")
    else:
        print("No songs in the list.")



def open_music_player(genre_index):
    # Open the music player and pass the genre index as a command-line argument
    subprocess.Popen(["python3", "music_player.py", str(genre_index)])




def delete_song():
    # Get selected songs
    selected_song = song_listbox.get(tk.ACTIVE)
    if selected_song:
        # Deleting Song Files
        song_path = os.path.join(userdata_folder, selected_song)
        if os.path.exists(song_path):
            os.remove(song_path)
            print("Deleted song file:", selected_song)
        # Delete the selected song from the list
        song_listbox.delete(tk.ACTIVE)
        # Saving the updated file list
        save_file_list()
    else:
        print("No song selected.")


def open_main_homepage():
    subprocess.run(["python3", "main_homepage/main.py"])
    root.destroy()


def go_back():
    # Return to the previous page (Main Home Page)
    root.withdraw()
    open_main_homepage()



root = tk.Tk()
root.title("Music Uploader")

# Creating the top frame
top_frame = tk.Frame(root, padx=20, pady=20)
top_frame.pack()

# Creating a Back Button
back_button = tk.Button(top_frame, text="Back", command=go_back)
back_button.pack()

# Create Upload Button
upload_button = tk.Button(top_frame, text="Upload Song", command=browse_files)
upload_button.pack()

# Create Delete Button
delete_button = tk.Button(top_frame, text="Delete Song", command=delete_song, state=tk.DISABLED)
delete_button.pack()

def on_song_select(event):
    # Updates the status of the delete button according to the selected song
    selected_song = song_listbox.get(tk.ACTIVE)
    if selected_song:
        delete_button.config(state=tk.NORMAL)
    else:
        delete_button.config(state=tk.DISABLED)

# Creating a Song List Framework
listbox_frame = tk.Frame(root, padx=20, pady=10)
listbox_frame.pack()

# Creating a Song List
song_listbox = tk.Listbox(listbox_frame, width=50)
song_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Creating Scroll Bars
scrollbar = tk.Scrollbar(listbox_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Binding scrollbars and song lists
song_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=song_listbox.yview)

# Bind the selected song event
song_listbox.bind("<<ListboxSelect>>", on_song_select)

# Creating the Play Button Framework
play_button_frame = tk.Frame(root, padx=20, pady=20)
play_button_frame.pack()

# Creating a Play Button
play_button = tk.Button(play_button_frame, text="Play Music List", command=play_music_list, state=tk.DISABLED)
play_button.pack()

# Load Music File List
load_file_list()

# Update Song List
update_song_list()

# Center the window
center_window(root)

root.mainloop()
