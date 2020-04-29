#!/usr/bin/python
from ChessPiece import ChessPiece
from Board import Board
from anytree import Node, RenderTree
import random

class CPU(object):
    random = False
    
    def __init__(self):
        self.xChoiceI = -1
        self.yChoiceI = -1
        self.xChoiceN = -1
        self.yChoiceN = -1
        self.testB = Board() # Board object that can be altered without causing damage, just to be safe
        self.boardList = []

    def getxChoiceI(self):
        print("Returning X1: " + str(self.xChoiceI))
        return self.xChoiceI
        
    def getxChoiceN(self):
        print("Returning X2: " + str(self.xChoiceN))
        return self.xChoiceN
        
    def getyChoiceN(self):
        print("Returning Y2: " + str(self.yChoiceN))
        return self.yChoiceN
        
    def getyChoiceI(self):
        print("Returning Y1: " + str(self.yChoiceI))
        return self.yChoiceI

    if (random == False):
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            # Create tree
            self.testB.setBoard(board)
            self.testB.incrementTurn()
            self.index = 0
            for x in range(8):
                for y in range(8):
                    for x2 in range(8):
                        for y2 in range(8):
                            if self.testB.isLegal(x, y, x2, y2):
                                self.board = Board()
                                self.boardList.append(self.board)
                                self.boardList[self.index].setBoard(board)
                                self.boardList[self.index].incrementTurn()
                                self.boardList[self.index].movePiece(x, y, x2, y2)
                                self.index += 1
            self.xChoiceI = 0
            self.yChoiceI = 1
            self.xChoiceN = 0
            self.yChoiceN = 2
            for x in range(len(self.boardList)):
                print(str(x) + ": " + self.boardList[x].toString() + "\n")

    else:
        # Random solution
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            self.testB.setBoard(board)
            self.testB.incrementTurn()
            while (self.testB.isLegal(self.xChoiceI, self.yChoiceI, self.xChoiceN, self.yChoiceN) == False):
                self.findRandomPieces()
            self.testB.incrementTurn()
            print("Found legal solution: " + str(self.xChoiceI) + "," + str(self.yChoiceI) + " --> " + str(self.xChoiceN) + "," + str(self.yChoiceN))
        def findRandomPieces(self):
            self.xChoiceI = random.choice(range(0, 8))
            self.yChoiceI = random.choice(range(0, 8))
            self.xChoiceN = random.choice(range(0, 8))
            self.yChoiceN = random.choice(range(0, 8))