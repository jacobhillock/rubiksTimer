from pyTwistyScrambler import scrambler333
import pycuber as pc
import pygame
import json
from pygame import (
    QUIT,
    K_r,
    K_q,
    KEYDOWN,
    K_SPACE
)
import sys, os, time, datetime

pygame.init()
pygame.font.init()

# constants for the program
FPS = 19
spf = 1 / FPS
FONT_SIZE = 32
PIXEL_SIZE = 40
myfont = pygame.font.SysFont('Nato Mono', FONT_SIZE)

height = 9 * PIXEL_SIZE + 1
width = 12 * PIXEL_SIZE
size = width, height
screen = pygame.display.set_mode(size)

config = {}
with open("config.json") as conf:
    config = json.load(conf)

# generates a scrambled 3x3x3 rubik's cube and save it as a 2d cube net
def generate():
    # create a random scramble according the the WCA scramble algorithm
    scramble = scrambler333.get_WCA_scramble()
    # scramble = scramble.split(" ")
    # print(scramble, len(scramble))


    # Create a Cube object
    mycube = pc.Cube()
    # Scramble the cube according to the wca scamble
    mycube(scramble)

    # convert cube into a sctring for manipulation
    cube_state = str(mycube)
    # split cube string into a grid list
    grid = [[i] for i in cube_state.split("\n")]
    grid.pop(-1)


    # make sure all rows of grid are the same length
    for i in range(len(grid)):
        if(len(grid[i][0]) < 36):
            grid[i][0] += " "*18

    # make grid truly 2d
    for i in range(len(grid)):
        temp = []
        for j in range(12):
            temp.append(grid[i][0][1 + j*3])
        # print(temp)
        grid[i] = temp

    # make scramble as if white is on top (swap orange for red, and yellow for white)
    for r in range(len(grid)):
        for c in range(len(grid[r])):
            if grid[r][c] == 'o':
                grid[r][c] = 'right'
            elif grid[r][c] == 'r':
                grid[r][c] = 'left'
            elif grid[r][c] == 'y':
                grid[r][c] = 'up'
            elif grid[r][c] == 'w':
                grid[r][c] = 'down'
            elif grid[r][c] == 'g':
                grid[r][c] = 'front'
            elif grid[r][c] == 'b':
                grid[r][c] = 'back'
    
    # print grid (for debugging)
    # for r in grid:
    #     print(r)
    
    return grid, scramble

# draws the rubik's cube and shows text based scramble
def draw_cube(grid, scramble):
    # https://www.pygame.org/docs/tut/PygameIntro.html
    # startup for gui

    black = pygame.Color(0, 0, 0)
    screen.fill(black)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            color = config.get(grid[i][j], [0,0,0])

            x = i * PIXEL_SIZE
            y = j * PIXEL_SIZE
            l = PIXEL_SIZE - 1
            rect = pygame.Rect(y, x, l, l)
            pygame.draw.rect(screen, color, rect)

    # pygame.display.update()
    scramble_split = scramble.split(' ')
    scramble_layers = []

    t = ""
    for s in scramble_split:
        t += s + " "
        if len(t) >= 18:
            scramble_layers.append(t)
            t = ""
    scramble_layers.append(t)

    for i in range(len(scramble_layers)):
        textsurface = myfont.render(scramble_layers[i], True, (255,255,255))
        screen.blit(textsurface, (6*PIXEL_SIZE + 5, 6*PIXEL_SIZE + 5 + i*FONT_SIZE))

    pygame.display.update()

    draw_time(0, 0, False)

#
def format_time(time):
    
    m = int(time / 60)
    s = time % 60
    # ss = f"{round(s, 3)}"
    if s < 10:
        s = "0" + f"{round(s, 3)}"
    else:
        s = f"{round(s, 3)}"
    
    return f"{round(m, 0)}:{s}"


def draw_time(t0, t1, started):
    time = "0:00.000"
    if started: 
        net = t1 - t0
        time = format_time(net)

    pygame.draw.rect(screen, (0,0,0), pygame.Rect(6*PIXEL_SIZE+5, PIXEL_SIZE, int(3.4*PIXEL_SIZE), int(.7*PIXEL_SIZE)))

    textsurface = myfont.render(time, True, (255,255,255))
    screen.blit(textsurface, (6*PIXEL_SIZE + 50, PIXEL_SIZE + 3))

    pygame.display.update()

def update_times(time):
    print(round(time, 3))
    now = datetime.datetime.now()
    format_now = now.isoformat().split('T')
    dict_ = {
        'date': format_now[0],
        'timeOfDay': format_now[1].split('.')[0],
        'time': round(time, 3),
        'readable': format_time(time)
        }
    
    directory = os.path.dirname(os.path.realpath(__file__))
    time_folder = "/times/"
    if sys.platform == 'win32':
        time_folder = "\\times\\"
    path = directory + time_folder

    print(path)

    dirs = os.listdir(path)
    f_name = f"{format_now[0]}.csv"
    header = False
    if f_name not in dirs:
        header = True
    with open(f'{path}/{f_name}', 'a') as file_:
        if header:
            file_.write("Date, Time of Day, Time, Readable\n")
        file_.write(f"{dict_['date']}, {dict_['timeOfDay']}, {dict_['time']}, {dict_['readable']}\n")

    print(dict_)


def main():
    t0 = time.time()
    grid, scramble = generate()
    start = False
    draw_cube(grid, scramble)

    while True:
        # Draw the time on the cube screen
        draw_time(t0, time.time(), start)
        fTime0 = time.time()

        # frame rate holding, also where keyboard input happens
        while time.time() - fTime0 < spf:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    keys=pygame.key.get_pressed()
                    new = False
                    if keys[K_SPACE]:
                        if not start:
                            t0 = time.time()
                            start = True
                        else:
                            solve_t = time.time() - t0
                            update_times(solve_t)
                            start = False
                            new = True
                    if keys[K_r] or new:
                        grid, scramble = generate()
                        draw_cube(grid, scramble)
                        new = False
                    if keys[K_q]:
                        sys.exit()

                if event.type == QUIT:
                    sys.exit()

if __name__ == "__main__":
    main()
