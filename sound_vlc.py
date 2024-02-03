import os
import vlc
import time
import threading

SOUND_PATH = "/user_sounds/"
PATH = None

# Create a new instance of the VLC player
instance = vlc.Instance()
player_test = instance.media_player_new()
players = []


def init(path_in):
    global PATH
    PATH = path_in


def full_name(filename):
    name = PATH + SOUND_PATH + filename
    if PATH.find('\\') > 0:
        name = name.replace('/', '\\')
    return name


def is_valid(filename):
    final_name = full_name(filename)
    try:
        media = instance.media_new(final_name)
        player_test.set_media(media)
        return True
    except:
        return False


def play_vlc(filename, volume=100):
    final_name = full_name(filename)
    # Create a new instance of the VLC player
    player = instance.media_player_new()
    players.append(player)

    # Play the media
    media = instance.media_new(final_name)
    player.set_media(media)
    player.audio_set_volume(int(volume))
    player.play()


def stop_vlc():
    for player in players:
        player.stop()
    players.clear()


def fadeout_vlc(delay):
    global players
    fadeout_players = []
    for player in players:
        fadeout_players.append(player)
    players.clear()
    fadeout_vlc_thread_instance = threading.Thread(target=fadeout_vlc_thread, args=(delay,fadeout_players,))
    fadeout_vlc_thread_instance.start()


def fadeout_vlc_thread(delay,fadeout_players):
    delay = delay / 1000
    fadeout_start_time = time.time()
    current_volumes = [playerI.audio_get_volume() for playerI in fadeout_players]
    while time.time() - fadeout_start_time < delay:
        for i, player in enumerate(fadeout_players):
            volume = int((1 - (time.time() - fadeout_start_time) / delay) * current_volumes[i])
            player.audio_set_volume(volume)
        time.sleep(0.01)
    for player in fadeout_players:
        player.stop()

    fadeout_players.clear()

