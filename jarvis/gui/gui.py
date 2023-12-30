import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QTimer
from PyQt5.QtGui import QPainter, QRadialGradient, QColor
import json
import os

from threading import Thread
from PyQt5.QtGui import QFont

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
        self.on_color = QColor(25,195,25, 27)
        self.off_color = QColor(195,25,25, 27)
        self.current_color = self.on_color
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Jarvis Interface')
        self.setGeometry(300, 300, 800, 600)  # x, y, width, height

        # Set the window opacity
        self.setWindowOpacity(0.85)  # 0.5 alpha value

        # Set a stylesheet for the window
        self.setStyleSheet("color: white; font-size: 16px; ")  # blue with 0.4 opacity

        # Conversation Text Field
        self.conversation_text = QTextEdit(self)
        self.conversation_text.setReadOnly(True)  # Make the text field read-only
        self.conversation_text.move(10, 10)  # x, y
        self.conversation_text.resize(780, 580)  # width, height
        self.conversation_text.setStyleSheet("background-color: rgba(0,0,0,0); color: rgba(20,20,20,255); font-size: 16px; padding: 8px; border-radius: 18px;")  # black with 0.5 opacity
        # self.conversation_text.setFont(QFont("Inter"))

        # Toggle Jarvis Button
        self.toggle_button = QPushButton('Start Jarvis', self)
        self.toggle_button.move(700, 10)  # x, y
        self.toggle_button.resize(90, 30)
        self.toggle_button.clicked.connect(self.toggle_jarvis)
        
        # Set a stylesheet for the button
        self.toggle_button.setStyleSheet("background-color: rgba(15,175,35,0.6); border-radius: 16px; border: none; outline: none;")  # red button
        self.toggle_button.setFont(QFont("Inter"))

        self.load_conversation()

    @property
    def current_color(self):
        return self._current_color

    @current_color.setter
    def current_color(self, color):
        self._current_color = color
        self.update()  # Schedule a repaint event

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QRadialGradient(self.width(), 0, min(2*self.width(), self.height()))
        gradient.setColorAt(0.0, self.current_color)
        gradient.setColorAt(1.0, QColor(182,186,89, 27))  # white at the edges
        painter.fillRect(self.rect(), gradient)


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
            self.toggle_button.setStyleSheet("background-color: rgba(15,175,35,0.6); border-radius: 16px; border: none; outline: none;")  # red button
            self.current_color = self.on_color
        else:
            self.jarvis_thread = Thread(target=self.jarvis_core.run, daemon=True)
            self.is_jarvis_active = True
            self.jarvis_thread.start()
            self.toggle_button.setText('Stop Jarvis')
            self.toggle_button.setStyleSheet("background-color: rgba(235,15,15,0.6); border-radius: 16px; border: none; outline: none;")  # red button
            self.current_color = self.off_color

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

    # Start with the first two words, if available
    initial_words = words[:2]
    for word in initial_words:
        conversation_signal.update_conversation.emit('jarvis', word)
        word_index += 1

    # Start the timer for the remaining words
    if len(words) > 2:
        timer.start(interval)