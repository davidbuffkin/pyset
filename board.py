from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
from random import shuffle
from os.path import dirname, join

color = {'R' : 'red', 'G' : 'green', 'P' : 'purple'}
shape = {'O' : 'oval', 'D' : 'diamond', 'S' : 'squiggle'}
shade = {'F' : 'filled', 'E' : 'empty', 'L' : 'shaded'}

tints = {0 : 'rgba(0, 0, 0, 0)', 1 : 'rgba(142, 232, 229, .2)', 2 : 'rgba(127, 245, 159, .2)', 3 : 'rgba(252, 123, 116, .2)'}
direc = dirname(__file__)

def cardToFilename(card):
    return join(direc, f'img/{"".join([color[card[1]], shape[card[2]], shade[card[3]], card[0]])}.png')

#Renders a board. Calls event(set) when a set is made or event('done') the game is done
class Board(QWidget):
    def __init__(self, callback, parent):
        super().__init__(parent)
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(10)
        self.grid.setVerticalSpacing(10)
        #self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setLayout(self.grid)
        self.callback = callback
        self.cardimgs = []
        self.cardbtns = []
        self.chosen = [False] * 12
        self.waiting = False
        for i in range(1,5):
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
        for i in range(12):
            c = self.deck.pop()

            self.setCardImg(i, c)
            self.cards += [c]

        self.callback(f"initial {''.join(self.cards)}")

        if not self.hasSet():
           self.expandBoard(True)
      

    def click(self, n = None):
        if self.waiting:
            return
        if n is False:
            n = self.cardbtns.index(self.sender()) 
        self.chosen[n] = not self.chosen[n]
        if(sum(self.chosen) == 3):
            self.waiting = True
            choices = [i for i in range(len(self.cards)) if self.chosen[i]]
            self.chosen = [False] * len(self.cards)
            if self.isSet(*[self.cards[i] for i in choices]):
                for i in choices:
                    self.setTint(i, 2)
                QTimer.singleShot(500, self.zeroTint)
                if len(self.deck) == 0:
                    self.callback('done')
                else:
                    self.callback('set ' + ''.join([self.cards[i] for i in choices]))
                    QTimer.singleShot(500, lambda: self.makeSet(choices))
            else:
                for i in choices:
                    self.setTint(i, 3)
                self.callback('misset ' + ''.join([self.cards[i] for i in choices]))
                QTimer.singleShot(500, self.zeroTint)
                
        else:
            self.setTint(n, 1 if self.chosen[n] else 0)
        

    def isSet(self, c1, c2, c3):
        for i in range(4):
            if c1[i] == c2[i] == c3[i]:
                continue
            if c1[i] == c2[i] or c1[i] == c3[i] or c2[i] == c3[i]:
                return False
        return True

    def hasSet(self, cardsToCheck = None, n = None):
        if cardsToCheck == None: cardsToCheck = self.cards
        if n == None: n = len(self.cards)
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    if self.isSet(cardsToCheck[i], cardsToCheck[j], cardsToCheck[k]):
                        return True
        return False

    def shrinkBoard(self, removals):

        for btn in self.cardbtns[-3:]:
            self.grid.removeWidget(btn)
            btn.deleteLater()
            btn = None
        for img in self.cardimgs[-3:]:
            self.grid.removeWidget(img)
            img.deleteLater()
            img = None

        self.cardbtns = self.cardbtns[:-3]
        self.cardimgs = self.cardimgs[:-3]  
        
        for i in removals[::-1]:
            del self.cards[i]
        
        self.chosen = [False] * len(self.cards)

        self.resetCardImgs()

        self.callback("shrink")

    def expandBoard(self, suppress=False):
        
        for j in range(1,4):
            cardimg = QLabel("", self)
            cardimg.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.grid.addWidget(cardimg,len(self.cards) // 3 + 1,j)
            self.cardimgs += [cardimg]

            button = QPushButton("", self)
            button.clicked.connect(self.click)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.grid.addWidget(button,len(self.cards) // 3 + 1,j)
            self.cardbtns += [button]
            button.setStyleSheet("background-color : rgba(0, 0, 0, 0);"
                                "border-color: rgba(0, 0, 0, 0);")
        for i in range(len(self.cardimgs) - 3, len(self.cardimgs)):
            c = self.deck.pop()
            self.setCardImg(i, c)
            self.cards += [c]
        self.chosen += [False] * 3
        
        if not suppress:
            self.callback('expand ' + ''.join(self.cards[-3:]))

        if not self.hasSet():
            self.expandBoard()
        

    
    def makeSet(self, choices):
        if len(self.cards) > 12:
            remaining = [self.cards[i] for i in range(len(self.cards)) if i not in choices]
            if self.hasSet(cardsToCheck = remaining, n = len(remaining)):
                self.shrinkBoard(choices)
            else:
                for i in choices:
                    self.cards[i] = self.deck.pop()
                    self.setCardImg(i, self.cards[i])
                if not self.hasSet():
                    self.expandBoard()
        else:
            for i in choices:
                self.cards[i] = self.deck.pop()
                self.setCardImg(i, self.cards[i])
            if not self.hasSet():
                self.expandBoard()

    def resetCardImgs(self):
        for i, c in enumerate(self.cards):
            self.setCardImg(i, c)

    def setCardImg(self, i, card):
        self.cardimgs[i].setStyleSheet(f'border-image : url({cardToFilename(card)});')

    def zeroTint(self):
        for i in range(len(self.cardbtns)):
            self.setTint(i, 0)
        self.waiting = False
    
    # 0 is none, 1 is blue, 2 is green, 3 is red
    def setTint(self, i, tint):
        self.cardbtns[i].setStyleSheet(f"background-color : {tints[tint]};")

        
