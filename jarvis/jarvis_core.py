import sys
import threading
import pvporcupine
import pyaudio
from jarvis.components.wake_word_listener import listen_for_wake_word
from jarvis.components.speech_output import set_update_gui_function, set_toggle_gui_function
from jarvis.components.command_listener import set_update_gui_function as set_command_listener_gui_function

class JarvisCore:
    def __init__(self, access_key):
        self.access_key = access_key
        self.is_running = True

    def run(self):
        self.is_running = True
        while self.is_running:
            try:
                porcupine = pvporcupine.create(access_key=self.access_key, keywords=["jarvis"])
                pa = pyaudio.PyAudio()
                audio_stream = pa.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length
                )
                if self.is_running:
                    listen_for_wake_word(porcupine, pa, audio_stream, lambda: self.is_running)

            finally:
                if porcupine is not None:
                    porcupine.delete()
                if audio_stream is not None:
                    audio_stream.close()
                if pa is not None:
                    pa.terminate()

    def stop(self):
        self.is_running = False

if __name__ == "__main__":
    ACCESS_KEY = 'DZzwIYi6/ckJ66kdntAOPfjmzl9iLhYJChPDMOvMaTaeFQMEcIWtHQ=='
    jarvis_core = JarvisCore(ACCESS_KEY)
    threading.Thread(target=jarvis_core.run, daemon=True).start()
