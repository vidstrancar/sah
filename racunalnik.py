import threading # Za vzporedno izvajanje
import logging

from minimax import *
from logika import *

class Racunalnik():
    def __init__(self, gui, algoritem):
        self.gui = gui
        self.algoritem = algoritem # Algoritem, ki računa potezo
        self.mislec = None

    def igraj(self):
        '''Igraj potezo, ki jo vrne algoritem.'''
        # Naredimo vlakno, ki mu podamo kopijo igre, da ne zmedemo GUI-ja
        kopija = self.gui.sah.kopija()
        self.mislec = threading.Thread(
            target=lambda: self.algoritem.izracunaj_potezo(kopija))

        # Poženemo vlakno
        self.mislec.start()

        # Preverjamo, ali je bila najdena poteza
        self.gui.plosca.after(100, self.preveri_potezo)

    def preveri_potezo(self):
        '''Vsakih 100ms preveri, ali je algoritem že izračunal potezo.'''
        if self.algoritem.poteza is not None:
            # Algoritem je že našel potezo. Povlečemo jo, če ni bilo prekinitve.
            figura, poteza = self.algoritem.poteza
            logging.debug('Računalnik je našel potezo: {} premakne na {}'.format(figura, poteza))
            self.gui.premakni_figuro(figura, poteza)
            # Vzporedno vlakno ni več aktivno, zato ga 'pozabimo'
            self.mislec = None
        elif self.algoritem.poteza is None:
            # Algoritem še ni našel poteze, preveri še enkrat čez 100 ma
            self.gui.plosca.after(100, self.preveri_potezo)

    def prekini(self):
        '''To metodo kliče GUI, če je treba prekiniti razmišljanje.'''
        if self.mislec:
            logging.debug("Prekinjam {0}".format(self.mislec))
            # Algoritmu sporočimo, da je treba nehati z razmišljanjem
            self.algoritem.prekini()
            # Počakamo, da se vlakno ustavi
            self.mislec.join()
            self.mislec = None

    def klik(self, p):
        # Računalnik ignorira klike
        pass
