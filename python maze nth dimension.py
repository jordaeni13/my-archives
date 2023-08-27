import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import math
import random
import queue

print("give n that is greater or equal to 3 and less or equal to 9(due to the input limit; this code actually supports up to infinite dimension)")
n_d = int(input())

#predefine colors
topColor = "#75C9C8"
mazeBgColor = "#80A1D4"
endColor = "#C0B9DD"
startColor = "#DED9E2"
normalColor = "#F7F4EA"
blockedColor = "#E3D8B5"
passedColor = "#E8E4F1"
standingColor = "#888888"

class MazeRunner:
    def __init__(self, maze = None, current_position = [0 for _ in range(n_d)]):
        self.maze = maze
        self.current_position = current_position
        self.end_position = None

    def set_end_position(self, position):
        self.end_position = position

    def move(self, dimension, direction):
        mazeSize = len(maze)
        cellMaze[tuple(reversed(self.current_position))].state = 3
        cellMaze[tuple(reversed(self.current_position))].update_color()
        if direction == '1' and self.current_position[dimension-1] < mazeSize - 1:
            print(self.current_position)
            print(dimension-1)

            self.current_position[dimension-1] += 1
            print(self.current_position)
            if maze[tuple(reversed(self.current_position))] == 1:
                self.current_position[dimension-1] -= 1

        elif direction == '0' and self.current_position[dimension-1] > 0:
            self.current_position[dimension-1] -= 1
            if self.maze[tuple(reversed(self.current_position))] == 1:
                self.current_position[dimension-1] += 1
        cellMaze[tuple(reversed(self.current_position))].state = 9
        cellMaze[tuple(reversed(self.current_position))].update_color()
        if np.array_equal(np.array(self.current_position), np.array(self.end_position)):
            messagebox.showinfo("성공", "미로 탈출 성공!")
            self.current_position = [0 for _ in range(n_d)]


jaedorli = MazeRunner()

class Cell:
    def __init__(self, position, state, parent = None):
        self.position = position
        self.state = state
        self.rect = None
        self.visited = False
        self.parent = parent

        self.f = 0
        self.g = 0
        self.h = 0

    def toggle_state(self):
        if self.state == 0:
            self.state = 1
        elif self.state == 1:
            self.state = 0
        self.update_color()
        maze[tuple(reversed(self.position))] = self.state  #update the maze value

    def update_color(self):
        color = None
        if self.state == 0:
            color = normalColor
        elif self.state == 1:
            color = blockedColor
        elif self.state == 2:
            color = passedColor
        elif self.state == 3:
            color = standingColor
        elif self.state == 9:
            color = "#000000"
        elif self.state == 4:
            color = startColor
        elif self.state == -1:
            color = endColor
        canvas.itemconfig(self.rect, fill=color)

#maze generation; coordinates are set to numpy array
def willsonAlgorithm(mazeSize, startPoint = [0 for _ in range(n_d)], endPoint = [-1 for _ in range(n_d)]):
    paddedmaze = np.full(tuple([2*mazeSize-1 for _ in range(n_d)]), 1) #initiate
    start_coord = np.array([random.randint(0, mazeSize-1) for _ in range(n_d)]) #(x,y,z, ...)
    paddedmaze[tuple(reversed(2*start_coord))] = 0
    visited = np.full(tuple([mazeSize for _ in range(n_d)]), False)
    visited[tuple(reversed(start_coord))] = True #unpadded visited list to perform proper algorithm
    
    while not np.all(visited): #ending condition
        current_coord = get_unvisited_cell(visited, mazeSize)
        path = [current_coord]
        visited[tuple(reversed(current_coord))] = True
        
        while visited[tuple(reversed(current_coord))] == False or len(path)==1:
            current_coord = random.choice(get_neighbors(current_coord, mazeSize))
            indices = np.where(np.all(path == current_coord, axis=1))[0]
            print(indices)
            if len(indices) > 0:
                path = path[:indices[0] + 1]  # if the path collides then cut the branch
            else:
                path.append(current_coord)

        
        for i in range(len(path)-1): #connection between two padded plot
            paddedmaze[tuple(reversed(2*path[i]))] = 0
            paddedmaze[tuple(reversed(path[i]+path[i+1]))] = 0
            visited[tuple(reversed(path[i]))] = True
        print()

    #is start and endpoint visitable?
    if not (paddedmaze[tuple(reversed(startPoint))] == 0 and paddedmaze[tuple(reversed(endPoint))] ==0):
        return willsonAlgorithm(mazeSize)
    
    paddedmaze[tuple(reversed(startPoint))] = 4
    paddedmaze[tuple(reversed(endPoint))] = -1
    print_maze(paddedmaze)
    return paddedmaze

def get_unvisited_cell(visited, mazeSize):
    while True:
        current_coord = np.array([random.randint(0, mazeSize-1) for _ in range(n_d)])
        if not visited[tuple(reversed(current_coord))]:
            return current_coord

def get_neighbors(current_coord, mazeSize):
    current_coord = np.array(current_coord)
    neighbors = []
    for i in range(n_d):
        if current_coord[i] > 0:
            temp = current_coord.copy()
            temp[i] -= 1
            neighbors.append(temp)
        if current_coord[i] < mazeSize - 1:
            temp = current_coord.copy()
            temp[i] += 1
            neighbors.append(temp)
    return neighbors
    

def print_maze(maze):
    pass

jaedorli = MazeRunner()

