import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread, Event
import time

class VisualIndicator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # No window border/decorations
        self.root.attributes('-topmost', True)  # Keep on top
        #make background black
        self.root.configure(background='black')

        # Set up images
        self.original_thinking_image = Image.open('thinking.png').resize((500, 500))
        self.images = {
            'listening': ImageTk.PhotoImage(Image.open('listening.png').resize((500, 500))),
            'thinking': ImageTk.PhotoImage(self.original_thinking_image),
            'talking': ImageTk.PhotoImage(Image.open('talking.png').resize((500, 500)))
        }
        self.label = tk.Label(self.root, image=self.images['listening'], background='black')
        self.label.pack()

        # Center the window at the top of the screen
        ws = self.root.winfo_screenwidth()
        self.root.geometry(f'500x500+{ws//2-50}+0')
        # Setting window size and position
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws // 2) - (500 // 2)
        y = (hs // 2) - (500 // 2)
        self.root.geometry(f'500x500+{x}+{y}')

        # Set window opacity to 90%
        self.root.attributes("-alpha", 0.1)
        
        self.root.withdraw()
        self.current_mode = 'listening'
        self.rotate_event = Event()
        self.rotate_thread = Thread(target=self.rotate_thinking_image)


    def show(self):
        self.root.deiconify()
        if self.current_mode == 'thinking':
            self.rotate_event.set()
            if not self.rotate_thread.is_alive():
                self.rotate_thread.start()

    def hide(self):
        self.root.withdraw()
        self.rotate_event.clear()

    def change_mode(self, mode):
        self.current_mode = mode
        self.label.config(image=self.images[mode])
        if mode == 'thinking':
            self.rotate_event.set()
            if not self.rotate_thread.is_alive():
                self.rotate_thread = Thread(target=self.rotate_thinking_image)
                self.rotate_thread.start()
        else:
            self.rotate_event.clear()
            self.current_mode = mode
            self.label.config(image=self.images[mode])
        

    def rotate_thinking_image(self):
        while self.rotate_event.is_set():
            for angle in range(0, 180, 20):  # Rotate the image in 10 steps (36 degrees each)
                if self.current_mode != 'thinking':
                    return
                rotated_image = ImageTk.PhotoImage(self.original_thinking_image.rotate(angle))
                self.label.config(image=rotated_image)
                self.label.image = rotated_image  # Prevent garbage collection
                time.sleep(0.1)  # Time for each rotation step (total rotation time = 1 second)

    def start(self):
        Thread(target=self.root.mainloop, daemon=True).start()

# Usage
# indicator = VisualIndicator()
# indicator.start()  # Start the visual indicator thread

# # Example of changing modes
# indicator.change_mode('thinking')  # Change to thinking mode
# indicator.show()  # Show the indicator
