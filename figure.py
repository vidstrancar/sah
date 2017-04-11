# figure in njihovo premikanje

import tkinter as tk


def je_v_polju(poteza):
    '''Preveri, ali je poteza v polju.'''
    x, y = poteza
    return 0 <= min(x, y) <= max(x, y) <= 7

def figura_istega(figura, poteza, IGRA):
    '''Vrne True, je na polju figura iste barve.'''
    i, j = poteza
    if IGRA[i][j] is not None:
        return figura.barva == IGRA[i][j].barva
    return False


class Figura:
    # vsebuje lastnosti, skupne vsem figuram; njeni podrazredi so posamezne figure

    def __init__(self, barva, polozaj, vrsta):
        self.barva = barva
        self.polozaj = polozaj
        self.vrsta = vrsta



    def vrni_barvo(self):
        return self.barva

    def veljavne_poteze(self, IGRA):
        '''Vrne seznam veljavnih potez glede na pozicijo.'''
        veljavne = []
        for vektor in self.vektorji:
            x, y = self.polozaj
            x += vektor[0]
            y += vektor[1]
            while je_v_polju((x, y)):
                if IGRA[x][y] is not None:
                    if IGRA[x][y].barva == self.barva:
                        break
                    else:  # nasprotno figuro lahko pojemo
                        veljavne.append((x, y))
                        break
                veljavne.append((x, y))
                x += vektor[0]
                y += vektor[1]
        print('Veljavne trdnjava:', veljavne)
        return veljavne


class Konj(Figura):
    def __init__(self, barva, polozaj):
        Figura.__init__(self, barva, polozaj, "konj")
        self.vektorji = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]

        self.foto = tk.PhotoImage(file=r"slike_figur\konj_{}.gif".format(self.barva))
        self.id_slike = None

    def __repr__(self):
        return 'Konj'

    def veljavne_poteze(self, IGRA):
        veljavne = []
        for vektor in self.vektorji:
            x, y = self.polozaj
            x += vektor[0]
            y += vektor[1]
            if je_v_polju((x, y)):
                if not figura_istega(self, (x, y), IGRA):
                    veljavne.append((x, y))
        return veljavne


class Kmet(Figura):
    def __init__(self, barva, polozaj):
        Figura.__init__(self, barva, polozaj, "kmet")
        self.vektor = (-1,0) if self.barva == 'beli' else (1,0)

        self.foto = tk.PhotoImage(file=r"slike_figur\kmet_{}.gif".format(self.barva))
        self.id_slike = None


    def __repr__(self):
        return 'Kmet'

    def veljavne_poteze(self, IGRA):
        '''Veljavni premiki kmeta.'''
        naprej = self.vektor[0]
        veljavne = []
        # ena naprej
        x, y = self.polozaj
        if IGRA[x + naprej][y] is None:
            veljavne.append((x + naprej, y))
            if IGRA[x + 2*naprej][y] is None:
                zacetek = 6 if self.barva == 'beli' else 1
                if x == zacetek: # če sta v začetnih vrstah
                    veljavne.append((x + 2*naprej, y))
        # vstran
        if je_v_polju((x + naprej, y + 1)):
            if not figura_istega(self, (x + naprej, y + 1), IGRA) and IGRA[x + naprej][y + 1] is not None:
                veljavne.append((x + naprej, y  + 1))
        if je_v_polju((x + naprej, y - 1)):
            if not figura_istega(self, (x + naprej, y - 1), IGRA) and IGRA[x + naprej][y - 1] is not None:
                veljavne.append((x + naprej, y - 1))
        return veljavne





