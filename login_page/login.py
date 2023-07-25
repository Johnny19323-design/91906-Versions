import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import json
from PIL import Image, ImageTk
import uuid
import subprocess

# RegisterFrame is a child of tk.Toplevel
class RegisterFrame(tk.Toplevel):
    def __init__(self, login_frame, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Register")
        self.geometry("350x300+560+300")
        self.login_frame = login_frame 

        # Create widgets when the frame is initialized
        self.create_widgets()

    def create_widgets(self):
        # Create and set the position of username label
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Create and set the position of username entry
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # Create and set the position of password label
        self.password_label = tk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Create and set the position of password entry
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="e")
        
        # Add a label to display password creation conditions
        self.password_condition_label = tk.Label(self, text="Password conditions: \n✦ Password must start with an uppercase letter\n✦ Password must be atleast 8 characters long!\n✦ Password must contain both letters and numbers")
        self.password_condition_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

        # Create and set the position of register button
        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=20)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Generate a unique user ID
        uid = str(uuid.uuid4())

        # Show an error if the username or password is only whitespace
        if not username.strip() or not password.strip():
            messagebox.showerror("Wrong", "Password or Username cannot only be space!")
        
        # Show an error if the username already exists
        elif username in self.login_frame.user_data:
            messagebox.showerror("Error", "This user name already Registed!")

        # Check password creation conditions
        elif not password[0].isupper():
            messagebox.showerror("Error", "Password must start with an uppercase letter!")
        
        elif len(password) <= 7:
            messagebox.showerror("Error", "Password must be atleast 8 characters long!")

        elif not any(char.isalpha() for char in password) or not any(char.isdigit() for char in password):
            messagebox.showerror("Error", "Password must contain both letters and numbers!")

        else:
            # Add the username, password, and UID to the user data
            self.login_frame.user_data[username] = {"password": password, "uid": uid}
            # Save the user data
            self.login_frame.save_user_data()
            messagebox.showinfo("Congratulation", "Registered successfully!")
            print(f"Registered successfully: Username={username}, Password={password}, UID={uid}")
            self.destroy()


    def register_success(self):
        # Call the login_success method of the login_frame
        self.login_frame.login_success()

# LoginFrame is a child of tk.Frame
class LoginFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Login")
        self.grid(row=0, column=0, sticky="nsew")

        # Load and display the background image
        self.bg_image = Image.open("assets/background.jpeg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Load and display the center background image
        self.center_image = Image.open("assets/background.jpeg")
        self.center_photo = ImageTk.PhotoImage(self.center_image)

        # Create widgets when the frame is initialized
        self.create_widgets()
        # Load user data when the frame is initialized
        self.load_user_data()


    # Load and display the background image
    def create_widgets(self):
        bg_image = Image.open("assets/background.jpeg")
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        self.background_label = tk.Label(self, image=self.bg_photo)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Create a new transparent frame in the center of the window
        self.center_frame = tk.Frame(self, bg="")
        self.center_frame.place(relx=0.5, rely=0.5, anchor='c')

        # Create frames for username, password and buttons
        self.username_frame = tk.Frame(self.center_frame)
        self.username_frame.pack(pady=5)
        self.password_frame = tk.Frame(self.center_frame)
        self.password_frame.pack(pady=5)
        self.buttons_frame = tk.Frame(self.center_frame)
        self.buttons_frame.pack(pady=5)

        # Create and place the username label and entry
        self.username_label = tk.Label(self.username_frame, text="Username:", width=10, anchor='w')
        self.username_label.pack(side="left")
        self.username_entry = tk.Entry(self.username_frame)
        self.username_entry.pack(side="left", fill="x", expand=True)

        # Create and place the password label and entry
        self.password_label = tk.Label(self.password_frame, text="Password:", width=10, anchor='w')
        self.password_label.pack(side="left")
        self.password_entry = tk.Entry(self.password_frame, show="*")
        self.password_entry.pack(side="left", fill="x", expand=True)

        # Create and place the login and register buttons
        self.login_button = ttk.Button(self.buttons_frame, text="Login", command=self.login, width=50, style="TButton")
        self.login_button.pack(pady=20)
        self.register_button = ttk.Button(self.buttons_frame, text="Register", command=self.open_register_window, width=50, style="TButton")
        self.register_button.pack(pady=0)

    # Load user data from the json file, if it exists
    def load_user_data(self):
        try:
            with open("login_page/user_data.json", "r") as f:
                self.user_data = json.load(f)
        except FileNotFoundError:
            self.user_data = {}

    # Save user data to the json file
    def save_user_data(self):
        with open("login_page/user_data.json", "w") as f:
            json.dump(self.user_data, f)

    # Get username and password input
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Show an error if the username or password is only whitespace
        if not username.strip() or not password.strip():
            messagebox.showerror("Error", "Account or Password!")
        else:
            # Show a success message if the login is correct, otherwise show an error
            if username in self.user_data and self.user_data[username]["password"] == password:
                # Save the user name to the file after successful login
                with open("login_page/username.txt", "w") as f:
                    f.write(username)
                messagebox.showinfo("Congratulation", "Login succeed")
                print(f"Login successfully: Username={username}, Password={password}")
                self.master.withdraw()
                self.open_main_page(username)
                root.destroy()
               
            else:
                messagebox.showerror("Error", "Incorrect Account or Password!")

    # Open the RegisterFrame and pass the reference of LoginFrame
    def open_register_window(self):
        RegisterFrame(self, self.master)

     # Jump to the main page and pass the user name
    def open_main_page(self, username):
        self.master.withdraw()  
        subprocess.run(["python3", "main_homepage/main.py", username])

    # After successful login, go to the main page
    def login_success(self):
        self.master.withdraw() 
        self.open_main_page()

# Create the root Tk object, set the size, and make it responsive to window resizing
if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("900x600+300+125")
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    app = LoginFrame(master=root)
    app.mainloop()
