from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from board import Board
import sys
from os.path import dirname, join, exists
from os import mkdir

direc = dirname(__file__)

class SetGameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set")
        self.initLayout()
        self.initGameplay()
        
        self.show()

    def initGameplay(self):
        self.n = 81 - len(self.board.cards)
        self.timer=QTimer()
        self.timer.timeout.connect(self.showTime)
        self.playing = False
    
    def initLayout(self):
        self.logbox = QCheckBox('Log Game', self)
        self.logbox.setGeometry(590, 40, 150, 40)
        #self.logbox.setChecked(True)
        self.gameLog = ''

        self.board = Board(self.callback, self)
        self.hy = 120
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

        self.timelabel = QLabel('00:00', self)
        self.timelabel.setGeometry(self.bx//2 - 50, 48, 100, 50)
        self.timelabel.setFont(QFont('Arial', 40))
        self.timelabel.hide()

        self.numlabel = QLabel('99 cards left', self)
        self.numlabel.setGeometry(50, 48, 200, 50)
        self.numlabel.setFont(QFont('Arial', 30))
        self.numlabel.hide()

        self.againButton = QPushButton("Play Again!", self)
        self.againButton.setGeometry(590, 20, 150, 40)
        self.againButton.hide()
        self.againButton.released.connect(self.reset)

        self.quitButton = QPushButton("Quit", self)
        self.quitButton.setGeometry(590, 60, 150, 40)
        self.quitButton.hide()
        self.quitButton.released.connect(self.close)


    def fixSize(self):
        self.setGeometry(100, 100, self.bx, self.by + self.hy)
        self.board.resize(self.bx, self.by)

    def start(self):
        self.board.show()
        QTimer.singleShot(25, self.startButton.hide)
        QTimer.singleShot(25, self.timelabel.show)
        QTimer.singleShot(25, self.logbox.hide)
        self.numlabel.setText(f"{self.n} cards left")
        self.numlabel.show()
        self.startTime = QDateTime.currentSecsSinceEpoch()
        self.timer.start(1000)
        self.playing = True

    def getTime(self):
        return QDateTime.currentSecsSinceEpoch() - self.startTime

    def showTime(self):
        time = self.getTime()
        self.timelabel.setText(f"{time // 60:02}:{time % 60:02}")
    
    def callback(self, m):
        toks = m.split(" ")
        if toks[0] == "expand":
            self.by += 400//3
            self.fixSize()
        elif toks[0] == "shrink":
            self.by -= 400//3
            self.fixSize()
        
        if toks[0] in {'expand', 'set'}:
            self.n -= 3
            self.numlabel.setText(f"{self.n} cards left")

        if toks[0] == 'initial':
            self.gameLog += f"0 {m}\n"
        else:
            self.gameLog += f"{self.getTime()} {m}\n"

        if toks[0] == 'done':
            QTimer.singleShot(500, self.done)
            self.log()
            
    def log(self):
        if not exists(join(direc, 'logs')):
            mkdir(join(direc, 'logs'))
        i = 1
        while(exists(join(direc, f'logs/pysetgame{i}.txt'))): i += 1
        with open(join(direc, f'logs/pysetgame{i}.txt'), 'w') as writer:
            writer.write(self.gameLog)
        
        
    
    def done(self):
        self.playing = False
        self.timer.stop()
        self.againButton.show()
        self.quitButton.show()
        self.numlabel.setText("You Won!")
    
    def reset(self):
        #This is pretty bad but ho hum
        log = self.logbox.isChecked()
        self.close()
        self.__init__()
        self.logbox.setChecked(log)
        


    def keyPressEvent(self, event):
        if not self.playing:
            return
        try:
            self.board.click(n=[Qt.Key_1, Qt.Key_2, Qt.Key_3, 
                                Qt.Key_Q, Qt.Key_W, Qt.Key_E, 
                                Qt.Key_A, Qt.Key_S, Qt.Key_D, 
                                Qt.Key_Z, Qt.Key_X, Qt.Key_C,].index(event.key()))
        except Exception:
            pass
  

if __name__ == "__main__":

    App = QApplication(sys.argv)
    App.setWindowIcon(QIcon(join(direc, 'img/icon.png')))
    window = SetGameWindow()
    sys.exit(App.exec())