import pvporcupine
import pyaudio
import struct
import os
import platform
import winsound
import jarvis.components.command_listener as command_listener

_toggle_gui = None

def set_toggle_gui_function(func):
    global _toggle_gui
    _toggle_gui = func

def listen_for_wake_word(porcupine, pa, audio_stream, is_running):
    print("Listening for the wake word...")

    while is_running():
        pcm = audio_stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm)

        if keyword_index >= 0:
            print("Jarvis wake word detected!")
            on_wake_word_detected()
            break # Exit the loop to stop listening for the wake word

def on_wake_word_detected():
    """
    Called when the wake word is detected.
    """
    # Play a beep sound
    if platform.system() == "Windows":
        total_duration = 300  # Total duration in ms
        min_frequency = 200  # Minimum frequency in Hz
        max_frequency = 500  # Maximum frequency in Hz
        num_steps = 4  # Number of frequency steps

        for i in range(num_steps):
            frequency = min_frequency + i * (max_frequency - min_frequency) / num_steps
            duration = total_duration / num_steps
            winsound.Beep(int(frequency), int(duration))
    else:
        duration = 0.05  # Duration in seconds for Unix systems
        for frequency in range(20, 501):
            os.system('play -nq -t alsa synth {} sine {}'.format(duration / 500, frequency))
    if _toggle_gui:
        _toggle_gui()
    command_listener.listen_for_command()
