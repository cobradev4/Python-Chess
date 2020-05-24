#!/usr/bin/python
from ChessPiece import ChessPiece
from Board import Board
import random
from anytree import Node, RenderTree, PreOrderIter 
from anytree.exporter import DotExporter
from childEvaluator import childEvaluator

class CPU(object):
    random = False
    
    def __init__(self):
        self.xChoiceI = -1
        self.yChoiceI = -1
        self.xChoiceN = -1
        self.yChoiceN = -1
        self.testB = Board()
        self.depth = -1

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
            self.testB.setBoard(board)
            self.root = Node(self.testB)
            self.nodeListList = [[self.root]]
        
            def terminalNode(node, maximizingPlayer):
                testB = Board()
                testB.setBoard(node.name.getBoard())
                if maximizingPlayer:
                    testB.incrementTurn()
                return testB.checkWin() != ""

            # Mainly for the use of creating the initial 20 possible moves
            def evaluateChildren(node, attackingTeam):
                nodeList = []
                testB = Board()
                testB.setBoard(node.name.getBoard())
                if attackingTeam == "Black":
                    testB.incrementTurn()
                for x in range(8):
                    for y in range(8):
                        for x2 in range(8):
                            for y2 in range(8):
                                if testB.isLegal(x, y, x2, y2, True):
                                    tempB = Board()
                                    tempB.setBoard(testB.getBoard())
                                    if attackingTeam == "Black":
                                        tempB.incrementTurn()
                                    tempB.movePiece(x, y, x2, y2)
                                    tempB.setCPUVars(x, y, x2, y2)
                                    nodeList.append(Node(tempB, parent=node))
                self.nodeListList.append(nodeList[:])

            def getNumChildren(node, attackingTeam):
                testB = Board()
                testB.setBoard(node.name.getBoard())
                if attackingTeam == "Black":
                    testB.incrementTurn()
                numMoves = 0
                for x in range(8):
                    for y in range(8):
                        for x2 in range(8):
                            for y2 in range(8):
                                if testB.isLegal(x, y, x2, y2, True):
                                    numMoves += 1      
                return numMoves

            # Minimax with alpha beta pruning
            def minimax(position, depth, alpha, beta, maximizingPlayer):
                if depth == 0 or terminalNode(position, maximizingPlayer):
                    if position.name.getPoints() != 0:
                        print(str(position.name.getPoints()))
                    return position.name.getPoints()
                if maximizingPlayer:
                    maxEval = -float("inf")
                    evaluator = childEvaluator(position, "Black")
                    while not evaluator.isComplete():
                        thisChild = evaluator.evaluateNextChild()
                        if thisChild == False:
                            break
                        eval = minimax(thisChild, depth - 1, alpha, beta, False)
                        maxEval = max(maxEval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
                    return maxEval
                else:
                    minEval = float("inf")
                    evaluator2 = childEvaluator(position, "White")
                    while not evaluator2.isComplete():
                        thisChild = evaluator2.evaluateNextChild()
                        if thisChild == False:
                            break
                        eval = minimax(thisChild, depth - 1, alpha, beta, True)
                        minEval = min(minEval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
                    return minEval

            # Run minimax with each possible result from current board
            self.depth = 9
            self.highestValue = -float("inf")
            evaluateChildren(self.nodeListList[0][0], "Black")
            self.index = 0
            for child in self.nodeListList[0][0].children:
                self.eval = minimax(child, self.depth - 1, -float("inf"), float("inf"), False)
                if (self.eval > self.highestValue):
                    self.highestValue = self.eval
                    self.xChoiceI = child.name.x1
                    self.yChoiceI = child.name.y1
                    self.xChoiceN = child.name.x2
                    self.yChoiceN = child.name.y2
                self.index += 1
            # for node in PreOrderIter(self.nodeListList[0][0]):
            #     print(node.name.toString())

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