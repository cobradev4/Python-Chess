#!/usr/bin/python
from ChessPiece import *
from Board import *
from anytree import Node, RenderTree
import random

class CPU:
    random = True
    
    def __init__(self):
        self.xChoiceI = -1
        self.yChoiceI = -1
        self.xChoiceN = -1
        self.yChoiceN = -1
        self.testB = Board() # Board object that can be altered without causing damage, just to be safe
        self.boardList = []

    if (random == False):
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            # Create tree
            # self.root = Node(board)
            # self.testB.setBoard(board)
            # self.list1 = []
            # self.index = 0
            # for x in range(8):
            #     for y in range(8):
            #         for x2 in range(8):
            #             for y2 in range(8):
            #                 if self.testB.isLegal(x, y, x2, y2):
            #                     self.boardList[self.index].setBoard(board)
            #                     self.boardList[self.index].incrementTurn()
            #                     self.boardList[self.index].movePiece(x, y, x2, y2)
            #                     self.list1.append(Node(str(self.index), parent=self.root))
            #                     self.index += 1
            self.xChoiceI = 0
            self.ychoiceI = 1
            self.xChoiceN = 0
            self.yChoiceN = 2
            print("done")
            return True

    else:
        # Random solution
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            self.testB.setBoard(board)
            self.testB.incrementTurn()
            while (self.testB.isLegal(self.xChoiceI, self.yChoiceI, self.xChoiceN, self.yChoiceN) == False):
                self.findRandomPieces()
            print("Found legal solution: " + str(self.xChoiceI) + "," + str(self.yChoiceI) + " --> " + str(self.xChoiceN) + "," + str(self.yChoiceN))
            self.testB.incrementTurn()
        def findRandomPieces(self):
            self.xChoiceI = random.choice(range(0, 8))
            self.yChoiceI = random.choice(range(0, 8))
            self.xChoiceN = random.choice(range(0, 8))
            self.yChoiceN = random.choice(range(0, 8))

    def getxChoiceI(self):
        return self.xChoiceI
        
    def getxChoiceN(self):
        return self.xChoiceN
        
    def getyChoiceN(self):
        return self.yChoiceN
        
    def getyChoiceI(self):
        return self.yChoiceI
