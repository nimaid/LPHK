# A fake connector to allow operation without a launchpad connected

class Launchpad():
    def __init__(self):
        pass

    def ButtonFlush(self):
        pass

    def LedCtrlBpm(self, x):
        pass

    def ButtonStateXY(self):
        return []
        
    def LedCtrlXYByRGB(self, x, y, z):
        pass
        
    def LedCtrlXY(self, x, y, z, t):
        pass
        
    def LedCtrlXYByCode(self, x, y, z):
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
        return "*ALONE*"

    def get_display_name(self, lp):
        return "Standalone Mode"

    def disconnect(self, lp_object):
        pass


launchpad_fake_connector = Launchpad_Fake_Connector()
