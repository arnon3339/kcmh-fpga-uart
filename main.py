from PyQt5.QtWidgets import QApplication
import sys
from modules.window import MyWindow
import subprocess


if __name__ == "__main__":
    subprocess.run(['tmux', 'kill-session', '-t', 'ITS3'])
    app = QApplication(sys.argv)
    w = MyWindow()
    w.showMaximized()
    app.exec_()
    subprocess.run(['tmux', 'kill-session', '-t', 'ITS3'])