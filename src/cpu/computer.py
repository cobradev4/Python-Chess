#!/usr/bin/python
from anytree import Node, RenderTree, PreOrderIter 
from anytree.exporter import DotExporter

from game.chess_piece import ChessPiece
from game.board import Board
from .child_evaluator import ChildEvaluator

from multiprocessing import Pool
import os

class CPU(object):

    def __init__(self):
        self.xChoiceI = -1
        self.yChoiceI = -1
        self.xChoiceN = -1
        self.yChoiceN = -1
        self.testB = Board()
        self.depth = 9

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

    def terminalNode(self, node, maximizingPlayer):
        testB = Board()
        testB.setBoard(node.name.getBoard())
        if maximizingPlayer:
            testB.incrementTurn()
        return testB.checkWin() != ""

     # Mainly for the use of creating the initial 20 possible moves
    def evaluateChildren(self, node, attackingTeam):
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

    # Minimax with alpha beta pruning
    def minimax(self, position, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or self.terminalNode(position, maximizingPlayer):
            # if position.name.getPoints() != 0:
            #     print(str(position.name.getPoints()))
            return position.name.getPoints()
        if maximizingPlayer:
            maxEval = -float("inf")
            evaluator = ChildEvaluator(position, "Black")
            while not evaluator.isComplete():
                thisChild = evaluator.evaluateNextChild()
                if thisChild == False:
                    break
                eval = self.minimax(thisChild, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float("inf")
            evaluator = ChildEvaluator(position, "White")
            while not evaluator.isComplete():
                thisChild = evaluator.evaluateNextChild()
                if thisChild == False:
                    break
                eval = self.minimax(thisChild, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval
    
    def evaluate(self, child):
        result = self.minimax(child, self.depth - 1, -float("inf"), float("inf"), False)
        return result

    def playMove(self, board):
        print("CPU - Analyzing Board...")
        self.testB.setBoard(board)
        self.root = Node(self.testB)
        self.nodeListList = [[self.root]]

        # Run minimax with each possible result from current board
        self.evaluateChildren(self.nodeListList[0][0], "Black")
        children = self.nodeListList[0][0].children

        pool = Pool(os.cpu_count())

        results = pool.map(self.evaluate, children)
        
        print(results)
        highestIndex = results.index(max(results))

        self.xChoiceI = children[highestIndex].name.x1
        self.yChoiceI = children[highestIndex].name.y1
        self.xChoiceN = children[highestIndex].name.x2
        self.yChoiceN = children[highestIndex].name.y2