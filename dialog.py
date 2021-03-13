# a routine that allows a single script at a time to access dialogs
import threading, tkinter as tk
from constants import *

DR_ABORT = -1   # returned when aborted for any reason
DR_CANCEL = 0   # Cancel return
DR_OK = 1       # OK return

DLG_INFO = 1    # a simple titled box with OK

M_REF = 0       # reference number of message
M_REQ = 1       # request of message

R_TYPE = 0      # dialog type requested
R_BUTTON = 1    # button that called dialog
R_CALLBACK = 2  # callback function
R_TITLE = 3     # dialog title

class Dialog(tk.Toplevel):

    def __init__(self, parent, title = None):
        tk.Toplevel.__init__(self, parent)
        self.transient(parent)
        if title:
            self.title(title)
        self.parent = parent
        self.result = None
        body = tk.Frame(self)
        
        b1 = tk.Button(self, text="OK", command=self.btn_OK)
        b1.place(x=0, y=0)
        b2 = tk.Button(self, text="Cancel", command=self.btn_Cancel)
        b2.place(x=100, y=0)
        #register validators
        #self.validatePosInt = (body.register(self.OnValidatePosInt),
        #        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        #self.initial_focus = self.body(body)   #this calls the body function which is overridden, and which draws the dialog
        #body.grid()
        #self.buttonbox()
        #self.grab_set()
        #if not self.initial_focus:
        #    self.initial_focus = self
        #self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))
        #self.initial_focus.focus_set()


    def btn_OK(self):
        global DIALOG_RETURN
        DIALOG_RETURN = DR_OK
        self.destroy()


    def btn_Cancel(self):
        global DIALOG_RETURN
        DIALOG_RETURN = DR_CANCEL
        self.destroy()


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
    def pop(self, btn=None):
        ok = self.acquire(btn)                                 # try to get a lock

        if not ok:                                             # error return for death notification
            return (False, None)

        try:
            if len(self.queue) == 0:                           # if the queue is empty
                return (True, None)                            # return success, but a value of None
            return (True, self.queue.pop())                    # otherwise return the head of the queue

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
DIALOG_OBJECT = None           # the dialog
DIALOG_RETURN = DR_ABORT       # return from the dialog


# routine that must be called periodically to initiate and kill dialogs
def IdleProcess(parent):
    global DIALOG_LOCK
    global DIALOG_ACTIVE
    global DIALOG_BUTTON
    global DIALOG_OBJECT

    if DIALOG_LOCK.acquire(False):                             # try to acquire a lock
        try:                                                   # then do what we need to do
            # Determine if dialog has closed
            if DIALOG_ACTIVE:
                try:
                    DIALOG_OBJECT.state()                      # Raises an exception if the window is closed
                except:
                    DIALOG_ACTIVE = False
                    CloseDialog()                              # act to close the dialog

            if DIALOG_ACTIVE:                                  # if there is a dialog

                if DIALOG_BUTTON.root.thread.kill.is_set():    # has the controlling button been killed?
                    CloseDialog()                              # act to close the dialog

            else:                                              # there is no dialog open

                ok, msg = DIALOG_QUEUE.pop()                   # pop a request off the queue
                if ok and msg != None:                         # if there is a request
                    OpenDialog(parent, msg[M_REQ])             # open the dialog

        finally:
           DIALOG_LOCK.release()                               # ensure lock is released before exiting


# Close any open dialog
def CloseDialog():
    global DIALOG_ACTIVE
    global DIALOG_BUTTON
    global DIALOG_REQUEST
    global DIALOG_OBJECT
    global DIALOG_RETURN

    # do what is required to close the window
    if DIALOG_OBJECT:
        DIALOG_OBJECT.destroy()
    DIALOG_REQUEST[R_CALLBACK]((True, DIALOG_RETURN))          # and return success, and the return info from the dialog
    
    DIALOG_OBJECT = None
    DIALOG_ACTIVE = False                                      # no dialog open
    DIALOG_BUTTON = None                                       # no button
    DIALOG_REQUEST = None                                      # no request


# Open a new dialog
def OpenDialog(parent, request):
    global DIALOG_ACTIVE
    global DIALOG_BUTTON
    global DIALOG_REQUEST
    global DIALOG_OBJECT
    global DIALOG_RETURN

    DIALOG_ACTIVE = True                                       # a dialog is open
    DIALOG_BUTTON = request[R_BUTTON]                          # it's for this button
    DIALOG_REQUEST = request                                   # and this is the request
    DIALOG_RETURN = None                                       # the default return

    # do what is needed to actually open the window
    DIALOG_OBJECT = Dialog(parent, request[3])

