import os
import vlc
import time
import threading

SOUND_PATH = "/user_sounds/"
PATH = None

# Create a new instance of the VLC player
instance_test = vlc.Instance()
player_test = instance_test.media_player_new()
instances = []
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
        media = instance_test.media_new(final_name)
        player_test.set_media(media)
        return player_test.will_play()
    except:
        return False


def play_vlc(filename, volume=100, start_time=0, end_time=0, fadeout=0):
    final_name = full_name(filename)

    instance_name = filename + ":" + str(volume)

    print("New instance created for", instance_name)
    # instance = instances[instance_name]
    instance = vlc.Instance()

    # Create a new player
    player = instance.media_player_new()
    players.append(player)

    # Play the media
    media = instance.media_new(final_name)
    player.set_media(media)
    # Set volume using
    player.audio_set_volume(volume)
    player.play()

    if start_time > 0:
        print("Setting start time to", start_time)
        player.set_time(int(start_time * 1000))
    if end_time > 0 and end_time > start_time:
        # Non-blocking timer to stop the player after the end time
        stop_player_thread_instance = threading.Thread(target=stop_player_thread,
                                                       args=(player, end_time - start_time, fadeout))
        stop_player_thread_instance.start()


def stop_player_thread(player, delay, fadeout):
    time.sleep(delay)
    if fadeout > 0:
        fadeout_vlc(fadeout, [player])
    else:
        player.stop()
        players.remove(player)


def stop_vlc():
    for player in players:
        player.stop()
    players.clear()


def fadeout_vlc(delay, fadeout_players=None):
    global players
    if fadeout_players is None:
        fadeout_players = []
        for player in players:
            fadeout_players.append(player)
        players.clear()

    fadeout_vlc_thread_instance = threading.Thread(target=fadeout_vlc_thread, args=(delay, fadeout_players,))
    fadeout_vlc_thread_instance.start()


def fadeout_vlc_thread(delay, fadeout_players):
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
