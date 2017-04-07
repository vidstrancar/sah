# šahovnica
# GUI: tukaj se riše in zaznava klike, za pravila povprašamo logiko


import tkinter as tk
import logika


def narisi_sahovnico(platno, velikost_polj, odmik):
    '''Nariše šahovnico 8d X 8d. Desno spodaj je belo polje.'''
    x1, y1 = odmik, odmik # določimo odmik
    for i in range(8): # vrstice
        for j in range(8): # stolpci
            barva = "white" if (i + j) % 2 == 0 else "gray"
            platno.create_rectangle(x1, y1, x1 + velikost_polj, y1 + velikost_polj, fill=barva)
            x1 += velikost_polj # naslednji kvadratek v vrsti
        x1, y1 = odmik, odmik + velikost_polj * (i + 1) # premaknemo se eno vrstico navzdol



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

        self.oznacena_figura = None



        # narišemo šahovnico
        narisi_sahovnico(self.platno, self.velikost_polj, self.odmik)

        # registriramo se za klike z miško
        self.platno.bind('<Button-1>', self.klik)

        # naredimo oznako za izpisovanje

        okvir_oznake = tk.LabelFrame(self.platno)
        okvir_oznake.pack() 
        self.izpis_potez = tk.StringVar(value='klikni nekam')
        oznaka_izpis_potez = tk.Label(okvir_oznake, textvariable=self.izpis_potez)
        oznaka_izpis_potez.pack()
        x, y = self.odmik + 8 * self.velikost_polj / 2, self.odmik / 2
        self.platno.create_window(x, y, window=okvir_oznake, width = 140)
        # self.platno.create_text(600, 20, text=self.izpis_potez.get()) ZAKAJ SE TO NE SPREMINJA?


        self.zacni_igro()


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

        if self.oznacena_figura is None:
            # jo označimo
            if self.sah.lahko_oznacimo(i, j):
                self.oznacena_figura = self.IGRA[i][j]
                self.sah.oznacena_figura = self.oznacena_figura # prenesemo informacijo
                # sedaj tudi pobarvamo polje z označeno figuro
                self.oznaceno_polje = self.platno.find_overlapping(event.x, event.y, event.x + 1, event.y + 1)[0]
                self.barva_oznacenega_polja = self.platno.itemcget(self.oznaceno_polje, "fill")
                self.platno.itemconfig(self.oznaceno_polje, fill="blue")
                self.oznacena_figura = self.IGRA[i][j]
                # povemo logiki, katero figuro smo označili; logika vrne možne poteze in pokliče metodo za barvanje kvadratkov

        else:
            # ponastavimo barvo polja :)
            self.platno.itemconfig(self.oznaceno_polje, fill=self.barva_oznacenega_polja) # lahko bi tudi z (i + j) % 2, ko bi za i in j vprašal označeno figuro
            if self.sah.je_poteza_veljavna(i, j):
                # sporočimo logiki, da se je nekaj spremenilo
                self.sah.premakni_figuro(i, j)
                self.izpis_potez.set('Na vrsti je {}.'.format(self.sah.na_potezi))


                # premaknemo sliko figure na novi koordinati
                x = self.odmik + (j * self.velikost_polj) + self.velikost_polj / 2 # centriramo klik
                y = self.odmik + (i * self.velikost_polj) + self.velikost_polj / 2
                # če je na polju kakšna druga figura, jo 'pojemo'
                if self.IGRA[i][j] is not None:
                    nasprotna_figura = self.IGRA[i][j]
                    id_slike = nasprotna_figura.id_slike
                    self.platno.delete(id_slike)
                # narišemo novo sliko in shranimo nov id_slike
                foto = self.oznacena_figura.foto
                id_slike = self.platno.create_image(x, y, image=foto)
                self.oznacena_figura.id_slike = id_slike

            # odznačimo figuro
            self.oznacena_figura = None

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