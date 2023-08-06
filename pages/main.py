import tkinter as tk
from PIL import Image, ImageTk, ImageDraw
import subprocess
from tkinter import messagebox

class MusicPlayerApp(tk.Frame):
    def __init__(self, root):
        self.root = root
        self.genres = ["rock", "pop", "jazz", "classical", "hip_hop", "country"]
        self.genre_images = {
            "rock": "assets/rock.jpg",
            "pop": "assets/pop.jpg",
            "jazz": "assets/jazz.jpg",
            "classical": "assets/classical.jpg",
            "hip_hop": "assets/hip_hop.jpg",
            "country": "assets/country.jpeg"
        }

        # Create a dictionary to store image objects
        self.genre_image_objects = {}
        self.local_music_image = None
        self.important_notice_image = None

        self.setup_ui()

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def open_music_player(self, genre_index):
        subprocess.Popen(["python3", "playmusic_page/play.py", str(genre_index)])

    def open_link(self, event):
        selected_genre = event.widget.cget("text")
        print("Opening link for genre:", selected_genre)

    def open_local_music(self):
        subprocess.Popen(["python3", "pages/uploadpage.py"])
        self.root.destroy()

    def destroy_root(self):
        self.root.destroy()

    def crop_to_circle(self, image):
        mask = Image.new("L", image.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        width, height = image.size
        mask_draw.ellipse((0, 0, width, height), fill=255)

        # Apply the circular mask to the image
        result = Image.new("RGBA", image.size)
        result.paste(image, mask=mask)
        return result

    def open_me_page(self):
        subprocess.Popen(["python3", "pages/me.py"])

    def load_images(self):
        for genre in self.genres:
            image = Image.open(self.genre_images[genre])
            image = image.resize((200, 200), Image.LANCZOS)
            cropped_image = self.crop_to_circle(image)
            self.genre_image_objects[genre] = ImageTk.PhotoImage(cropped_image)

        # Load images for the bottom buttons
        self.local_music_image = ImageTk.PhotoImage(Image.open("assets/local.png"))
        self.important_notice_image = ImageTk.PhotoImage(Image.open("assets/user.png"))

    def setup_ui(self):
        self.root.title("Music Player")
        self.load_images()

        # Create a frame for the genre labels
        genre_frame = tk.Frame(self.root)
        genre_frame.pack(side=tk.TOP, padx=10, pady=(10, 40))  # Increased the vertical padding

        # Create genre labels with separate images
        for i, genre in enumerate(self.genres):
            row = i // 3
            column = i % 3

            # Load the background image for the genre
            image = self.genre_image_objects[genre]  # Use the corresponding image for each genre

            # Create a frame to hold the image and label
            frame = tk.Frame(genre_frame)
            frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

            # Create a label with circular background image
            label = tk.Label(frame, image=image, cursor="hand2", bd=0)  # Set bd to 0 to remove border
            label.image = image  # Keep a reference to the image to prevent garbage collection
            label.pack()

            # Create a label for the genre text
            text_label = tk.Label(frame, text=genre, font=("Arial", 12, "underline"), fg="blue", cursor="hand2")
            text_label.pack()

            label.bind("<Button-1>", lambda event, index=i: self.open_music_player(index))
            text_label.bind("<Button-1>", lambda event, index=i: self.open_music_player(index))

        # Create a bottom frame for the menu
        bottom_frame = tk.Frame(self.root, bg="gray")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Load the images for the buttons
        local_music_image = ImageTk.PhotoImage(Image.open("assets/local.png"))
        important_notice_image = ImageTk.PhotoImage(Image.open("assets/user.png"))

         # Create buttons in the bottom frame with images and without border
        local_music_button = tk.Button(bottom_frame, image=self.local_music_image, bd=0, command=self.open_local_music)
        local_music_button.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")  # Set sticky to "nsew"

        important_notice_button = tk.Button(bottom_frame, image=self.important_notice_image, bd=0, command=self.open_me_page)
        important_notice_button.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")  # Set sticky to "nsew"

        # Configure bottom_frame to expand with window size
        bottom_frame.grid_columnconfigure(0, weight=1)  # Make first column expandable
        bottom_frame.grid_columnconfigure(1, weight=1)  # Make second column expandable

        # Configure root to expand with window size
        self.root.grid_rowconfigure(0, weight=1)  # Make first row expandable
        self.root.grid_columnconfigure(0, weight=1)  # Make first column expandable

        # Bind the closing event of uploadpage.py window to destroy_root
        self.root.protocol("WM_DELETE_WINDOW", self.destroy_root)

        # Center the window
        self.center_window()

# Add a message box at the beginning
messagebox.showinfo("Welcome", "Welcome to the Music Player!")

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()




