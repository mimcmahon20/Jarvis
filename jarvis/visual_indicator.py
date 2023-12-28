import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os

class IndicatorWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        talking_image_path = os.path.join(current_dir, "faceTalking.png")
        listening_image_path = os.path.join(current_dir, "faceListening.png")

        self.talkingPixmap = QPixmap(talking_image_path)
        self.listeningPixmap = QPixmap(listening_image_path)

        self.label = QLabel(self)
        self.label.setPixmap(self.listeningPixmap)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.show()

    def update_to_talking(self):
        self.label.setPixmap(self.talkingPixmap)

    def update_to_listening(self):
        self.label.setPixmap(self.listeningPixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IndicatorWindow()
    sys.exit(app.exec_())
