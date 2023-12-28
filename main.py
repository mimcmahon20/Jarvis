import sys
import threading
from wake_word_listener import listen_for_wake_word
from speech_output import cleanup_speech_threads
import visual_indicator  # Import the modified visual_indicator module
import pvporcupine
import pyaudio

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
            cleanup_speech_threads()
    
   


def check_for_exit():
    if not is_running:
        visual_indicator.stop_mainloop()  # This will exit the Tkinter main loop


def main():
    global is_running

    def on_closing():
        global is_running
        is_running = False  # This will signal the Jarvis thread to stop

    # Start Jarvis logic in a separate thread
    jarvis_thread = threading.Thread(target=run_jarvis, daemon=True)
    jarvis_thread.start()

    # Setup Tkinter mainloop and exit checking
    visual_indicator.root.protocol("WM_DELETE_WINDOW", on_closing)
    visual_indicator.root.after(100, check_for_exit)  # Check every 100 ms
    visual_indicator.start_mainloop()

    on_closing()  # Ensure Jarvis stops if the Tkinter window is closed

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        is_running = False