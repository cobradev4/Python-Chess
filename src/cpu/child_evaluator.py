#!/usr/bin/python

from anytree import Node, RenderTree, PreOrderIter
from game.board import Board 

# Child evaluation object for cpu player
class ChildEvaluator(object):

    def __init__(self, node, attackingTeam):
        self.x, self.y, self.x2, self.y2 = 0, 0, 0, 0
        self.testB = Board()
        self.testB.setBoard(node.name.getBoard())
        if attackingTeam == "Black":
            self.testB.incrementTurn()
        self.attackingTeam = attackingTeam
        self.evaluationNode = node
    
    def setPreviousVars(self, x, y, x2, y2):
        self.prevX = x
        self.prevY = y
        self.prevX2 = x2
        self.prevY2 = y2

    def evaluateNextChild(self):
        for x in range(self.x, 8):
            for y in range(self.y, 8):
                for x2 in range(self.x2, 8):
                    for y2 in range(self.y2, 8):
                        if self.testB.isLegal(x, y, x2, y2, True):
                            tempB = Board()
                            tempB.setBoard(self.testB.getBoard())
                            if self.attackingTeam == "Black":
                                tempB.incrementTurn()
                            tempB.movePiece(x, y, x2, y2)
                            if x != self.prevX:
                                x += 1
                            elif y != self.prevY:
                                y += 1
                            elif x2 != self.prevX2:
                                x2 += 1
                            else:
                                y2 += 1
                            self.x, self.y, self.x2, self.y2 = x, y, x2, y2
                            return Node(tempB, parent=self.evaluationNode)
                        self.setPreviousVars(x, y, x2, y2)
        return False
    
    def isComplete(self):
        return self.x == 7 and self.y == 7 and self.x2 == 7 and self.y2 == 7