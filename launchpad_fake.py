# A fake connector to allow operation without a launchpad connected

import global_vars

FAKE_EVENT_QUEUE = []

def AddEvent(x):
   FAKE_EVENT_QUEUE.append(x)

def Pop():
   if FAKE_EVENT_QUEUE == []:
       return []
   else:
      return FAKE_EVENT_QUEUE.pop(0)

class Launchpad():
    def __init__(self):
        pass

    def ButtonFlush(self):
        pass

    def LedCtrlBpm(self, x):
        pass

    def ButtonStateXY(self):
        return Pop()

    def LedCtrlXYByRGB(self, x, y, z):
        pass

    def LedCtrlXY(self, x, y, z, t):
        pass

    def LedCtrlXYByCode(self, x, y, z):
        pass

    def LedCtrlFlashXYByCode(self, x, y, z):
        pass

    def Close(self):
        pass


launchpad = Launchpad()


class Launchpad_Fake_Connector():
    def __init__(self):
        pass

    def get_launchpad(self):
        global launchpad
        return launchpad

    def connect(self, lp):
        return True

    def get_mode(self, lp):
        return global_vars.ARGS['standalone']

    def get_display_name(self, lp):
        return "Emulated Launchpad " + global_vars.ARGS['standalone']

    def disconnect(self, lp_object):
        pass


launchpad_fake_connector = Launchpad_Fake_Connector()
