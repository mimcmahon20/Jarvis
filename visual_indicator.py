import tkinter as tk
from threading import Thread

class IndicatorWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.overrideredirect(True)  # Remove window decorations
        self.root.attributes("-topmost", True)  # Keep on top
        self.root.geometry("+{}+{}".format(self.root.winfo_screenwidth() - 100, 50))  # Position
        self.canvas = tk.Canvas(self.root, height=50, width=50, bg="blue", highlightthickness=0)
        self.canvas.pack()

    def show(self):
        self.root.deiconify()
        self.root.mainloop()

    def hide(self):
        self.root.withdraw()

indicator = None

def show_indicator():
    global indicator
    indicator = IndicatorWindow()
    indicator.show()

def hide_indicator():
    global indicator
    if indicator:
        indicator.hide()

# Example usage in a separate thread
def start_indicator():
    Thread(target=show_indicator).start()

def stop_indicator():
    Thread(target=hide_indicator).start()
