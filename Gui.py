# Authors: Yohann Berthomieu--Maliyakkal, Elias Chantemesse
import pygame #python3 -m pip install -U pygame --user
import pygame_gui #pythn3 -m pip install -U pygame --user
from pygame.locals import* 
import time
from Tetromino import *
from Grid import *
from Core import *
import shelve

pygame.init()

pygame.display.set_caption("Tetris")
window_surface = pygame.display.set_mode((875, 770))
background = pygame.Surface((278, 555))
background.fill(pygame.Color('#000000'))
manager = pygame_gui.UIManager((400, 600))
is_running = True

QuitButton = pygame_gui.elements.UIButton(relative_rect=(100, 50),
                                          text="Quit",
                                          manager=manager)

# Define grid properties
grid_width = 10
grid_height = 20
cell_size = 28

# Calculate the starting position of the grid to center it on the screen
grid_start_x = 0
grid_start_y = 0
grid_inbetween = 1

clock = pygame.time.Clock()  # Create a clock object

cell_colors=[[0 for i in range(grid_height)] for j in range(grid_width)]

fall_speed = 1
movement_speed = None
score = 0
level = 0
core = Core()
t_end = time.time() + fall_speed
core.start()
left=K_a
right=K_d
rotate=K_w
down=K_s
drop=K_SPACE
frame_count = 0
lines=0
cnt=0
I=0
J=0
L=0
O=0
S=0
T=0
Z=0
bg = pygame.image.load('preview.png')
next=random.randint(0,6)
d = shelve.open('score.txt')
highscore = d['score']  # the score is read from disk
d.close()

def scorcnt():
            global score
            global cnt
            full_lines = []
            full_line_count=0
            for i in range(grid_height):
                if all(len(str(cell)) > 1 for cell in core.lattice.grid[i]):
                    full_lines.append(i)
                    full_line_count+=1
            global lines
            lines+=full_line_count
            cnt += full_line_count
            if full_line_count == 1:
                score += 40 * (level + 1)
            elif full_line_count == 2:
                score += 100 * (level + 1)
            elif full_line_count == 3:
                score += 300 * (level + 1)
            elif full_line_count == 4:
                score += 1200 * (level + 1)

            if full_lines:
                for line in full_lines:
                    for i in range(line, 0, -1):
                        core.lattice.grid[i] = core.lattice.grid[i-1].copy()
                    core.lattice.grid[0] = [0] * grid_width

def start():
    global next
    global I
    global J
    global L
    global O
    global S
    global T
    global Z
    scorcnt()
    core.start(next)
    if next == 0:
        I+=1
    elif next == 1:
        J+=1
    elif next == 2:
        L+=1
    elif next == 3:
        O+=1
    elif next == 4:
        S+=1
    elif next == 5:
        T+=1
    elif next == 6:
        Z+=1
    next=random.randint(0,6)

def quickdrop():
    if core.checkbelow() == False:
        start()
        return 
    core.fall()
    quickdrop()
    

