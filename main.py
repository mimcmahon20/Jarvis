import sys
from threading import Thread
from jarvis.jarvis_core import JarvisCore
from jarvis.visual_indicator import VisualIndicator
import jarvis.components.speech_output as speech_output
import jarvis.components.command_listener as command_listener
import jarvis.components.wake_word_listener as wake_word_listener

# Create the visual indicator instance
indicator = VisualIndicator()

# Define GUI update functions
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


# Initialize Jarvis Core
jarvis_core = JarvisCore('DZzwIYi6/ckJ66kdntAOPfjmzl9iLhYJChPDMOvMaTaeFQMEcIWtHQ==')

if __name__ == "__main__":
    try:
        # Start Jarvis Core in a separate thread
        Thread(target=jarvis_core.run, daemon=True).start()

        # Run the Tkinter main loop in the main thread
        indicator.root.mainloop()
    except KeyboardInterrupt:
        jarvis_core.stop()
        sys.exit()