class Kralj(Figura):
    def __init__(self, barva, polozaj):
        Figura.__init__(self, barva, polozaj, "kralj")
        self.vektorji = [(-1, 1), (1, 1), (-1, -1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]

        self.foto = tk.PhotoImage(file=r"slike_figur\kralj_{}.gif".format(self.barva))
        self.id_slike = None

    def __repr__(self):
        return 'Kralj'

    def je_sah(self, IGRA):
        '''Vrne True, če je kralj v šahu.'''
        diagonalni_vektorji = [(-1, -1), (1, 1), (1, -1), (-1, 1)]
        premi_vektorji = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for vektor in diagonalni_vektorji: # po diagonalah preverjamo, ali nas ogrožata nasprotna kraljica ali lovec
            x, y = self.polozaj
            x += vektor[0]
            y += vektor[1]
            while je_v_polju((x, y)):
                if IGRA[x][y] is not None:
                    if IGRA[x][y].barva == self.barva:
                        break
                    if IGRA[x][y].barva != self.barva:
                        if IGRA[x][y].vrsta in ["dama", "lovec"]:
                            return True
                        break # naleteli smo na eno njegovih drugih figur, ki nas 'ščiti'
                x += vektor[0]
                y += vektor[1]
        for vektor in premi_vektorji: # po vrstah / stolpcih preverjamo, ali nas ogrožata nasprotna kraljica ali trdnjava
            x, y = self.polozaj
            x += vektor[0]
            y += vektor[1]
            while je_v_polju((x, y)):
                if IGRA[x][y] is not None:
                    if IGRA[x][y].barva == self.barva:
                        break
                    if IGRA[x][y].barva != self.barva:
                        if IGRA[x][y].vrsta in ["dama", "trdnjava"]:
                            return True
                        break
                x += vektor[0]
                y += vektor[1]
        # preverimo še šah zaradi konja
        vektorji_konja = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
        for vektor in vektorji_konja:
            x, y = self.polozaj
            x += vektor[0]
            y += vektor[1]
            if je_v_polju((x, y)):
                if IGRA[x][y] is not None:
                    if IGRA[x][y].barva != self.barva:
                        if IGRA[x][y].vrsta == "konj":
                            return True
        # šah zaradi kmeta
        x, y = self.polozaj
        vektor = 1 if self.barva == 'crni' else -1
        if je_v_polju((x + vektor, y + 1)) and IGRA[x + vektor][y + 1] is not None and IGRA[x + vektor][y + 1].barva != self.barva and IGRA[x + vektor][y + 1].vrsta == 'kmet':
            return True
        if je_v_polju((x + vektor, y - 1)) and IGRA[x + vektor][y - 1] is not None and IGRA[x + vektor][y - 1].barva != self.barva and IGRA[x + vektor][y - 1].vrsta == 'kmet':
            return True
        return False



    def veljavne_poteze(self, IGRA): # povozimo metodo iz Figure
        '''Vrne seznam dovoljenih potez za kralja.'''
        veljavne = []
        print('KRALJ KRALJ KRALJ')
        for vektor in self.vektorji:
            x, y = self.polozaj
            x += vektor[0]
            y += vektor[1]
            if je_v_polju((x, y)):
                if not figura_istega(self, (x,y), IGRA):
                    veljavne.append((x, y))
        return veljavne

class Dama(Figura):
    def __init__(self, barva, polozaj):
        Figura.__init__(self, barva, polozaj, "dama")
        self.vektorji = [(-1, 1), (1, 1), (-1, -1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]

        self.foto = tk.PhotoImage(file=r"slike_figur\dama_{}.gif".format(self.barva))
        self.id_slike = None

    def __repr__(self):
        return 'Dama'


class Lovec(Figura):
    def __init__(self, barva, polozaj):
        Figura.__init__(self, barva, polozaj, "lovec")
        self.vektorji = [(-1,-1), (1,1), (1,-1), (-1,1)]


        self.foto = tk.PhotoImage(file=r"slike_figur\lovec_{}.gif".format(self.barva))
        self.id_slike = None


    def __repr__(self):
        return 'Lovec'


class Trdnjava(Figura):
    def __init__(self, barva, polozaj):
        Figura.__init__(self, barva, polozaj, "trdnjava")
        self.vektorji = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        self.foto = tk.PhotoImage(file=r"slike_figur\trdnjava_{}.gif".format(self.barva))
        self.id_slike = None

    def __repr__(self):
        return 'Trdnjava'

















# class Konj(Figura):
#
#     def __init__(self, igra, barva, polozaj):
#         Figura.__init__(self, igra, barva, polozaj)


#################################################################################3
##      spodnje funkcije potrebujejo dopolnitev, spremembo ali so odveč        ##3
#################################################################################3


# =====================================================================# prvi poskusi

polozaj_lastnih = [(1, 1)]
polozaj_nasprotnih = [(2, 2), (4, 4)]


def lastne_ovire(zeljena_poteza, polozaj_lastnih):
    '''Figura se ne sme premakniti na polje, ki je že zasedeno z eno od figur iste barve.'''
    if zeljena_poteza in polozaj_lastnih:
        return False
    return True


##class Konj:
##    '''Zameril si se mi, konj!'''
##    def __init__(self, IGRA):
##        self.polozaj = polozaj
##        self.poteze = []
##        self.mozne_poteze(polozaj) # napolnimo self.poteze z možnimi potezami
##
##    def mozne_poteze(self, polozaj):
##        '''Vrne seznam možnih potez konja.'''
##        x, y = polozaj # x: A, B, C, D, E, F, G, H;    y: 1, 2, 3, 4, 5, 6, 7, 8
##        mozne_p = list()
##        veljavne_mozne  = list()
##        # gor in dol
##        gor = y + 2
##        dol = y - 2
##        mozne_p += [(x-1, gor), (x+1, gor)]
##        mozne_p += [(x-1, dol), (x+1, dol)]
##        # levo in desno
##        levo = x - 2
##        desno = x + 2
##        mozne_p += [(levo, y-1), (levo, y+1)]
##        mozne_p += [(desno, y-1), (desno, y+1)]
##        for poteza in mozne_p:
##            if je_v_polju(poteza) and lastne_ovire(poteza, polozaj_lastnih):
##                veljavne_mozne.append(poteza)
##        self.poteze.extend(veljavne_mozne)
##        return veljavne_mozne
##
polozaj = (1, 4)
polozaj2 = (0, 0)
polozaj3 = (4, 4)
##
##konj = Konj((1, 4))
##print('konji\n', konj.poteze, sep = '')
##
##konj = Konj(polozaj2)
##print(konj.poteze)
##
##konj = Konj(polozaj3)
##print(konj.poteze)

# class Lovec:
#     def __init__(self, polozaj):
#         self.polozaj = polozaj
#         self.poteze = []
#         self.mozne_poteze(polozaj)
#
#     def mozne_poteze(self, polozaj):
#         '''Vrne seznam vseh možnih potez lovca.'''
#         mozne_veljavne = []
#         x, y = polozaj
#         odmik = 1
#         # desno
#         while x + odmik <= 7:
#             if 0 <= y - odmik:
#                 mozne_veljavne.append((x + odmik, y - odmik)) # dol
#             if y + odmik <= 7:
#                 mozne_veljavne.append((x + odmik, y + odmik)) # gor
#             odmik += 1
#         # levo
#         odmik = 1
#         while 0 <= x - odmik:
#             if 0 <= y - odmik:
#                 mozne_veljavne.append((x - odmik, y - odmik)) # dol
#             if y + odmik <= 7:
#                 mozne_veljavne.append((x - odmik, y + odmik)) # gor
#             odmik += 1 # PREKINITI JE TREBA, ČE JE POT NAPREJ BLOKIRANA Z LASTNO ALI NASPROTNO FIGURO
#         for poteza in mozne_veljavne:
#             if lastne_ovire(poteza, polozaj_lastnih):
#                 self.poteze.extend([poteza])
#         return mozne_veljavne
#
# lovec = Lovec(polozaj)
# print('\nlovci\n', polozaj, lovec.poteze, sep = '')
#
# lovec = Lovec(polozaj2)
# print(polozaj2, lovec.poteze)
#
# lovec = Lovec(polozaj3)
# print(polozaj3, lovec.poteze)
#
# class Kmet():
#     '''Počasi se daleč pride.'''
#     def __init__(self, polozaj, polozaj_lastnih, polozaj_nasprotnih):
#         self.polozaj = polozaj
#         self.polozaj_lastnih = polozaj_lastnih
#         self.polozaj_nasprotnih = polozaj_nasprotnih
#         self.poteze = []
#         self.mozne_poteze(polozaj)
#
#     def mozne_poteze(polozaj):
#         '''Vrne možne poteze kmeta.'''
#         # povsod bo treba preverjati, ali ne odkrijemo šaha
#         polozaj_lastnih = self.polozaj_lastnih # lahko pa dava v parametre funkcije: mozne_poteze(polozaj, polozaj_lastnih, polozaj_nasprotnih) in tedaj self... ni potreben
#         polozaj_nasprotnih = self.polozaj_nasprotnih
#         mozne = []
#         # premik za ena naprej
#         x, y = polozaj
#         # append in extend ne vračata ničesar, le spreminjata sezname; to je nevarno
#         if (x, y+1) not in polozaj_lastnih or (x, y+1) not in polozaj_nasprotnih:
#             mozne.append(x, y+1)
#         # da lahko poje levo ali desno
#         if (x+1, y+1) in polozaj_nasprotnih:
#             mozne.append(x+1, y+1)
#         if (x+1, y-1) in polozaj_nasprotih:
#             mozne.append(x+1, y+1)
#         # za dve naprej
#
#
#         # en-passant (mimogrede)
#
#
# class Trdnjava():
#     '''Castrum ad Fluvium frigidum.'''
#     def __init__(self, polozaj, polozaj_lastnih, polozaj_nasprotnih):
#         self.poteze = [] # ali zaenkrat rabiva kaj več?
#         self.mozne_poteze(polozaj, polozaj_lastnih, polozaj_nasprotnih)
#
#
#     def mozne_poteze(self, polozaj, polozaj_lastnih, polozaj_nasprotnih):
#         '''Vrne seznam vseh možnih potez trdnjave.'''
#         mozne = []
#         (x, y) = polozaj
#                                        # for i in range(2): # zaradi simetrije, za gor in dol bomo zamenjali vlogi x in y :)
#         # desno:
#         premik = 1
#         while x + premik <= 7:
#             if (x + premik, y) in polozaj_lastnih:
#                 break # blokirana linija
#             if (x + premik, y) in polozaj_nasprotnih:
#                 mozne.append((x + premik, y))
#                 break # polja za nasprotno figuro so blokirana
#             mozne.append((x + premik, y))
#             premik += 1
#         # levo:
#         premik = 1
#         while 0 <= x - premik:
#             if (x - premik, y) in polozaj_lastnih:
#                 break
#             if (x - premik, y) in polozaj_nasprotnih:
#                 mozne.append((x - premik, y))
#                 break
#             mozne.append((x - premik, y))
#             premik += 1
#                                         # sedaj zamenjamo vlogi x in y :)
#                                         # (y, x) = polozaj
#         # gor:
#         premik = 1
#         while y + premik <= 7:
#             if (x, y + premik) in polozaj_lastnih:
#                 break # blokirana linija
#             if (x, y + premik) in polozaj_nasprotnih:
#                 mozne.append((x, y + premik))
#                 break # polja za nasprotno figuro so blokirana
#             mozne.append((x, y + premik))
#             premik += 1
#         # dol:
#         premik = 1
#         while 0 <= y - premik:
#             if (x, y - premik) in polozaj_lastnih:
#                 break
#             if (x, y - premik) in polozaj_nasprotnih:
#                 mozne.append((x, y - premik))
#                 break
#             mozne.append((x, y - premik))
#             premik += 1
#         self.poteze.extend(mozne)
#         return mozne
#
#
# trdnjava = Trdnjava(polozaj, polozaj_lastnih, polozaj_nasprotnih)
# print('\ntrdnjave\n', polozaj, trdnjava.poteze, sep = '')






# šah = Šah('šahovnica')