while is_running:
    if frame_count % 60 == 0:
        frame_count = 0

    if cnt % 10 == 0 and lines != 0:
        level+=1
        fall_speed-=0.1
        cnt+=1

    if time.time() > t_end:
        
        couldyounot = False

        if core.player.position[0] == 20-len(core.player.pattern):
            if core.lattice.grid[0][4] != 0 or core.lattice.grid[1][4] != 0:
                print('Game Over')
                break
            scorcnt()
            start()
            couldyounot = True
        elif core.checkbelow() == False:
            if core.lattice.grid[0][4] != 0 or core.lattice.grid[1][4] != 0:
                print('Game Over')
                break
            scorcnt()
            start()
            couldyounot = True
        if not couldyounot:    
            core.fall()
        t_end = time.time() + fall_speed
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
    keys = pygame.key.get_pressed()
    if keys[left]:
        core.mv_left()
    if keys[right]:
        core.mv_right()
    if keys[down]:
        core.fall()
    if keys[drop]:
        quickdrop()
        time.sleep(0.2)
    if keys[rotate]:
        core.rotate()
        time.sleep(0.15)
    
    for i in range(grid_height):
        for j in range(grid_width):
            if core.lattice.grid[i][j] == 0:
                color = '#100000'
            else:
                color = core.lattice.grid[i][j][1]
            try:
                cell_colors[j][i] = pygame.Color(color)
            except:
                pass

    

    # Draw the grid
    for x in range(grid_width):
        for y in range(grid_height):
            pygame.draw.rect(background, cell_colors[x][y], (grid_start_x + x * cell_size, grid_start_y + y * cell_size, cell_size, cell_size), 0)
            pygame.draw.rect(background, pygame.Color('#000000'), (grid_start_x + x * cell_size, grid_start_y + y * cell_size, cell_size, cell_size), 1)

    # Calculate the position where the block would land
    landing_position = core.player.position[0]
    while landing_position != 20 - len(core.player.pattern):
        if core.checkbelow(landing_position-core.player.position[0]) == False:
            break
        landing_position += 1

    # Draw the Tetris block
    for i in range(len(core.player.pattern)):
        for j in range(len(core.player.pattern[i])):
            if core.player.pattern[i][j] != 0 and core.player.position[1]+j < grid_width and core.lattice.grid[landing_position+i][core.player.position[1]+j] == 0:
                dim_color = '#d6d6d6'
                pygame.draw.rect(background, dim_color, (grid_start_x + (core.player.position[1] + j) * cell_size, grid_start_y + (landing_position + i) * cell_size, cell_size, cell_size), 0)
                pygame.draw.rect(background, pygame.Color('#000000'), (grid_start_x + (core.player.position[1] + j) * cell_size, grid_start_y + (landing_position + i) * cell_size, cell_size, cell_size), 1)

    font = pygame.font.Font(None, 40)
    

    # Clear the screen
    window_surface.fill((0, 0, 0))
    window_surface.blit(bg, (0, 0))
    # Create a Surface with the score text
    score_text = font.render('SCORE', True, (255, 255, 255))
    points_text = font.render(f'{score:06}', True, (255, 255, 255))
    highscore_text = font.render('HIGHSCORE', True, (255, 255, 255))
    highscore_text2 = font.render(f'{highscore:06}', True, (255, 255, 255))
    tile=Tetromino(next)
    next_text = font.render('NEXT', True, (255, 255, 255))
    lines2 = f'{lines:03}'
    lines_text = font.render(f'LINES - {lines2}', True, (255, 255, 255))
    level_text = font.render('LEVEL', True, (255, 255, 255))
    lvl_txt = font.render(f'{level}', True, (255, 255, 255))
    statistics = font.render('STATISTICS', True, (255, 255, 255))
    I_text = font.render(f'{I:03}', True, (255, 255, 255))
    J_text = font.render(f'{J:03}', True, (255, 255, 255))
    L_text = font.render(f'{L:03}', True, (255, 255, 255))
    O_text = font.render(f'{O:03}', True, (255, 255, 255))
    S_text = font.render(f'{S:03}', True, (255, 255, 255))
    T_text = font.render(f'{T:03}', True, (255, 255, 255))
    Z_text = font.render(f'{Z:03}', True, (255, 255, 255))

    # Get the rectangular area of the text
    text_rect = score_text.get_rect()
    points_text_rect = points_text.get_rect()
    highscore_text_rect = highscore_text.get_rect()
    highscore_text_rect2 = highscore_text2.get_rect()
    next_text_rect = next_text.get_rect()
    lines_text_rect = lines_text.get_rect()
    level_text_rect = level_text.get_rect()
    lvl_txt_rect = lvl_txt.get_rect()
    statistics_rect = statistics.get_rect()
    I_text_rect = I_text.get_rect()
    J_text_rect = J_text.get_rect()
    L_text_rect = L_text.get_rect()
    O_text_rect = O_text.get_rect()
    S_text_rect = S_text.get_rect()
    T_text_rect = T_text.get_rect()
    Z_text_rect = Z_text.get_rect()

    # Position the text at the top right corner
    text_rect.topleft = (663, 169)
    points_text_rect.topleft = (663, 209)
    highscore_text_rect.topleft = (658, 60)
    highscore_text_rect2.topleft = (658, 100)
    next_text_rect.topleft = (663, 329)
    lines_text_rect.topleft = (390, 57)
    level_text_rect.topleft = (687, 520)
    lvl_txt_rect.center = (731, 566)
    statistics_rect.topleft = (84, 225)
    I_text_rect.topleft = (184, 275)
    J_text_rect.topleft = (184, 345)
    L_text_rect.topleft = (184, 403)
    O_text_rect.topleft = (184, 461)
    S_text_rect.topleft = (184, 523)
    T_text_rect.topleft = (184, 583)
    Z_text_rect.topleft = (184, 642)

    # Blit the text onto the screen
    window_surface.blit(score_text, text_rect)
    window_surface.blit(points_text, points_text_rect)
    window_surface.blit(highscore_text, highscore_text_rect)
    window_surface.blit(highscore_text2, highscore_text_rect2)
    window_surface.blit(next_text, next_text_rect)
    window_surface.blit(lines_text, lines_text_rect)
    window_surface.blit(level_text, level_text_rect)
    window_surface.blit(lvl_txt, lvl_txt_rect)
    window_surface.blit(statistics, statistics_rect)
    window_surface.blit(I_text, I_text_rect)
    window_surface.blit(J_text, J_text_rect)
    window_surface.blit(L_text, L_text_rect)
    window_surface.blit(O_text, O_text_rect)
    window_surface.blit(S_text, S_text_rect)
    window_surface.blit(T_text, T_text_rect)
    window_surface.blit(Z_text, Z_text_rect)


    # Define the dimensions of the second grid
    second_grid_width = 3
    second_grid_height = 4

    # Define the new position of the second grid
    second_grid_x = 670  # Adjust the x-coordinate as desired
    second_grid_y = 354  # Adjust the y-coordinate as desired

    # Create a new surface for the second grid
    second_grid_surface = pygame.Surface((second_grid_width * cell_size, second_grid_height * cell_size))

    # Draw the second grid on the second grid surface
    for x in range(second_grid_width):
        for y in range(second_grid_height):
            pygame.draw.rect(second_grid_surface, pygame.Color('#000000'), (x * cell_size, y * cell_size, cell_size, cell_size), 1)

    # Draw the next Tetris block on the second grid surface
    for i in range(len(tile.pattern)):
        for j in range(len(tile.pattern[i])):
            if tile.pattern[i][j] != 0 and tile.position[1]+j < second_grid_width and tile.pattern[i][j] != 0:
                pygame.draw.rect(second_grid_surface, pygame.Color(tile.pattern[i][j][1]), (j * cell_size, i * cell_size, cell_size, cell_size), 0)
                pygame.draw.rect(second_grid_surface, pygame.Color('#000000'), (j * cell_size, i * cell_size, cell_size, cell_size), 1)

    # Blit the second grid surface onto the main window surface at the new position
    window_surface.blit(second_grid_surface, (second_grid_x, second_grid_y))


    third_grid_width = 4
    third_grid_height = 20
    third_cell_size = 20

    # Define the new position of the third grid
    third_grid_x = 84  # Adjust the x-coordinate as desired
    third_grid_y = 275  # Adjust the y-coordinate as desired

    # Create a new surface for the third grid
    third_grid_surface = pygame.Surface((third_grid_width * third_cell_size, third_grid_height * third_cell_size))

    # Draw the third grid on the third grid surface
    for x in range(third_grid_width):
        for y in range(third_grid_height):
            pygame.draw.rect(third_grid_surface, pygame.Color('#000000'), (x * third_cell_size, y * third_cell_size, third_cell_size, third_cell_size), 1)

    # Draw each Tetromino on the third grid surface
    tetrominos = [Tetromino(0), Tetromino(1), Tetromino(2), Tetromino(3), Tetromino(4), Tetromino(5), Tetromino(6)]
    for i, tetromino in enumerate(tetrominos):
        for j in range(len(tetromino.pattern)):
            for k in range(len(tetromino.pattern[j])):
                if tetromino.pattern[j][k] != 0:
                    pygame.draw.rect(third_grid_surface, pygame.Color(tetromino.pattern[j][k][1]), (k * third_cell_size, (j + i * 3) * third_cell_size, third_cell_size, third_cell_size), 0)
                    pygame.draw.rect(third_grid_surface, pygame.Color('#000000'), (k * third_cell_size, (j + i * 3) * third_cell_size, third_cell_size, third_cell_size), 1)

    # Blit the third grid surface onto the main window surface at the new position
    window_surface.blit(third_grid_surface, (third_grid_x, third_grid_y))


    window_surface.blit(background, (325, 133))
    frame_count += 1
    pygame.display.update()
    clock.tick(12)  # Limit the frame rate to 60 FPS

d = shelve.open('score.txt')  # here you will save the score variable   
if score > highscore:  # if current score is more than the highscore that we had
    d['score'] = score            # thats all, now it is saved on disk.
d.close()