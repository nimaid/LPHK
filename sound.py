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
    final_name = PATH + SOUND_PATH + filename
    try:
        m.Sound(final_name).play()
    except:
        print("[sound] Could not play sound " + final_name)
