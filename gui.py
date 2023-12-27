import tkinter as tk
import subprocess

def toggle_jarvis():
    global jarvis_on
    global jarvis_process
    if jarvis_on:
        # Stop Jarvis
        subprocess.run(["python", "main.py", "--stop"])
        jarvis_on = False
        button.config(text="Start Jarvis")
    else:
        # Start Jarvis
        jarvis_process = subprocess.Popen(["python", "main.py"])
        jarvis_on = True
        button.config(text="Stop Jarvis")

# Initialize the state of Jarvis
jarvis_on = False
jarvis_process = None

# Create the main window
root = tk.Tk()

# Create a button
button = tk.Button(root, text="Start Jarvis", command=toggle_jarvis)

# Add the button to the window
button.pack()

# Start the event loop
root.mainloop()