############################################################################################################

class Grid:
    def __init__(self):
        self.grid = [[0 for i in range(10)] for j in range(20)]
        self.tetromino = None
        self.tetromino_pos = [0, 0]

    def __str__(self):
        prt = ''
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if len(str(self.grid[i][j])) > 1:
                    prt += str(self.grid[i][j][0]) + ' '
                else:
                    prt += str(self.grid[i][j]) + ' '
            prt += '\n'
        return prt + '__________________________________________________________' + '\n'
