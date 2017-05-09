import logging

class Clovek():
    def __init__(self, gui):
        self.gui = gui

    def igraj(self):
        '''Čakamo, da bo uporabnik kliknil na ploščo.
        Ko se to zgodi, nas Gui obvesti preko metode klik'''
        logging.debug("Na potezi je človek")
        pass

    def prekini(self):
        pass

    def klik(self, poteza):
        '''Povlečemo potezo. Če ni veljavna, se ne bo zgodilo nič.'''
        logging.debug("Človek vleče potezo {0}".format(poteza))
        self.gui.razberi_potezo(poteza)
