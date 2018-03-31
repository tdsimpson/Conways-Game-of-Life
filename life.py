"""
CISC 352: Assignment 3
April 2, 2018
Matthew Rodgers		    10192731
Mitchell Skarupa 	    10197030
Bo Chen          	    10190141
Martin Woo       	    10191152
Taylor Simpson	            10197558
Sean Remedios               10190433

Conway's Game of Life algorithm is determined by its initial sate, requiring no further input.
It is represented on a grid of cells that are alive (coloured), or dead(white). Every cell interacts
with its neighbours, and changes state depending on four rules:

1. Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
"""

#tkinter - a python graphics library
from tkinter import *

root = Tk()

"""Initializing graphics settings"""
root.title("CISC 352 Assignment 3 - Conway's Game of Life")
frame = Frame(root, width=1000, height=1000)
frame.pack()
canvas = Canvas(frame, width=1000, height=1000)
canvas.pack()

#global variable that represents each generation or cycle of life / death
generation = 0

#cell class in which the status of the cell (dead or alive)is tracked. 
class Cell:
    def __init__(self, x, y, i, j):
        #current cell
        self.isAlive = False
        #neighbouring ce;;
        self.nextStatus = None
        self.pos_screen = (x, y)
        self.pos_matrix = (i, j)

    def __str__(self):
        return str(self.isAlive)

    def __repr__(self):
        return str(self.isAlive)

    def switchStatus(self):
        self.isAlive = not self.isAlive


"""
The create graph function creates the board in which the game will exist.
All squares will start off as white (dead).
"""
def create_graph():

    x = 10
    y = 10
    global grid #variable to store the Cell objects
    global rectangles # Variable to store rectangles
    rectangles= []
    grid = []

    #number of columns - the width of the input
    for i in range(len(graph[0])):
        grid.append([])
        rectangles.append([])
        #number of rows - the length of the input (could have used same value as above bc it's square)
        for j in range(len(graph)):
            rect = canvas.create_rectangle(x, y, x+10, y+10, fill="white")
            rectangles[i].append(rect)
            grid[i].append(Cell(x, y, i, j))
            #moving to next column
            x += 10
        #moving the next row
        x = 10
        y += 10


"""
The setInput function loops through the input matrix of 1s and 0s
and marks the visual grid with a blue square if it is alive (1) or
white square if it is dead (0)
"""
def setInput():
    global graph
    for i in range(len(graph)):
        for j in range(len(graph[i])):
            #if the input at a certain locaiton is alive
            if graph[i][j] == '1':
                if i == -1 or j == -1: #index cannot be less than 1
                    raise IndexError
                #if cell is not alive, set it to blue
                if not grid[i][j].isAlive:
                    canvas.itemconfig(rectangles[i][j], fill="blue")
                #swtich the status of the cell from dead to alive
                grid[i][j].switchStatus()
    return


"""
he colourSquares function loops through the grid defined by the cell
and colours the alive squares blue where neccessary and the dead ones white
"""
def colourSquares():
    for i in grid:
        for j in i:
            #if neighour is not the same value as the current cell
            if j.nextStatus != j.isAlive:
                x, y = j.pos_matrix
                #if neighbour is alive
                if j.nextStatus:
                    canvas.itemconfig(rectangles[x][y], fill="blue")
                else:
                    canvas.itemconfig(rectangles[x][y], fill="white")
                j.switchStatus()


"""
The changeStatus function takes in the cell, and if the cell's status changes
in the next gen, return True. If it doesn't, return false.
"""
def changeStatus(cell):
    numberAlive = 0

    #get the position matrix of the cell
    x, y = cell.pos_matrix
    #checking left and right 
    for i in (x-1, x, x+1):
        #checking up and down
        for j in (y-1, y, y+1):
            if i == x and j == y:
                continue
            if i == -1 or j == -1:
                continue
            try:
                if grid[i][j].isAlive:
                    numberAlive += 1
            except IndexError:
                pass
    if cell.isAlive:
        return not(numberAlive == 2 or numberAlive == 3)
    else:
        return numberAlive == 3

"""
The startSim function begins the simulation and stops when the maximum amount
of generations given by the m value has been reached. 
"""
def startSim():

    global m
    global generation

    #loop through grid changing from alive to dead if neccessary
    #by calling change status
    for i in grid:
        for j in i:
            if changeStatus(j):
                j.nextStatus = not j.isAlive
            else:
                j.nextStatus = j.isAlive

    colourSquares()
    global begin_id


    #if the specified generations amount of generations have not yet been reached
    if generation < int(m):
        generation +=1
        print("Generation", generation)
        #recursive call to next generation. 300 is the amount of miliseconds between each generation
        begin_id = root.after(300, startSim)
    else:
        endSim()
    
"""
The endSim funciton is called from startSim and calls root to
stop the simulation. 
"""
def endSim():
    root.after_cancel(begin_id)


"""
The readFile funciton finds the input file from a give folder, assigns the variable
m (amount of generations) from the first line, and creates a global variable called
graph which is a 2D list representing rows and columns. 
"""
def readFile():
    with open("C:\\Users\\taylo\\Desktop\\352Assignment3\\inLife.txt") as f:
        content = f.readlines()

    #strip off the line breaks
    content = [x.strip() for x in content]

    global m
    global graph

    #first line
    m = content[0]

    #all but the first line
    graph = content[1:]
    return


"""
The main file is the starting point of the program and calls other functions
in the neccessary order. 
"""    
def main():

    readFile()
    create_graph()
    setInput()
    startSim()

    #continue to show the visual interface
    root.mainloop()

main()




