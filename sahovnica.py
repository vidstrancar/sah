# šahovnica
# GUI: tukaj se riše in zaznava klike, za pravila povprašamo logiko


import tkinter as tk
import logika






class Sahovnica:
    print("RAZRED ŠAHOVNICA")

    def __init__(self, master):
        # nastavitve velikosti
        self.velikost_polj = 110
        self.odmik = 80
        self.platno = tk.Canvas(master, width=self.velikost_polj * 10, height=self.velikost_polj * 10)
        self.platno.pack()

        self.sah = logika.Šah()
        self.IGRA = self.sah.IGRA





        # narišemo šahovnico
        self.polja = self.narisi_sahovnico()

        self.oznacena_polja = []

        # registriramo se za klike z miško
        self.platno.bind('<Button-1>', self.klik)

        # naredimo oznako za izpisovanje

        okvir_oznake = tk.LabelFrame(self.platno)
        okvir_oznake.pack() 
        self.izpis_potez = tk.StringVar(value='Na potezi je beli.')
        oznaka_izpis_potez = tk.Label(okvir_oznake, textvariable=self.izpis_potez)
        oznaka_izpis_potez.pack()
        x, y = self.odmik + 8 * self.velikost_polj / 2, self.odmik / 2
        self.platno.create_window(x, y, window=okvir_oznake, width = 140)
        # self.platno.create_text(600, 20, text=self.izpis_potez.get()) ZAKAJ SE TO NE SPREMINJA?

        self.zacni_igro()

    def narisi_sahovnico(self):
        '''Nariše šahovnico 8d X 8d. Desno spodaj je belo polje.'''
        x1, y1 = self.odmik, self.odmik  # določimo odmik
        matrika_id = [[None for i in range(8)] for j in range(8)]
        for i in range(8):  # vrstice
            for j in range(8):  # stolpci
                barva = "white" if (i + j) % 2 == 0 else "gray"
                id_polja = self.platno.create_rectangle(x1, y1, x1 + self.velikost_polj, y1 + self.velikost_polj, fill=barva)
                matrika_id[i][j] = id_polja
                x1 += self.velikost_polj  # naslednji kvadratek v vrsti
            x1, y1 = self.odmik, self.odmik + self.velikost_polj * (i + 1)  # premaknemo se eno vrstico navzdol
        return matrika_id

    def klik(self, event):
        '''Zazna klik in to sporoči logiki igre.'''

        # najprej pridobi koordinate
        i = int((event.y - self.odmik) // self.velikost_polj) # vrstica
        j = int((event.x - self.odmik) // self.velikost_polj) # stolpec
        # stolpci = 'ABCDEFGH'
        # self.izpis_potez.set('Kliknil si na {}{}.'.format(stolpci[j], 7 - i + 1))


        if not(0 <= i <= 7 and 0 <= j <= 7): # klik izven šahovnice
            return

        if self.sah.konec_igre:
            return

        if self.sah.oznacena_figura is None:
            # jo označimo, če lahko
            if self.sah.lahko_oznacimo(i, j):
                print(self.sah.oznacena_figura)

                # jo označimo
                self.sah.oznacena_figura = self.IGRA[i][j]

                # pobarvamo polje, ki smo ga označili
                polje = self.polja[i][j]
                self.platno.itemconfig(polje, fill="yellow")


                # pobarvamo možne poteze
                for poteza in self.sah.veljavne_poteze():
                    i_polja, j_polja = poteza
                    self.oznacena_polja.append(poteza)
                    self.platno.itemconfig(self.polja[i_polja][j_polja], fill="blue")

                # zmeraj preverjamo, ali je kralj v dosegu možnih potez

        else:
            # ponastavimo barvo polja označene figure
            i_stari, j_stari = self.sah.oznacena_figura.polozaj
            barva = "white" if (i_stari + j_stari) % 2 == 0 else "gray"
            self.platno.itemconfig(self.polja[i_stari][j_stari], fill=barva) # lahko bi tudi z (i + j) % 2, ko bi za i in j vprašal označeno figuro

            # ponastavimo barvo možnih polj
            for poteza in self.oznacena_polja:
                i_polja, j_polja = poteza
                barva = "white" if (i_polja + j_polja) % 2 == 0 else "gray"
                self.platno.itemconfig(self.polja[i_polja][j_polja], fill = barva)




            if (i, j) in self.sah.veljavne_poteze():

                # sporočimo logiki, da se je nekaj spremenilo
                self.sah.premakni_figuro(i, j)
                self.sah.zamenjaj_igralca()
                self.izpis_potez.set('Na potezi je {}.'.format(self.sah.na_potezi))


                # premaknemo sliko figure na novi koordinati
                x = self.odmik + (j * self.velikost_polj) + self.velikost_polj / 2 # centriramo klik
                y = self.odmik + (i * self.velikost_polj) + self.velikost_polj / 2

                # če je na polju kakšna druga figura, jo 'pojemo'
                if self.IGRA[i][j] is not None:
                    nasprotna_figura = self.IGRA[i][j]
                    id_slike = nasprotna_figura.id_slike
                    self.platno.delete(id_slike)

                # narišemo novo sliko in shranimo nov id_slike
                foto = self.sah.oznacena_figura.foto
                id_slike = self.platno.create_image(x, y, image=foto)
                self.sah.oznacena_figura.id_slike = id_slike

            # odznačimo figuro
            self.sah.oznacena_figura = None

            print('nova poteza')
            for i in range(8):
                print(self.IGRA[i])



    def zacni_igro(self):
        '''Prične igro.'''
        self.prikaz_figur()
        # nastavi odštevalnik ure

    
    def prikaz_figur(self):
        '''Na šahovnici prikaže figure.'''
        for i in range(8):
            for j in range(8):
                figura = self.IGRA[i][j]
                if figura is not None:
                    i, j = figura.polozaj # rišemo lahko direktno iz položaja figur, lahko bi tudi iz položaja v matriki
                    foto = figura.foto
                    x = self.odmik + (j * self.velikost_polj) + self.velikost_polj / 2
                    y = self.odmik + (i * self.velikost_polj) + self.velikost_polj / 2
                    id_slike = self.platno.create_image(x, y, image=foto)
                    figura.id_slike = id_slike


root = tk.Tk()

partija_saha = Sahovnica(root)

root.mainloop()


#===========================================================#
#                  NASVETI PROFESORJA                       #
#===========================================================#
# matrika je zaradi rekonstrukcije, zato da programer vidi, kaj se dogaja
# IGRA v logiki
# najprej spremeniš v logiki, nato sporočiš GUI, da nariše drugam
# class Figura: x, y, barva -> kar je skupno vsem figuram
# class Kmet(Figura): mozne poteze, slika