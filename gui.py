# GUI: risanje in zaznavanje klikov

# Zvrsti graficnih objektov
POLJE="polje" # ta se nariše enkrat in se potem ne briše več
FIGURA="figura"
PLAVI="plavi"

import tkinter as tk
import argparse        # za argumente iz ukazne vrstice
import logging         # za odpravljanje napak

import sah2
import clovek
import racunalnik
import minimax

MINIMAX_GLOBINA = 2


class Sahovnica():
    # nastavitve velikosti
    VELIKOST_POLJA = 100
    ODMIK = 30

    def __init__(self, master, globina):
        self.igralec_beli = None # (nastavimo ob začetku igre)
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
                              command=lambda: self.zacni_igro(clovek.Clovek(self), clovek.Clovek(self)))
        menu_igra.add_command(label="Človek - Računalnik",
                              command=lambda: self.zacni_igro(clovek.Clovek(self), racunalnik.Racunalnik(self, minimax.Minimax(globina))))

        # Igralna površina
        self.platno = tk.Canvas(master, width=Sahovnica.VELIKOST_POLJA * 10, height=Sahovnica.VELIKOST_POLJA * 10)
        # self.platno.grid(row=0, column=0)
        self.platno.pack()

        # Dovoljeni kliki
        self.prvi_klik = True
        self.dovoljeni_drugi_kliki = []
        self.prvi_klikx = self.prvi_kliky = 0

        self.oznacena_figura = None

        # narišemo šahovnico
        self.narisi_sahovnico()

        # registriramo se za klike z miško
        self.platno.bind('<Button-1>', self.klik)


        # Oznaka za izpisovanje
        # self.izpis_potez = tk.StringVar(master, value="Dobrodošli v 3 x 3!")
        # tk.Label(master, textvariable=self.izpis_potez).grid(row=0, column=0)
        self.okvir_oznake = tk.LabelFrame(self.platno)
        self.okvir_oznake.pack()
        self.izpis_potez = tk.StringVar(value='klikni nekam')
        oznaka_izpis_potez = tk.Label(self.okvir_oznake, textvariable=self.izpis_potez)
        oznaka_izpis_potez.pack()
        x, y = Sahovnica.ODMIK + 8 * Sahovnica.VELIKOST_POLJA / 2, Sahovnica.ODMIK / 2
        self.platno.create_window(x, y, window=self.okvir_oznake, width = 140)
        # self.platno.create_text(600, 20, text=self.izpis_potez.get()) ZAKAJ SE TO NE SPREMINJA?


        # Začnemo igro v načinu človek proti računalniku
        self.zacni_igro(clovek.Clovek(self), racunalnik.Racunalnik(self, minimax.Minimax(globina)))


    def zacni_igro(self, beli, crni):
        '''Nastavi stanje na začetek igre. Za igralca uporabi dana igralca.'''
        # Ustavimo vse igralce, ki morda razmišljajo.
        self.prekini_igralce()
        # Nastavimo igralca
        self.igralec_beli = beli
        self.igralec_crni = crni
        # Začnemo novo igro
        self.sah = sah2.Sah()
        self.prikaz_figur()
        self.izpis_potez.set("Na potezi je beli.")
        self.igralec_beli.igraj()
        # nastavi odštevalnik ure

    def koncaj_igro(self, zmagovalec):
        '''Nastavi stanje igre na konec igre.'''
        if zmagovalec == IGRALEC_BELI:
            self.izpis_potez.set('Zmagal je beli.')
        elif zmagovalec == IGRALEC_CRNI:
            self.izpis_potez.set('Zmagal je črni.')
        else:
            self.izpis_potez.set('Neodločeno.')


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
        '''Ogdovori na klik uporabnika.'''
        # Tistemu, ki je na potezi, sporočimo, da je uporabnik kliknil na ploščo.
        # Podamo mu potezo.
        i = int((event.y - Sahovnica.ODMIK) // Sahovnica.VELIKOST_POLJA) # vrstica
        j = int((event.x - Sahovnica.ODMIK) // Sahovnica.VELIKOST_POLJA) # stolpec
        poteza = (i, j)
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




    def povleci_potezo(self, poteza):
        '''Prebere prvi in drugi klik.'''
        i, j = poteza
        # sporočimo logiki, naj povleče potezo, to storimo v obliki:
        # self.sah.naredi_potezo(self.oznacena_figura, poteza); če nam le-ta vrne None, je poteza neveljavna
        # pomagamo si z označeno figuro


        if self.prvi_klik:
            #preberemo prvi klik (označimo figuro ki jo želimo premikat)
            if sah2.v_sahovnici((i, j)) and (self.sah.slika[i][j] != None) and (
                        self.sah.na_vrsti == self.sah.slika[i][j].barva):
                self.oznacena_figura = self.sah.slika[i][j]
                self.dovoljene_poteze = list(self.sah.dovoljene_poteze_iterator(self.oznacena_figura)) # seznam oblike [(vr, st), ...]
            else:
                return
            if len(self.dovoljene_poteze) == 0:
                self.prvi_klik = True
                return
            self.izpis_potez.set(str(i)+", "+str(j)+'\t1.klik')
            #oznaka_izpis_potez = tk.Label(self.okvir_oznake, textvariable=tk.StringVar(value=str(i)+", "+str(j)+'\t1.klik'))
            #oznaka_izpis_potez.pack()
            self.prvi_klik = False

            #pobarvamo dovoljena polja
            pobarvane_tocke = []
            for poteza in self.dovoljene_poteze:
                pobarvane_tocke.append(poteza)
            self.prikaz_figur(plave_tocke = pobarvane_tocke)
            return

        #izračunamo dovoljene končne lokacije označene figure. shranimo v dovoljeni_drugi_kliki -seznam
        #preberemo drugi klik
        poteza = (i, j)
        if self.oznacena_figura.vrsta == 'kralj' and abs(self.oznacena_figura.j - j) == 2:
            if j == 2:
                poteza = 'leva_rošada'
            elif j == 6:
                poteza = 'desna_rošada'
        if sah2.v_sahovnici((i, j)) and poteza in self.dovoljene_poteze:
            self.sah.naredi_potezo(self.oznacena_figura, poteza)
            self.prvi_klik = True
            self.izpis_potez.set(str(i)+", "+str(j)+'\t2.klik')
            #oznaka_izpis_potez = tk.Label(self.okvir_oznake, textvariable=tk.StringVar(value=str(i)+", "+str(j)+'\t2.klik'))
            #oznaka_izpis_potez.pack()
            self.prikaz_figur()
            return
        self.prvi_klik = True
        self.prikaz_figur()


    def prikaz_figur(self, plave_tocke = []):
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
