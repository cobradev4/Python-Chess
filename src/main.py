#!/usr/bin/python
from tkinter import Tk, Button
from game.chess import Chess

mode = ""

# Setup window
window = Tk()
window.title("Select a Gamemode!")
lpvp = Button(window, width = 15, height = 10, text = "Local PVP", bg = "red", command = lambda: startGame("lpvp"))
cpuA = Button(window, width = 15, height = 10, text = "CPU - Algorithm", bg = "blue", command = lambda: startGame("CPU"))
cpuN = Button(window, width = 15, height = 10, text = "CPU - Neural Network", bg = "green", command = lambda: startGame("NN"))
opvp = Button(window, width = 15, height = 10, text = "Online PVP", bg = "orange", command = lambda: startGame("opvp"))
lpvp.grid()
cpuA.grid()
cpuN.grid(row = 1, column = 1)
opvp.grid(row = 0, column = 1)

def startGame(m):
    global mode
    window.destroy()
    mode = m

# Finalize window
window.mainloop()

# Create game based on mode
if (mode != ""):
    print(mode)
    Chess(mode)