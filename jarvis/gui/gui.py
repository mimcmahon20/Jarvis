import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QTimer
import json
import os

from threading import Thread

class ConversationSignal(QObject):
    # Signal with two string arguments
    update_conversation = pyqtSignal(str, str)

class JarvisWindow(QMainWindow):
     # Define a signal
    start_update_signal = pyqtSignal(list, float)  # Arguments are words list and duration per word


    def __init__(self, jarvis_core):
        super().__init__()
        self.jarvis_core = jarvis_core
        self.jarvis_thread = None
        self.is_jarvis_active = False
        self.conversation_signal = ConversationSignal()
        self.conversation_signal.update_conversation.connect(self.update_conversation_callback)
        self.start_update_signal.connect(self.start_update)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Jarvis Interface')
        self.setGeometry(300, 300, 800, 600)  # x, y, width, height

        # Toggle Jarvis Button
        self.toggle_button = QPushButton('Toggle Jarvis', self)
        self.toggle_button.move(10, 10)  # x, y
        self.toggle_button.clicked.connect(self.toggle_jarvis)

        # Conversation Text Field
        self.conversation_text = QTextEdit(self)
        self.conversation_text.setReadOnly(True)  # Make the text field read-only
        self.conversation_text.move(150, 10)  # x, y
        self.conversation_text.resize(640, 580)  # width, height

        self.load_conversation()

    def load_conversation(self):
        # Path to the conversation.json file
        conversation_file = os.path.join('jarvis', 'conversation.json')
        if os.path.exists(conversation_file):
            with open(conversation_file, 'r') as file:
                conversation_data = json.load(file)
                conversation_data = parse_json_conversation(conversation_data)
                self.conversation_text.setText(str(conversation_data))
        else:
            self.conversation_text.setText("No conversation history found.")

    def add_message_to_conversation(self, speaker, text):
        # Append the new message to the conversation
        self.conversation_text.setText(self.conversation_text.toPlainText() + speaker + ": " + text + "\n")

        # Write the updated conversation to the file
        #self.write_conversation_to_file()

    def write_conversation_to_file(self):
        conversation_file = os.path.join('jarvis', 'conversation.json')
        with open(conversation_file, 'w') as file:
            json.dump(self.conversation, file, indent=4)


    @pyqtSlot(str, str)
    def update_conversation_callback(self, speaker, text):
        current_text = self.conversation_text.toPlainText()
        lines = current_text.split('\n')

        if speaker == 'jarvis':
            # Check if the last line already starts with "Jarvis: "
            if not lines[-1].startswith("Jarvis:"):
                # Start a new line for Jarvis's speech
                current_text += "\nJarvis: " + text
            else:
                # Continue appending words in the same line
                current_text += " " + text
        else:
            # For user or other speakers
            current_text += "\nUser: " + text

        self.conversation_text.setText(current_text)

    def start_update(self, words, duration_per_word):
        update_conversation_in_intervals(words, duration_per_word, self.conversation_signal)

    def toggle_jarvis(self):
        if self.is_jarvis_active:
            self.jarvis_core.stop()  # Assuming you have a stop method to safely terminate Jarvis
            self.is_jarvis_active = False
            self.toggle_button.setText('Start Jarvis')
        else:
            self.jarvis_thread = Thread(target=self.jarvis_core.run, daemon=True)
            self.is_jarvis_active = True
            self.jarvis_thread.start()
            self.toggle_button.setText('Stop Jarvis')

def parse_json_conversation(conversation):
    """
    Parses the conversation JSON object and returns a string representation.
    """
    conversation_text = ""
    for message in conversation:
        if message['speaker'] == 'user':
            conversation_text += "User: " + message['text'] + "\n\n"
        else:
            conversation_text += "Jarvis: " + message['text'] + "\n"
    return conversation_text


def update_conversation_in_intervals(words, duration_per_word, conversation_signal):
    word_index = 0

    def update():
        nonlocal word_index
        if word_index < len(words):
            current_word = words[word_index]
            conversation_signal.update_conversation.emit('jarvis', current_word)
            word_index += 1
        else:
            timer.stop()

    timer = QTimer()
    interval = round(duration_per_word * 1000)  # Convert to milliseconds and round
    timer.timeout.connect(update)
    timer.start(interval)