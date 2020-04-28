#!/usr/bin/python

from tkinter import Tk, Button, Toplevel
from tkinter.ttk import Frame, Label, Style
from PIL import Image, ImageTk
from ChessPiece import *
from Board import *
from CPU import *

#Global variables for tile interaction
numClicked = 0
prevBG = ""
gameOver = False
prevR, prevC, newR, newC = -1, -1, -1, -1

class Chess(object):
 
    def __init__(self, mode):
        self.b = Board()
        self.gm = mode
        self.c = CPU()
        self.setupWindow()
        self.loadWindowItems()
        self.window.mainloop()
    
    def setupWindow(self):
        self.window = Tk()
        self.window.title("Chess - White's Turn")
        self.window.geometry("1000x1000")   
        self.window.resizable(False, False)

    def tileClick(self, r, c): 
        global numClicked, prevR, prevC, newR, newC, prevBG, gameOver
        print(str(r) + "," + str(c) + " has been clicked!")
        numClicked += 1
        if (numClicked == 1):
            prevR = r
            prevC = c
            # Highlight chosen tile
            prevBG = self.tileMatrix[r][c].cget("bg")
            self.tileMatrix[r][c].configure(bg = "yellow")
        if (numClicked == 2):
            newR = r
            newC = c
            self.b.movePiece(prevR, prevC, newR, newC)
            self.loadMatrix()
            numClicked = 0
            # Reset highlighted background
            self.tileMatrix[prevR][prevC].configure(bg = prevBG)
            # Perform actions based on which turn it is
            print(str(self.b.checkTurn()))
            if (self.b.checkTurn() == 0):
                self.window.title("Chess - White's Turn")
            else:
                self.window.title("Chess - Black's Turn")
                if (self.gm == "CPU" and gameOver == False and self.b.checkWin() == ""): # Have to check for a win to stop program from freezing
                    self.window.title("CPU Calculating...")
                    self.c.playMove(self.b.getBoard())
                    self.tileClick(self.c.getxChoiceI(), self.c.getyChoiceI())
                    self.tileClick(self.c.getxChoiceN(), self.c.getyChoiceN())
            # Check for wins
            if (self.b.checkWin() == "Black"):
                self.window.title("Game Over - Black Wins!")
                for x in range(8):
                    for y in range(8):
                        self.tileMatrix[x][y]["state"] = "disabled"
                gameOver = True
            elif (self.b.checkWin() == "White"):
                self.window.title("Game Over - White Wins!")
                for x in range(8):
                    for y in range(8):
                        self.tileMatrix[x][y]["state"] = "disabled"
                gameOver = True
        # Search for pawn upgrades
        if (self.b.searchForPawnUpgrade("White") > -1):
            self.upgradePawn(self.b.searchForPawnUpgrade("White"), 0, "White")
        elif (self.b.searchForPawnUpgrade("Black") > -1):
            self.upgradePawn(self.b.searchForPawnUpgrade("Black"), 7, "Black")

    def upgradePawn(self, x, y, c):
        self.colorPieceList = []
        # Save x value so it can be grabbed later
        for i in range(len(self.b.getDestroyedPieces())):
            if (self.b.getDestroyedPieces()[i].returnColor() == c):
                self.colorPieceList.append(self.b.getDestroyedPieces()[i])
        self.onlyPawns = True
        for i in range(len(self.colorPieceList)):
            if (self.colorPieceList[i].returnType() != "blank") and (self.colorPieceList[i].returnType() != "Pawn"):
                self.onlyPawns = False
        if not (self.onlyPawns):
            self.upgradeW = Toplevel()
            self.upgradeW.title('Pawn Upgrade')
            self.destroyedTileList = [Button(self.upgradeW, width = 10, height = 5, bg = "red") for x in range(0, len(self.colorPieceList))]
            print(len(self.destroyedTileList))
            self.completeImageList = [ImageTk.PhotoImage(Image.open("./images/noneblank.png")) for x in range(0, len(self.colorPieceList))]
            if (len(self.colorPieceList) > 0):
                for i in range(0, len(self.colorPieceList)):
                    if (self.colorPieceList[i].returnType() != "Pawn"):
                        self.imageLocation = self.colorPieceList[i].findImage()
                        print("\n" + self.imageLocation)
                        self.completeImageList[i] = ImageTk.PhotoImage(Image.open(self.imageLocation).resize((40, 40), Image.ANTIALIAS))
                        self.destroyedTileList[i].grid()
                        self.destroyedTileList[i].configure(image = self.completeImageList[i], width = 60, height = 60)
                        self.destroyedTileList[i].configure(command = lambda x=x, y=y, i=i: self.doPawnUpgrade(x, y, self.colorPieceList[i].returnType()))
                
    def doPawnUpgrade(self, x, y, t):
        self.b.upgradePawn(x, y, t)
        self.loadWindowItems()
        self.upgradeW.destroy()

    def loadWindowItems(self):
        # Tile Matrix (Setup chess board)
        self.tileMatrix = [[Button(self.window, width = 20, height = 10) for x in range(8)] for y in range(8)] # create matrix of chess squares
        self.index = 1
        for r in range(8):
            for c in range(8):
                # Alternate background colors
                if (self.index % 2 != 0):
                    self.tileMatrix[r][c].configure(bg = "gray")
                else:
                    self.tileMatrix[r][c].configure(bg = "brown")
                self.tileMatrix[r][c].configure(activebackground = "yellow") # For mouse hovering
                self.tileMatrix[r][c].place(x=r*125, y=c*125)
                self.index += 1
            self.index += 1 
        self.loadMatrix()

    def loadMatrix(self): # updates gui from board matrix
        self.pieceImage = [[ImageTk.PhotoImage(Image.open("./images/noneblank.png")) for x in range(8)] for y in range(8)]
        for r in range(8):
            for c in range(8):
                self.location = self.b.getImage(r, c)
                self.pieceImage[r][c] = ImageTk.PhotoImage(Image.open(self.location).resize((80, 80), Image.ANTIALIAS))
                #print("Loading image: " + self.location)
                if (self.b.getImage(r,c) != "./images/noneblank.png"):
                    self.tileMatrix[r][c].configure(image = self.pieceImage[r][c], width = 120, height = 120)
                else:
                    self.tileMatrix[r][c].configure(image = '', width = 20, height = 10)
                self.tileMatrix[r][c].configure(command = lambda c=c, r=r: Chess.tileClick(self, r, c)) # https://stackoverflow.com/questions/17677649/tkinter-assign-button-command-in-loop-with-lambda