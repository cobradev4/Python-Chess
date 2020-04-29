#!/usr/bin/python
from ChessPiece import ChessPiece
from Board import Board
import random
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

class CPU(object):
    random = False
    
    def __init__(self):
        self.xChoiceI = -1
        self.yChoiceI = -1
        self.xChoiceN = -1
        self.yChoiceN = -1
        self.testB = Board() # Board object that can be altered without causing damage, just to be safe
        self.boardList = []
        self.boardList2 = []

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
            self.nodeList = []
            self.testB.setBoard(board)
            self.testB.incrementTurn()
            self.root = Node(self.testB)
            self.index = 0
            # Layer 1
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
                                self.nodeList.append(Node(self.boardList[self.index], parent=self.root))
                                self.index += 1
            self.nodeList2 = []
            # Layer 2
            self.index = 0
            for i in range(len(self.nodeList)):
                self.testB.setBoard(self.boardList[i].getBoard())
                for x in range(8):
                    for y in range(8):
                        for x2 in range(8):
                            for y2 in range(8):
                                if (self.testB.isLegal(x, y, x2, y2)):
                                    self.board = Board()
                                    self.boardList2.append(self.board)
                                    self.boardList2[self.index].setBoard(self.testB.getBoard())
                                    self.boardList2[self.index].incrementTurn()
                                    self.boardList2[self.index].movePiece(x, y, x2, y2)
                                    self.nodeList2.append(Node(self.boardList2[self.index], parent=self.nodeList[i]))
                                    self.index += 1
            self.xChoiceI = 0
            self.yChoiceI = 1
            self.xChoiceN = 0
            self.yChoiceN = 2
            for pre, fill, node in RenderTree(self.root):
                print("%s%s" % (pre, node.name))
            DotExporter(self.root).to_dotfile("test1.dot")

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