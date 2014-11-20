import pygame
import math
import random
from shooter_utils import *

class Game(object):
	def __init__(self, screen):
		super(Game, self).__init__()
		self.screenRect = pygame.Rect(0,0,800,600)
		self.screen = screen
		self.shootFrames = 4
		self.enemyNum = 0
		self.fps = 29
		self.clock = pygame.time.Clock()

		self.keydown = {
			pygame.K_UP: False,
			pygame.K_DOWN: False,
			pygame.K_LEFT: False,
			pygame.K_RIGHT: False,
			pygame.K_w: False,
			pygame.K_s: False,
			pygame.K_a: False,
			pygame.K_d: False,
		}
		self.mousedown = False

		self.bg = GameObject(self.screen, pygame.image.load("img/bg.png"), Vector(400,300))
		self.player = Player(self.screen, pygame.image.load("img/blue_player.png"), Vector(400,300))
		self.obstacles = Obstacles(self.screen)
		self.bullets = []

		self.splatSmallSprites = []
		for i in range(1,6):
			self.splatSmallSprites.append(pygame.image.load("img/splatters/splatter_small_%d.png" % i))

		self.splatBigSprites = []
		for i in range(1,6):
			self.splatBigSprites.append(pygame.image.load("img/splatters/splatter_big_%d.png" % i))

		self.splatters = []

		self.enemies = []
		self.enemySprite = pygame.image.load("img/red_player.png")

		self.shootCounter = self.shootFrames

		self.health = Health(self.screen, pygame.image.load("img/heart.png"))

	def Reset(self):
		self.player.pos = Vector(400,300)
		self.obstacles = Obstacles(self.screen)
		self.bullets = []
		self.splatters = []
		self.enemyNum = 1
		self.enemies = []
		self.shootCounter = self.shootFrames

	def EnemySpawn(self):
		side = random.randint(0,4)
		if side == 0:
			return Vector(-10, random.randint(0, 600))
		elif side == 1:
			return Vector(random.randint(0, 800), -10)
		elif side == 2:
			return Vector(810, random.randint(0, 600))
		else:
			return Vector(random.randint(0, 800), 610)

	def startScreen(self):
		runGame = True
		while runGame:
			self.clock.tick(self.fps)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					exit()
				elif event.type == pygame.MOUSEBUTTONDOWN:
					return True

			

			pygame.display.flip()

	def mainGameLoop(self):
		runGame = True
		while runGame:
			self.clock.tick(self.fps)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit()
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					exit()
				elif event.type == pygame.KEYDOWN:
					self.keydown[event.key] = True
					if event.key == pygame.K_ESCAPE:
						exit()
				elif event.type == pygame.KEYUP:
					self.keydown[event.key] = False
				elif event.type == pygame.MOUSEBUTTONDOWN:
					self.mousedown = True
				elif event.type == pygame.MOUSEBUTTONUP:
					self.mousedown = False

			speed = [0,0]
			if self.keydown[pygame.K_UP] == True or self.keydown[pygame.K_w] == True:
				speed[1] = -1
			if self.keydown[pygame.K_DOWN] == True or self.keydown[pygame.K_s] == True:
				speed[1] = 1
			if self.keydown[pygame.K_LEFT] == True or self.keydown[pygame.K_a] == True:
				speed[0] = -1
			if self.keydown[pygame.K_RIGHT] == True or self.keydown[pygame.K_d] == True:
				speed[0] = 1

			self.player.input(speed)

			if self.obstacles.isCollide(self.player) and not self.player.speed.isZero():
				self.player.stop()
			else:
				self.player.update()

			mousePos = pygame.mouse.get_pos()
			self.player.face(mousePos[0], mousePos[1])

			for anim in self.splatters:
				anim.update()
				if anim.dead:
					self.splatters.remove(anim)

			for enemy in self.enemies:
				enemy.update()

			for bullet in self.bullets:
				bullet.update()
				if not self.screenRect.collidepoint(bullet.pos.getRaw()) or self.obstacles.isCollide(bullet):
					self.bullets.remove(bullet)
				else:
					for enemy in self.enemies:
						if bullet in self.bullets and bullet.isCollide(enemy):
							enemy.damage()
							self.splatters.append(Anim(self.screen, self.splatSmallSprites, bullet.pos, 4, True))
							self.bullets.remove(bullet)
							if enemy.health == 0:
								self.player.health = self.player.health + 1 if self.player.health < 8 else 8

			for enemy in self.enemies:
				if self.player.isCollide(enemy):
					enemy.health = 0
					self.player.speed.add(enemy.speed.unit().mult(10))
					self.player.damage()

			if self.mousedown:
				if self.shootCounter >= self.shootFrames:
					self.shootCounter = 0
					self.bullets.append(Bullet(self.screen, self.player.pos, self.player.facing.unit()))
				self.shootCounter += 1
					
				# self.mousedown = self.player.pickup
			else:
				self.shootCounter = 0

			self.bg.draw()
			self.obstacles.draw()

			self.player.draw()

			for anim in self.splatters:
				anim.draw()

			for enemy in self.enemies:
				if enemy.health <= 0:
					self.splatters.append(Anim(self.screen, self.splatBigSprites, enemy.pos, 4, True))
					self.enemies.remove(enemy)
				else:
					enemy.draw()
					
			if len(self.enemies) == 0:
				self.enemyNum += 1
				for i in range(0,self.enemyNum):
					self.enemies.append(Enemy(self.screen, self.enemySprite, self.EnemySpawn(), self.player, math.sqrt(self.enemyNum) + 1))


			for bullet in self.bullets:
				bullet.draw()

			self.health.draw(self.player.health)
		
			pygame.display.flip()
			