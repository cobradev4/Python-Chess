#!/usr/bin/python
from ChessPiece import *

# Variable to keep track of white (0) or black (1)
turn = 0 

# Castling variables
wrRookMoved = False
wlRookMoved = False
blRookMoved = False
brRookMoved = False
wKingMoved = False
bKingMoved = False

class Board:
    
    def __init__(self):
        self.board = [[ChessPiece("blank", "none") for j in range(8)] for i in range(8)]
        self.initializeBoard()
        self.upgradablePawnX = -1
        self.upgradablePawnY = -1
        self.upgradablePawn = False
        self.destroyedPieces = [] # List to hold destoryed pieces (ChessPiece list)

    # Argument variables indicate new and previous locations in said column or row
    def movePiece(self, prevR, prevC, newR, newC):
        global wrRookMoved, wlRookMoved, blRookMoved, brRookMoved, wKingMoved, bKingMoved
        self.prevType = self.board[prevR][prevC].returnType()
        self.prevColor = self.board[prevR][prevC].returnColor()

        if (self.isLegal(prevR, prevC, newR, newC)):
            # Castling - Keep track of which kings and rooks have been moved
            if (self.prevType == "King"):
                if (self.prevColor == "White"):
                    wKingMoved = True
                else:
                    bKingMoved = True
            if (self.prevType == "Rook"):
                if (self.prevColor == "White"):
                    if (prevR == 7) and (prevC == 7):
                        wrRookMoved = True
                    else:
                        wlRookMoved = True
                else:
                    if (prevR == 0) and (prevC == 0):
                        blRookMoved = True
                    else:
                        brRookMoved = True
            self.board[prevR][prevC].setEnPassantEligible(False, -1, -1)
            # Save list of destroyed pieces
            if (self.board[newR][newC].returnType() != "blank"):
                self.destroyedPieces.append(self.board[newR][newC])
            self.board[newR][newC] = self.board[prevR][prevC]
            self.board[prevR][prevC] = ChessPiece("blank", "none")
            self.incrementTurn()
    
    def getDestroyedPieces(self):
        for i in range(len(self.destroyedPieces)):
            print("\n" + str(i) + ":" + self.destroyedPieces[i].toString())
        return self.destroyedPieces
    
    def searchForPawnUpgrade(self, c):
        for x in range(8):
            if (c == "White"):
                if (self.board[x][0].returnType() == "Pawn") and (self.board[x][0].returnColor() == "White"):
                    return x
            else:
                if (self.board[x][7].returnType() == "Pawn") and (self.board[x][7].returnColor() == "Black"):
                    return x
        return -1

    def checkPawnUpgrade(self):
        return self.upgradablePawn
    
    def setPawnUpgradable(self, x, y):
        self.upgradablePawn = True
        self.upgradablePawnX = x
        self.upgradablePawnY = y
    
    def upgradePawn(self, x, y, t):
        print("Setting " + str(x) + "," + str(y) + " to " + t)
        self.board[x][y] = ChessPiece(t, self.board[x][y].returnColor())
    
    def getBoard(self):
        return self.board
    
    def setBoard(self, b):
        self.board = b

    def incrementTurn(self):
        global turn
        if (turn == 0):
            turn += 1
        elif (turn == 1):
            turn -= 1
    
    def checkTurn(self):
        return turn
    
    def checkWin(self):
        self.whiteKPresent = False  
        self.blackKPresent = False
        for i in range(8):
            for j in range(8):
                if (self.board[i][j].returnType() == "King"):
                    if (self.board[i][j].returnColor() == "White"):
                        self.whiteKPresent = True
                    elif (self.board[i][j].returnColor() == "Black"):
                        self.blackKPresent = True
        if (self.whiteKPresent == False):
            return "black"
        elif (self.blackKPresent == False):
            return "white"
                
    def isInCheck(self, r, c):
        self.incrementTurn() # Need to allow opposite attacks to be legal
        print("Checking for possible checks...")
        for x in range(8):
            for y in range(8):
                if (self.isLegal(x, y, r, c)):
                    print("Found check!")
                    self.incrementTurn() # Reset turns
                    return True
        self.incrementTurn() # Reset turns
        return False

    # Have to write out all rules of chess here :(
    def isLegal(self, prevR, prevC, newR, newC):
        global turn, wrRookMoved, wlRookMoved, blRookMoved, brRookMoved, wKingMoved, bKingMoved

        self.pType = self.board[prevR][prevC].returnType()
        self.nType = self.board[newR][newC].returnType()
        self.pColor = self.board[prevR][prevC].returnColor()
        self.nColor = self.board[newR][newC].returnColor()

        # Check and make sure it is the player's turn
        if (turn == 0) and (self.pColor == "Black"):
            return False
        if (turn == 1) and (self.pColor == "White"):
            return False 
        
        # Prevent from attacking own team
        if (self.pColor == self.nColor):
            return False
        if (self.pType == "blank"):
            return False

        # Pawn rules
        if (self.pType == "Pawn"):
            if (self.pColor == "Black"):
                if (self.nType == "blank") and (prevR == newR):
                    if (newC - 1 == prevC):
                        return True
                    if (newC - 2 == prevC) and (prevC == 1):
                        print("Potentially En passant eligible...")
                        if (newR - 1 > -1): # Prevent IndexError
                            if (self.board[newC][newR - 1].returnType() == "Pawn") and (self.board[newC][newR - 1].returnColor() != "Black"):
                                self.board[newC][newR - 1].setEnPassantEligible(True, newR, newC)
                        if (newR + 1 < 8): # Prevent IndexError
                            if (self.board[newC][newR + 1].returnType() == "Pawn") and (self.board[newC][newR + 1].returnColor() != "Black"):
                                self.board[newC][newR + 1].setEnPassantEligible(True, newR, newC)
                        return True
                # elif wouldn't work for some reason
                if (self.nType != "blank") and (newC - 1 == prevC) and ((newR + 1 == prevR) or (newR - 1 == prevR)):
                    print("Pawn attacking: " + self.nType)
                    return True
                # En passant
                if (self.nType == "blank") and (newC - 1 == prevC) and ((newR + 1 == prevR) or (newR - 1 == prevR)):
                    if (self.board[prevR][prevC].isEnPassantEligible()):
                        print("En passant!")
                        self.board[self.board[prevR][prevC].getEnPassantAttackX()][self.board[prevR][prevC].getEnPassantAttackY()] = ChessPiece("blank","none")
                        return True
            if (self.pColor == "White"):
                if (self.nType == "blank") and (prevR == newR):
                    if (newC + 1 == prevC):
                        return True
                    if (newC + 2 == prevC) and (prevC == 6):
                        print("Potentially En passant eligible")
                        if (newR - 1 > -1): # Prevent IndexError
                            if (self.board[newC][newR - 1].returnType() == "Pawn") and (self.board[newC][newR - 1].returnColor() != "White"):
                                self.board[newC][newR - 1].setEnPassantEligible(True, newR, newC)
                        if (newR + 1 < 8): #prevent IndexError
                            if (self.board[newC][newR + 1].returnType() == "Pawn") and (self.board[newC][newR + 1].returnColor() != "White"):
                                self.board[newC][newR + 1].setEnPassantEligible(True, newR, newC)
                        return True
                # elif wouldn't work for some reason
                if (self.nType != "blank") and (newC + 1 == prevC) and ((newR + 1 == prevR) or (newR - 1 == prevR)):
                    print("Pawn attacking: " + self.nType)
                    return True
                # En passant
                if (self.nType == "blank") and (newC + 1 == prevC) and ((newR + 1 == prevR) or (newR - 1 == prevR)):
                    if (self.board[prevR][prevC].isEnPassantEligible()):
                        print("En passant!")
                        self.board[self.board[prevR][prevC].getEnPassantAttackX()][self.board[prevR][prevC].getEnPassantAttackY()] = ChessPiece("blank","none")
                        return True

        # Rook rules      
        if (self.pType == "Rook") or (self.pType == "Queen"):
            if (prevC == newC):
                if (newR > prevR): # Moving to the right
                    if (newR == prevR + 1):
                        return True
                    for i in range(prevR + 1, newR):
                        if (self.board[i][newC].returnType() != "blank"):
                            return False
                if (prevR > newR): # Moving to the left
                    if (newR == prevR - 1):
                        return True
                    for i in range(newR + 1, prevR):
                        if (self.board[i][newC].returnType() != "blank"):
                            return False
                return True
            elif (prevR == newR):
                if (newC > prevC): # Moving down
                    if (newC == prevC + 1):
                        return True
                    for i in range(prevC + 1, newC):
                        if (self.board[newR][i].returnType() != "blank"):
                            return False
                if (prevC > newC): # Moving up
                    if (newC == prevC - 1):
                        return True
                    for i in range(newC + 1, prevC):
                        if (self.board[newR][i].returnType() != "blank"):
                            return False
                return True
    
        # Knight rules 
        if (self.pType == "Knight"):
            if (newC - 2 == prevC) or (newC + 2 == prevC):
                if (newR + 1 == prevR) or (newR - 1 == prevR):
                    return True
            if (newR - 2 == prevR) or (newR + 2 == prevR):
                    if (newC + 1 == prevC) or (newC - 1 == prevC):
                        return True
            return False
        
        # Bishop rules
        if (self.pType == "Bishop") or (self.pType == "Queen"):
            # Moving up right
            if (newC < prevC) and (newR > prevR):
                while (newC != prevC - 1) and (newR != prevR + 1):
                    prevR += 1
                    prevC -= 1
                    print("Checking: " + str(prevR) + "," + str(prevC))
                    print(self.board[prevR][prevC].returnType())
                    if (self.board[prevR][prevC].returnType() != "blank"):
                        return False
                return (newC == prevC - 1) and (newR == prevR + 1) # Final check to ensure diagonal
            # Moving down right
            if (newC > prevC) and (newR > prevR):
                while (newC != prevC + 1) and (newR != prevR + 1):
                    prevR += 1
                    prevC += 1
                    print("Checking: " + str(prevR) + "," + str(prevC))
                    print(self.board[prevR][prevC].returnType())
                    if (self.board[prevR][prevC].returnType() != "blank"):
                        return False
                return (newC == prevC + 1) and (newR == prevR + 1)
            # Moving up left
            if (newC < prevC) and (newR < prevR):
                while (newC != prevC - 1) and (newR != prevR -1):
                    prevR -= 1
                    prevC -= 1
                    print("Checking: " + str(prevR) + "," + str(prevC))
                    print(self.board[prevR][prevC].returnType())
                    if (self.board[prevR][prevC].returnType() != "blank"):
                        return False
                return (newC == prevC - 1) and (newR == prevR - 1)
            # Moving down left
            if (newC > prevC) and (newR < prevR):
                while (newC != prevC + 1) and (newR != prevR - 1):
                    prevR -= 1
                    prevC += 1
                    print("Checking: " + str(prevR) + "," + str(prevC))
                    print(self.board[prevR][prevC].returnType())
                    if (self.board[prevR][prevC].returnType() != "blank"):
                        return False
                return (newC == prevC + 1) and (newR == prevR - 1)
        
        # Queen rules - integrated into bishop and rook rules
        
        # King rules
        if (self.pType == "King"):
            if (newC + 1 == prevC ) or (newC - 1 == prevC):
                if (newR + 1 == prevR) or (newR - 1 == prevR):
                    return True
                elif (newR == prevR):
                    return True
            elif (newC == prevC):
                if (newR + 1 == prevR) or (newR - 1 == prevR):
                    return True
            # Castling
            if (prevR + 2 == newR) and (newC == prevC):
                if (self.isInCheck(prevR, prevC)):
                    return False
                for i in range(5, 7):
                        if (self.board[i][newC].returnType() != "blank"):
                            return False
                        if (self.isInCheck(i, newC)):
                            return False
                # Move rook
                if (self.pColor == "White"):
                    if (wKingMoved == True) or (wrRookMoved == True):
                        return False
                    self.board[5][7] = self.board[7][7]
                    self.board[7][7] = ChessPiece("blank", "none")
                else:
                    if (bKingMoved == True) or (brRookMoved == True):
                        return False
                    self.board[5][0] = self.board[7][0]
                    self.board[7][0] = ChessPiece("blank", "none")
                return True
            if (prevR - 2 == newR) and (newC == prevC):
                if (self.isInCheck(prevR, prevC)):
                    return False
                for i in range(1, 4):
                            if (self.board[i][newC].returnType() != "blank"):
                                return False
                            if (self.isInCheck(i, newC)):
                                return False
                # Move rook
                if (self.pColor == "Black"):
                    if (bKingMoved == True) or (blRookMoved == True):
                        return False
                    self.board[2][7] = self.board[0][7]
                    self.board[0][7] = ChessPiece("blank", "none")
                else:
                    if (wKingMoved == True) or (wlRookMoved == True):
                        return False
                    self.board[2][0] = self.board[0][0]
                    self.board[0][0] = ChessPiece("blank", "none")
                return True
            return False
        return False

    def getImage(self, x, y):
        return self.board[x][y].findImage()

    def initializeBoard(self):
        # Black Side
        self.board[0][0] = ChessPiece("Rook", "Black")
        self.board[1][0] = ChessPiece("Knight", "Black")
        self.board[2][0] = ChessPiece("Bishop", "Black")
        self.board[3][0] = ChessPiece("Queen", "Black")
        self.board[4][0] = ChessPiece("King", "Black")
        self.board[5][0] = ChessPiece("Bishop", "Black")
        self.board[6][0] = ChessPiece("Knight", "Black")
        self.board[7][0] = ChessPiece("Rook", "Black")
        self.board[0][1] = ChessPiece("Pawn", "Black")
        self.board[1][1] = ChessPiece("Pawn", "Black")
        self.board[2][1] = ChessPiece("Pawn", "Black")
        self.board[3][1] = ChessPiece("Pawn", "Black")
        self.board[4][1] = ChessPiece("Pawn", "Black")
        self.board[5][1] = ChessPiece("Pawn", "Black")
        self.board[6][1] = ChessPiece("Pawn", "Black")
        self.board[7][1] = ChessPiece("Pawn", "Black")

        # White Side
        self.board[0][7] = ChessPiece("Rook", "White")
        self.board[1][7] = ChessPiece("Knight", "White")
        self.board[2][7] = ChessPiece("Bishop", "White")
        self.board[3][7] = ChessPiece("Queen", "White")
        self.board[4][7] = ChessPiece("King", "White")
        self.board[5][7] = ChessPiece("Bishop", "White")
        self.board[6][7] = ChessPiece("Knight", "White")
        self.board[7][7] = ChessPiece("Rook", "White")
        self.board[0][6] = ChessPiece("Pawn", "White")
        self.board[1][6] = ChessPiece("Pawn", "White")
        self.board[2][6] = ChessPiece("Pawn", "White")
        self.board[3][6] = ChessPiece("Pawn", "White")
        self.board[4][6] = ChessPiece("Pawn", "White")
        self.board[5][6] = ChessPiece("Pawn", "White")
        self.board[6][6] = ChessPiece("Pawn", "White")
        self.board[7][6] = ChessPiece("Pawn", "White")