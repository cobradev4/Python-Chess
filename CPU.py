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

            def terminalNode(node):
                isTerminal = True
                if node.children:
                    isTerminal = False
                return isTerminal
            
            def createTree(depth):
                self.testB.setBoard(board)
                self.root = Node(self.testB)
                self.nodeListList = [[self.root]]
                self.boardListList = [[self.testB]]
                for d in range(depth):
                    self.nodeList = []
                    self.boardList = []
                    self.index = 0
                    if d % 2 == 0:
                        self.testB.incrementTurn()
                    for i in range(len(self.nodeListList[d])):
                        self.testB.setBoard(self.boardListList[d][i].getBoard())
                        for x in range(8):
                            for y in range(8):
                                for x2 in range(8):
                                    for y2 in range(8):
                                        if (self.testB.isLegal(x, y, x2, y2, True)):
                                            self.board = Board()
                                            self.boardList.append(self.board)
                                            self.boardList[self.index].setBoard(self.testB.getBoard())
                                            if d % 2 == 0:
                                                self.boardList[self.index].incrementTurn()
                                            self.boardList[self.index].movePiece(x, y, x2, y2)
                                            self.boardList[self.index].setCPUVars(x, y, x2, y2)
                                            self.nodeList.append(Node(self.boardList[self.index], parent=self.nodeListList[d][i]))
                                            self.index += 1
                    self.nodeListList.append(self.nodeList)
                    self.boardListList.append(self.boardList)

            def minimax(position, depth, maximizingPlayer):
                if depth == 0 or terminalNode(position):
                    return position.name.getPoints()
                if maximizingPlayer:
                    maxEval = -float("inf")
                    for child in position.children:
                        eval = minimax(child, depth -1, False)
                        maxEval = max(maxEval, eval)
                    return maxEval
                else:
                    minEval = float("inf")
                    for child in position.children:
                        eval = minimax(child, depth - 1, True)
                        minEval = min(minEval, eval)
                    return minEval

            # Run minimax with each value from current board
            self.depth = 4
            self.highestValue = -float("inf")
            createTree(self.depth)
            for child in self.nodeListList[0][0].children:
                print(minimax(child, self.depth - 1, True))
                if (minimax(child, self.depth - 1, True) > self.highestValue):
                    print(str(self.highestValue))
                    self.highestValue = minimax(child, self.depth - 1, True)
                    self.xChoiceI = child.name.x1
                    self.yChoiceI = child.name.y1
                    self.xChoiceN = child.name.x2
                    self.yChoiceN = child.name.y2
            for node in PreOrderIter(self.nodeListList[0][0]):
                print(node.name.toString())
            

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