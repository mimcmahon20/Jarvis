import pvporcupine
import pyaudio
import struct
import command_listener 
from visual_indicator import start_indicator, stop_indicator, destroy_indicator
import sys

ACCESS_KEY = 'DZzwIYi6/ckJ66kdntAOPfjmzl9iLhYJChPDMOvMaTaeFQMEcIWtHQ=='

def listen_for_wake_word():
    porcupine = None
    pa = None
    audio_stream = None

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

        print("Listening for the wake word...")

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                print("Jarvis wake word detected!")
                on_wake_word_detected()

    except KeyboardInterrupt:
        # Clean up operations
        destroy_indicator()
        sys.exit(0)

    finally:
        try:
            if porcupine is not None:
                print("Deleting Porcupine instance...")
                porcupine.delete()
        except Exception as e:
            print(f"Error deleting Porcupine instance: {e}")

        try:
            if audio_stream is not None:
                print("Closing audio stream...")
                audio_stream.close()
        except Exception as e:
            print(f"Error closing audio stream: {e}")

        try:
            if pa is not None:
                print("Terminating PyAudio instance...")
                pa.terminate()
        except Exception as e:
            print(f"Error terminating PyAudio instance: {e}")


def on_wake_word_detected():
    """
    Called when the wake word is detected.
    """
    start_indicator()
    command_listener.listen_for_command()
    stop_indicator()

if __name__ == "__main__":
    listen_for_wake_word()
