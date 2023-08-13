import tkinter as tk

# Create a Tkinter window
root = tk.Tk()
root.title("About Me") 

# Set window size
window_width = 800
window_height = 400
root.geometry(f"{window_width}x{window_height}")

# Read the user name file
try:
    with open("username.txt", "r") as f:
        username = f.read().strip()
except FileNotFoundError:
    username = "Unknown"


def center_window(window):
    # Update the size information of the window
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Class for the Me page
class MePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()


    def create_widgets(self):
        # User name tag
        username_label = tk.Label(self, text="Username：", font=("Arial", 16))
        username_label.pack(pady = 20)

        # User name display
        username_text = tk.StringVar()
        username_text.set(username)
        username_display = tk.Label(self, textvariable = username_text, font = ("Arial", 16, "bold"))
        username_display.pack()

        # Software usage description title
        intro_label = tk.Label(
            self,
            text = "Important notice while using the app",
            font = ("Arial", 18, "underline")
        )

        intro_label.pack(pady=20)

        # Software usage introduction text
        intro_text = """
        This is a simple music player software.
        It can play various music genres such as rock, pop, jazz, etc. And some of the genres are built - in.
        You can also upload the music you want to play through the built - in local music button 
        This program supports uploading MP3 / MP4 / WAV / FLAC / CD/New format total six types music at present.
        You can also use the player's interface to include the basic features that a full music player would have 
        I hope you enjoy using this music player!
        """
        intro_display = tk.Label(self, text = intro_text, font = ("Arial", 14))
        intro_display.pack()

# Create an instance of the MePage class and pack it
me_page = MePage(root)
me_page.pack(fill = tk.BOTH, expand = True)

# Center the window
center_window(root)

# Run the Tkinter event loop
root.mainloop()
