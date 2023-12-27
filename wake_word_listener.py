import pvporcupine
import pyaudio
import struct
from visual_indicator import start_indicator, stop_indicator
import command_listener 

def listen_for_wake_word(porcupine, pa, audio_stream):
    print("Listening for the wake word...")

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Jarvis wake word detected!")
            on_wake_word_detected()

def on_wake_word_detected():
    """
    Called when the wake word is detected.
    """
    start_indicator()
    command_listener.listen_for_command()
    stop_indicator()
