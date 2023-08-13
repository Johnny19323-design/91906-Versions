import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import shutil
from pydub import AudioSegment
from tkinter import filedialog
from tkinter import messagebox

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

        # Construct the user folder path by adding the username to the user data folder path
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
        
    # Return to the previous page (Main Home Page)
    def go_back(self):       
        self.withdraw()
        self.open_main_homepage()
    
    # Define acceptable file types and corresponding file extensions
    def browse_files(self):   
        filetypes = [("MP3 files", "*.mp3"), ("MP4 files", "*.mp4"), ("WAV files", "*.wav"), ("FLAC files", "*.flac"), ("CD files", "*.cd"), ("New format", "*.ext")]
        filepath = filedialog.askopenfilename(filetypes=filetypes)
        
        # Ensure a valid file was selected
        if filepath:
            audio = AudioSegment.from_file(filepath)
            # Convert the filename to lowercase
            filename = os.path.basename(filepath)
            filename_lower = filename.lower()
            # Update the file extension to .mp3
            filename_lower = os.path.splitext(filename_lower)[0] + ".mp3"
            # Construct the new file path
            mp3_filepath = os.path.join(os.path.dirname(filepath), filename_lower)
            # Export to MP3
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
                        messagebox.showinfo("Alert")

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
            
    # Save a list of music files to a file
    def save_file_list(self):
        songs = self.song_listbox.get(0, tk.END)
        with open(self.file_list_path, "w") as file:
            file.write("\n".join(songs))
    
    # Set window to center
    def center_window(self):
        self.update_idletasks()  
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")
        
    # Load a list of music files from a file
    def load_file_list(self):
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
                
    # Get the song list
    def play_music_list(self):
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
            
    # Open the music player and pass the genre index as a command-line argument
    def open_music_player(self, genre_index):
        subprocess.Popen(["python3", "music_player.py", str(genre_index)])
        
    # Get data store file
    def delete_song(self):
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
        
    # Open Main home page
    def open_main_homepage(self):
        subprocess.run(["python3", "pages/main.py"])
        self.destroy()
        
    # Updates the status of the delete button according to the selected song
    def on_song_select(self, event):
        selected_song = self.song_listbox.get(tk.ACTIVE)
        if selected_song:
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)

# Create the root Tk object
if __name__ == "__main__":
    root = UploadPage()
    root.mainloop()
