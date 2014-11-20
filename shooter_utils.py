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

	def add(self, vec):
		self.x += vec.x
		self.y += vec.y
		return self

	def addCopy(self, vec):
		return Vector(self.x + vec.x, self.y + vec.y)

	def minusCopy(self, vec):
		return Vector(self.x - vec.x, self.y - vec.y)

	def mult(self, a):
		self.x *= a
		self.y *= a
		return self

	def multCopy(self, a):
		return Vector(self.x * a, self.y * a)

	def isZero(self):
		return (self.x == 0) and (self.y == 0)

	def getRaw(self):
		return (int(self.x), int(self.y))

	def magnitude(self):
		return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

	def unit(self):
		m = self.magnitude()
		return Vector(self.x/m, self.y/m)

	def randomize(self, amount):
		self.x += random.uniform(-amount, amount);
		self.y += random.uniform(-amount, amount);
		return self

class GameObject(object):
	def __init__(self, screen, img, pos):
		super(GameObject, self).__init__()
		self.screen = screen
		self.img = img
		self.pos = pos
		self.rot = 0
		
		if img == None:
			self.rect = pygame.Rect(0,0,0,0)
		else:
			r = self.img.get_rect()
			self.rect = pygame.Rect(pos.x, pos.y, r.width, r.height)

	def moveBy(self, speed):
		self.pos.x += speed.x
		self.pos.y += speed.y
		self.rect.left = self.pos.x
		self.rect.top = self.pos.y

	def getPos(self):
		return (self.rect.left, self.rect.top)

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

	def isCollide(self, gameObject):
		return ((gameObject.radius + self.radius) > gameObject.pos.minusCopy(self.pos).magnitude())


class Bullet(GameObject):
	def __init__(self, screen, pos, speed):
		super(Bullet, self).__init__(screen, None, pos.addCopy(speed.multCopy(10)))
		self.speed = speed
		self.speed.mult(10)
		self.speed.randomize(0.5)
		self.radius = 2
		self.color = (random.randint(230,255), random.randint(220,230), 50)

	def update(self):
		self.moveBy(self.speed)

	def draw(self):
		pygame.draw.line(self.screen, self.color, self.speed.multCopy(-1).addCopy(self.pos).getRaw(), self.pos.getRaw(), self.radius)
		# pygame.draw.circle(self.screen, self.color, self.pos.getRaw(), self.radius)

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
		self.pickup = False
		self.health = 5

	def input(self, inpt):
		self.speed.x += inpt[0] * 2
		self.speed.y += inpt[1] * 2

	def update(self):
		self.moveBy(self.speed)
		self.speed.mult(0.75)

	def stop(self):
		self.speed = Vector(0,0)

	def damage(self):
		self.health -= 1

class Enemy(Player):
	def __init__(self, screen, img, pos, player, speedMag):
		super(Enemy, self).__init__(screen, img, pos)
		self.player = player
		self.health = 2
		self.speedMag = speedMag

	def update(self):
		self.speed = self.player.pos.minusCopy(self.pos).unit().mult(self.speedMag)
		f = self.speed.addCopy(self.pos)
		self.face(f.x, f.y)
		self.moveBy(self.speed)
		# self.speed.mult(0.7)

  	def face(self, x, y):
  		self.facing = Vector(x - self.pos.x, y - self.pos.y)
  		self.rot = -math.atan2(self.facing.x, -self.facing.y) / math.pi * 180

	def draw(self):
  		self.drawImg = pygame.transform.rotate(self.img, self.rot)
  		self.rect = self.drawImg.get_rect()
		self.rect.center = (self.pos.x, self.pos.y)
		self.screen.blit(self.drawImg, self.rect)

class Health():
	def __init__(self, screen, img):
		self.screen = screen
		self.img = img

	def draw(self, health):
		for i in range(0, health):
			self.screen.blit(self.img, pygame.Rect(700 - i*100, 0, 50, 50))
		

class Anim(GameObject):
	def __init__(self, screen, imgs, pos, frameSkip, killAfter = True):
		super(Anim, self).__init__(screen, imgs[0], pos)
		self.screen = screen
		self.imgs = imgs
		self.frame = 0
		self.count = 0
		self.frameSkip = frameSkip
		self.length = len(self.imgs)
		self.killAfter = killAfter
		self.dead = False

	def update(self):
		self.count += 1
		if self.count == self.frameSkip:
			self.count = 0
			self.frame += 1
			if self.killAfter and self.frame >= self.length:
				self.dead = True
				self.frame = 0
			else:
				self.frame %= self.length

			self.img = self.imgs[self.frame]
		

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

	def isCollide(self, gameObject):
		temp = pygame.Rect(self.rect.left - gameObject.radius, self.rect.top - gameObject.radius, self.rect.width + 2*gameObject.radius, self.rect.height + 2*gameObject.radius)
		return temp.collidepoint(gameObject.pos.x + gameObject.speed.x, gameObject.pos.y + gameObject.speed.y)


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
		
		border = 20

		self.walls.append(Wall(screen, 0, 0, 800, border))
		self.walls.append(Wall(screen, 0, 600 - border, 800, border))
		self.walls.append(Wall(screen, 0, 0, border, 600))
		self.walls.append(Wall(screen, 800-border, 0, border, 600))

	def draw(self):
		for wall in self.walls:
			wall.draw()

	def isCollide(self, gameObject):
		for wall in self.walls:
			if wall.isCollide(gameObject):
				return True

		return False