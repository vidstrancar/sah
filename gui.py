# GUI: risanje in zaznavanje klikov

# Zvrsti graficnih objektov
POLJE="polje" # ta se nariše enkrat in se potem ne briše več
FIGURA="figura"
PLAVI="plavi"

import tkinter as tk
import argparse        # za argumente iz ukazne vrstice
import logging         # za odpravljanje napak

import sah2
from clovek import *
from racunalnik import *
from minimax import *

MINIMAX_GLOBINA = 2


class Sahovnica():
    # nastavitve velikosti
    VELIKOST_POLJA = 100
    ODMIK = 30

    def __init__(self, master, globina):
        self.igralec_beli = None # (nastavimo ob začetku igre)
        self.igralec_crni = None
        self.sah = sah2.Sah()

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
                              command=lambda: self.zacni_igro(Clovek(self), racunalnik.Racunalnik(self, Minimax(globina))))

        # Igralna površina
        self.platno = tk.Canvas(master, width=Sahovnica.VELIKOST_POLJA * 10, height=Sahovnica.VELIKOST_POLJA * 10)
        self.platno.grid(row=1, column=0)
        # self.platno.pack()

        # Dovoljeni kliki
        self.prvi_klik = True
        self.dovoljeni_drugi_kliki = []
        self.prvi_klikx = self.prvi_kliky = 0

        self.oznacena_figura = None

        # narišemo šahovnico
        self.narisi_sahovnico()


        # registriramo se za klike z miško

        self.platno.bind('<Button-1>', self.klik)
        self.platno.bind('<Control-z>', self.vrni_potezo)
        self.platno.focus_force()


        # Oznaka za izpisovanje
        self.izpis_potez = tk.StringVar(master, value="Dobrodošli šah!")
        tk.Label(master, textvariable=self.izpis_potez).grid(row=0, column=0)


        # Začnemo igro v načinu človek proti računalniku
        self.zacni_igro(Racunalnik(self, Minimax(globina)), Clovek(self))

    def vrni_potezo(self, event):
        self.izpis_potez.set('Vračamo potezo.')
        # if isinstance(self.igralec_beli, Clovek) and isinstance(self.igralec_crni, Clovek):
        self.sah.vrni_potezo()
        self.prikaz_figur()

    def zacni_igro(self, beli, crni):
        '''Nastavi stanje na začetek igre. Za igralca uporabi dana igralca.'''
        # Ustavimo vse igralce, ki morda razmišljajo.
        self.prekini_igralce()

        # Začnemo novo igro
        self.sah = sah2.Sah()
        self.prikaz_figur()
        self.izpis_potez.set("Na potezi je beli.")

        # Nastavimo igralca
        self.igralec_beli = beli
        self.igralec_crni = crni

        self.igralec_beli.igraj()
        # nastavi odštevalnik ure


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
        x1, y1 = Sahovnica.ODMIK, Sahovnica.ODMIK  # določimo odmik
        matrika_id = [[None for i in range(8)] for j in range(8)]
        for i in range(8):  # vrstice
            for j in range(8):  # stolpci
                barva = "white" if (i + j) % 2 == 0 else "gray"
                id_polja = self.platno.create_rectangle(x1, y1, x1 + Sahovnica.VELIKOST_POLJA, y1 + Sahovnica.VELIKOST_POLJA,
                                                        fill=barva, tag=POLJE)
                matrika_id[i][j] = id_polja
                x1 += Sahovnica.VELIKOST_POLJA  # naslednji kvadratek v vrsti
            x1, y1 = Sahovnica.ODMIK, Sahovnica.ODMIK + Sahovnica.VELIKOST_POLJA * (i + 1)  # premaknemo se eno vrstico navzdol
        return matrika_id

    def narisi_plave(self, plave_tocke):
        '''Z modro pobarva polja, na katere se označena figura lahko premakne..'''
        for poteza in plave_tocke:
            if poteza == 'leva_rošada':
                i = self.oznacena_figura.i
                j = 2
            elif poteza == 'desna_rošada':
                i = self.oznacena_figura.i
                j = 6
            else:
                i, j = poteza
            barva = "blue"
            x1 = Sahovnica.ODMIK + j * Sahovnica.VELIKOST_POLJA
            y1 = Sahovnica.ODMIK + i * Sahovnica.VELIKOST_POLJA
            self.platno.create_rectangle(x1, y1, x1 + Sahovnica.VELIKOST_POLJA, y1 + Sahovnica.VELIKOST_POLJA, fill=barva, tag=PLAVI)

    def klik(self, event):
        '''Ogdovori na klik uporabnika. Sporočimo tistemu, ki je na potezi'''
        if self.sah.zmagovalec is None:
            i = int((event.y - Sahovnica.ODMIK) // Sahovnica.VELIKOST_POLJA) # vrstica
            j = int((event.x - Sahovnica.ODMIK) // Sahovnica.VELIKOST_POLJA) # stolpec
            poteza = (i, j)

            # self.platno.itemconfig(self.text, text="klik.")
            if sah2.v_sahovnici(poteza):
                if self.sah.na_vrsti == 'bel':
                    self.igralec_beli.klik(poteza)
                elif self.sah.na_vrsti == 'crn':
                    self.igralec_crni.klik(poteza)
                else:
                    # Nihče ni na potezi, zato ne naredimo nič.
                    pass
            else:
                logging.debug("klik izven ploše")

    def razberi_potezo(self, poteza):
        '''Prebere prvi in drugi klik.'''
        i, j = poteza
        if self.oznacena_figura is None: # označimo figuro
            if (self.sah.slika[i][j] != None) and (self.sah.na_vrsti == self.sah.slika[i][j].barva):
                self.oznacena_figura = self.sah.slika[i][j]
                self.dovoljene_poteze = list(self.sah.dovoljene_poteze_iterator(self.oznacena_figura))
                self.prikaz_figur(plave_tocke = self.dovoljene_poteze) # pobarvamo dovoljena polja
            else:
                self.oznacen_figura = None
            self.izpis_potez.set('označimo {}'.format(self.oznacena_figura))
        else:
            self.premakni_figuro(self.oznacena_figura, poteza)

    def premakni_figuro(self, figura, poteza):
        '''Premakne figuro, če je poteza veljavna.'''
        i, j = poteza
        if self.oznacena_figura.vrsta == 'kralj' and abs(self.oznacena_figura.j - j) == 2:
            if j == 2:
                poteza = 'leva_rošada'
            elif j == 6:
                poteza = 'desna_rošada'
        if self.sah.naredi_potezo(self.oznacena_figura, poteza):
            self.izpis_potez.set('premaknemo {}'.format(self.oznacena_figura))
        else:
            self.izpis_potez.set('Označimo None')
        self.oznacena_figura = None
        self.prikaz_figur()
        self.sah.stanje_igre()
        if self.sah.zmagovalec is not None:
            self.izpis_potez.set('zmagal je {}'.format(self.sah.zmagovalec))



    def prikaz_figur(self, plave_tocke=[]):
        '''Pobriše vse figure in nariše nove.'''
        self.platno.delete(FIGURA)
        self.platno.delete(PLAVI)
        self.narisi_plave(plave_tocke)
        bele = self.sah.figure['bel']
        crne = self.sah.figure['crn']
        for figura in bele + crne:
            if figura.ziv:
                foto = figura.foto
                x = Sahovnica.ODMIK + (figura.j * Sahovnica.VELIKOST_POLJA) + Sahovnica.VELIKOST_POLJA / 2
                y = Sahovnica.ODMIK + (figura.i * Sahovnica.VELIKOST_POLJA) + Sahovnica.VELIKOST_POLJA/2
                foto_id = self.platno.create_image(x, y, image=foto, tag=FIGURA)
                figura.foto_id = foto_id


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



#==========================================================================
def koncaj_igro(self, zmagovalec):
    '''Nastavi stanje igre na konec igre.'''
    if zmagovalec == IGRALEC_BELI:
        self.izpis_potez.set('Zmagal je beli.')
    elif zmagovalec == IGRALEC_CRNI:
        self.izpis_potez.set('Zmagal je črni.')
    else:
        self.izpis_potez.set('Neodločeno.')