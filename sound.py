import pygame
from time import sleep

PATH = None
SOUND_PATH = "/user_sounds/"

import pygame

m = pygame.mixer

def init(path_in):
    global PATH
    PATH = path_in

    m.init()

def play(filename):
    m.Sound(PATH + SOUND_PATH + filename).play()
