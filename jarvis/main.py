import sys
import threading
from wake_word_listener import listen_for_wake_word
import pvporcupine
import pyaudio
import tkinter as tk
from visual_indicator import VisualIndicator
from threading import Thread
import speech_output
import wake_word_listener
import command_listener

# Create the visual indicator instance
indicator = VisualIndicator()

ACCESS_KEY = 'DZzwIYi6/ckJ66kdntAOPfjmzl9iLhYJChPDMOvMaTaeFQMEcIWtHQ=='

is_running = True

def run_jarvis():
    global is_running
    porcupine = None
    pa = None
    audio_stream = None
   

    while(is_running):
        try:
            porcupine = pvporcupine.create(access_key=ACCESS_KEY, keywords=["jarvis"])
            pa = pyaudio.PyAudio()
            audio_stream = pa.open(
                rate=porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=porcupine.frame_length
            )

            listen_for_wake_word(porcupine, pa, audio_stream)

        finally: 
            if porcupine is not None:
                porcupine.delete()
            if audio_stream is not None:
                audio_stream.close()
            if pa is not None:
                pa.terminate()


def update_gui(mode):
    # This function updates the GUI in a thread-safe manner.
    def change_mode():
        indicator.change_mode(mode)
        indicator.show() if mode != 'hide' else indicator.hide()

    indicator.root.after(0, change_mode)

speech_output.set_update_gui_function(update_gui)
command_listener.set_update_gui_function(update_gui)



def toggle_gui():
    if indicator.root.state() == 'normal':
        indicator.hide()
    else:
        indicator.show()

speech_output.set_toggle_gui_function(toggle_gui)
wake_word_listener.set_toggle_gui_function(toggle_gui)

def exit_jarvis():
    global is_running
    is_running = False
    sys.exit()


if __name__ == "__main__":
    try:
        #Start the main application function in a separate thread
        Thread(target=run_jarvis, daemon=True).start()

        # Run the Tkinter main loop in the main thread
        indicator.root.mainloop()
        toggle_gui()
    except KeyboardInterrupt:
        is_running = False
        sys.exit()