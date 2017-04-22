# GUI: risanje in zaznavanje klikov

# Zvrsti graficnih objektov
POLJE="polje" # ta se nariše enkrat in se potem ne briše več
FIGURA="figura"
PLAVI="plavi"

import tkinter as tk
import sah2


class Sahovnica:

    def __init__(self, master):
        # nastavitve velikosti
        self.velikost_polj = 100
        self.odmik = 30

        self.platno = tk.Canvas(master, width=self.velikost_polj * 10, height=self.velikost_polj * 10)
        self.platno.pack()

        self.prvi_klik = True
        self.dovoljeni_drugi_kliki = []
        self.prvi_klikx = self.prvi_kliky = 0
        self.sah = sah2.sah()
        self.oznacena_figura = None

        # narišemo šahovnico
        self.narisi_sahovnico()

        # registriramo se za klike z miško
        self.platno.bind('<Button-1>', self.klik)

        # naredimo oznako za izpisovanje
        self.okvir_oznake = tk.LabelFrame(self.platno)
        self.okvir_oznake.pack()
        self.izpis_potez = tk.StringVar(value='klikni nekam')
        oznaka_izpis_potez = tk.Label(self.okvir_oznake, textvariable=self.izpis_potez)
        oznaka_izpis_potez.pack()
        x, y = self.odmik + 8 * self.velikost_polj / 2, self.odmik / 2
        self.platno.create_window(x, y, window=self.okvir_oznake, width = 140)
        # self.platno.create_text(600, 20, text=self.izpis_potez.get()) ZAKAJ SE TO NE SPREMINJA?
        self.zacni_igro()

    def narisi_sahovnico(self):
        '''Nariše šahovnico 8d X 8d. Desno spodaj je belo polje.'''
        x1, y1 = self.odmik, self.odmik  # določimo odmik
        matrika_id = [[None for i in range(8)] for j in range(8)]
        for i in range(8):  # vrstice
            for j in range(8):  # stolpci
                barva = "white" if (i + j) % 2 == 0 else "gray"
                id_polja = self.platno.create_rectangle(x1, y1, x1 + self.velikost_polj, y1 + self.velikost_polj,
                                                        fill=barva, tag=POLJE)
                matrika_id[i][j] = id_polja
                x1 += self.velikost_polj  # naslednji kvadratek v vrsti
            x1, y1 = self.odmik, self.odmik + self.velikost_polj * (i + 1)  # premaknemo se eno vrstico navzdol
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
            x1 = self.odmik + j * self.velikost_polj
            y1 = self.odmik + i * self.velikost_polj
            self.platno.create_rectangle(x1, y1, x1 + self.velikost_polj, y1 + self.velikost_polj, fill=barva, tag=PLAVI)


    def klik(self, event):
        '''Prebere prvi in drugi klik.'''
        i = int((event.y - self.odmik) // self.velikost_polj) # vrstica
        j = int((event.x - self.odmik) // self.velikost_polj) # stolpec

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
        print(self.dovoljene_poteze)
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

    def zacni_igro(self):
        '''Prične igro.'''
        self.prikaz_figur()
        # nastavi odštevalnik ure


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
                x = self.odmik + (figura.j * self.velikost_polj) + self.velikost_polj / 2
                y = self.odmik + (figura.i * self.velikost_polj) + self.velikost_polj/2
                foto_id = self.platno.create_image(x, y, image=foto, tag=FIGURA)
                figura.foto_id = foto_id


root = tk.Tk()

partija_saha = Sahovnica(root)

root.mainloop()
