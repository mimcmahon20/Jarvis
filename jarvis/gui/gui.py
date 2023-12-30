import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget, QListWidgetItem, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, QTimer, Qt
from PyQt5.QtGui import QPainter, QRadialGradient, QColor, QFont, QColor
import json
import os

from threading import Thread

class ConversationSignal(QObject):
    # Signal with two string arguments
    update_conversation = pyqtSignal(str, str)

class ChatItemWidget(QWidget):
    def __init__(self, text, alignment=Qt.AlignLeft):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel(text)
        self.label.setWordWrap(True)
        self.label.setAlignment(alignment)
        self.label.setMaximumWidth(768)  # Set maximum width for text wrapping

        # Set size policy
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)

        self.setLayout(layout)
        layout.addWidget(self.label)


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
        self.setMinimumSize(600, 400)  # Set a minimum window size

        # Central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

       # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignTop)  # Align the layout to the top

        # Toggle Jarvis Button
        self.toggle_button = QPushButton('Start Jarvis', self)
        self.toggle_button.setStyleSheet("background-color: rgba(15,175,35,0.6); border-radius: 16px; border: none; outline: none;")  # Style for the button
        self.toggle_button.setFont(QFont("Arial", 12))
        self.toggle_button.clicked.connect(self.toggle_jarvis)
        self.toggle_button.setFixedSize(120, 40)  # Fixed size for the button

        # Button layout (right aligned)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.toggle_button, 0, Qt.AlignRight)  # Align button to the right
        main_layout.addLayout(button_layout)

        # Dark gray background
        self.setStyleSheet("background-color: rgb(52, 53, 65);")

         # Conversation List Container (to center the list)
        conversation_container = QWidget()
        conversation_layout = QHBoxLayout(conversation_container)
        conversation_layout.setAlignment(Qt.AlignCenter)  # Center the layout

        # Conversation List
        # Conversation List setup
        self.conversation_list = QListWidget()
        self.conversation_list.setMaximumWidth(768)  # Set maximum width
        self.conversation_list.setStyleSheet("""
            QListWidget {
                background-color: rgba(52, 53, 65, 255);
                color: #ececf1;
                border-radius: 8px;
                padding: 10px;
                font-family: Arial;
            }
            QListWidgetItem {
                border-bottom: 1px solid #ececf1;
                padding: 5px;
                margin: 5px;
            }
        """)

        # Add conversation list to its container
        conversation_layout.addWidget(self.conversation_list)

        # Add the conversation container to the main layout
        main_layout.addWidget(conversation_container)

        # Set the main layout for the central widget
        central_widget.setLayout(main_layout)

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
                for message in conversation_data:
                    speaker = message.get('speaker')
                    text = message.get('text')
                    self.add_message_to_conversation(speaker, text)
        else:
            # You might want to add a placeholder or leave it empty
            self.add_message_to_conversation('system', 'No conversation history found.')


    def add_message_to_conversation(self, speaker, text):
        chat_item_widget = ChatItemWidget(f"{speaker}: {text}", Qt.AlignRight if speaker == 'user' else Qt.AlignLeft)
        list_widget_item = QListWidgetItem(self.conversation_list)
        list_widget_item.setSizeHint(chat_item_widget.sizeHint())  # Important for custom widgets
        self.conversation_list.addItem(list_widget_item)
        self.conversation_list.setItemWidget(list_widget_item, chat_item_widget)


    def write_conversation_to_file(self):
        conversation_file = os.path.join('jarvis', 'conversation.json')
        with open(conversation_file, 'w') as file:
            json.dump(self.conversation, file, indent=4)

    @pyqtSlot(str, str)
    def update_conversation_callback(self, speaker, text):
        if speaker == 'jarvis':
            lines = text.split('\n')
            for line in lines:
                self.add_message_to_jarvis_conversation(line)
        else:
            self.add_message_to_conversation(speaker, text + '\n')

        self.conversation_list.scrollToBottom()

    def add_message_to_jarvis_conversation(self, text):
        if self.conversation_list.count() > 0:
            last_item = self.conversation_list.item(self.conversation_list.count() - 1)
            chat_widget = self.conversation_list.itemWidget(last_item)

            if chat_widget.label.text().startswith("jarvis:") and not chat_widget.label.text().endswith('\n'):
                # Append the word to the existing Jarvis message
                chat_widget.label.setText(chat_widget.label.text() + " " + text)
            else:
                # Start a new Jarvis message
                self.add_message_to_conversation('jarvis', text)
        else:
            # If the list is empty, add the message
            self.add_message_to_conversation('jarvis', text)

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