import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import shutil
from pydub import AudioSegment
from tkinter import filedialog


# Class for the Upload page
class UploadPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Uploader")

        # Path to the file list where the file is stored
        self.file_list_path = "file_list.txt"
        # userdata
        self.userdata_folder = os.path.join(os.getcwd(), "playmusic_page", "userdata")

        # Creating the top frame
        top_frame = tk.Frame(self, padx=20, pady=20)
        top_frame.pack()
        
        # Create user folder
        username_file_path = "username.txt"
        if os.path.exists(username_file_path):
            with open(username_file_path, "r") as username_file:
                username = username_file.read().strip().lower()
        else:
            print("Username file not found.")
            return

        user_folder = os.path.join(self.userdata_folder, username)
        os.makedirs(user_folder, exist_ok=True)

        # Creating a Back Button
        back_button = tk.Button(top_frame, text="Back", command=self.go_back)
        back_button.pack()

        # Create Upload Button
        upload_button = tk.Button(top_frame, text="Upload Song", command=self.browse_files)
        upload_button.pack()

        # Create Delete Button
        self.delete_button = tk.Button(top_frame, text="Delete Song", command=self.delete_song, state=tk.DISABLED)
        self.delete_button.pack()

        # Creating the Song List Framework
        listbox_frame = tk.Frame(self, padx=20, pady=10)
        listbox_frame.pack()

        # Creating a Song List
        self.song_listbox = tk.Listbox(listbox_frame, width=50)
        self.song_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

        # Creating Scroll Bars
        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Binding scrollbars and song lists
        self.song_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.song_listbox.yview)

        # Bind the selected song event
        self.song_listbox.bind("<<ListboxSelect>>", self.on_song_select)

        # Creating the Play Button Framework
        play_button_frame = tk.Frame(self, padx=20, pady=20)
        play_button_frame.pack()

        # Creating a Play Button
        self.play_button = tk.Button(play_button_frame, text="Play Music List", command=self.play_music_list, state=tk.DISABLED)
        self.play_button.pack()

        # Load Music File List
        self.load_file_list()

        # Update Song List
        self.update_song_list()

        # Center the window
        self.center_window()

    def go_back(self):
        # Return to the previous page (Main Home Page)
        self.withdraw()
        self.open_main_homepage()

    def browse_files(self):   
        filetypes = [("MP3 files", "*.mp3"), ("MP4 files", "*.mp4"), ("WAV files", "*.wav"), ("FLAC files", "*.flac"), ("CD files", "*.cd"), ("New format", "*.ext")]
        #filetypes = [("Music files", "*.mp3;*.wav;*.flac;*.aac;*.ogg;*.aiff;*.wma;*.cd;*.mp4")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        
        # Ensure a valid file was selected
        if filepath:
            audio = AudioSegment.from_file(filepath)
            # Export to MP3
            mp3_filepath = os.path.splitext(filepath)[0] + ".mp3"
            audio.export(mp3_filepath, format="mp3")
            
            if filepath:
                # Read username from username.txt file
                username_file_path = "username.txt"
                if os.path.exists(username_file_path):
                    with open(username_file_path, "r") as username_file:
                        username = username_file.read().strip().lower()
                else:
                    print("Username file not found.")
                    return

                # Create a folder with the username
                user_folder = os.path.join(self.userdata_folder, username)
                os.makedirs(user_folder, exist_ok=True)

                # Copy the file to the user folder
                filename = os.path.basename(mp3_filepath)  # Update filename to the converted MP3 file
                destination = os.path.join(user_folder, filename)  # Update destination to the converted MP3 file

                try:
                    # Copy file
                    shutil.copy2(mp3_filepath, destination)  # Copy the converted MP3 file

                    # Check if a song with the same name already exists in the list
                    if filename not in self.song_listbox.get(0, tk.END):
                        # Add to song list
                        self.song_listbox.insert(tk.END, filename)
                    else:
                        print("The song is already in the list.")

                    # Save the list of updated files
                    self.save_file_list()
                    # Update the song list and button state
                    self.update_song_list()
                except IOError:
                    print("Failed to copy the file.")
        else:
            print("No file selected.")


    def update_song_list(self):
        # Empty song list
        self.song_listbox.delete(0, tk.END)
        # Reload the song file and add it to the list
        with open('username.txt', 'r') as file:
            username = file.readline().strip()
        user_folder = os.path.join(self.userdata_folder, username)
        if os.path.exists(user_folder) and os.path.isdir(user_folder):
            songs = os.listdir(user_folder)
            for song in songs:
                self.song_listbox.insert(tk.END, song)
        # Check if the music list is empty
        if len(songs) > 0:
            self.play_button.config(state=tk.NORMAL)
        else:
            self.play_button.config(state=tk.DISABLED)

    def save_file_list(self):
        # Save a list of music files to a file
        songs = self.song_listbox.get(0, tk.END)
        with open(self.file_list_path, "w") as file:
            file.write("\n".join(songs))

    def center_window(self):
        self.update_idletasks()  
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def load_file_list(self):
        # Load a list of music files from a file
        if os.path.exists(self.file_list_path):
            with open(self.file_list_path, "r") as file:
                songs = file.read().splitlines()
                for song in songs:
                    self.song_listbox.insert(tk.END, song)
            # Check if the music list is empty
            if len(songs) > 0:
                self.play_button.config(state=tk.NORMAL)
            else:
                self.play_button.config(state=tk.DISABLED)

    def play_music_list(self):
        # Get the song list
        songs = self.song_listbox.get(0, tk.END)

        if len(songs) > 0:
            # Jump to play.py page
            play_py_path = os.path.join(os.getcwd(), "playmusic_page", "play.py")
            if os.path.exists(play_py_path):
                # Run Play.py
                subprocess.run(["python3", play_py_path, str(6)])
            else:
                print("play_user.py file not found.")
        else:
            print("No songs in the list.")

    def open_music_player(self, genre_index):
        # Open the music player and pass the genre index as a command-line argument
        subprocess.Popen(["python3", "music_player.py", str(genre_index)])

    def delete_song(self):
        # Get data store file
        with open('username.txt', 'r') as file:
            username = file.readline().strip()
        # Get selected songs
        selected_song = self.song_listbox.get(tk.ACTIVE)
        if selected_song:
            # Deleting Song Files
            song_path = os.path.join(self.userdata_folder, username, selected_song)
            if os.path.exists(song_path):
                os.remove(song_path)
                print("Deleted song file:", selected_song)
            # Delete the selected song from the list
            self.song_listbox.delete(tk.ACTIVE)
            # Saving the updated file list
            self.save_file_list()
            self.update_song_list()
        else:
            print("No song selected.")

    def open_main_homepage(self):
        subprocess.run(["python3", "pages/main.py"])
        self.destroy()

    def on_song_select(self, event):
        # Updates the status of the delete button according to the selected song
        selected_song = self.song_listbox.get(tk.ACTIVE)
        if selected_song:
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = UploadPage()
    root.mainloop()
