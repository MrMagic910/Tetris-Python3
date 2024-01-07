import time
from Grid import *
from Tetromino import *

#############################################################################################################

class Core:
    def __init__(self):
        # Initialize the game with a new grid, no player, and a score of 0
        self.lattice = Grid()
        self.player = None

    def draw(self):
        # Draw the current player on the grid
        for i in range(len(self.player.pattern)):
            for j in range(len(self.player.pattern[i])):
                if self.player.pattern[i][j] == 0:
                    pass
                else:
                    self.lattice.grid[i+self.player.position[0]][j+self.player.position[1]] = self.player.pattern[i][j]
    
    def rmv(self):
        # Remove the current player from the grid
        for i in range(len(self.player.pattern)):
            for j in range(len(self.player.pattern[i])):
                if self.player.pattern[i][j] == 0:
                    pass
                else:
                    self.lattice.grid[i+self.player.position[0]][j+self.player.position[1]] = 0
            
    def checkrotate(self):
        #check if the player can rotate
        self.rmv()
        self.player.rotate_90()
        for y in range(len(self.player.pattern)):
            for x in range(len(self.player.pattern[y])):
                if self.player.position[1]+len(self.player.pattern[0]) > 10 or self.lattice.grid[y+self.player.position[0]][x+self.player.position[1]]!=0 and len(str(self.player.pattern[y][x])) > 1 :
                    self.player.rotate_270()
                    self.draw()
                    return False
        return True
    
    def checkbelow(self, height=0):
        #check if there is a block below the current player
        if self.player.position[0] == 20-len(self.player.pattern):
            return False
        for x in range (len(self.player.pattern[0])):
            y=len(self.player.pattern)-1
            while True:
                if self.player.pattern[y][x] != 0:
                    break
                else:
                    y-=1
            if self.lattice.grid[self.player.position[0]+y+1+height][self.player.position[1]+x] != 0:
                return False
        return True

    def checkleft(self):
        #check if there is a block to the left of the current player
        if self.player.position[1] == 0:
            return False
        for y in range (len(self.player.pattern)):
            x=0
            while True:
                if self.player.pattern[y][x] != 0:
                    break
                else:
                    x+=1
            if self.lattice.grid[self.player.position[0]+y][self.player.position[1]+x-1] != 0:
                return False
        return True
    
    def checkright(self):
        #check if there is a block to the right of the current player
        if self.player.position[1] == 10-len(self.player.pattern[0]):
            return False
        for y in range (len(self.player.pattern)):
            x=len(self.player.pattern[0])-1
            while True:
                if self.player.pattern[y][x] != 0:
                    break
                else:
                    x-=1
            if self.lattice.grid[self.player.position[0]+y][self.player.position[1]+x+1] != 0:
                return False
        return True
    
    def rotate(self):
        # Rotate the player 90 degrees clockwise
        if not self.checkrotate():
            return
        self.draw()

    def fall(self):
        # Move the player down one row
        if not self.checkbelow():
            return False
        else:
            for y in range(len(self.player.pattern)):
                for x in range(len(self.player.pattern[y])):
                    if len(str(self.lattice.grid[y+self.player.position[0]][x+self.player.position[1]])) > 1 and len(str(self.player.pattern[y][x])) > 1:
                        self.lattice.grid[y+self.player.position[0]][x+self.player.position[1]] = 0
            self.player.position[0] += 1
            self.draw()
    
    def mv_left(self):
        # Move the player left one column
        if not self.checkleft():
            return
        for y in range(len(self.player.pattern)):
            for x in range(len(self.player.pattern[y])):
                if len(str(self.lattice.grid[y+self.player.position[0]][x+self.player.position[1]])) > 1 and len(str(self.player.pattern[y][x])) > 1:
                    self.lattice.grid[y+self.player.position[0]][x+self.player.position[1]] = 0
        self.player.position[1] -= 1
        self.draw()
    
    def mv_right(self):
        # Move the player right one column
        if not self.checkright():
            return
        for y in range(len(self.player.pattern)):
            for x in range(len(self.player.pattern[y])):
                if len(str(self.lattice.grid[y+self.player.position[0]][x+self.player.position[1]])) > 1 and len(str(self.player.pattern[y][x])) > 1:
                    self.lattice.grid[y+self.player.position[0]][x+self.player.position[1]] = 0
        self.player.position[1] += 1
        self.draw()

    def start(self,typ=None):
        # Start a new game with a new player
        self.player = Tetromino(typ)
        for i in range(len(self.player.pattern)):
            for j in range(len(self.player.pattern[i])):
                self.lattice.grid[i][j+(10-len(self.player.pattern[0]))//2] = self.player.pattern[i][j]
        self.player.position = [0, (10-len(self.player.pattern[0]))//2]

