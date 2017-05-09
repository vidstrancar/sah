import logging
from copy import deepcopy

KRALJ = 'kralj'
KRALJICA = 'kraljica'
TRDNJAVA = 'trdnjava'
LOVEC = 'lovec'
KONJ = 'konj'
KMET = 'kmet'

def v_sahovnici(polozaj):
    x, y = polozaj
    return  0 <= x <= 7 and 0 <= y <= 7


class Figura:
    def __init__(self, polozaj, barva):
        self.ziv = True
        self.barva = barva
        self.vrsta = None
        self.i, self.j = polozaj # stolpec, vrstica
        self.vektorji_premika = []

    def __hash__(self):
        return hash((self.barva, self.i, self.j, self.vrsta))

    def __eq__(self, other):
        return (other != None and
                (self.barva, self.i, self.j, self.vrsta) == (other.barva, other.i, other.j, other.vrsta))

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not(self == other)

    def dovoljeni_premiki(self, slika, igra):
        '''Vraca tocke, na katere se lahko premaknemo s kraljico, lovcem in trdnjavo.'''
        for i_premika, j_premika in self.vektorji_premika:
            n = 1
            while v_sahovnici((self.i + n * i_premika, self.j + n * j_premika)):
                if slika[self.i + n * i_premika][self.j + n * j_premika] is None: # Na prazno polje se lahko premaknemo
                    yield ((self.i + n * i_premika, self.j + n * j_premika))
                else:
                    if slika[self.i + n * i_premika][self.j + n * j_premika].barva != self.barva:
                        yield ((self.i + n * i_premika, self.j + n * j_premika))
                    break # Ne moremo preskočiti nasprotnikove figure
                n += 1

    def pojej(self):
        '''Figuro odstranimo s šahovnice.'''
        self.ziv = False
        self.i = -1
        self.j = -1


    def premakni(self, lokacija):
        '''Spremenimo koordinati i in j figure.'''
        (self.i, self.j) = lokacija

    def __str__(self):
        return '{1} {0}, na ({2}, {3})'.format(self.vrsta, self.barva, self.i, self.j)


