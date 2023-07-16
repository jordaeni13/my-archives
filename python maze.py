import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import queue

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
    def __init__(self, maze = None, current_position = (0,0)):
        self.maze = maze
        self.current_position = current_position
        self.end_position = None

    def set_end_position(self, position):
        self.end_position = position

    def move_up(self):
        x, y = self.current_position
        if y > 0 and self.maze[y-1][x] != 1:
            self.current_position = (x, y-1)

    def move_down(self):
        x, y = self.current_position
        if y < len(self.maze) - 1 and self.maze[y+1][x] != 1:
            self.current_position = (x, y+1)

    def move_left(self):
        x, y = self.current_position
        if x > 0 and self.maze[y][x-1] != 1:
            self.current_position = (x-1, y)

    def move_right(self):
        x, y = self.current_position
        if x < len(self.maze[0]) - 1 and self.maze[y][x+1] != 1:
            self.current_position = (x+1, y)

    def move(self, direction):
        cellMaze[self.current_position[1]][self.current_position[0]].state = 3
        cellMaze[self.current_position[1]][self.current_position[0]].update_color()
        if direction == 'up':
            self.move_up()
        elif direction == 'down':
            self.move_down()
        elif direction == 'left':
            self.move_left()
        elif direction == 'right':
            self.move_right()
        cellMaze[self.current_position[1]][self.current_position[0]].state = 9
        cellMaze[self.current_position[1]][self.current_position[0]].update_color()
        if self.current_position == self.end_position:
            messagebox.showinfo("성공", "미로 탈출 성공!")
            self.current_position = (0,0)


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
        if self.state != 1:
            self.state = 1
        elif self.state == 1:
            self.state = 0
        self.update_color()
        maze[self.position[1]][self.position[0]] = self.state  #update the maze value


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

#maze generation
def willsonAlgorithm(width, height, startPoint = (0, 0), endPoint = (-1, -1)):
    paddedmaze = [[1] * ( 2*width - 1) for _ in range(2* height -1)] #initiate
    
    start_x = random.randint(0, width - 1)
    start_y = random.randint(0, height - 1)
    paddedmaze[2*start_y][2*start_x] = 0

    visited = [[False] * width for _ in range(height)]
    visited[start_y][start_x] = True #unpadded visited list to perform proper algorithm
    
    while not all(all(row) for row in visited): #ending condition
        x, y = get_unvisited_cell(visited)
        path = [(x, y)]
        visited[y][x] = True
        
        while visited[y][x] == False or len(path)==1:
            x, y = random.choice(get_neighbors(x, y, width, height))
            if (x, y) in path:
                idx = path.index((x, y))
                path = path[:idx + 1] #if the path colides then cut the branch
            else:
                path.append((x, y))
        
        for i in range(len(path)-1): #connection between two padded plot
            x1, y1 = path[i]
            x2, y2 = path[i+1]
            paddedmaze[2*y1][2*x1] = 0
            paddedmaze[y1+y2][x1+x2] = 0
            visited[y1][x1] = True
            visited[y2][x2] = True 

        print()

    #start and endpoint setting
    sx, sy = startPoint
    ex, ey = endPoint
    if not (paddedmaze[sx][sy] == 0 and paddedmaze[ex][ey] ==0):
        return willsonAlgorithm(width, height)
    
    paddedmaze[sy][sx] = 4
    paddedmaze[ey][ex] = -1
    
    return paddedmaze

def get_unvisited_cell(visited):
    height = len(visited)
    width = len(visited[0])
    
    while True:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if not visited[y][x]:
            return x, y

def get_neighbors(x, y, width, height):
    neighbors = []
    if x > 0:
        neighbors.append((x - 1, y))
    if x < width - 1:
        neighbors.append((x + 1, y))
    if y > 0:
        neighbors.append((x, y - 1))
    if y < height - 1:
        neighbors.append((x, y + 1))
    return neighbors

def print_maze(maze):
    for row in maze:
        print(' '.join(map(str,row)))

