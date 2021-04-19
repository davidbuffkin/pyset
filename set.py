from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from random import shuffle
from threading import Timer
import sys

color = {'R' : 'red', 'G' : 'green', 'P' : 'purple'}
shape = {'O' : 'oval', 'D' : 'diamond', 'S' : 'squiggle'}
shade = {'F' : 'filled', 'E' : 'empty', 'L' : 'shaded'}

tints = {0 : 'rgba(0, 0, 0, 0)', 1 : 'rgba(142, 232, 229, .2)', 2 : 'rgba(127, 245, 159, .2)', 3 : 'rgba(252, 123, 116, .2)'}

def cardToFilename(card):
    return 'img/' + ''.join([color[card[1]], shape[card[2]], shade[card[3]], card[0]]) + '.png'

#Renders a board. Calls event(set) when a set is made or event('done') the game is done
class Board(QWidget):
    def __init__(self, callback):
        super().__init__()
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)
        self.setLayout(self.grid)
        self.callback = callback
        self.cardimgs = []
        self.cardbtns = []
        self.chosen = [False] * 9
        for i in range(1,4):
            for j in range(1,4):
                cardimg = QLabel("", self)
                cardimg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.grid.addWidget(cardimg,i,j)
                self.cardimgs += [cardimg]

                button = QPushButton("", self)
                button.clicked.connect(self.click)
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
                self.grid.addWidget(button,i,j)
                self.cardbtns += [button]
                button.setStyleSheet("background-color : rgba(0, 0, 0, 0);"
                                     "border-color: rgba(0, 0, 0, 0);")
        
        self.deck = []
        for n in "123":
            for c in "RGP":
                for s in "OSD":
                    for sh in "FLE":
                        self.deck += [''.join([n,c,s,sh])]
        
        shuffle(self.deck)
        self.cards = []
        for i in range(9):
            c = self.deck.pop()
            self.setCardImg(i, c)
            self.cards += [c]
      

    def click(self):
        n = self.cardbtns.index(self.sender()) 
        self.chosen[n] = not self.chosen[n]
        if(sum(self.chosen) == 3):
            choices = [i for i in range(9) if self.chosen[i]]
            self.chosen = [False] * 9
            if self.isSet(*[self.cards[i] for i in choices]):
                for i in choices:
                    self.setTint(i, 0)
                if len(self.deck) == 0:
                    self.callback('done')
                else:
                    self.makeSet(choices)
            else:
                for i in choices:
                    self.setTint(i, 0)
        else:
            self.setTint(n, 1 if self.chosen[n] else 0)

    def isSet(self, c1, c2, c3):
        for i in range(4):
            if c1[i] == c2[i] == c3[i]:
                continue
            if c1[i] == c2[i] or c1[i] == c3[i] or c2[i] == c3[i]:
                return False
        return True
    
    def makeSet(self, choices):
        for i in choices:
            self.cards[i] = self.deck.pop()
            self.setCardImg(i, self.cards[i])


    def setCardImg(self, i, card):
        self.cardimgs[i].setStyleSheet(f'border-image : url({cardToFilename(card)});')

    def zeroTint(self):
        for i in range(len(self.cardbtns)):
            self.setTint(i, 0)
    
    # 0 is none, 1 is blue, 2 is green, 3 is red
    def setTint(self, i, tint):
        self.cardbtns[i].setStyleSheet(f"background-color : {tints[tint]};")


class SetGameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Set")
        self.setGeometry(100, 100, 800, 400)
  
        self.board = Board(self.callback)

        self.grid = QGridLayout()
        self.grid.addWidget(self.board, 0, 0)
        self.setLayout(self.grid)
        self.show()
    
    def callback(self, n):
        print(n)


  

if __name__ == "__main__":

    App = QApplication(sys.argv)
    window = SetGameWindow()
    sys.exit(App.exec())