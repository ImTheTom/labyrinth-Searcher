import os
import pygame
from labyrinth_generator import generate
from random import randint
from time import time, sleep
import mazeFinder

BLOCKSIZE = 16
WIDTH = 590
HEIGHT = 480

DELAY = 20

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


# Class for the orange dude
class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)

    @property
    def position(self):
        return self.rect.x, self.rect.y


# Nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], BLOCKSIZE, BLOCKSIZE)


def setup(width,height):
    global walls, player, clock, end_rect, screen
    # Initialise pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # Set up the display
    pygame.display.set_caption("Wait for the program to calculate the route")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    walls = []
    level = generate(width,height)
    
    x = y = 0
    for row in level:
        for col in row:
            if col == "W":
                Wall((x, y))
            elif col == "E":
                end_rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)
            elif col == "P":
                player = Player(x, y)
            x += BLOCKSIZE
        y += BLOCKSIZE
        x = 0

    return screen, clock, walls, player, end_rect

def playOut(actions, called):
    if not (called):
        for action in actions:

            if(action == "Move Up"):
                player.rect.y -= BLOCKSIZE
            elif(action == "Move Down"):
                player.rect.y += BLOCKSIZE
            elif(action == "Move Right"):
                player.rect.x += BLOCKSIZE
            elif(action == "Move Left"):
                player.rect.x -= BLOCKSIZE

            updateScreen(player, end_rect, walls)
            sleep(0.1)
    return True


def updateScreen(player, end_rect, walls):
    screen.fill(BLACK)
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall.rect)
    pygame.draw.rect(screen, RED, end_rect)
    pygame.draw.rect(screen, GREEN, player.rect)
    pygame.display.flip()

def recordResutls(time, width, height, method,filterActionsValue):
    string = "Solver took "+str(time)+", for " +str(width)+" by "+str(height)+" maze using method ID "+str(method)+" with filter actions set to "+str(filterActionsValue) +"\n\r"
    f= open("results.txt","a")
    f.write(string)
    f.close()

    

def game(method, filterActionsValue, width,height):
    setup(width,height)
    running = True
    called = False
    updateScreen(player, end_rect, walls)
    t0 = time()
    path = mazeFinder.findSolution(method,filterActionsValue,player, end_rect, walls)
    t1 = time()
    totalTime = t1-t0
    print ("Solver took ",totalTime, ' seconds')
    recordResutls(totalTime, width, height, method, filterActionsValue)
    pygame.display.set_caption("Press space to start the route")
    while running:

        clock.tick(5)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
                pygame.quit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
                pygame.quit()

        updateScreen(player, end_rect, walls)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            pygame.display.set_caption("Following route")
            called = playOut(path,called)
            running = False
            pygame.quit()
        

if __name__ == '__main__':
    game()
