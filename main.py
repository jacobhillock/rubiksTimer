from pyTwistyScrambler import scrambler333
import pycuber as pc
import pygame
from pygame import (
    QUIT,
    K_r,
    K_q,
    KEYDOWN
)
import sys

pygame.init()
pygame.font.init()

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
                grid[r][c] = 'r'
            elif grid[r][c] == 'r':
                grid[r][c] = 'o'
            elif grid[r][c] == 'w':
                grid[r][c] = 'y'
            elif grid[r][c] == 'y':
                grid[r][c] = 'w'
    
    # print grid (for debugging)
    # for r in grid:
    #     print(r)
    
    return grid, scramble

def draw(grid, scramble):
    # https://www.pygame.org/docs/tut/PygameIntro.html
    # startup for gui

    pixel_size = 40

    height = len(grid) * pixel_size + 1
    width = len(grid[0]) * pixel_size
    size = width, height
    screen = pygame.display.set_mode(size)
    black = pygame.Color(0, 0, 0)
    screen.fill(black)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            cl = grid[i][j]
            color = pygame.Color(0, 0, 0)

            if cl == 'w':
                color = pygame.Color(255, 255, 255)
            elif cl == 'y':
                color = pygame.Color(255, 255, 0)
            elif cl == 'r':
                color = pygame.Color(255, 0, 0)
            elif cl == 'o':
                color = pygame.Color(255, 165, 0)
            elif cl == 'b':
                color = pygame.Color(0, 0, 255)
            elif cl == 'g':
                color = pygame.Color(0, 255, 0)
            
            x = i * pixel_size
            y = j * pixel_size
            l = pixel_size - 1
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
        size = 32
        myfont = pygame.font.SysFont('Nato Mono', size)
        textsurface = myfont.render(scramble_layers[i], True, (255,255,255))

        screen.blit(textsurface, (6*pixel_size + 5, 6*pixel_size + 5 + i*size))

    pygame.display.update()


def main():
    grid, scramble = generate()
    draw(grid, scramble)

    while True:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                keys=pygame.key.get_pressed()
                if keys[K_r]:
                    grid, scramble = generate()
                    draw(grid, scramble)
                if keys[K_q]:
                    sys.exit()

            if event.type == QUIT:
                sys.exit()

if __name__ == "__main__":
    main()