def makeMaze():
    global maze
    global cellMaze

    cellMaze = []

    mazeSize = [colValue.get(), rowValue.get()]
    sizeQueue.put(mazeSize)
    cellSize = 75*(-math.log10((mazeSize[0]+mazeSize[1])-6)+2)  #using log to resize a cell's size
    clearMaze()

    maze = willsonAlgorithm((mazeSize[0]+1)//2, (mazeSize[1]+1)//2)

    jaedorli.maze = maze
    jaedorli.set_end_position((colValue.get()-1, rowValue.get()-1))

    #adjust the size of the frames
    menuFrame.config(width=cellSize*mazeSize[0])
    mainFrame.config(width=cellSize*mazeSize[0], height=cellSize*mazeSize[1])
    canvas.config(width=cellSize*mazeSize[0], height=cellSize*mazeSize[1])


    for i in range(mazeSize[1]): # row (y ~ y+1)
        row=[]
        for j in range(mazeSize[0]): # column (x ~ x+1)
            cell = Cell((j, i), maze[i][j])
            cell.rect = canvas.create_rectangle(j*cellSize, i*cellSize, (j+1)*cellSize, (i+1)*cellSize, fill=normalColor, outline="")
            canvas.tag_bind(cell.rect, '<Button-1>', lambda e, cell=cell: cell.toggle_state())
            cell.update_color()
            row.append(cell)
        cellMaze.append(row)
    


#clear previous maze to prevent the data corruption 
def clearMaze():
    prevMazeSize = sizeQueue.get()
    for i in range(prevMazeSize[1]):
        for j in range(prevMazeSize[0]):
            cell = Cell((j, i), 0)
            del cell
            canvas.delete("all")

#pathfinding algorithm
def autoSolve(startPoint=(0,0), endPoint=(-1,-1)):

    for row in cellMaze:
        for cell in row:
            if cell.state == 2:
                cell.state = 0
                cell.update_color()

    start = cellMaze[startPoint[1]][startPoint[0]]
    end = cellMaze[endPoint[1]][endPoint[0]]

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
            return print(path[::-1])
        

        for cell in get_neighbors(*current_cell.position, len(maze[0]), len(maze)):
            cell = cellMaze[cell[1]][cell[0]]
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
                    cell.h = abs(cell.position[0] - end.position[0]) + abs(cell.position[1] - end.position[1])
                    cell.parent = current_cell
                    open_list.append(cell)
    return None


sizeQueue = queue.Queue() #a variable that stores previous size to perform clearMaze
sizeQueue.put([9, 9])

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
colValue = tk.IntVar()
rowValue = tk.IntVar()

colValue.set(9)  #set initial value of colValue to 6
rowValue.set(9)  #set initial value of rowValue to 6

s = ttk.Style()
s.configure('.', font=('Inter', 14))
colModifier = ttk.Spinbox(subMenuFrame, from_=9, to=43, increment=2, textvariable=colValue, width=5, justify="center", command=makeMaze)
colModifier.grid(row=0, column=0)

rowModifier = ttk.Spinbox(subMenuFrame, from_=9, to=43, increment=2, textvariable=rowValue, width=5, justify="center", command=makeMaze)
rowModifier.grid(row=0, column=1)

autoSolveBtn = ttk.Button(subMenuFrame, text="Auto Solve", command=autoSolve)
autoSolveBtn.grid(row=0, column=2)

antiFocusBtn = ttk.Button(subMenuFrame, text="Anti Focus on Spinbox")
antiFocusBtn.grid(row=0, column=3)
root.focus_force()

makeMaze()

def key(event):
    if event.keysym == 'Up':
        jaedorli.move('up')
    elif event.keysym == 'Down':
        jaedorli.move('down')
    elif event.keysym == 'Left':
        jaedorli.move('left')
    elif event.keysym == 'Right':
        jaedorli.move('right')


root.bind('<Key>', key)

root.mainloop()