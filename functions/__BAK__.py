            ######################## OLD OLD OLD ########################
            elif split_line[0] == "DELAY":
                print("[scripts] " + coords + "    Delay for " + split_line[1] + " seconds")
                
                delay = float(split_line[1])
                while delay > DELAY_EXIT_CHECK:
                    sleep(DELAY_EXIT_CHECK)
                    delay -= DELAY_EXIT_CHECK
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not is_async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return -1
                if delay > 0:
                    sleep(delay)
            elif split_line[0] == "WEB":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                print("[scripts] " + coords + "    Open website " + link + " in default browser")
                webbrowser.open(link)
            elif split_line[0] == "WEB_NEW":
                link = split_line[1]
                if "http" not in link:
                    link = "http://" + link
                print("[scripts] " + coords + "    Open website " + link + " in default browser, try to make a new window")
                webbrowser.open_new(link)
            elif split_line[0] == "SOUND":
                if len(split_line) > 2:
                    print("[scripts] " + coords + "    Play sound file " + split_line[1] + " at volume " + str(split_line[2]))
                    sound.play(split_line[1], float(split_line[2]))
                else:
                    print("[scripts] " + coords + "    Play sound file " + split_line[1])
                    sound.play(split_line[1])
            elif split_line[0] == "WAIT_UNPRESSED":
                print("[scripts] " + coords + "    Wait for script key to be unpressed")
                while lp_events.pressed[x][y]:
                    sleep(DELAY_EXIT_CHECK)
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not is_async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return idx + 1
            elif split_line[0] == "M_STORE":
                print("[scripts] " + coords + "    Store mouse position")
                m_pos = ms.getXY()
            elif split_line[0] == "M_RECALL":
                if m_pos == tuple():
                    print("[scripts] " + coords + "    No 'M_STORE' command has been run, cannot do 'M_RECALL'")
                else:
                    print("[scripts] " + coords + "    Recall mouse position " + str(m_pos))
                    ms.setXY(m_pos[0], m_pos[1])
            elif split_line[0] == "M_RECALL_LINE":
                x1, y1 = m_pos

                delay = None
                if len(split_line) > 1:
                    delay = float(split_line[1]) / 1000.0

                skip = 1
                if len(split_line) > 2:
                    skip = int(split_line[2])

                if (delay == None) or (delay <= 0):
                    print("[scripts] " + coords + "    Recall mouse position " + str(m_pos) + " in a line by " + str(skip) + " pixels per step")
                else:
                    print("[scripts] " + coords + "    Recall mouse position " + str(m_pos) + " in a line by " + str(skip) + " pixels per step and wait " + split_line[1] + " milliseconds between each step")

                x_C, y_C = ms.getXY()
                points = ms.line_coords(x_C, y_C, x1, y1)
                for x_M, y_M in points[::skip]:
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not is_async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return -1
                    ms.setXY(x_M, y_M)
                    if (delay != None) and (delay > 0):
                        temp_delay = delay
                        while temp_delay > DELAY_EXIT_CHECK:
                            sleep(DELAY_EXIT_CHECK)
                            temp_delay -= DELAY_EXIT_CHECK
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not is_async:
                                    running = False
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return -1
                        if temp_delay > 0:
                            sleep(temp_delay)
            elif split_line[0] == "M_MOVE":
                if len(split_line) >= 3:
                    print("[scripts] " + coords + "    Relative mouse movement (" + split_line[1] + ", " + str(split_line[2]) + ")")
                    ms.moveXY(float(split_line[1]), float(split_line[2]))
                else:
                    print("[scripts] " + coords + "    Both X and Y are required for mouse movement, skipping...")
            elif split_line[0] == "M_SET":
                if len(split_line) >= 3:
                    print("[scripts] " + coords + "    Set mouse position to (" + split_line[1] + ", " + str(split_line[2]) + ")")
                    ms.setXY(float(split_line[1]), float(split_line[2]))
                else:
                    print("[scripts] " + coords + "    Both X and Y are required for mouse positioning, skipping...")
            elif split_line[0] == "M_SCROLL":
                if len(split_line) > 2:
                    print("[scripts] " + coords + "    Scroll (" + split_line[1] + ", " + split_line[2] + ")")
                    ms.scroll(float(split_line[2]), float(split_line[1]))
                else:
                    print("[scripts] " + coords + "    Scroll " + split_line[1])
                    ms.scroll(0, float(split_line[1]))
            elif split_line[0] == "M_LINE":
                x1 = int(split_line[1])
                y1 = int(split_line[2])
                x2 = int(split_line[3])
                y2 = int(split_line[4])

                delay = None
                if len(split_line) > 5:
                    delay = float(split_line[5]) / 1000.0

                skip = 1
                if len(split_line) > 6:
                    skip = int(split_line[6])

                if (delay == None) or (delay <= 0):
                    print("[scripts] " + coords + "    Mouse line from (" + split_line[1] + ", " + split_line[2] + ") to (" + split_line[3] + ", " + split_line[4] + ") by " + str(skip) + " pixels per step")
                else:
                    print("[scripts] " + coords + "    Mouse line from (" + split_line[1] + ", " + split_line[2] + ") to (" + split_line[3] + ", " + split_line[4] + ") by " + str(skip) + " pixels per step and wait " + split_line[5] + " milliseconds between each step")

                points = ms.line_coords(x1, y1, x2, y2)
                for x_M, y_M in points[::skip]:
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not is_async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return -1
                    ms.setXY(x_M, y_M)
                    if (delay != None) and (delay > 0):
                        temp_delay = delay
                        while temp_delay > DELAY_EXIT_CHECK:
                            sleep(DELAY_EXIT_CHECK)
                            temp_delay -= DELAY_EXIT_CHECK
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not is_async:
                                    running = False
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return -1
                        if temp_delay > 0:
                            sleep(temp_delay)
            elif split_line[0] == "M_LINE_MOVE":
                x1 = int(split_line[1])
                y1 = int(split_line[2])

                delay = None
                if len(split_line) > 3:
                    delay = float(split_line[3]) / 1000.0

                skip = 1
                if len(split_line) > 4:
                    skip = int(split_line[4])

                if (delay == None) or (delay <= 0):
                    print("[scripts] " + coords + "    Mouse line move relative (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step")
                else:
                    print("[scripts] " + coords + "    Mouse line move relative (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step and wait " + split_line[3] + " milliseconds between each step")

                x_C, y_C = ms.getXY()
                x_N, y_N = x_C + x1, y_C + y1
                points = ms.line_coords(x_C, y_C, x_N, y_N)
                for x_M, y_M in points[::skip]:
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not is_async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return -1
                    ms.setXY(x_M, y_M)
                    if (delay != None) and (delay > 0):
                        temp_delay = delay
                        while temp_delay > DELAY_EXIT_CHECK:
                            sleep(DELAY_EXIT_CHECK)
                            temp_delay -= DELAY_EXIT_CHECK
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not is_async:
                                    running = False
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return -1
                        if temp_delay > 0:
                            sleep(temp_delay)
            elif split_line[0] == "M_LINE_SET":
                x1 = int(split_line[1])
                y1 = int(split_line[2])

                delay = None
                if len(split_line) > 3:
                    delay = float(split_line[3]) / 1000.0

                skip = 1
                if len(split_line) > 4:
                    skip = int(split_line[4])

                if (delay == None) or (delay <= 0):
                    print("[scripts] " + coords + "    Mouse line set (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step")
                else:
                    print("[scripts] " + coords + "    Mouse line set (" + split_line[1] + ", " + split_line[2] + ") by " + str(skip) + " pixels per step and wait " + split_line[3] + " milliseconds between each step")

                x_C, y_C = ms.getXY()
                points = ms.line_coords(x_C, y_C, x1, y1)
                for x_M, y_M in points[::skip]:
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not is_async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return -1
                    ms.setXY(x_M, y_M)
                    if (delay != None) and (delay > 0):
                        temp_delay = delay
                        while temp_delay > DELAY_EXIT_CHECK:
                            sleep(DELAY_EXIT_CHECK)
                            temp_delay -= DELAY_EXIT_CHECK
                            if threads[x][y].kill.is_set():
                                print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                                threads[x][y].kill.clear()
                                if not is_async:
                                    running = False
                                threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                                return -1
                        if temp_delay > 0:
                            sleep(temp_delay)

                print("[scripts] " + coords + "    Repeat LABEL " + split_line[1] + " " + split_line[2] + " times max")
                if idx in repeats:
                    if repeats[idx] > 0:
                        print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                        repeats[idx] -= 1
                        return labels[split_line[1]]
                    else:
                        print("[scripts] " + coords + "        No repeats left, not repeating.")
                else:
                    repeats[idx] = int(split_line[2])
                    repeats_original[idx] = int(split_line[2])
                    print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                    repeats[idx] -= 1
                    return labels[split_line[1]]
            elif split_line[0] == "OPEN":
                path_name = " ".join(split_line[1:])
                print("[scripts] " + coords + "    Open file or folder " + path_name)
                files.open_file_folder(path_name)
            elif split_line[0] == "@SIMPLE":
                print("[scripts] " + coords + "    Simple keybind: " + split_line[1])
                
                #PRESS
                key = kb.sp(split_line[1])
                kb.press(key)
                
                #WAIT_UNPRESSED
                while lp_events.pressed[x][y]:
                    sleep(DELAY_EXIT_CHECK)
                    if threads[x][y].kill.is_set():
                        print("[scripts] " + coords + " Recieved exit flag, script exiting...")
                        threads[x][y].kill.clear()
                        if not is_async:
                            running = False
                        threading.Timer(EXIT_UPDATE_DELAY, lp_colors.updateXY, (x, y)).start()
                        return idx + 1
                #RELEASE
                kb.release(key)
            
            
            

                print("[scripts] " + coords + "    If key is not pressed repeat LABEL " + split_line[1] + " " + split_line[2] + " times max")
                if not lp_events.pressed[x][y]:
                    if idx in repeats:
                        if repeats[idx] > 0:
                            print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                            repeats[idx] -= 1
                            return labels[split_line[1]]
                        else:
                            print("[scripts] " + coords + "        No repeats left, not repeating.")
                    else:
                        repeats[idx] = int(split_line[2])
                        print("[scripts] " + coords + "        " + str(repeats[idx]) + " repeats left.")
                        repeats[idx] -= 1
                        return labels[split_line[1]]
            elif split_line[0] == "RESET_REPEATS":
                print("[scripts] " + coords + "    Reset all repeats")
                for i in repeats:
                    repeats[i] = repeats_original[i]
            ####^^^^^^^^^^^^^^^^^^^^ OLD OLD OLD ^^^^^^^^^^^^^^^^^^^^^####
            
            
            
            
    ##################### OLD OLD #####################

    
   
        if split_line[0] in ["STRING", "DELAY", "TAP", "PRESS", "RELEASE", "WEB", "WEB_NEW", "SOUND", "M_MOVE", "M_SET", "M_SCROLL", "OPEN"]:
            if len(split_line) < 2:
                return ("Too few arguments for command '" + split_line[0] + "'.", line)
        if split_line[0] in ["WAIT_UNPRESSED", "RELEASE_ALL", "RESET_REPEATS"]:
            if len(split_line) > 1:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)
        if split_line[0] in ["DELAY", "WEB", "WEB_NEW", "PRESS", "RELEASE"]:
            if len(split_line) > 2:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)
        if split_line[0] in ["SOUND", "M_MOVE", "M_SCROLL", "M_SET"]:
            if len(split_line) > 3:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)
        if split_line[0] in ["TAP"]:
            if len(split_line) > 4:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)
            if len(split_line) > 3:
                try:
                    temp = float(split_line[3])
                except:
                    return (split_line[0] + "Tap wait time '" + split_line[3] + "' not valid.", line)
            if len(split_line) > 2:
                try:
                    temp = int(split_line[2])
                except:
                    return (split_line[0] + " repetitions '" + split_line[2] + "' not valid.", line)
        if split_line[0] in ["M_LINE"]:
            if len(split_line) > 7:
                return ("Too many arguments for command '" + split_line[0] + "'.", line)
        if split_line[0] in ["TAP", "PRESS", "RELEASE"]:
            if kb.sp(split_line[1]) == None:
                return ("No key named '" + split_line[1] + "'.", line)
        if split_line[0] == "DELAY":
            try:
                temp = float(split_line[1])
            except:
                return ("Delay time '" + split_line[1] + "' not valid.", line)
        if split_line[0] == "WAIT_UNPRESSED":
            if len(split_line) > 1:
                return ("'WAIT_UNPRESSED' takes no arguments.", line)
        if split_line[0] == "SOUND":
            final_name = sound.full_name(split_line[1])
            if not os.path.isfile(final_name):
                return ("Sound file '" + final_name + "' not found.", line)
            if not sound.is_valid(split_line[1]):
                return ("Sound file '" + final_name + "' not valid.", line)
            if len(split_line) > 2:
                try:
                    vol = float(float(split_line[2]) / 100.0)
                    if (vol < 0.0) or (vol > 1.0):
                        return ("'SOUND' volume must be between 0 and 100.", line)
                except:
                    return ("'SOUND' volume " + split_line[2] + " not valid.", line)
        if split_line[0] in ["M_STORE", "M_RECALL"]:
            if len(split_line) > 1:
                return ("'" + split_line[0] + "' takes no arguments.", line)
        if split_line[0] == "M_RECALL_LINE":
            if len(split_line) > 1:
                try:
                    temp = float(split_line[1])
                except:
                    return ("'" + split_line[0] + "' wait value '" + split_line[1] + "' not valid.", line)
            if len(split_line) > 2:
                try:
                    temp = int(split_line[2])
                    if temp == 0:
                        return ("'" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    return ("'" + split_line[0] + "' skip value '" + split_line[2] + "' not valid.", line)
        if split_line[0] == "M_MOVE":
            if len(split_line) < 3:
                return ("'M_MOVE' requires both an X and a Y movement value.", line)
            try:
                temp = int(split_line[1])
            except:
                return ("'M_MOVE' X value '" + split_line[1] + "' not valid.", line)
            try:
                temp = int(split_line[2])
            except:
                return ("'M_MOVE' Y value '" + split_line[2] + "' not valid.", line)
        if split_line[0] == "M_SET":
            if len(split_line) < 3:
                return ("'M_SET' requires both an X and a Y value.", line)
            try:
                temp = int(split_line[1])
            except:
                return ("'M_SET' X value '" + split_line[1] + "' not valid.", line)
            try:
                temp = int(split_line[2])
            except:
                return ("'M_SET' Y value '" + split_line[2] + "' not valid.", line)
        if split_line[0] == "M_SCROLL":
            try:
                temp = float(split_line[1])
            except:
                return ("Invalid scroll amount '" + split_line[1] + "'.", line)

            if len(split_line) > 2:
                try:
                    temp = float(split_line[2])
                except:
                    return ("Invalid scroll amount '" + split_line[2] + "'.", line)
        if split_line[0] == "M_LINE":
            if len(split_line) < 5:
                return ("'M_LINE' requires at least X1, Y1, X2, and Y2 arguments.", line)
            try:
                temp = int(split_line[1])
            except:
                return ("'M_LINE' X1 value '" + split_line[1] + "' not valid.", line)
            try:
                temp = int(split_line[2])
            except:
                return ("'M_LINE' Y1 value '" + split_line[2] + "' not valid.", line)
            try:
                temp = int(split_line[3])
            except:
                return ("'M_LINE' X2 value '" + split_line[3] + "' not valid.", line)
            try:
                temp = int(split_line[4])
            except:
                return ("'M_LINE' Y2 value '" + split_line[4] + "' not valid.", line)
            if len(split_line) >= 6:
                try:
                    temp = float(split_line[5])
                except:
                    return ("'M_LINE' wait value '" + split_line[5] + "' not valid.", line)
            if len(split_line) >= 7:
                try:
                    temp = int(split_line[6])
                    if temp == 0:
                        return ("'M_LINE' skip value cannot be zero.", line)
                except:
                    return ("'M_LINE' skip value '" + split_line[6] + "' not valid.", line)
        if split_line[0] in ["M_LINE_MOVE", "M_LINE_SET"]:
            if len(split_line) < 3:
                return ("'" + split_line[0] + "' requires at least X and Y arguments.", line)
            try:
                temp = int(split_line[1])
            except:
                return ("'" + split_line[0] + "' X value '" + split_line[1] + "' not valid.", line)
            try:
                temp = int(split_line[2])
            except:
                return ("'" + split_line[0] + "' Y value '" + split_line[2] + "' not valid.", line)
            if len(split_line) >= 4:
                try:
                    temp = float(split_line[3])
                except:
                    return ("'" + split_line[0] + "' wait value '" + split_line[3] + "' not valid.", line)
            if len(split_line) >= 5:
                try:
                    temp = int(split_line[4])
                    if temp == 0:
                        return ("'" + split_line[0] + "' skip value cannot be zero.", line)
                except:
                    return ("'" + split_line[0] + "' skip value '" + split_line[4] + "' not valid.", line)

        if split_line[0] == "OPEN":
            path_name = " ".join(split_line[1:])
            if (not os.path.isfile(path_name)) and (not os.path.isdir(path_name)):
                return (split_line[0] + " folder or file location '" + path_name + "' does not exist.", line)
    ###########^^^^^^^^^ OLD OLD ^^^^^^^^^^###########