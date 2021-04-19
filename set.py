from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from board import Board
import sys

class SetGameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set")
        self.initLayout()
        
        self.show()
    
    def initLayout(self):
        self.board = Board(self.callback, self)
        self.hy = 150
        self.bx = 800
        self.by = int(400 * len(self.board.cards) / 9)
        self.setGeometry(100, 100, self.bx, self.by + self.hy)
        self.board.resize(800, self.by)
        self.board.move(0, self.hy)
        self.board.hide()

        self.startButton = QPushButton("Start", self)
        self.btnx = 130
        self.btny = 60
        self.startButton.setGeometry(self.bx//2 - self.btnx//2, self.hy//2 - self.btny//2, self.btnx, self.btny)
        self.startButton.released.connect(self.start)

    def fixSize(self):
        self.setGeometry(100, 100, self.bx, self.by + self.hy)
        self.board.resize(self.bx, self.by)

    def start(self):
        self.board.show()
        QTimer.singleShot(25, self.startButton.hide)
    
    def callback(self, m):
        print(m)
        toks = m.split(" ")
        if toks[0] == "expand":
            self.by += 400//3
            self.fixSize()
        elif toks[0] == "shrink":
            self.by -= 400//3
            self.fixSize()



  

if __name__ == "__main__":

    App = QApplication(sys.argv)
    #App.setStyle("macintosh")
    window = SetGameWindow()
    sys.exit(App.exec())