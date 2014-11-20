from __future__ import division
import pygame
import math
import random
from shooter_utils import *
from game import *

random.seed()
# initialize pygame
pygame.init()

# set up the screen
width = 800
height = 600
size = (width, height)
screen = pygame.display.set_mode(size)
screenRect = pygame.Rect(0,0,800,600)
fps = 29

game = Game(screen)

runGame = True
while runGame:
	game.startScreen()

	game.mainGameLoop()
