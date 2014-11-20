from __future__ import division
import pygame
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

keydown = {
	pygame.K_UP: False,
	pygame.K_DOWN: False,
	pygame.K_LEFT: False,
	pygame.K_RIGHT: False,
	pygame.K_w: False,
	pygame.K_s: False,
	pygame.K_a: False,
	pygame.K_d: False,
}

bg = GameObject(screen, pygame.image.load("img/bg.png"), Vector(0,0))
player = Player(screen, pygame.image.load("img/blue_player.png"), Vector(400,300))
obstacles = Obstacles(screen)

runGame = True
while runGame:
	clock.tick(fps)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			exit()
		elif event.type == pygame.KEYDOWN:
			keydown[event.key] = True
			if event.key == pygame.K_ESCAPE:
				exit()
		elif event.type == pygame.KEYUP:
			keydown[event.key] = False

	speed = [0,0]
	if keydown[pygame.K_UP] == True or keydown[pygame.K_w] == True:
		speed[1] = -1
	if keydown[pygame.K_DOWN] == True or keydown[pygame.K_s] == True:
		speed[1] = 1
	if keydown[pygame.K_LEFT] == True or keydown[pygame.K_a] == True:
		speed[0] = -1
	if keydown[pygame.K_RIGHT] == True or keydown[pygame.K_d] == True:
		speed[0] = 1

	player.input(speed)

	if obstacles.isCollide(player) and not player.speed.isZero():
		player.stop()
	else:
		player.update()

	mousePos = pygame.mouse.get_pos()
	player.face(mousePos[0], mousePos[1])

	bg.draw()
	obstacles.draw()

	player.draw()

	pygame.display.flip()