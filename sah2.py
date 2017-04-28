import os
from copy import *


def v_sahovnici(polozaj):
    x, y = polozaj
    return  0 <= x <= 7 and 0 <= y <= 7


class Figura:
    def __init__(self, polozaj, barva):
        self.ziv = True
        self.barva = barva
        self.i, self.j = polozaj # stolpec, vrstica
        self.vektorji_premika = []


    def izracunaj_dovoljene_premike_iterator(self, slika,
                                             igra):  ##vraca tocke(na sahovnici) na katere se lahko premaknemo z to figuro
        for i_premika, j_premika in self.vektorji_premika:
            n = 1
            while v_sahovnici((self.i + n * i_premika, self.j + n * j_premika)):
                if slika[self.i + n * i_premika][self.j + n * j_premika] is None:
                    yield ((self.i + n * i_premika, self.j + n * j_premika))
                else:
                    if slika[self.i + n * i_premika][self.j + n * j_premika].barva != self.barva:
                        yield ((self.i + n * i_premika, self.j + n * j_premika))
                    break
                n += 1

    def pojej(self):
        self.ziv = False
        self.i *= -1
        self.j *= -1

    def premakni(self, koncna_lokacija):
        i_koncen, j_koncen = koncna_lokacija
        self.i = i_koncen
        self.j = j_koncen

    def __str__(self):
        return '{1} {0}, na ({2}, {3})'.format(self.vrsta, self.barva, self.i, self.j)

