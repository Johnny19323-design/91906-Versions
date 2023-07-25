import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import subprocess
from tkinter import messagebox

# Add a message box at the beginning
messagebox.showinfo("Welcome", "Welcome to the Music Player!")

# Update window size information
def center_window(window):
    window.update_idletasks()  
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Get the selected genre from the label text
def open_link(event):
    selected_genre = event.widget.cget("text")
    print("Opening link for genre:", selected_genre)

# Open the local music GUI program
def open_local_music():
    subprocess.Popen(["python3", "main_homepage/upload_page/uploadpage.py"])
    root.destroy()

# Create a circular mask
def crop_to_circle(image):
    mask = Image.new("L", image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    width, height = image.size
    mask_draw.ellipse((0, 0, width, height), fill=255)

    # Apply the circular mask to the image
    result = Image.new("RGBA", image.size)
    result.paste(image, mask=mask)
    return result

# Destroy the root window
def destroy_root():
    root.destroy()

# List of genres
genres = ["Rock", "Pop", "Jazz", "Classical", "Hip_Hop", "Country"]

def open_music_player(genre_index):
    # Open the music player and pass the genre index as a command-line argument
    subprocess.Popen(["python3", "music_player.py", str(genre_index)])

#Create title
root = tk.Tk()
root.title("Music Player")


# Create a frame for the genre labels
genre_frame = tk.Frame(root)
genre_frame.pack(side=tk.TOP, padx=10, pady=(10, 40))  # Increased the vertical padding

# Create genre labels
selected_genre_var = tk.StringVar()

for i, genre in enumerate(genres):
    row = i // 3
    column = i % 3
    
    # Load the background image at a higher resolution
    image = Image.open("main_homepage/assets/classical.jpg")  # Replace with the actual path to your background image
    image = image.resize((200, 200), Image.LANCZOS)  # Adjust the size and resampling method as needed
    cropped_image = crop_to_circle(image)
    background_image = ImageTk.PhotoImage(cropped_image)
    
    # Create a frame to hold the image and label
    frame = tk.Frame(genre_frame)
    frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")
    
    # Create a label with circular background image
    label = tk.Label(frame, image=background_image, cursor="hand2", bd=0)  # Set bd to 0 to remove border
    label.image = background_image  # Keep a reference to the image to prevent garbage collection
    label.pack()
    
    # Create a label for the genre text
    text_label = tk.Label(frame, text=genre, font=("Arial", 12, "underline"), fg="blue", cursor="hand2")
    text_label.pack()
    
    def open_music_player(event, index=i):
        # Open the music player and pass the genre index as a command-line argument
        subprocess.Popen(["python3", "playmusic_page/play.py", str(index)])
    
    label.bind("<Button-1>", open_music_player)
    text_label.bind("<Button-1>", open_music_player)


# Create a bottom frame for the menu
bottom_frame = tk.Frame(root, bg="gray")
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Load the images for the buttons
local_music_image = ImageTk.PhotoImage(Image.open("main_homepage/assets/local.png"))
important_notice_image = ImageTk.PhotoImage(Image.open("main_homepage/assets/user.png"))

# Create buttons in the bottom frame with images and without border
local_music_button = tk.Button(bottom_frame, image=local_music_image, bd=0, command=open_local_music)
local_music_button.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")  # Set sticky to "nsew"

def open_me_page():
    # Open the Me page
    subprocess.Popen(["python3", "main_homepage/me_page/me.py"])

important_notice_button = tk.Button(bottom_frame, image=important_notice_image, bd=0, command=open_me_page)
important_notice_button.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")  # Set sticky to "nsew"

# Configure bottom_frame to expand with window size
bottom_frame.grid_columnconfigure(0, weight=1)  # Make first column expandable
bottom_frame.grid_columnconfigure(1, weight=1)  # Make second column expandable

# Configure root to expand with window size
root.grid_rowconfigure(0, weight=1)  # Make first row expandable
root.grid_columnconfigure(0, weight=1)  # Make first column expandable

# Bind the closing event of uploadpage.py window to destroy_root
root.protocol("WM_DELETE_WINDOW", destroy_root)

# 将窗口居中显示
center_window(root)

root.mainloop()
