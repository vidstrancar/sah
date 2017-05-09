import logging

KRALJ = 'kralj'
KRALJICA = 'kraljica'
TRDNJAVA = 'trdnjava'
LOVEC = 'lovec'
KONJ = 'konj'
KMET = 'kmet'
PRAZNO = 'prazno'

BELI = 'beli'
CRNI = 'crni'
REMI = 'remi'

def v_sahovnici(polozaj):
    x, y = polozaj
    return  0 <= x <= 7 and 0 <= y <= 7

class Figura:
    def __init__(self, barva, vrsta, vrednost, vektorji_premika=None):
        self.barva = barva
        self.vrsta = vrsta
        self.vrednost = vrednost
        self.vektorji_premika = vektorji_premika

    def dovoljeni_premiki(self, igra, i, j):
        '''Vraca polja, na katera se lahko figura premakne, če je na polju (i,j).'''
        # Ta verzija deluje za kraljico, lovca in trdnjavo
        assert (self.vektorji_premika is not None)
        for i_premika, j_premika in self.vektorji_premika:
            n = 1
            while v_sahovnici((i + n * i_premika, j + n * j_premika)):
                if igra.plosca[i + n * i_premika][j + n * j_premika] == PRAZNO: # Na prazno polje se lahko premaknemo
                    yield ((i + n * i_premika, j + n * j_premika))
                else:
                    if igra.plosca[i + n * i_premika][j + n * j_premika].barva != self.barva:
                        yield ((i + n * i_premika, j + n * j_premika))
                    break # Ne moremo preskočiti nasprotnikove figure
                n += 1

    def __str__(self):
        return '{1} {0}'.format(self.vrsta, self.barva)


class Kraljica(Figura):
    def __init__(self, barva):
        Figura.__init__(self, barva, KRALJICA, 9,
                        [(-1, 1), (1, 1), (-1, -1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)])


class Lovec(Figura):
    def __init__(self, barva):
        Figura.__init__(self, barva, LOVEC, 3, [(-1, 1), (1, 1), (-1, -1), (1, -1)])

class Konj(Figura):
    SKOKI = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]

    def __init__(self, barva):
        Figura.__init__(self, barva, KONJ, 3)

    def dovoljeni_premiki(self, igra, i, j):
        '''Premiki konja.'''
        for i_skok, j_skok in Konj.SKOKI:
            if v_sahovnici((i + i_skok, j + j_skok)):
                if igra.plosca[i + i_skok][j + j_skok] == PRAZNO:
                    yield ((i + i_skok, j + j_skok))
                elif igra.plosca[i + i_skok][j + j_skok].barva != self.barva:
                    yield ((i + i_skok, j + j_skok))

class Trdnjava(Figura):
    def __init__(self, barva):
        Figura.__init__(self, barva, TRDNJAVA, 5, [(0, 1), (0, -1), (1, 0), (-1, 0)])

class Kralj(Figura):
    def __init__(self, barva):
        Figura.__init__(self, barva, KRALJ, 100)
        self.koraki = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def dovoljeni_premiki(self, igra, i, j):
        '''Premiki kralja.'''
        # XXX tu bi morali gledati rošade
        for i_korak, j_korak in self.koraki:
            if v_sahovnici((i + i_korak, j + j_korak)):
                if (igra.plosca[i + i_korak][j + j_korak] == PRAZNO or
                    igra.plosca[i + i_korak][j + j_korak].barva != self.barva):
                    yield ((i + i_korak, j + j_korak))

