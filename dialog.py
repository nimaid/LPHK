# a routine that allows a single script at a time to access dialogs
import threading
from constants import *


DLG_INFO = 1                   # a simple info box


class SyncQueue():
    def __init__(self):
        self.queue = []                                        # the queue
        self.lock = threading.Lock()                           # the lock to protect it
        self.msg_id = 1                                        # and the id to return for each push to allow pull


    # Acquire a lock
    def acquire(self, btn=None):
        if btn == None:                                        # if there's no button
            while not self.lock.acquire(True, -1):             # wait forever for a lock
                pass
        else:
            locked = False                                     # we start unlocked
            while not locked:                                  # and while unlocked
                btn.Safe_sleep(DELAY_EXIT_CHECK)               # we take a short nap
                if btn.Check_kill():                           # and make sure we're not dead
                    return False                               # returning False if we are

                locked = self.lock.acquire(False)              # but the main job is to attempt to acquire the lock without blocking)

        return True                                            # if we're here, we have a lock


    # push a value onto the queue.  If a button is passed, do it in a way that
    # doesn't stall things
    def push(self, x, btn=None):
        ok = self.acquire(btn)                                 # try to get a lock

        if not ok:                                             # error return for death notification
            return -1

        self.msg_id += 1                                       # increment the message id
        m = self.msg_id                                        # and store our local message id

        try:
            self.queue.append((m, x))                          # this is what we're here to do!

        except:
            return -1                                          # unlikely, but something bad happened

        finally:
            self.lock.release()                                # Always release the lock

        return m                                               # and return msg_id on success


    # pop a value off the queue.  If a button is passed, do it in a way that
    # doesn't stall things
    def pop(self, x, btn=None):
        ok = self.acquire(btn)                                 # try to get a lock

        if not ok:                                             # error return for death notification
            return (False, None)

        try:
            if len(self.queue) == 0:                           # if the queue is empty
                return (True, None)                            # return success, but a value of None
            return (True, self.queue.pop(x))                   # otherwise return the head of the queue

        except:
            return (False, None)                               # unlikely, but something bad happened

        finally:
            self.lock.release()                                # Always release the lock


    # removes a message off the queue.  This is always allowed to stall
    def pull(self, msg_id):
        ok = self.acquire(None)                                # try to get a lock

        if not ok:                                             # error return for weird situations (should never happen)
            return False

        try:
            for idx, (m_id, val) in enumerate(self.queue):     # for all items in the queue
                if m_id > msg_id:                              # if it's not on the queue
                    return False                               # it must bebeing handled
                if m_id == msg_id:                             # found it!
                    del self.queue[idx]                        # remove it
                    return True                                # and that is success

            return False                                       # error if we don't find it at all

        finally:
            self.lock.release()                                # Always release the lock


DIALOG_QUEUE = SyncQueue()                                     # create a queue object to synchronise requests for dialogs


# request any type of dialog
def Sync_Request(btn, m_type, args):
    waiting = True                                             # we're waiting (by default)
    info = None                                                # and we have nothing returned

    def EndWait(p_info):                                       # callback routine to end the wait
        nonlocal info
        info = p_info                                          # here is what we get back

        nonlocal waiting
        waiting = False                                        # and the flag telling us the wait is over

    msg = DIALOG_QUEUE.push((m_type, btn, EndWait, args), btn) # push the request for the dialog
    if msg < 0:                                                # in case of error
        return (False, info)                                   # we have failed

    while waiting:                                             # while we're waiting
        btn.Safe_sleep(DELAY_EXIT_CHECK)                       # we take a short nap
        if btn.Check_kill():                                   # and make sure we're not dead
            if DIALOG_QUEUE.pull(msg):                         # can we pull the request before it gets actioned?
                return (False, info)                           # yep, return immediately
            else:
                while waiting:                                 # otherwise just keep waiting
                    btn.Safe_sleep(DELAY_EXIT_CHECK)
                return (False, info)                           # and return false when the dialog ends

    return (True, info)                                        # a normal return


# request a simple comment box
def CommentBox(btn, message):
    return Sync_Request(btn, DLG_INFO, message)                # the arguments are simply the message


DIALOG_LOCK = threading.Lock() # lock to be used to access dialog variables
DIALOG_ACTIVE = False          # true if we're showing (or preparing to show) a dialog
DIALOG_BUTTON = None           # the button object in charge of the dialog
DIALOG_REQUEST = None          # information about the request

# routine that must be called periodically to initiate and kill dialogs
def IdleProcess():
    global DIALOG_LOCK
    global DIALOG_ACTIVE
    global DIALOG_BUTTON

    if DIALOG_LOCK.acquire(False):                             # try to acquire a lock
        try:                                                   # then do what we need to do
            if DIALOG_ACTIVE:                                  # if there is a dialog

                if DIALOG_BUTTON.root.thread.kill.is_set():    # has the controlling button been killed?
                    CloseDialog()                              # act to close the dialog

            else:                                              # there is no dialog open

                ok, request = DIALOG_QUEUE.pop()               # pop a request off the queue
                if ok:                                         # if there is a request
                    OpenDialog(request)                        # open the dialog

        finally:
           DIALOG_LOCK.release()                                # ensure lock is released before exiting


# Close any open dialog
def CloseDialog():
    global DIALOG_ACTIVE
    global DIALOG_BUTTON
    global DIALOG_REQUEST
    
    # do what is required to close the window
    
    DIALOG_ACTIVE = False                                      # no dialog open
    DIALOG_BUTTON = None                                       # no button
    DIALOG_REQUEST[2]((False, None))                           # and return failure, and no information as return info


# Open a new dialog
def OpenDialog(request):
    global DIALOG_ACTIVE
    global DIALOG_BUTTON
    global DIALOG_REQUEST

    DIALOG_ACTIVE = True                                       # a dialog is open
    DIALOG_BUTTON = request[1]                                 # it's for this button
    DIALOG_REQUEST = request[0]                                # and this is the request

    # do what is needed to actually open the window    