class Kraljica(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = KRALJICA
        self.vektorji_premika = [(-1, 1), (1, 1), (-1, -1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        self.vrednost = 9


class Lovec(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = LOVEC
        self.vektorji_premika = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        self.vrednost = 3


class Konj(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = KONJ
        self.vektorji_premika = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]
        self.vrednost = 3

    def dovoljeni_premiki(self, slika, igra):
        '''Premiki konja.'''
        for i_premika, j_premika in self.vektorji_premika:
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if slika[self.i + i_premika][self.j + j_premika] is None:
                    yield ((self.i + i_premika, self.j + j_premika))
                elif slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                    yield ((self.i + i_premika, self.j + j_premika))


class Trdnjava(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = TRDNJAVA
        self.premaknjen = False # Zaradi preverjanja rošade
        self.vektorji_premika = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.vrednost = 5

    def premakni(self, koncna_lokacija):
        '''Spremenimo koordinati i in j trdnjave.'''
        Figura.premakni(self, koncna_lokacija)
        self.premaknjen = True


class Kralj(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.barva = barva
        self.vrsta = KRALJ
        self.premaknjen = False
        self.vektorji_premika = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.vrednost = 0

    def dovoljeni_premiki(self, slika, igra):
        '''Premiki kralja.'''
        for i_premika, j_premika in self.vektorji_premika:
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if slika[self.i + i_premika][self.j + j_premika] is None or \
                                slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                    yield ((self.i + i_premika, self.j + j_premika))

    def premakni(self, koncna_lokacija):
        '''Spremenimo koordinati i in j kralja.'''
        Figura.premakni(self, koncna_lokacija)
        self.premaknjen = True


class Kmet(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = KMET
        self.vektorji_premika = [(1, 0), (2, 0), (1, 1), (1, -1)]
        self.koeficient = -1 if self.barva == 'bel' else 1 # Smer premikanja kmeta
        self.vrednost = 1

    def dovoljeni_premiki(self, slika, igra):
        '''Premiki kmeta.'''
        for i_premika, j_premika in self.vektorji_premika:
            i_premika *= self.koeficient
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if j_premika != 0: # Pojemo nasprotnikovo figuro
                    if slika[self.i + i_premika][self.j + j_premika] is not None and \
                                    slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                        yield ((self.i + i_premika, self.j + j_premika))
                else: # Skoka naprej
                    zacetna_pozicija = 1 if self.barva == 'crn' else 6
                    if abs(i_premika) == 1 and slika[self.i + i_premika][self.j] is None: # Skok za 1
                        yield ((self.i + i_premika, self.j))
                    elif slika[self.i + i_premika // 2][self.j] is None and slika[self.i + i_premika][self.j] is None and \
                            self.i == zacetna_pozicija: # Skok za 2, obe polji morata biti prosti
                        yield ((self.i + i_premika, self.j))




class Sah():
    def __init__(self):
        self.igra = [] # Zgodovina igre
        self.na_vrsti = 'bel'
        self.figure = {'bel': [Kmet((6, i), 'bel') for i in range(8)] +
                              [Trdnjava((7, 0), 'bel'), Trdnjava((7, 7), 'bel'),
                               Konj((7, 1), 'bel'), Konj((7, 6), 'bel'),
                               Lovec((7, 2), 'bel'), Lovec((7, 5), 'bel'),
                               Kraljica((7, 3), 'bel'),
                               Kralj((7, 4), 'bel')],

                       'crn': [Kmet((1, i), 'crn') for i in range(8)] +
                              [Trdnjava((0, 0), 'crn'), Trdnjava((0, 7), 'crn'),
                               Konj((0, 1), 'crn'), Konj((0, 6), 'crn'),
                               Lovec((0, 2), 'crn'), Lovec((0, 5), 'crn'),
                               Kraljica((0, 3), 'crn'),
                               Kralj((0, 4), 'crn')]}

    def kopija(self):
        '''Vrne 'globoko' kopijo trenutnega stanja igre. Uporabno za minimax.'''
        sah = Sah()
        sah.figure = deepcopy(self.figure)
        sah.na_vrsti = self.na_vrsti
        return sah

    def stanje_igre(self):
        '''Če je igre konec, nastavi zmagovalca.'''
        for figura in self.figure[self.na_vrsti]:
            if self.se_lahko_premakne(figura):
                return None # Zmagovalca še nimamo
        return self.nasprotna_barva()

    def se_lahko_premakne(self, figura):
        return (len(list(self.poteze_figure(figura))) > 0)

    def vrni_kralja_na_vrsti(self):
        '''Vrne figuro nasprotnega kralja.'''
        for figura in self.figure[self.na_vrsti]:
            if figura.vrsta == KRALJ:
                return figura

    def nasprotna_barva(self):
        '''Vrne barvo nasprotnega igralca.'''
        return 'crn' if self.na_vrsti == 'bel' else 'bel'

    def slika(self):
        '''Pretvori slovar figur v matriko figur in jo vrne.'''
        slika = [[None] * 8 for _ in range(8)]
        for figura in self.figure['bel'] + self.figure['crn']:
            if figura.ziv:
                if figura.i == -1 and figura.j == -1: # Dodatna varovalka
                    raise Exception ('{} ni živa.'.format(figura))
                slika[figura.i][figura.j] = figura
        return slika

    def shrani_igro(self):
        self.igra.append((deepcopy(self.figure), self.na_vrsti))

    def vrni_potezo(self):
        '''Povrne situacijo pred eno potezo.'''
        if len(self.igra) > 0:
            (self.figure, self.na_vrsti) = self.igra.pop()

    def premakni_figuro(self, figura, poteza, belezi_zgo=True):
        '''Premakne figuro. Zabeleži v zgodovino igre.'''
        self.shrani_igro() # shrani pozicijo
        i_z, j_z = figura.i, figura.j
        i_k, j_k = poteza
        # Premaknemo figuro
        figura.premakni((i_k, j_k)) # Spremeni ji koordinate na (i_k, j_k)
        # Pogledamo, če smo ob tem pojedli kakšno figuro
        pojedena_figura = self.slika()[i_k][j_k]  # Lahko je tudi None
        if pojedena_figura is not None:
            pojedena_figura.pojej() # Spremeni ji koordinate na (-1, -1), figura.ziv = False

    def naredi_potezo(self, figura, poteza):
        '''Če je poteza veljavna, jo naredi in vrne True. Če poteza ni dovoljena, vrni False.'''
        if poteza in self.poteze_figure(figura):
            logging.debug('sah prejel ukaz, naj premakne {} na {}'.format(figura, poteza))
            self.premakni_figuro(figura, poteza)
            self.na_vrsti = self.nasprotna_barva()
            return True
        else:
            return False

    def vse_poteze(self):
        '''Vrne seznam vseh veljavnih potez v dani situaciji.'''
        for figura in self.figure[self.na_vrsti]:
            if figura.ziv:
                for poteza in self.poteze_figure(figura):
                    yield (figura, poteza)

    def poteze_figure(self, figura):
        '''Vrne seznam dovoljenih potez za posamezno figuro.'''
        slika = self.slika()
        premiki = tuple(figura.dovoljeni_premiki(self.slika(), self.igra))
        logging.debug("premiki figure {0} so {1}".format(figura, premiki))
        for premik in premiki:
            self.premakni_figuro(figura, premik) # Simuliramo
            je_sah = self.bo_sah_po_potezi()
            self.vrni_potezo()
            if not je_sah:
                print ("poteze_figure: {0}".format(premik))
                yield premik

    def bo_sah_po_potezi(self):
        '''Vrne True, če bo po potezi šah.'''
        kralj = self.vrni_kralja_na_vrsti()
        slika = self.slika()
        # Šah zaradi kraljice, trdnjave ali lovca
        vektorji_nevarnih = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        for vektor in vektorji_nevarnih:
            n = 1
            i, j = kralj.i + n * vektor[0], kralj.j + n * vektor[1]
            while v_sahovnici((i, j)):
                druga_figura = 'trdnjava' if abs(vektor[0] + vektor[1]) == 1 else 'lovec'
                if slika[i][j] is not None:
                    if slika[i][j].barva != kralj.barva and ((n == 1 and slika[i][j].vrsta == KRALJ) or
                                    slika[i][j].vrsta in [KRALJICA, druga_figura]):
                        return True
                    else:
                        break  # Druge figure niso nevarne
                n += 1
                i, j = kralj.i + n * vektor[0], kralj.j + n * vektor[1]
        # Šah zaradi konja
        vektorji_konja = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]
        for i_premika, j_premika in vektorji_konja:
            if v_sahovnici((kralj.i + i_premika, kralj.j + j_premika)):
                if slika[kralj.i + i_premika][kralj.j + j_premika] is not None and \
                            slika[kralj.i + i_premika][kralj.j + j_premika].barva != kralj.barva and \
                            slika[kralj.i + i_premika][kralj.j + j_premika].vrsta == KONJ:
                        return True
        # Šah zaradi kmeta
        vektorji_kmeta = [(1, 1), (1, -1)]
        koeficient = -1 if kralj.barva == 'bel' else 1
        for i_premika, j_premika in vektorji_kmeta:
            i_premika *= koeficient
            if v_sahovnici((kralj.i + i_premika, kralj.j + j_premika)):
                if slika[kralj.i + i_premika][kralj.j + j_premika] is not None and \
                            slika[kralj.i + i_premika][kralj.j + j_premika].barva != kralj.barva and \
                            slika[kralj.i + i_premika][kralj.j + j_premika].vrsta == KMET:
                        return True
        return False

# sahec = Sah()
