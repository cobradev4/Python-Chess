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
    
    def isTerminalNode(self, node):
        self.isTerminal = False
        for child in node.children:
            self.isTerminal = True
        return self.isTerminal

    if (random == False):
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            self.testB.setBoard(board)
            self.root = Node(self.testB)

            # Minimax algorithm
            def minimax(self, node, depth, maximizingPlayer):
                if depth == 0 or self.isTerminal(node):
                    return node.name.getPoints()
                if maximizingPlayer:
                    self.value =  -1 * float("inf")
                    for child in node.children:
                        self.value = self.max(self.value, self.minimax(child, depth - 1, False))
                    return self.value
                else:
                    self.value = float("inf")
                    for child in node.children:
                        self.value = self.min(self.value, self.minimax(child, depth - 1, True))
                    return self.value



            # self.xChoiceI = self.nodeList[self.choiceIndex].name.x1
            # self.yChoiceI = self.nodeList[self.choiceIndex].name.y1
            # self.xChoiceN = self.nodeList[self.choiceIndex].name.x2
            # self.yChoiceN = self.nodeList[self.choiceIndex].name.y2

    else:
        # Random solution
        def playMove(self, board):
            print("CPU - Analyzing Board...")
            self.testB.setBoard(board)
            self.testB.incrementTurn()
            while (self.testB.isLegal(self.xChoiceI, self.yChoiceI, self.xChoiceN, self.yChoiceN, True) == False):
                self.findRandomPieces()
            self.testB.incrementTurn()
            print("Found legal solution: " + str(self.xChoiceI) + "," + str(self.yChoiceI) + " --> " + str(self.xChoiceN) + "," + str(self.yChoiceN))
        def findRandomPieces(self):
            self.xChoiceI = random.choice(range(0, 8))
            self.yChoiceI = random.choice(range(0, 8))
            self.xChoiceN = random.choice(range(0, 8))
            self.yChoiceN = random.choice(range(0, 8))