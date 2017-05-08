import logging
from sah2 import Figura

class Minimax:
    # Objekt, ki hrani stanje igre in algoritma, nima pa dostopa do GUI,
    # ker ga ne sme uporablati, saj deluje v drugem vlaknu kot tkinter.

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
        self.prekinitev = False # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.jaz = 'bel' if self.igra.na_vrsti == 'bel' else 'crn'
        self.nasprotnik = self.igra.nasprotna_barva()
        self.poteza = None # Sem napišemo potezo, ki jo najedmo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.nasprotnik = None
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
        nasprotnik = 'bel' if self.jaz == 'crn' else 'crn'
        vsota_figur = 0
        for figura in self.igra.figure[self.jaz]:
            if figura.ziv:
                vsota_figur += figura.vrednost
        for figura in self.igra.figure[nasprotnik]:
            if figura.ziv:
                vsota_figur -= figura.vrednost
        return vsota_figur

    def minimax(self, globina, maksimiziramo):
        '''Glavna metoda minimax.'''
        if self.prekinitev:
            logging.debug("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        zmagovalec = self.igra.stanje_igre()
        if zmagovalec in ('bel', 'crn', 'neodloceno'):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == self.nasprotnik:
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)
        elif zmagovalec is None:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for figura, poteze in self.igra.vse_poteze().items():
                        for p in poteze:
                            self.igra.premakni_figuro(figura, p)
                            self.igra.na_vrsti = self.igra.nasprotna_barva()
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.vrni_potezo()
                            self.igra.na_vrsti = self.igra.nasprotna_barva()
                            print('{} -> {}, vrednost: {}'.format(figura, p, vrednost))
                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = ((figura.i, figura.j), p)
                else:
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for figura, poteze in self.igra.vse_poteze().items():
                        for p in poteze:
                            self.igra.premakni_figuro(figura, p)
                            self.igra.na_vrsti = self.igra.nasprotna_barva()
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.vrni_potezo()
                            self.igra.na_vrsti = self.igra.nasprotna_barva()
                            print('{} -> {}, vrednost: {}'.format(figura, p, vrednost))
                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = ((figura.i, figura.j), p)

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)

        else:
            assert False, "minimax: nedefinirano stanje igre"

































