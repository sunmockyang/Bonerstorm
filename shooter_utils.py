import pygame
import math

class Vector(object):
	def __init__(self, x, y):
		super(Vector, self).__init__()
		self.x = x
		self.y = y
	def __str__(self):
		return "[x: %f, y: %f]" % (self.x, self.y)

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




  		