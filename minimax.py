import logging
import logika

import random

class Minimax:
    '''Objekt, ki hrani stanje igre in algoritma, nima pa dostopa do GUI.
    Ker ga ne sme uporablati, saj deluje v drugem vlaknu kot tkinter'''

    def __init__(self, globina):
        self.globina = globina
        self.prekinitev = False
        self.igra = None # Dobimo naknadno
        self.jaz = None
        self.poteza = None

    def prekini(self):
        '''Metodo pokliče GUI, ko je uporabnik zaprl okno ali izbral novo igro.'''
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        '''Izračuna 'najboljšo' potezo za trenutno stanje igre.'''
        # To metodo pokličemo iz vzporednega vlakna.
        self.igra = igra
        self.jaz = self.igra.na_vrsti
        self.prekinitev = False # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.poteza = None # Sem napišemo potezo, ki jo najedmo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            logging.debug("minimax: poteza {0}, vrednost {1}".format(poteza, vrednost))
            self.poteza = poteza

    # Vrednost igre
    ZMAGA = 10000000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        '''Sešteje vrednosti figur na šahovnici.'''
        vsota_figur = 0
        for i in range(8):
            for j in range(8):
                figura = self.igra.plosca[i][j]
                if figura != logika.PRAZNO:
                    if figura.barva == self.jaz:
                        vsota_figur += figura.vrednost
                    else:
                        vsota_figur -= figura.vrednost
        stevilo_potez = 0.1 * len(tuple(self.igra.vse_poteze()))
        if self.igra.na_vrsti != self.jaz:
            stevilo_potez = -stevilo_potez
        return vsota_figur + stevilo_potez

    def minimax(self, globina, maksimiziramo):
        '''Glavna metoda minimax.'''
        if self.prekinitev:
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        zmagovalec = self.igra.stanje_igre()
        if zmagovalec in (logika.BELI, logika.CRNI, logika.REMI):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == logika.REMI:
                return (None, 0)
            elif zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            else:
                return (None, -Minimax.ZMAGA)
        elif zmagovalec is None:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    poteze = list(self.igra.vse_poteze())
                    random.shuffle(poteze)
                    for poteza in poteze:
                        self.igra.naredi_potezo(poteza)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.vrni_potezo()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza
                else:
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    poteze = list(self.igra.vse_poteze())
                    random.shuffle(poteze)
                    for poteza in poteze:
                        self.igra.naredi_potezo(poteza)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.vrni_potezo()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = poteza

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)

        else:
            assert False, "minimax: nedefinirano stanje igre"