class Kraljica(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'kraljica'
        self.vektorji_premika = [(-1, 1), (1, 1), (-1, -1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        self.vrednost = 9


class Lovec(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'lovec'
        self.vektorji_premika = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        self.vrednost = 3


class Konj(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'konj'
        self.vektorji_premika = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]
        self.vrednost = 3

    def izracunaj_dovoljene_premike_iterator(self, slika, igra):
        for i_premika, j_premika in self.vektorji_premika:
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if slika[self.i + i_premika][self.j + j_premika] is None:
                    yield ((self.i + i_premika, self.j + j_premika))
                elif slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                    yield ((self.i + i_premika, self.j + j_premika))


class Trdnjava(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'trdnjava'
        self.premaknjen = False
        self.vektorji_premika = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.vrednost = 5

    def premakni(self, koncna_lokacija):
        Figura.premakni(self, koncna_lokacija)
        self.premaknjen = True


class Kralj(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.sah_mat = False
        self.barva = barva
        self.vrsta = 'kralj'
        self.premaknjen = False
        self.vektorji_premika = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.vrednost = 0

    def izracunaj_dovoljene_premike_iterator(self, slika,
                                             igra):  ##dodamo kot parameter še vse veljavne poteze nasprotnih, za preverjanje saha
        for i_premika, j_premika in self.vektorji_premika:
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if slika[self.i + i_premika][self.j + j_premika] is None or \
                                slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                    yield ((self.i + i_premika, self.j + j_premika))
        # možnost rošade
        # if not self.premaknjen:
        #     # leva rošada
        #     if not slika[self.i][0].premaknjen:
        #         leva = True
        #         # preverimo, če so polja vmes prosta
        #         for j in [3, 2, 1]:
        #             if slika[self.i][j] is not None:
        #                leva = False
        #                break
        #         if leva:
        #             yield('leva_rošada')
        #     # desna rošada
        #     if not (slika[self.i][7].premaknjen):
        #         # print('desnaaaa')
        #         desna = True
        #         for j in [5, 6]:
        #             if slika[self.i][j] is not None:
        #                 desna = False
        #                 break
        #         if desna:
        #             yield('desna_rošada')


    def premakni(self, koncna_lokacija):
        Figura.premakni(self, koncna_lokacija)
        self.premaknjen = True


class Kmet(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'kmet'
        self.vektorji_premika = [(1, 0), (2, 0), (1, 1), (1, -1)]
        self.koeficient = -1 if self.barva == 'bel' else 1
        self.vrednost = 1

    def izracunaj_dovoljene_premike_iterator(self, slika, igra):  ##dodaj en passeu
        for i_premika, j_premika in self.vektorji_premika:
            i_premika *= self.koeficient
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if j_premika != 0: # pojemo nasprotnikovo figuro
                    if slika[self.i + i_premika][self.j + j_premika] is not None and \
                                    slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                        yield ((self.i + i_premika, self.j + j_premika))
                else: # skoka naprej
                    zacetna_pozicija = 1 if self.barva == 'crn' else 6
                    if abs(i_premika) == 1 and slika[self.i + i_premika][self.j] is None: # skok za 1
                        yield ((self.i + i_premika, self.j))
                    elif slika[self.i + i_premika // 2][self.j] is None and slika[self.i + i_premika][self.j] is None and \
                            self.i == zacetna_pozicija: # skok za 2, obe polji morata biti prosti
                        yield ((self.i + i_premika, self.j))




class Sah():
    def __init__(self):
        self.igra = [] # beleži zgodovino igre
        self.na_vrsti = 'bel'
        self.zmagovalec = None
        self.figure = {'bel': [Kmet((6, i), 'bel') for i in range(8)] +
                              [Lovec((7, 2), 'bel'), Lovec((7, 5), 'bel'),
                               Trdnjava((7, 0), 'bel'), Trdnjava((7, 7), 'bel'),
                               Konj((7, 1), 'bel'), Konj((7, 6), 'bel'),
                               Kraljica((7, 3), 'bel'),
                               Kralj((7, 4), 'bel')],

                       'crn': [Kmet((1, i), 'crn') for i in range(8)] +
                              [Lovec((0, 2), 'crn'), Lovec((0, 5), 'crn'),
                               Konj((0, 1), 'crn'), Konj((0, 6), 'crn'),
                               Trdnjava((0, 0), 'crn'), Trdnjava((0, 7), 'crn'),
                               Kraljica((0, 3), 'crn'),
                               Kralj((0, 4), 'crn')]}


        self.slika = self.figure_v_sliko()


    def vse_poteze(self):
        '''Vrne seznam vseh potez v dani situaciji.'''
        poteze = dict()
        for figura in self.figure[self.na_vrsti]:
            poteze_figure = list(self.dovoljene_poteze_iterator(figura))
            poteze[figura] = poteze_figure
            # print(figura, poteze_figure)
        return poteze



    def kopija(self):
        '''Vrne kopijo trenutnega stanja igre. Uporabno za minimax.'''
        sah = Sah()
        # sah.figure = deepcopy(self.figure)
        sah.figure = self.figure.copy()
        sah.na_vrsti = self.na_vrsti
        # sah.igra = deepcopy(self.igra)
        sah.igra = self.igra.copy()
        sah.slika = self.figure_v_sliko()
        return sah



    def stanje_igre(self):
        '''Če je igre konec, nastavi zmagovalca.'''
        for figura in self.figure[self.na_vrsti]:
            if len(list(self.dovoljene_poteze_iterator(figura))) > 0:
                return
        self.zmagovalec = self.nasprotna_barva()
        return self.zmagovalec


    def vrni_kralja_na_vrsti(self):
        '''Vrne figuro nasprotnega kralja.'''
        for figura in self.figure[self.na_vrsti]:
            if figura.vrsta == 'kralj':
                return figura

    def nasprotna_barva(self):
        '''Vrne barvo nasprotnega igralca.'''
        return 'crn' if self.na_vrsti == 'bel' else 'bel'

    def figure_v_sliko(self):
        '''Pretvori iz slovarjev figur v matriko figur in jo vrne.'''
        slika = [[None] * 8 for i in range(8)]
        vse_figure = self.figure['bel'] + self.figure['crn']
        for figura in vse_figure:
            if figura.ziv:
                slika[figura.i][figura.j] = figura
        return slika

    def vrni_potezo(self):
        '''Povrne situacijo pred eno potezo.'''
        if len(self.igra) != 0:
            poteza, pojedena_figura, figura = self.igra.pop()
            i, j = figura.i, figura.j # na teh koordinatah je bila pojedena figura
            self.premakni_figuro(figura, poteza, False)
            if pojedena_figura is not None:
                self.premakni_figuro(pojedena_figura, (i, j), False)
                pojedena_figura.ziv = True
            self.na_vrsti = self.nasprotna_barva()

    def premakni_figuro(self, figura, poteza, belezi_zgo=True):
        '''Premakne figuro, spremeni njene atribute. Zabeleži v zgodovino igre.'''
        i_z, j_z = figura.i, figura.j
        i_k, j_k = poteza
        pojedena_figura = self.slika[i_k][j_k]  # lahko je tudi None
        if belezi_zgo:
            self.igra.append(((i_z, j_z), pojedena_figura, figura))
        if self.slika[i_k][j_k] is not None:
            self.slika[i_k][j_k].pojej()
        figura.premakni((i_k, j_k))
        self.slika[i_z][j_z] = None
        self.slika[i_k][j_k] = figura


    def naredi_potezo(self, figura, poteza):
        '''Služi kot filter za rošade in en-passante.'''
        if poteza in self.dovoljene_poteze_iterator(figura):
            # promocija kmeta
            # zadnja_vrsta = 0 if figura.barva == 'bel' else 7
            # if figura.vrsta == 'kmet' and poteza[0] == zadnja_vrsta:
            #     nova_kraljica = Kraljica((figura.i, figura.j), figura.barva)
            #     figura.ziv = False
            #     self.figure[figura.barva].append(nova_kraljica)
            #     self.figure_v_sliko()
            #     self.premakni_figuro(nova_kraljica, poteza)
            # rošadi
            if poteza == 'leva_rošada':
                self.premakni_figuro(figura, (figura.i, 2)) # premaknemo kralja
                self.premakni_figuro(self.slika[figura.i][0], (figura.i, 3)) # premaknemo trdnjavo
            elif poteza == 'desna_rošada':
                self.premakni_figuro(figura, (figura.i, 6))
                self.premakni_figuro(self.slika[figura.i][7], (figura.i, 5))
            else:
                # print('sah prejel ukaz, naj premakne {} na {}'.format(figura, poteza))
                self.premakni_figuro(figura, poteza)
                # print('sah premaknil figuro')
                # for figura in self.figure[self.na_vrsti]:
                    # print(figura)
            # spremenimo, kdo je na vrsti
            self.na_vrsti = self.nasprotna_barva()
            return True
        return False

    def dovoljene_poteze_iterator(self, figura):
        '''Vrne seznam dovoljenih potez za posamezno figuro.'''
        for poteza in figura.izracunaj_dovoljene_premike_iterator(self.slika, self.igra):
            if poteza == 'leva_rošada':
                veljavna_leva = True
                for j in [4, 3, 2]: # gledamo, ali bo kralj kdajkoli vmes v šahu
                    if not self.simuliraj_potezo(figura, (figura.i, j)):
                        veljavna_leva = False
                if veljavna_leva:
                    yield poteza
            elif poteza == 'desna_rošada':
                veljavna_desna = True
                for j in [4, 5, 6]:
                    if not self.simuliraj_potezo(figura, (figura.i, j)):
                        veljavna_desna = False
                if veljavna_desna:
                    yield poteza                                                
            # za vse druge primere                                     
            elif self.simuliraj_potezo(figura, poteza):
                yield poteza

    def simuliraj_potezo(self, figura, poteza):
        '''Simulira potezo, in vrne True, če je veljavna.'''
        stari_i, stari_j = figura.i, figura.j
        novi_i, novi_j = poteza
        kar_je_na_novem_mestu = self.slika[novi_i][novi_j]
        # sedaj simuliramo potezo, spreminjamo le stanje v matriki
        self.slika[stari_i][stari_j] = None
        self.slika[novi_i][novi_j] = figura
        figura.i = novi_i
        figura.j = novi_j
        # preverimo, ali bo šah po potezi
        bo_sah = self.bo_sah_po_potezi()
        # vrnemo v prvotno stanje
        self.slika[stari_i][stari_j] = figura
        self.slika[novi_i][novi_j] = kar_je_na_novem_mestu
        figura.i = stari_i
        figura.j = stari_j
        return not bo_sah

    def bo_sah_po_potezi(self):
        '''Vrne True, če bo po potezi šah.'''
        kralj = self.vrni_kralja_na_vrsti()
        # šah zaradi kraljice, trdnjave ali lovca
        vektorji_nevarnih = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (1, -1), (-1, -1), (-1, 1)]
        for vektor in vektorji_nevarnih:
            n = 1
            i, j = kralj.i + n * vektor[0], kralj.j + n * vektor[1]
            while v_sahovnici((i, j)):
                druga_figura = 'trdnjava' if abs(vektor[0] + vektor[1]) == 1 else 'lovec'
                if self.slika[i][j] is not None:
                    if self.slika[i][j].barva != kralj.barva and ((n == 1 and self.slika[i][j].vrsta == 'kralj') or \
                                    self.slika[i][j].vrsta in ['kraljica', druga_figura]):
                        return True
                    else:
                        break  # druge figure niso nevarne
                n += 1
                i, j = kralj.i + n * vektor[0], kralj.j + n * vektor[1]
        # šah zaradi konja
        vektorji_konja = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]
        for i_premika, j_premika in vektorji_konja:
            if v_sahovnici((kralj.i + i_premika, kralj.j + j_premika)):
                if self.slika[kralj.i + i_premika][kralj.j + j_premika] is not None and \
                            self.slika[kralj.i + i_premika][kralj.j + j_premika].barva != kralj.barva and \
                            self.slika[kralj.i + i_premika][kralj.j + j_premika].vrsta == 'konj':
                        return True
        # šah zaradi kmeta
        vektorji_kmeta = [(1, 1), (1, -1)]
        koeficient = -1 if kralj.barva == 'bel' else 1
        for i_premika, j_premika in vektorji_kmeta:
            i_premika *= koeficient
            if v_sahovnici((kralj.i + i_premika, kralj.j + j_premika)):
                if self.slika[kralj.i + i_premika][kralj.j + j_premika] is not None and \
                            self.slika[kralj.i + i_premika][kralj.j + j_premika].barva != kralj.barva and \
                            self.slika[kralj.i + i_premika][kralj.j + j_premika].vrsta == 'kmet':
                        return True
        return False

# sahec = sah()

