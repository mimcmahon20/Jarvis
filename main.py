import sys
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtWidgets, QtCore
from threading import Thread
from jarvis.jarvis_core import JarvisCore
from jarvis.visual_indicator import VisualIndicator
import jarvis.components.speech_output as speech_output
import jarvis.components.command_listener as command_listener
import jarvis.components.wake_word_listener as wake_word_listener
from jarvis.gui.gui import JarvisWindow

# Initialize Jarvis Core
jarvis_core = JarvisCore('DZzwIYi6/ckJ66kdntAOPfjmzl9iLhYJChPDMOvMaTaeFQMEcIWtHQ==')

if __name__ == "__main__":
    try:
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseStyleSheetPropagationInWidgetStyles, True)
        app = QApplication(sys.argv)
        mainWin = JarvisWindow(jarvis_core)  # Pass the jarvis_core instance

        # Show the PyQt window
        mainWin.show()

         # Pass the conversation signal to the command_listener
        import jarvis.components.command_listener as command_listener
        command_listener.set_conversation_signal(mainWin.conversation_signal)

        # Set the main window in speech_output
        import jarvis.components.speech_output as speech_output
        speech_output.set_main_window(mainWin)
        
        # Start the PyQt event loop in the main thread
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        jarvis_core.stop()
        sys.exit()