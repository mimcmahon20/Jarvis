import sys
from PyQt5.QtWidgets import QApplication, QMainWindow

class JarvisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Jarvis Interface')
        self.setGeometry(300, 300, 800, 600)  # x, y, width, height

def main():
    app = QApplication(sys.argv)
    mainWin = JarvisWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
