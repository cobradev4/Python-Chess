#!/usr/bin/python
from ChessPiece import ChessPiece
from Board import Board
import random
from anytree import Node, RenderTree, PreOrderIter
from anytree.exporter import DotExporter

class CPU(object):
    random = False
    
    def __init__(self):
        self.xChoiceI = -1
        self.yChoiceI = -1
        self.xChoiceN = -1
        self.yChoiceN = -1
        self.testB = Board()
        self.testB.incrementTurn() # Set initial turn to black
        self.boardList = []
        self.boardList2 = []
        self.boardList3 = []

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
                                self.boardList[self.index].setCPUVars(x, y, x2, y2) # Save coordinates for later use
                                self.nodeList.append(Node(self.boardList[self.index], parent=self.root))
                                self.index += 1
            # Layer 2
            self.index = 0
            self.nodeList2 = []
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
            # Layer 3
            self.index = 0
            self.nodeList3 = []
            for i in range(len(self.nodeList2)):
                self.testB.setBoard(self.boardList2[i].getBoard())
                for x in range(8):
                    for y in range(8):
                        for x2 in range(8):
                            for y2 in range(8):
                                if (self.testB.isLegal(x, y, x2, y2)):
                                    self.board = Board()
                                    self.boardList3.append(self.board)
                                    self.boardList3[self.index].setBoard(self.testB.getBoard())
                                    self.boardList3[self.index].incrementTurn()
                                    self.boardList3[self.index].movePiece(x, y, x2, y2)
                                    self.nodeList3.append(Node(self.boardList3[self.index], parent=self.nodeList2[i]))
                                    self.index += 1
            # Search tree
            self.choiceIndex = -1
            self.lowestEnemyCount = 17
            self.index = 0 # Index for current initial move
            for node in self.nodeList: # Layer 1
                for node2 in PreOrderIter(node): # Layer 2/Layer3 - Includes all children nodes
                    # Check if less enemies will be present
                    if (node2.name.getWhiteCount() < self.lowestEnemyCount):
                        self.choiceIndex = self.index
                        self.lowestEnemyCount = node2.name.getWhiteCount()
                self.index += 1
                    
            self.xChoiceI = self.nodeList[self.choiceIndex].name.x1
            self.yChoiceI = self.nodeList[self.choiceIndex].name.y1
            self.xChoiceN = self.nodeList[self.choiceIndex].name.x2
            self.yChoiceN = self.nodeList[self.choiceIndex].name.y2

            # Can print to string in text (node.name.toString())
            #for pre, fill, node in RenderTree(self.root):
            #    print("%s%s" % (pre, node.name)) 
            # Not sure how to export with toString to dot file
            #DotExporter(self.root).to_dotfile("test1.dot")

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