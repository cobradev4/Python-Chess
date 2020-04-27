#!/usr/bin/python
from ChessPiece import *
from Board import *
import random

class CPU:
    random = True
    # TODO - When entire enemy is destroyed and only king is left if king is attacked, game freezes :|
    
    def __init__(self):
        self.xRandomI = -1
        self.yRandomI = -1
        self.xRandomN = -1
        self.yRandomN = -1
        self.xChoiceI = -1
        self.yChoiceI = -1
        self.xChoiceN = -1
        self.yChoiceN = -1
        self.testB = Board()

    if (random == False):
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            return False
        
        def getxChoiceI(self):
            return self.xChoiceI
        
        def getyChoiceI(self):
            return self.yChoiceI

        def getxChoiceN(self):
            return self.xChoiceN
        
        def getyChoiceN(self):
            return self.yChoiceN

    else:
        # Random solution
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            self.testB.setBoard(board)
            while (self.testB.isLegal(self.xRandomI, self.yRandomI, self.xRandomN, self.yRandomN) == False):
                self.findRandomPieces()
            print("Found legal solution: " + str(self.xRandomI) + "," + str(self.yRandomI) + " --> " + str(self.xRandomN) + "," + str(self.yRandomN))

        def getxChoiceI(self):
            return self.xRandomI
        
        def getxChoiceN(self):
            return self.xRandomN
        
        def getyChoiceN(self):
            return self.yRandomN
        
        def getyChoiceI(self):
            return self.yRandomI

        def findRandomPieces(self):
            self.xRandomI = random.choice(range(0, 8))
            self.yRandomI = random.choice(range(0, 8))
            self.xRandomN = random.choice(range(0, 8))
            self.yRandomN = random.choice(range(0, 8))