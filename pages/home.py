import tkinter as tk
from tkinter import ttk
from tkinter import font
from login import LoginFrame
from tkinter import PhotoImage, END, CENTER

# Main class
class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Home")
        # set initial size of window
        self.geometry("900x600")  
        # make the row expandable 
        self.grid_rowconfigure(0, weight=1) 
        # make the column expandable 
        self.grid_columnconfigure(0, weight=1)
        # initial current frame is none 
        self._frame = None  
        # display HomePage as initial page
        self.switch_frame(HomePage) 
        

    def switch_frame(self, frame_class):
        # Function to switch from current frame to a new frame
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()  
        self._frame = new_frame
        self._frame.grid() 
        self.update_idletasks()  

# HomePage frame class
class HomePage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        # organize widgets in grid style
        self.grid()
        # create the widgets on HomePage  
        self.create_widgets()  
        # set the geometry of the window
        self.master.geometry("900x600+300+50") 


    def create_widgets(self):
        # Display the logo
        self.logo_image = PhotoImage(file='assets/logo.png')
        self.logo_label = tk.Label(self, image=self.logo_image)
        self.logo_label.pack(pady=20)    
    
        # Display welcome message
        self.welcome_label = tk.Label(
            self,
            text="Welcome to my Audio player\nPlease Login To Your Account",
            font=("Arial", 25)
        )
        self.welcome_label.pack(pady=20)
        
        # Create a font
        my_font = font.Font(size=20)
        
        # Define the style for button
        style = ttk.Style()
        style.configure("TButton", font=my_font)

        # Login button
        # Login button
        self.login_button = ttk.Button(
            self, 
        text = "Login", command = self.open_login_window, style = "TButton")
        self.login_button.pack(padx = 50, pady = 30)


    def open_login_window(self):
        # Switch to LoginFrame
        self.master.switch_frame(LoginFrame)  
        self.master.update()
        # update window geometry after switching to LoginFrame  
        self.master.after(0, self.master.geometry, "900x600+300+100")
        

# Main function to run the program
if __name__ == '__main__':
    # create MainApp instance
    app = MainApp()
    # start the application
    app.mainloop()

