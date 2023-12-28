# visual_indicator.py
import tkinter as tk
from tkinter import PhotoImage
import os

class IndicatorWindow:
    def __init__(self, root):
        self.root = root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.faceTalkingImg = PhotoImage(file=os.path.join(current_dir, "faceTalking.png"))
        self.faceListeningImg = PhotoImage(file=os.path.join(current_dir, "faceListening.png"))

        self.label = tk.Label(root, image=self.faceListeningImg)
        self.label.pack()
        self.hide()
    def update_to_talking(self):
        self.label.config(image=self.faceTalkingImg)

    def update_to_listening(self):
        self.label.config(image=self.faceListeningImg)

    def show(self):
        self.root.deiconify()  # Show the window

    def hide(self):
        self.root.withdraw()  # Hide the window

# Global instance of IndicatorWindow
root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
indicator_window = IndicatorWindow(root)

def show_talking():
    root.after(0, indicator_window.show)
    root.after(0, indicator_window.update_to_talking)

def show_listening():
    root.after(0, indicator_window.show)
    root.after(0, indicator_window.update_to_listening)

def hide():
    root.after(0, indicator_window.hide)

def start_mainloop():
    root.mainloop()

def stop_mainloop():
    root.quit()
