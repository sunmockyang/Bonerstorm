# BONERSTORM BY SUNMOCK YANG, NOV.20th 2014
# ALL ASSETS USED WITH PERMISSION
# IMAGE ASSETS: RUSSELL BAYLIS - http://imrusty.com/
# 	images are from a gamejam we did together - https://github.com/jahfer/bonestorm
# SOUNDS:
# GUNSHOT (shot.wav) - http://opengameart.org/content/shotgun-shoot-reload
# BACKGROUND SOUND (bg.ogg) - http://soundbible.com/2058-Massive-War-With-Alarm.html
# ENEMY DYING SOUND (monster/*.ogg) - http://opengameart.org/content/monster-sound-pack-volume-1
# PLAYER DAMAGE SOUNDS (player/*.wav) - http://opengameart.org/content/11-male-human-paindeath-sounds


from __future__ import division
import pygame
import math
import random
from shooter_utils import *
from game import *

random.seed()
# initialize pygame
pygame.init()
pygame.mixer.init(44100, 8, 2, 2048)
pygame.mixer.music.load("sound/bg.ogg")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1)

# set up the screen
width = 800
height = 600
size = (width, height)
screen = pygame.display.set_mode(size)
screenRect = pygame.Rect(0,0,800,600)
fps = 29

game = Game(screen)

game.startScreen()
runGame = True
while runGame:
	game.mainGameLoop()

	runGame = game.endScreen()
