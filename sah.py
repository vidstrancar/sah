# GUI: risanje in zaznavanje klikov

# Zvrsti graficnih objektov
POLJE="polje" # Ta se nariše enkrat in se potem ne briše več
FIGURA="figura"
PLAVI="plavi"

import tkinter as tk
import argparse        # Za argumente iz ukazne vrstice
import logging         # Za odpravljanje napak
import os

import logika
from clovek import *
from racunalnik import *
from minimax import *

MINIMAX_GLOBINA = 2


class Sahovnica():
    # Nastavitve velikosti
    VELIKOST_POLJA = 100
    ODMIK = 30

    def __init__(self, master, globina):
        self.igralec_beli = None # Nastavimo ob začetku igre
        self.igralec_crni = None
        self.sah = None

        # Ob zaprtju okna
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # Glavni menu
        menu = tk.Menu(master)
        master.config(menu=menu) # Dodamo glavni menu v okno

        # Podmenu za izbiro igre
        menu_igra = tk.Menu(menu)
        menu.add_cascade(label="Igra", menu=menu_igra)
        menu_igra.add_command(label="Človek - Človek",
                              command=lambda: self.zacni_igro(Clovek(self), Clovek(self)))
        menu_igra.add_command(label="Človek - Računalnik",
                              command=lambda: self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina))))
        menu_igra.add_command(label="Računalnik - Človek",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)), Clovek(self)))
        menu_igra.add_command(label="Računalnik - Računalnik",
                              command=lambda: self.zacni_igro(Racunalnik(self, Minimax(globina)), Racunalnik(self, Minimax(globina))))

        # Igralna površina
        self.plosca = tk.Canvas(master, width=Sahovnica.VELIKOST_POLJA * 10, height=Sahovnica.VELIKOST_POLJA * 10)
        self.plosca.grid(row=1, column=0)

        # Označena figura
        self.oznaceno_polje = None

        # Slovar slik vseh figur
        self.slike_figur = None

        # Narišemo šahovnico
        self.narisi_sahovnico()


        # Registriramo se za klike z miško in tipkovnico
        self.plosca.bind('<Button-1>', self.klik)
        self.plosca.bind('<Control-z>', self.vrni_potezo)
        self.plosca.focus_force()


        # Oznaka za izpisovanje
        self.izpis_potez = tk.StringVar(master, value="Dobrodošli šah!")
        tk.Label(master, textvariable=self.izpis_potez).grid(row=0, column=0)


        # Začnemo igro v načinu __ proti __
        # self.zacni_igro(Clovek(self), Clovek(self))
        # self.zacni_igro(Clovek(self), Racunalnik(self, Minimax(globina)))
        # self.zacni_igro(Racunalnik(self, Minimax(globina)), Clovek(self))
        self.zacni_igro(Racunalnik(self, Minimax(globina)), Racunalnik(self, Minimax(globina)))


    def vrni_potezo(self, event):
        '''Razveljavi zadnjo potezo.'''
        self.izpis_potez.set('Vračamo potezo.')
        self.sah.vrni_potezo()
        self.prikaz_figur()

    def zacni_igro(self, beli, crni):
        '''Nastavi stanje na začetek igre. Za igralca uporabi dana igralca.'''
        # Ustavimo vse igralce, ki morda razmišljajo
        self.prekini_igralce()

        # Začnemo novo igro
        self.sah = logika.Sah()
        self.vzpostavi_slike_figur()
        self.prikaz_figur()
        self.izpis_potez.set("Na potezi je beli.")

        # Nastavimo igralca
        self.igralec_beli = beli
        self.igralec_crni = crni

        # Nastavi odštevalnik ure in predaj potezo belemu
        self.igralec_beli.igraj()



    def prekini_igralce(self):
        '''Sporoči igralcem, da morajo nehati razmišljati.'''
        logging.debug("prekinjam igralce")
        if self.igralec_beli: self.igralec_beli.prekini()
        if self.igralec_crni: self.igralec_crni.prekini()

    def zapri_okno(self, master):
        '''Ustavi vlakna, ki razmišljajo in zapre okno.'''
        self.prekini_igralce()
        master.destroy()

    def narisi_sahovnico(self):
        '''Nariše šahovnico 8d X 8d. Desno spodaj je belo polje.'''
        x1, y1 = Sahovnica.ODMIK, Sahovnica.ODMIK  # Določimo odmik
        for i in range(8):  # Vrstice
            for j in range(8):  # Stolpci
                barva = "white" if (i + j) % 2 == 0 else "gray"
                self.plosca.create_rectangle(x1, y1, x1 + Sahovnica.VELIKOST_POLJA, y1 + Sahovnica.VELIKOST_POLJA,
                                                        fill=barva, tag=POLJE)
                x1 += Sahovnica.VELIKOST_POLJA  # Naslednji kvadratek v vrsti
            x1, y1 = Sahovnica.ODMIK, Sahovnica.ODMIK + Sahovnica.VELIKOST_POLJA * (i + 1)  # Premaknemo se eno vrstico navzdol

    def narisi_plave(self, plave_tocke):
        '''Z modro pobarva polja, na katere se označena figura lahko premakne..'''
        for (i,j) in plave_tocke:
            barva = "blue"
            x1 = Sahovnica.ODMIK + j * Sahovnica.VELIKOST_POLJA
            y1 = Sahovnica.ODMIK + i * Sahovnica.VELIKOST_POLJA
            self.plosca.create_rectangle(x1, y1, x1 + Sahovnica.VELIKOST_POLJA, y1 + Sahovnica.VELIKOST_POLJA, fill=barva, tag=PLAVI)

    def klik(self, event):
        '''Odgovori na klik uporabnika. Sporočimo tistemu, ki je na potezi'''
        zmagovalec = self.sah.stanje_igre()
        if zmagovalec is None:
            i = int((event.y - Sahovnica.ODMIK) // Sahovnica.VELIKOST_POLJA) # Vrstica
            j = int((event.x - Sahovnica.ODMIK) // Sahovnica.VELIKOST_POLJA) # Stolpec
            poteza = (i, j)
            logging.debug("Klik na polje {0}".format((i,j)))
            if logika.v_sahovnici(poteza):
                if self.sah.na_vrsti == logika.BELI:
                    self.igralec_beli.klik(poteza)
                elif self.sah.na_vrsti == logika.CRNI:
                    self.igralec_crni.klik(poteza)
                else:
                    # Nihče ni na potezi, zato ne naredimo nič
                    pass
            else:
                logging.debug("klik izven plošče")
        else:
            logging.debug("Klik v stanju igre {0}".format(zmagovalec))

    def razberi_potezo(self, polje):
        '''Prebere katero polje je označil igralec na vrsti.'''
        i, j = polje
        if self.oznaceno_polje is None:
            if (self.sah.plosca[i][j] != logika.PRAZNO) and (self.sah.na_vrsti == self.sah.plosca[i][j].barva):
                self.oznaceno_polje = polje
                logging.debug("označili smo polje {0}".format(self.oznaceno_polje))
                plava = [poteza[1] for poteza in self.sah.poteze_polja(polje)]
                self.prikaz_figur(plave_tocke = plava) # Pobarvamo dovoljena polja
        else: # Polje že imamo označeno
            self.premakni_figuro(self.oznaceno_polje, polje)

    def premakni_figuro(self, polje1, polje2):
        '''Premakne figuro, če je poteza veljavna.'''
        logging.debug('gui prejel ukaz, naj premakne {} na {}'.format(polje1, polje2))
        self.sah.naredi_potezo((polje1, polje2))
        # V vsakem primeru polje odznacimo
        self.oznaceno_polje = None
        self.prikaz_figur()

        # Preverimo, ali je prišlo do zmage
        zmagovalec = self.sah.stanje_igre()
        if zmagovalec is not None:
            self.izpis_potez.set('Zmagal je {}.'.format(zmagovalec))
        else:
            # Igro nadaljujemo
            if self.sah.na_vrsti == logika.BELI:
                self.izpis_potez.set('Na potezi je {}.'.format(self.sah.na_vrsti))
                self.igralec_beli.igraj()
            elif self.sah.na_vrsti == logika.CRNI:
                self.izpis_potez.set('Na potezi je {}.'.format(self.sah.na_vrsti))
                self.igralec_crni.igraj()
            else:
                assert False

    def vzpostavi_slike_figur(self):
        '''Poveže vsako figuro z njeno sliko.'''
        self.slike_figur = dict()
        for barva in (logika.BELI, logika.CRNI):
            for vrsta in (logika.KRALJ, logika.KRALJICA, logika.TRDNJAVA, logika.LOVEC, logika.KONJ, logika.KMET):
                datoteka = os.path.join(os.path.dirname(__file__), 'slike_figur', '{}_{}.gif'.format(vrsta, barva))
                self.slike_figur[(barva, vrsta)] = tk.PhotoImage(file=datoteka)

    def prikaz_figur(self, plave_tocke=[]):
        '''Pobriše vse figure in nariše nove.'''
        self.plosca.delete(FIGURA)
        self.plosca.delete(PLAVI)
        self.narisi_plave(plave_tocke)
        for i in range(8):
            for j in range(8):
                figura = self.sah.plosca[i][j]
                if figura != logika.PRAZNO:
                    foto = self.slike_figur[(figura.barva, figura.vrsta)]
                    x = Sahovnica.ODMIK + (j * Sahovnica.VELIKOST_POLJA) + Sahovnica.VELIKOST_POLJA/2
                    y = Sahovnica.ODMIK + (i * Sahovnica.VELIKOST_POLJA) + Sahovnica.VELIKOST_POLJA/2
                    self.plosca.create_image(x, y, image=foto, tag=FIGURA)

if __name__ == "__main__":

    # Preberemo argumente iz ukazne vrstice,
    # uporabimo modul https://docs.python.org/3.4/library/argparse.html

    # Opišemo argumente, ki jih sprejmemo iz ukazne vrstice
    parser = argparse.ArgumentParser(description="Šah")
    # Argument --debug vklopi sporočila o tem, kaj se dogaja
    parser.add_argument('--globina',
                        default=MINIMAX_GLOBINA ,
                        type=int,
                        help='globina iskanja za minimax algoritem')
    parser.add_argument('--debug',
                        action='store_true',
                        help='vklopi sporočila o dogajanju')

    # Obdelamo argumente iz ukazne vrstice
    args = parser.parse_args()

    # Vklopimo sporočila, če je uporabnik podal --debug
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    # Glavno okno
    root = tk.Tk()
    root.title("Šah")

    # Naredimo objekt GUI in ga shranimo v spremenljivko, da ga Python ne zbriše
    partija_saha = Sahovnica(root, args.globina)

    # Kontrolo pustimo glavnemu oknu
    root.mainloop()



