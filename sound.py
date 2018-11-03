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

def play(filename, volume=100.0):
    final_name = PATH + SOUND_PATH + filename
    try:
        sound = m.Sound(final_name)
        vol = float(volume / 100.0)
        sound.set_volume(vol)
        sound.play()
    except:
        print("[sound] Could not play sound " + final_name)
