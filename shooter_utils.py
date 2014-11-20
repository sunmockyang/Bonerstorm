import pygame
import math
import random

random.seed()

class Vector(object):
	def __init__(self, x, y):
		super(Vector, self).__init__()
		self.x = x
		self.y = y
	def __str__(self):
		return "[x: %f, y: %f]" % (self.x, self.y)

	def mult(self, a):
		self.x *= a
		self.y *= a

	def isZero(self):
		return (self.x == 0) and (self.y == 0)

class GameObject(object):
	def __init__(self, screen, img, pos):
		super(GameObject, self).__init__()
		self.screen = screen
		self.img = img
		self.pos = pos
		self.rot = 0
		
		r = self.img.get_rect()
		self.rect = pygame.Rect(pos.x, pos.y, r.width, r.height)

	def moveTo(self, pos):
		self.pos = pos
		self.rect.left = pos.x
		self.rect.top = pos.y

	def moveBy(self, speed):
		self.pos.x += speed.x
		self.pos.y += speed.y
		self.rect.left = self.pos.x
		self.rect.top = self.pos.y

	def getPos(self):
		return (self.rect.left, self.rect.top)

	def draw(self):
		self.screen.blit(self.img, self.rect)


class Player(GameObject):
  	def __init__(self, screen, img, pos):
  		super(Player, self).__init__(screen, img, pos)
  		self.screen = screen
  		self.img = img
  		self.pos = pos
  		self.moveTo(pos)
  		self.ammo = 30
  		self.facing = Vector(0, 1)
  		self.rot = 0
		self.radius = 10
		self.speed = Vector(0,0)

	def input(self, inpt):
		self.speed.x += inpt[0]
		self.speed.y += inpt[1]

	def update(self):
		self.moveBy(self.speed)
		self.speed.mult(0.7)

	def stop(self):
		self.speed = Vector(0,0)

  	def face(self, x, y):
  		self.facing = Vector(x - self.pos.x, y - self.pos.y)
  		self.rot = -math.atan2(self.facing.x, -self.facing.y) / math.pi * 180

	def moveTo(self, pos):
		self.pos = pos;
		self.rect.center = (pos.x, pos.y)

	def draw(self):
  		self.drawImg = pygame.transform.rotate(self.img, self.rot)
  		self.rect = self.drawImg.get_rect()
		self.rect.center = (self.pos.x, self.pos.y)
		self.screen.blit(self.drawImg, self.rect)


class Wall(object):
	def __init__(self, screen, x, y, width, height):
		super(Wall, self).__init__()
		self.screen = screen
		self.rect = pygame.Rect(x, y, width, height)

	def draw(self):
		pygame.draw.rect(self.screen, (30,30,30), self.rect, 0)

	def distanceFrom(self, px, py):
		dx = max(abs(px - self.rect.left) - self.rect.width / 2, 0);
		dy = max(abs(py - self.rect.top) - self.rect.height / 2, 0);
		return dx * dx + dy * dy;

	def isCollide(self, player):
		temp = pygame.Rect(self.rect.left - player.radius, self.rect.top - player.radius, self.rect.width + 2*player.radius, self.rect.height + 2*player.radius)
		return temp.collidepoint(player.pos.x + player.speed.x, player.pos.y + player.speed.y)


class Obstacles(object):
	def __init__(self, screen):
		super(Obstacles, self).__init__()
		self.walls = []
		for i in range(0,10):
			self.walls.append(Wall(screen, random.randint(50, 80), i * 75 + 20 + random.randint(-10, 10), random.randint(30,50), random.randint(30,50)))
		for i in range(0,10):
			self.walls.append(Wall(screen, random.randint(670, 700), i * 75 + 20 + random.randint(-10, 10), random.randint(30,50), random.randint(30,50)))
		for i in range(0,10):
			self.walls.append(Wall(screen, i * 80 + 20 + random.randint(-10, 10), random.randint(50, 80), random.randint(30,50), random.randint(30,50)))
		for i in range(0,10):
			self.walls.append(Wall(screen, i * 80 + 20 + random.randint(-10, 10), random.randint(470, 500), random.randint(30,50), random.randint(30,50)))

	def draw(self):
		for wall in self.walls:
			wall.draw()

	def isCollide(self, player):
		for wall in self.walls:
			if wall.isCollide(player):
				return True

		return False