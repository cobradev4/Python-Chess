#!/usr/bin/python
class ChessPiece:

    def __init__(self, type, color):
        self.type = type
        self.color = color
        self.enPassantEligible = False
        self.enPassantAttackX = -1
        self.enPassantAttackY = -1
    
    def findImage(self):
        return "./images/" + self.color + self.type + ".png"
    
    def returnType(self):
        return self.type
    
    def returnColor(self):
        return self.color
    
    def setEnPassantEligible(self, b, x, y):
        if (self.returnType() is "Pawn"):
            self.enPassantEligible = b
            self.enPassantAttackX = x
            self.enPassantAttackY = y

    def getEnPassantAttackX(self):
        return self.enPassantAttackX
    
    def getEnPassantAttackY(self):
        return self.enPassantAttackY

    def isEnPassantEligible(self):
        return self.enPassantEligible
    
    def toString(self):
        return self.type + ", " + self.color + "\n" + "En Passant Eligible: " + str(self.enPassantEligible) + "\n" + "Image Location: " + self.findImage()