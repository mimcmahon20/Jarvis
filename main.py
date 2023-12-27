import sys
from wake_word_listener import listen_for_wake_word
from speech_output import cleanup_speech_threads
from visual_indicator import destroy_indicator
import pvporcupine
import pyaudio

ACCESS_KEY = 'DZzwIYi6/ckJ66kdntAOPfjmzl9iLhYJChPDMOvMaTaeFQMEcIWtHQ=='

def main():
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

        listen_for_wake_word(porcupine, pa, audio_stream)

    except KeyboardInterrupt:
        # Clean up operations
        stop()

    finally:
        try:
            if porcupine is not None:
                porcupine.delete()
        except Exception as e:
            print(f"Error deleting Porcupine instance: {e}")

        try:
            if audio_stream is not None:
                audio_stream.close()
        except Exception as e:
            print(f"Error closing audio stream: {e}")

        try:
            if pa is not None:
                pa.terminate()
        except Exception as e:
            print(f"Error terminating PyAudio instance: {e}")

def stop(): 
    destroy_indicator()
    cleanup_speech_threads()

if __name__ == "__main__":
    main()