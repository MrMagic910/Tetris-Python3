import random

#############################################################################################################
# Colors #

black = (0,0,0)
white = (255, 255, 255)
red = (255, 0, 0)
orange = (240, 135, 80)
yellow = (255, 240, 0)
cyan = (115, 250, 250)
blue = (255, 0, 0)
purple = (115, 25, 125)

#############################################################################################################
# Tetris code #

class Tetromino:
    red = '#b4343b'
    orange = '#b36332'
    yellow = '#b39932'
    cyan = '#31b283'
    blue = '#503fa5'
    purple = '#a43d9a'
    green = '#82b331'

    tiles = {
        'I': [[[1, cyan], [1, cyan], [1, cyan], [1, cyan]]],
        'J': [[[1, blue], 0, 0], [[1, blue], [1, blue], [1, blue]]],
        'L': [[0, 0, [1, orange]], [[1, orange], [1, orange], [1, orange]]],
        'O': [[[1, yellow], [1, yellow]], [[1, yellow], [1, yellow]]],
        'S': [[0, [1, green], [1, green]], [[1, green], [1, green], 0]],
        'T': [[0, [1, purple], 0], [[1, purple], [1, purple], [1, purple]]],
        'Z': [[[1, red], [1, red], 0], [0, [1, red], [1, red]]]
    }
    tiles_num = ['I','J','L','O','S','T','Z']

    def __init__(self,typ=None):
        if typ==None:
            self.pattern = random.choice(list(self.tiles.values()))
        else:
            self.pattern = self.tiles[self.tiles_num[typ]]
        self.position = [0, 0]

    def rtrntile(self,tilenum):
        return self.tiles_num[tilenum]

    def __str__(self):
        pattern_str = ''
        for i in range(len(self.pattern)):
            for j in range(len(self.pattern[0])):
                if len(str(self.pattern[i][j]))>1:
                    pattern_str += str(self.pattern[i][j][0])+' '
                else:
                    pattern_str += '  '
            pattern_str += '\n'
        return pattern_str

        
    def rotate_90(self):
        list_of_tuples = zip(*self.pattern[::-1])
        self.pattern= [list(elem) for elem in list_of_tuples]

    def rotate_270(self):
        list_of_tuples = zip(*self.pattern)
        self.pattern= [list(elem) for elem in list_of_tuples][::-1]
    
    def rotate_180(self):
        self.rotate_90()
        self.rotate_90()


def test():
    t = Tetromino()
    print(t)
    t.rotate_90()
    print(t)
    t.rotate_270()
    print(t)
    t.rotate_180()
    print(t)
