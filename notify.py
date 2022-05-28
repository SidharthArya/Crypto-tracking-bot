class Notify:
    def __init__(self, telegram=None, libnotify=None, conky=None):
        if telegram:
            self.telegram = telegram
        if libnotify:
            self.libnotify = libnotify
        if conky:
            self.conky = conky
    
