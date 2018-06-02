#!/usr/bin/env python
# coding=utf-8
#   Python Script
#
#   Copyright © Manoel Vilela
#
#
from __future__ import print_function
import os
import pygame
from labyrinth_generator import generate
from random import randint
from time import time, sleep
import mazeFinder

BLOCKSIZE = 16
WIDTH = 590
HEIGHT = 480

WHITE = (255, 255, 255)
YELLOW = (255, 200, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)


# Class for the orange dude
class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, BLOCKSIZE, BLOCKSIZE)

    def move(self, dx, dy):
        # Move each axis separately.
        # Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    @property
    def position(self):
        return self.rect.x, self.rect.y


# Nice class to hold a wall rect
class Wall(object):
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], BLOCKSIZE, BLOCKSIZE)


def setup():
    global walls, player, clock, end_rect, screen
    # Initialise pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()

    # Set up the display
    pygame.display.set_caption("Get to the red square!")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()
    walls = []
    level = generate()
    
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

            sleep(1)
    return True


def updateScreen(player, end_rect, walls):
    # Draw the scene
    screen.fill(BLACK)
    for wall in walls:
        pygame.draw.rect(screen, WHITE, wall.rect)
    pygame.draw.rect(screen, RED, end_rect)
    pygame.draw.rect(screen, GREEN, player.rect)
    pygame.display.flip()
    

def game():
    setup()
    running = True
    called = False
    path = mazeFinder.findSolution(player, end_rect, walls)
    while running:

        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False

        # Move the player if an arrow key is pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            player.move(-2, 0)
        if key[pygame.K_RIGHT]:
            player.move(2, 0)
        if key[pygame.K_UP]:
            player.move(0, -2)
        if key[pygame.K_DOWN]:
            player.move(0, 2)
        if key[pygame.K_SPACE]:
            called = playOut(path,called)

        updateScreen(player, end_rect, walls)
        

if __name__ == '__main__':
    game()