#initialize maze and render
def makeMaze():
    global maze
    global cellMaze

    cellMaze = np.array([])
    mazeSize = sizeValue.get()
    sizeQueue.put(mazeSize)
    clearMaze()

    maze = willsonAlgorithm((mazeSize+1)//2)

    jaedorli.maze = maze
    jaedorli.set_end_position([mazeSize-1 for _ in range(n_d)])

    cellMaze = np.empty(tuple([mazeSize for _ in range(n_d)]), dtype=object)
    for index in np.ndindex(tuple(np.full((n_d), mazeSize))):
        cellMaze[index] = Cell(tuple(reversed(index)), maze[index])

    renderMaze(mazeSize)

def clearMaze():
    prevMazeSize = sizeQueue.get()
    for index in np.ndindex(tuple(np.full((n_d), prevMazeSize))):
        cell = Cell(tuple(reversed(index)), 0)
        del cell

def renderMaze(mazeSize, current_coord=np.full((n_d), 0)):
    cellSize = 75*(-math.log10((2*mazeSize)-6)+2)  #using log to resize a cell's size

    #adjust the size of the frames
    menuFrame.config(width=cellSize*mazeSize)
    mainFrame.config(width=cellSize*mazeSize, height=cellSize*mazeSize)
    canvas.config(width=cellSize*mazeSize, height=cellSize*mazeSize)
    current_coord_modified = tuple(reversed(current_coord[2:]))

    for i in range(mazeSize): # row (y ~ y+1)
        for j in range(mazeSize): # column (x ~ x+1)
            cell = cellMaze[current_coord_modified+(i, j)]
            cell.rect = canvas.create_rectangle(i*cellSize, j*cellSize, (i+1)*cellSize, (j+1)*cellSize, fill=normalColor, outline="")
            canvas.tag_bind(cell.rect, '<Button-1>', lambda e, cell=cell: cell.toggle_state())
            cell.update_color()



def autoSolve(startPoint=tuple([0 for _ in range(n_d)]), endPoint=tuple([-1 for _ in range(n_d)])):
    for cell in np.nditer(cellMaze, flags=['refs_ok']):
        if cell[()].state == 2:
            cell[()].state = 0
            cell[()].update_color()

    start = cellMaze[tuple(reversed(startPoint))]
    end = cellMaze[tuple(reversed(endPoint))]

    open_list = []
    closed_list = []

    open_list.append(start)

    while len(open_list) > 0:
        current_cell = min(open_list, key=lambda o:o.g + o.h)
        open_list.remove(current_cell)
        closed_list.append(current_cell)

        if current_cell == end:
            path = []
            while current_cell.parent is not None:
                current_cell.state=2
                current_cell.update_color()
                path.append(current_cell.position)
                current_cell = current_cell.parent
            
            end.state = -1
            end.update_color()
            print(path[::-1])
            return True
        

        for cell in get_neighbors(current_cell.position, len(maze[0])):
            cell = cellMaze[tuple(reversed(cell))]
            if cell.state == 1:  #ignore cells that are walls
                continue
            if cell not in closed_list:
                if cell in open_list:
                    new_g = current_cell.g + 1
                    if cell.g > new_g:
                        cell.g = new_g
                        cell.parent = current_cell
                else:
                    cell.g = current_cell.g + 1
                    cell.h = sum(abs(np.array(cell.position) - np.array(end.position)))
                    cell.parent = current_cell
                    open_list.append(cell)
    return False


sizeQueue = queue.Queue() #a variable that stores previous size to perform clearMaze
sizeQueue.put(5)

root = tk.Tk()


menuFrame = tk.Frame(root, width=600, height=30)
menuFrame.pack() 
subMenuFrame = tk.Frame(menuFrame, bg=topColor)
subMenuFrame.place(x=0, y=0, relwidth=1, relheight=1)
mainFrame = tk.Frame(root, width = 600, height = 600, bg=mazeBgColor)
mainFrame.pack()
canvas = tk.Canvas(mainFrame, width= 600, height= 600)
canvas.pack()


##below block is for modifying col and row size // autosolve
sizeValue = tk.IntVar()

sizeValue.set(5)  #set initial value of colValue to 5

s = ttk.Style()
s.configure('.', font=('Inter', 14))
sizeModifier = ttk.Spinbox(subMenuFrame, from_=5, to=21, increment=2, textvariable=sizeValue, width=5, justify="center", command=makeMaze)
sizeModifier.grid(row=0, column=0)

autoSolveBtn = ttk.Button(subMenuFrame, text="Auto Solve", command=autoSolve)
autoSolveBtn.grid(row=0, column=1)

antiFocusBtn = ttk.Button(subMenuFrame, text="Anti Focus on Spinbox")
antiFocusBtn.grid(row=0, column=2)
root.focus_force()

makeMaze()

current_selection_of_dimension = 1

def key(event):
    global current_selection_of_dimension
    if event.keysym == 'bracketleft':
        jaedorli.move(current_selection_of_dimension, '0')
        renderMaze(sizeValue.get(), jaedorli.current_position)
    elif event.keysym == 'bracketright':
        jaedorli.move(current_selection_of_dimension, '1')
        renderMaze(sizeValue.get(), jaedorli.current_position)
    elif int(event.keysym) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]:
        current_selection_of_dimension = int(event.keysym)
    
    print(current_selection_of_dimension)
    print(jaedorli.current_position)

jaedorli = MazeRunner(maze)
jaedorli.set_end_position(tuple([sizeValue.get()-1 for _ in range(n_d)]))

root.bind('<Key>', key)

root.mainloop()