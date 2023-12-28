# gui.py
import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from visual_indicator import IndicatorWindow  # Assuming IndicatorWindow is in indicator_window.py
import main  # Import the main module

class MainGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.indicatorWindow = IndicatorWindow()  # Initialize the indicator window

        self.startButton = QPushButton("Start Jarvis", self)
        self.startButton.clicked.connect(self.startJarvis)

        layout = QVBoxLayout()
        layout.addWidget(self.startButton)
        self.setLayout(layout)

        self.setWindowTitle('Jarvis Control')
        self.show()

    def startJarvis(self):
        # Call the function to start Jarvis
        main.run_jarvis()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainGUI()
    sys.exit(app.exec_())