class Kmet(Figura):
    def __init__(self, barva):
        Figura.__init__(self, barva, KMET, 1)
        self.koraki = [(1, 0), (2, 0), (1, 1), (1, -1)]

    def dovoljeni_premiki(self, igra, i, j):
        '''Premiki kmeta.'''
        koeficient = (-1 if self.barva == BELI else 1) # smer v katero gre
        for i_premika, j_premika in self.koraki:
            i_premika *=  koeficient
            if v_sahovnici((i + i_premika, j + j_premika)):
                if j_premika != 0: # Pojemo nasprotnikovo figuro
                    # XXX tu bi morali gledati tudi self.en_passant
                    if igra.plosca[i + i_premika][j + j_premika] != PRAZNO and \
                       igra.plosca[i + i_premika][j + j_premika].barva != self.barva:
                        yield ((i + i_premika, j + j_premika))
                else: # Premik naprej
                    zacetna_pozicija = (1 if self.barva == CRNI else 6)
                    if abs(i_premika) == 1 and igra.plosca[i + i_premika][j] == PRAZNO: # Skok za 1
                        yield ((i + i_premika, j))
                    elif igra.plosca[i + i_premika // 2][j] == PRAZNO and igra.plosca[i + i_premika][j] == PRAZNO and \
                            i == zacetna_pozicija: # Skok za 2, obe polji morata biti prosti
                        yield ((i + i_premika, j))

# Začetne pozicije, najprej za ne-kmete:
zacetne_pozicije = {
    (0,0) : Trdnjava(CRNI),
    (0,1) : Konj(CRNI),
    (0,2) : Lovec(CRNI),
    (0,3) : Kraljica(CRNI),
    (0,4) : Kralj(CRNI),
    (0,5) : Lovec(CRNI),
    (0,6) : Konj(CRNI),
    (0,7) : Trdnjava(CRNI),
    (7,0) : Trdnjava(BELI),
    (7,1) : Konj(BELI),
    (7,2) : Lovec(BELI),
    (7,3) : Kraljica(BELI),
    (7,4) : Kralj(BELI),
    (7,5) : Lovec(BELI),
    (7,6) : Konj(BELI),
    (7,7) : Trdnjava(BELI)
}
# dodamo še kmete
for i in range(8):
    zacetne_pozicije[(1,i)] = Kmet(CRNI)
    zacetne_pozicije[(6,i)] = Kmet(BELI)

class Sah():
    """Objekt razreda Sah opisuje trenutno stanje igre in hrani zgodovino igre."""

    def __init__(self):
        self.igra = [] # Zgodovina igre
        self.na_vrsti = BELI
        # Podatki o rosadah, zaenkrat se ne uporabljajo
        self.rosada_beli_kratka = True
        self.rosada_beli_dolga = True
        self.rosada_crni_kratka = True
        self.rosada_crni_dolga = True
        self.plosca = [[PRAZNO for j in range(8)] for i in range(8)]
        for ((i,j), figura) in zacetne_pozicije.items():
            self.plosca[i][j] = figura

    def kopija(self):
        '''Vrne 'globoko' kopijo trenutnega stanja igre. Uporabno za minimax.'''
        sah = Sah()
        sah.na_vrsti = self.na_vrsti
        sah.rosada_beli_kratka = self.rosada_beli_kratka
        sah.rosada_beli_dolga = self.rosada_beli_dolga
        sah.rosada_crni_kratka = self.rosada_crni_kratka
        sah.rosada_crni_dolga = self.rosada_crni_dolga
        sah.plosca = [vrstica[:] for vrstica in self.plosca]
        return sah

    def stanje_igre(self):
        '''Vrni None, če igra še poteka, sicer CRNI ali BELI ali REMI.'''
        for i in range(8):
            for j in range(8):
                if len(tuple(self.poteze_polja((i,j)))) > 0:
                    return None # Možna je poteza, ni konec
        if self.je_sah(self.na_vrsti):
            # kralj je šahu, a ni možne poteze
            return self.nasprotna_barva()
        else:
            return REMI

    def kralj(self, barva):
        '''Vrne pozicijo kralja dane barve'''
        for i in range(8):
            for j in range(8):
                if (self.plosca[i][j] != PRAZNO and
                    self.plosca[i][j].barva == barva and
                    self.plosca[i][j].vrsta == KRALJ):
                    return (i, j)
        assert False, "kralja ni na plošči?!"

    def nasprotna_barva(self):
        '''Vrne barvo nasprotnega igralca.'''
        return (CRNI if self.na_vrsti == BELI else BELI)

    def shrani_igro(self):
        self.igra.append((self.na_vrsti,
                          self.rosada_beli_kratka,
                          self.rosada_beli_dolga,
                          self.rosada_crni_kratka,
                          self.rosada_crni_dolga,
                          [vrstica[:] for vrstica in self.plosca]))

    def vrni_potezo(self):
        '''Povrne situacijo pred eno potezo.'''
        if len(self.igra) > 0:
            (self.na_vrsti,
             self.rosada_beli_kratka,
             self.rosada_beli_dolga,
             self.rosada_crni_kratka,
             self.rosada_crni_dolga,
             self.plosca) = self.igra.pop()

    def premakni_figuro(self, polje1, polje2):
        '''Premakni figuro iz polje1 na polje2. Spremeni, kdo je na potezi.'''
        (i1, j1) = polje1
        (i2, j2) = polje2
        # XXX ali je to rošada?
        # XXX ali je to en passant?
        # XXX ali je to promocija? (recimo, da vedno promoviramo v kraljico)
        # XXX ali je treba kako rosado nastaviti na False?
        # XXX ali je treba omogociti kak en passant?
        (self.plosca[i1][j1], self.plosca[i2][j2]) = (PRAZNO, self.plosca[i1][j1])
        self.na_vrsti = self.nasprotna_barva()

    def naredi_potezo(self, poteza):
        '''Če je poteza veljavna, jo naredi in vrne True. Če poteza ni dovoljena, vrni False.
           Poleg tega shrani prejšnjo pozicijo v zgodovino igre.'''
        (polje1, polje2) = poteza
        dovoljene = tuple(self.poteze_polja(polje1))
        if poteza in dovoljene:
            logging.debug('sah prejel veljavno potezo {0} -> {1}'.format(polje1, polje2))
            self.shrani_igro()
            self.premakni_figuro(polje1, polje2)
            return True
        else:
            logging.debug('sah prejel neveljavno potezo {0} -> {1}, na potezi je {2}, dovoljene so {3}'.format(polje1, polje2, self.na_vrsti, dovoljene))
            return False

    def vse_poteze(self):
        '''Vrne seznam vseh veljavnih potez v dani situaciji.'''
        for i in range(8):
            for j in range(8):
                for poteza in self.poteze_polja((i,j)):
                    yield poteza

    def poteze_polja(self, polje):
        '''Vrne seznam dovoljenih potez za figuro na danem polju.'''
        (i,j) = polje
        figura = self.plosca[i][j]
        if figura == PRAZNO or figura.barva != self.na_vrsti:
            # polje je prazno ali pa figura, ki je tu, ni na potezi
            pass
        else:
            premiki = tuple(figura.dovoljeni_premiki(self, i, j))
            logging.debug("premiki figure {0} so {1}".format(polje, premiki))
            barva = self.na_vrsti
            for polje2 in premiki:
                self.shrani_igro()
                self.premakni_figuro(polje, polje2) # Simuliramo
                je_sah = self.je_sah(barva)
                self.vrni_potezo()
                if not je_sah:
                    yield (polje, polje2)

    def je_sah(self, barva):
        '''Vrne True, če je kralj dane barve v šahu.'''
        (kralj_i, kralj_j) = self.kralj(barva)
        # Šah zaradi kraljice, trdnjave ali lovca
        vektorji_nevarnih = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        for vektor in vektorji_nevarnih:
            n = 1
            i, j = kralj_i + n * vektor[0], kralj_j + n * vektor[1]
            while v_sahovnici((i, j)):
                druga_figura = TRDNJAVA if abs(vektor[0] + vektor[1]) == 1 else LOVEC
                if self.plosca[i][j] != PRAZNO:
                    if self.plosca[i][j].barva != barva and ((n == 1 and self.plosca[i][j].vrsta == KRALJ) or
                                    self.plosca[i][j].vrsta in [KRALJICA, druga_figura]):
                        return True
                    else:
                        break  # Druge figure niso nevarne
                n += 1
                i, j = kralj_i + n * vektor[0], kralj_j + n * vektor[1]
        # Šah zaradi konja
        for i_premika, j_premika in Konj.SKOKI:
            if v_sahovnici((kralj_i + i_premika, kralj_j + j_premika)):
                if self.plosca[kralj_i + i_premika][kralj_j + j_premika] != PRAZNO and \
                            self.plosca[kralj_i + i_premika][kralj_j + j_premika].barva != barva and \
                            self.plosca[kralj_i + i_premika][kralj_j + j_premika].vrsta == KONJ:
                        return True
        # Šah zaradi kmeta
        vektorji_kmeta = [(1, 1), (1, -1)]
        koeficient = -1 if barva == BELI else 1
        for i_premika, j_premika in vektorji_kmeta:
            i_premika *= koeficient
            if v_sahovnici((kralj_i + i_premika, kralj_j + j_premika)):
                if self.plosca[kralj_i + i_premika][kralj_j + j_premika] != PRAZNO and \
                            self.plosca[kralj_i + i_premika][kralj_j + j_premika].barva != barva and \
                            self.plosca[kralj_i + i_premika][kralj_j + j_premika].vrsta == KMET:
                        return True
        return False

# sahec = Sah()
