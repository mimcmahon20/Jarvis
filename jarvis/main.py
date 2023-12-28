import sys
import threading
from wake_word_listener import listen_for_wake_word
from speech_output import cleanup_speech_threads
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

if __name__ == "__main__":
    try:
        run_jarvis()
    except KeyboardInterrupt:
        is_running = False