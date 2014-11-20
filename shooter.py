from __future__ import division
import pygame
import math
from shooter_utils import *

# initialize pygame
pygame.init()

# set up the screen
width = 800
height = 600
fps = 29
size = (width, height)
screen = pygame.display.set_mode(size)
screenRect = pygame.Rect(0,0,800,600)
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
mousedown = False

bg = GameObject(screen, pygame.image.load("img/bg.png"), Vector(400,300))
player = Player(screen, pygame.image.load("img/blue_player.png"), Vector(400,300))
obstacles = Obstacles(screen)
bullets = []

splatSmallSprites = []
for i in range(1,6):
	splatSmallSprites.append(pygame.image.load("img/splatters/splatter_small_%d.png" % i))

splatBigSprites = []
for i in range(1,6):
	splatBigSprites.append(pygame.image.load("img/splatters/splatter_big_%d.png" % i))

splatters = []


enemies = []
enemySprite = pygame.image.load("img/red_player.png")
for i in range(1,20):
	enemies.append(Enemy(screen, enemySprite, Vector(random.randint(0, 800),random.randint(0, 600)), player))

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
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mousedown = True
		elif event.type == pygame.MOUSEBUTTONUP:
			mousedown = False

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

	for anim in splatters:
		anim.update()
		if anim.dead:
			splatters.remove(anim)

	for enemy in enemies:
		enemy.update()

	for bullet in bullets:
		bullet.update()
		if not screenRect.collidepoint(bullet.pos.getRaw()) or obstacles.isCollide(bullet):
			bullets.remove(bullet)
		else:
			for enemy in enemies:
				if bullet in bullets and bullet.isCollide(enemy):
					enemy.damage()
					splatters.append(Anim(screen, splatSmallSprites, bullet.pos, 4, True))
					bullets.remove(bullet)

	for enemy in enemies:
		if player.isCollide(enemy):
			enemy.health = 0
			player.damage()

	if mousedown:
		bullets.append(Bullet(screen, player.pos, player.facing.unit()))
		# mousedown = player.pickup

	bg.draw()
	obstacles.draw()

	player.draw()

	for anim in splatters:
		anim.draw()

	for enemy in enemies:
		if enemy.health <= 0:
			splatters.append(Anim(screen, splatBigSprites, enemy.pos, 4, True))
			enemies.remove(enemy)
		else:
			enemy.draw()

	for bullet in bullets:
		bullet.draw()

	pygame.display.flip()