from __future__ import division
import pygame
import random
import math
from shooter_utils import *

# initialize pygame
pygame.init()

# set up the screen
width = 800
height = 600
fps = 60
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
random.seed()

bg = GameObject(screen, pygame.image.load("img/bg.png"), Vector(0,0))
player = Player(screen, pygame.image.load("img/blue_player.png"), Vector(400,300))

runGame = True
while runGame:
	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			exit()


	mousePos = pygame.mouse.get_pos()
	player.face(mousePos[0], mousePos[1])

	bg.draw()

	player.draw()

	pygame.display.flip()