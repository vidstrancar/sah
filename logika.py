# logika igre
# Tukaj se preverja stanje igre in veljavnost potez. Tukaj se ZARES DOGAJA :)

from figure import *

class Šah:
    '''Kraljevska igra kraljev.'''

    def __init__(self):

        self.zacni_igro()


    def zacni_igro(self):
        '''Začetno stanje igre.'''

        # bele figure
        K = Kralj('beli', (7, 4))
        D = Dama('beli', (7, 3))
        T1 = Trdnjava('beli', (7, 0))
        T2 = Trdnjava('beli', (7, 7))
        L1 = Lovec('beli', (7, 2))
        L2 = Lovec('beli', (7, 5))
        S1 = Konj('beli', (7, 1))
        S2 = Konj('beli', (7, 6))
        k1, k2, k3, k4, k5, k6, k7, k8 = [Kmet('beli', (6, i)) for i in range(8)]

        # črne figure
        K_ = Kralj('crni', (0, 4))
        D_ = Dama('crni', (0, 3))
        T1_ = Trdnjava('crni', (0,0))
        T2_ = Trdnjava('crni', (0, 7))
        L1_ = Lovec('crni', (0, 2))
        L2_ = Lovec('crni', (0, 5))
        S1_ = Konj('crni', (0, 1))
        S2_ = Konj('crni', (0, 6))
        k1_, k2_, k3_, k4_, k5_, k6_, k7_, k8_ = [Kmet('crni', (1, i)) for i in range(8)]

        # možnosti za rošado:
        self.rosada_b1 = True # leva
        self.rosada_b2 = True
        self.rosada_c1 = True
        self.rosada_c2 = True


        # self.poteza = 0
        self.na_potezi = 'beli'
        self.konec_igre = False
        self.dovoljene_poteze_nasprotnika = [] # tja se naš kralj ne sme premakniti
        # self.dovoljene_poteze = [(i, j) for i in range(8) for j in range(8)] # na začetku, za lažje premikanje :)
        self.oznacena_figura = None



        # matrika s trenutno pozicijo
        self.IGRA = [
            [T1_ , S1_ , L1_ , D_  , K_  , L2_ , S2_ , T2_ ],
            [k1_ , k2_ , k3_ , k4_ , k5_ , k6_ , k7_ , k8_ ],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [k1  , k2  , k3  , k4  , k5  , k6  , k7  , k8  ],
            [T1  , S1  , L1  , D   , K   , L2  , S2  , T2  ]]
        [print(i) for i in self.IGRA]



    def lahko_oznacimo(self, i, j):
        '''Vrne True, če smemo označiti željeno figuro, False sicer.'''
        zeljena_figura = self.IGRA[i][j]
        if zeljena_figura is None:  # smo kliknili 'v prazno':
            return False
        if zeljena_figura.barva != self.na_potezi:
            return False
        # se pozanimamo, če smo v šahu, ga moramo preprečit: ali ima figura, ki jo želimo označiti, kaj možnosti, da to doseže?

        return True


    def je_poteza_veljavna(self, i, j):
        '''Vrne dovoljene poteze z ozirom na označeno figuro.'''
        barva = self.oznacena_figura.barva
        if self.IGRA[i][j] is not None:
            if self.IGRA[i][j].barva == barva:
                return False
        return True


    def premakni_figuro(self, novi_i, novi_j):
        '''Premakne figuro v matriki igre.'''
        '''Najprej se pozanima, ali jo je mogoče premakniti.'''
        stari_i, stari_j = self.oznacena_figura.polozaj
        self.IGRA[stari_i][stari_j] = None # polje, ki ga je figura zapustila, je prazno
        self.oznacena_figura.polozaj = (novi_i, novi_j) # nastavimo figuri novi koordinati
        self.IGRA[novi_i][novi_j] = self.oznacena_figura # premaknemo na novi koordinati v matriki IGRE

        # self.IGRA[novi_i][novi_j] = None # da zbrišemo prejšnjo figuro, ampak to je v resnici ne izbriše, kajne??? KAKO SE V RESNICI ZBRIŠE RAZRED???

        self.na_potezi = 'crni' if self.na_potezi == 'beli' else 'beli'
        print(self.na_potezi)







#################################################################################3
##      spodnje funkcije potrebujejo dopolnitev, spremembo ali so odveč        ##3
#################################################################################3


def veljavne_poteze(self):
    '''Osveži seznam vseh veljavnih potez igralca, ki je na vrsti.'''
    veljavne_poteze = []
    for i in range(7):
        for j in range(7):  # gremo čez vsako polje v šahovnici
            na_potezi = na_potezi(self)
            figura = self.IGRA[i][j]
            if figura is not None:
                if figura.barva == na_potezi:
                    veljavne_poteze.append(figura.veljavne_poteze)
    self.veljavne_poteze.extend(veljavne_poteze)



            





        

     
