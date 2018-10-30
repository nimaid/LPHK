import pygame, os
from time import sleep

PATH = None
SOUND_PATH = "/user_sounds/"

import pygame

m = pygame.mixer

def init(path_in):
    global PATH
    PATH = path_in

    m.pre_init(44100, -16, 2, 2048)
    m.init()

def play(filename):
    try:
        m.Sound(PATH + SOUND_PATH + filename).play()
        return True
    except:
        return False
