import logging

class Minimax:
    # Objekt, ki hrani stanje igre in algoritma, nima pa dostopa do GUI,
    # ker ga ne sme uporablati, saj deluje v drugem vlaknu kot tkinter.

    def __init__(self, globina):
        self.globina = globina
        self.prekinitev = False
        self.igra = None # dobimo kasneje
        self.jaz = None # katerega igralca igramo (dobimo kasneje)
        self.poteza = None

    def prekini(self):
        '''Metodo pokliče GUI, ko je uporabnik zaprl okno ali izbral novo igro.'''
        self.prekinitev = True

    def izracunaj_potezo(self, igra):
        '''Izračuna 'najboljšo' potezo za trenutno stanje igre.'''
        # To metodo pokličemo iz vzporednega vlakna.
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.jaz = self.igra.na_vrsti
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
        vsota_figur = 0
        for figura in self.igra.figure[self.igra.na_vrsti]:
            if figura.ziv:
                vsota_figur += figura.vrednost
        return vsota_figur

    def minimax(self, globina, maksimiziramo):
        # print(self.igra.figure)
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
                    # Maksimiziramo, kar je enako, kot da minimiziramo nasprotnika
                    # PROBLEM: KO POVLEČEMO POTEZO, SE ŠTEVILO NAŠIH TOČK NE SPREMENI
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for figura in self.igra.figure[self.igra.na_vrsti]:
                        for p in list(self.igra.dovoljene_poteze_iterator(figura)):
                            self.igra.naredi_potezo(figura, p)
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.vrni_potezo()
                            # print(figura, end='')
                            # print('poteza: {}, vrednost: {}'.format(p, vrednost))
                            if vrednost < vrednost_najboljse:
                                vrednost_najboljse = vrednost
                                najboljsa_poteza = (figura, p)
                else:
                    # Minimiziramo nasprotnika, torej maksimiziramo sebe :)
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    for figura in self.igra.figure[self.igra.na_vrsti]:
                        for p in list(self.igra.dovoljene_poteze_iterator(figura)):
                            self.igra.naredi_potezo(figura, p)
                            vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                            self.igra.vrni_potezo()
                            if vrednost > vrednost_najboljse:
                                vrednost_najboljse  = vrednost
                                najboljsa_poteza = (figura, p)

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)

        else:
            assert False, "minimax: nedefinirano stanje igre"


































