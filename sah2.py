import math
import tkinter as tk
import os


#os.path.join(dir = os.path.dirname(__file__), r"/slike_figur/kraljica_{}i.gif".format(self.barva)
#self.foto = tk.PhotoImage(file=r"slike_figur\kraljica_{}i.gif".format(self.barva))


def v_sahovnici(polozaj):
    x, y = polozaj
    return  0 <= x <= 7 and 0 <= y <= 7



class Figura:
    def __init__(self, polozaj, barva):
        self.ziv = True
        self.barva = barva
        self.i, self.j = polozaj # stolpec, vrstica
        self.vektorji_premika = []
        self.foto = None
        self.foto_id = None


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

class kraljica(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'kraljica'
        self.vektorji_premika = [(-1, 1), (1, 1), (-1, -1), (1, -1), (0, 1), (0, -1), (1, 0), (-1, 0)]
        self.foto = tk.PhotoImage(file=r"slike_figur/kraljica_{}i.gif".format(self.barva))


class lovec(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'lovec'
        self.vektorji_premika = [(-1, 1), (1, 1), (-1, -1), (1, -1)]
        self.foto = tk.PhotoImage(file=r"slike_figur/lovec_{}i.gif".format(self.barva))


class konj(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'konj'
        self.vektorji_premika = [(1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]
        self.foto = tk.PhotoImage(file=r"slike_figur/konj_{}i.gif".format(self.barva))

    def izracunaj_dovoljene_premike_iterator(self, slika, igra):
        for i_premika, j_premika in self.vektorji_premika:
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if slika[self.i + i_premika][self.j + j_premika] is None:
                    yield ((self.i + i_premika, self.j + j_premika))
                elif slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                    yield ((self.i + i_premika, self.j + j_premika))


class trdnjava(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.vrsta = 'trdnjava'
        self.premaknjen = False
        self.vektorji_premika = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        self.foto = tk.PhotoImage(file=r"slike_figur/trdnjava_{}i.gif".format(self.barva))

    def premakni(self, koncna_lokacija):
        Figura.premakni(self, koncna_lokacija)
        self.premaknjen = True


class kralj(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.sah_mat = False
        self.barva = barva
        self.vrsta = 'kralj'
        self.premaknjen = False
        self.vektorji_premika = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        self.foto = tk.PhotoImage(file=r"slike_figur/kralj_{}i.gif".format(self.barva))  ##pa ja nje v figuri!

    def izracunaj_dovoljene_premike_iterator(self, slika,
                                             igra):  ##dodamo kot parameter še vse veljavne poteze nasprotnih, za preverjanje saha
        for i_premika, j_premika in self.vektorji_premika:
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if slika[self.i + i_premika][self.j + j_premika] is None or \
                                slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                    yield ((self.i + i_premika, self.j + j_premika))
        # možnost rošade
        if not self.premaknjen:
            # leva rošada
            if not slika[self.i][0].premaknjen:
                leva = True
                # preverimo, če so polja vmes prosta
                for j in [3, 2, 1]:
                    if slika[self.i][j] is not None:
                       leva = False
                       break
                if leva:
                    yield('leva_rošada')
            # desna rošada
            if not (slika[self.i][7].premaknjen):
                # print('desnaaaa')
                desna = True
                for j in [5, 6]:
                    if slika[self.i][j] is not None:
                        desna = False
                        break
                if desna:
                    yield('desna_rošada')


    def premakni(self, koncna_lokacija):
        Figura.premakni(self, koncna_lokacija)
        self.premaknjen = True


class kmet(Figura):
    def __init__(self, polozaj, barva):
        Figura.__init__(self, polozaj, barva)
        self.premaknjen = False
        self.vrsta = 'kmet'
        self.vektorji_premika = [(1, 0), (2, 0), (1, 1), (1, -1)]
        self.koeficient = -1 if self.barva == 'bel' else 1
        self.foto = tk.PhotoImage(file=r"slike_figur/kmet_{}i.gif".format(self.barva))

    def premakni(self, koncna_lokacija):
        Figura.premakni(self, koncna_lokacija)
        self.premaknjen = True

    def izracunaj_dovoljene_premike_iterator(self, slika, igra):  ##dodaj en passeu
        for i_premika, j_premika in self.vektorji_premika:
            i_premika *= self.koeficient
            if v_sahovnici((self.i + i_premika, self.j + j_premika)):
                if j_premika != 0: # pojemo nasprotnikovo figuro
                    if slika[self.i + i_premika][self.j + j_premika] is not None and \
                                    slika[self.i + i_premika][self.j + j_premika].barva != self.barva:
                        yield ((self.i + i_premika, self.j + j_premika))
                else: # skoka naprej
                    if abs(i_premika) == 1 and slika[self.i + i_premika][self.j] is None: # skok za 1
                        yield ((self.i + i_premika, self.j))
                    elif slika[self.i + i_premika // 2][self.j] is None and slika[self.i + i_premika][self.j] is None and \
                            not (self.premaknjen): # skok za 2, obe polji morata biti prosti
                        yield ((self.i + i_premika, self.j))




class Sah():
    def __init__(self):
        self.igra = []
        self.na_vrsti = 'bel'
        self.figure = {'bel': [kmet((6, i), 'bel') for i in range(8)] +
                              [lovec((7, 2), 'bel'), lovec((7, 5), 'bel'),
                               trdnjava((7, 0), 'bel'), trdnjava((7, 7), 'bel'),
                               konj((7, 1), 'bel'), konj((7, 6), 'bel'),
                               kraljica((7, 3), 'bel'),
                               kralj((7, 4), 'bel')],

                       'crn': [kmet((1, i), 'crn') for i in range(8)] +
                              [lovec((0, 2), 'crn'), lovec((0, 5), 'crn'),
                               konj((0, 1), 'crn'), konj((0, 6), 'crn'),
                               trdnjava((0, 0), 'crn'), trdnjava((0, 7), 'crn'),
                               kraljica((0, 3), 'crn'),
                               kralj((0, 4), 'crn')]}

        self.slika = self.figure_v_sliko()

    def vrni_kralja_na_vrsti(self):
        for figura in self.figure[self.na_vrsti]:
            if figura.vrsta == 'kralj':
                return figura

    def nasprotna_barva(self):
        return 'crn' if self.na_vrsti == 'bel' else 'bel'

    def figure_v_sliko(self):  # x in y sta bila zamenjana
        slika = [[None] * 8 for i in range(8)]
        vse_figure = self.figure['bel'] + self.figure['crn']
        for figura in vse_figure:
            slika[figura.i][figura.j] = figura
        return slika

    def premakni_figuro(self, figura, poteza):
        i_z, j_z = figura.i, figura.j
        i_k, j_k = poteza
        pojedena_figura = self.slika[i_k][j_k]  # lahko je tudi None
        self.igra.append(((i_z, j_z), pojedena_figura,
                          figura))  # rekonstrukcija: vprašamo figuro za x, y koordinati, tja postavimo pojedeno_figuro; figuro postavimo na (i_z, j_z)
        if self.slika[i_k][j_k] is not None:
            self.slika[i_k][j_k].pojej()
        figura.premakni((i_k, j_k))
        self.slika[i_z][j_z] = None
        self.slika[i_k][j_k] = figura
            
    def naredi_potezo(self, figura, poteza):
        '''Služi kot filter za rošade in en-passante.'''
        if poteza == 'leva_rošada':
            self.premakni_figuro(figura, (figura.i, 2)) # premaknemo kralja
            self.premakni_figuro(self.slika[figura.i][0], (figura.i, 3)) # premaknemo trdnjavo
        elif poteza == 'desna_rošada':
            self.premakni_figuro(figura, (figura.i, 6))
            self.premakni_figuro(self.slika[figura.i][7], (figura.i, 5))
        else:
            self.premakni_figuro(figura, poteza)
        # spremenimo, kdo je na vrsti
        self.na_vrsti = self.nasprotna_barva()

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





















#=================================================================2
# DRUGE UPORABNE FUNKCIJE
#=================================================================2
# x, y, z = v1
# dolzina = math.sqrt(x**2+y**2+z**2)
# return (x/dolzina, y/dolzina, z/dolzina)


def cross_product(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return (y1 * z2 - y2 * z1, x2 * z1 - x1 * z2, x1 * y2 - x2 * y1)


def vzporedna(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    x3, y3, z3 = cross_product((x1, y1, z1), (x2, y2, z2))
    if x3 ** 2 + y2 ** 2 + z3 ** 2 == 0:
        return True


def normiraj(v1):
    x, y, z = v1
    dolzina = math.sqrt(x ** 2 + y ** 2 + z ** 2)
    return (x / dolzina, y / dolzina, z / dolzina)


# normalen, če vzporeden enemu izmed osnovnih osmih premikov. Kateremu, sicer False
def normalen(v1):
    normalni = [(-1, 1, 0), (1, 1, 0), (-1, -1, 0), (1, -1, 0), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]
    x, y = v1
    ##normiran = normiraj((x, y, 0))
    for normalen_vektor in normalni:
        if vzporedna((x, y, 0), normalen_vektor):
            xn, yn, zn = normalen_vektor
            return (xn, yn)
    return False



def slika_v_figure(slika):
    figure = {'bel': [], 'crn': []}
    for vrsta in slika:
        for element in vrsta:
            if element != None:
                if element.barva == 'bel':
                    figure['bel'].append(element)
                else:
                    figure['crn'].append(element)
    return figure


def preberi_potezo(figure, na_vrsti, slika, igra):  ##preveri vnos (tukaj??)
    dovoljen_vnos = False
    zacetni_x = zacetni_y = koncni_x = koncni_y = 0
    while not (dovoljen_vnos):
        vnos = input(na_vrsti + ': ')
        parametri_vnosa = vnos.split(',')
        zacetni_x = int(parametri_vnosa[0])
        zacetni_y = int(parametri_vnosa[1])
        koncni_x = int(parametri_vnosa[2])
        koncni_y = int(parametri_vnosa[3])
    return (zacetni_x, zacetni_y, koncni_x, koncni_y)


def narisi_sliko(slika):
    for vrstica in slika:
        vrstica = ' '
        for element in vrstica:
            if element == None:
                vrstica += 'None'
            else:
                print("tlele")
                vrstica += element.barva + element.vrsta
        print(vrstica)

##class Figura(Figura):

##    def __str__(self, slika, igra): # mislim, da je lahko le self kot argument
##        izpis = 'figura: ' + self.barva + ' ' + self.vrsta + '\n'
##        izpis += '\tlokacija: ' + str(self.i) + ',' + str(self.j) + '\n'
##        izpis += '\tdovoljeni premiki: '
##        for premik in self.izracunaj_dovoljene_premike_iterator(slika, igra):
##            x, y = premik
##            izpis += '(' + str(x) + ',' + str(y) + '), '
##        izpis += '\n'
##        return izpis


#================================================================3
# original bo_sah_po_potezi
#================================================================3

##def bo_sah_po_potezi(igra, slika, figure, poteza, na_vrsti,
##                     kralj):  ##poteza v formatu (zacetni x, zace. y, koncni x, konc. y)
##    x_z, y_z, x_k, y_k = poteza
##    # če premikamo kralja, moramo poskrbeti, da ne bo pod šahom
##    if slika[x_z][y_z].vrsta == 'kralj':
##        igra.append(poteza)
##        kralj.premakni((x_k, y_k))
##        slika[x_z][y_z] = None
##        slika[x_k][y_l] = kralj
##        figure = slika_v_figure(slika)
##        for figura in figure[nasprotna_barva(
##                na_vrsti)]:  ## če je po potezi naš kralj med dovoljenimi premiki nasprotnih, potem smo v šahu po potezi
##            for poteza in figura.dovoljene_poteze_iterator(slika, igra):
##                x_z1, y_z1, x_k1, y_k1 = poteza
##                if (x_k1, y_k1) == (kralj[na_vrsti].x, kralj[na_vrsti].y):
##                    return True
##                # torej ne premikamo kralja.
##                # ali je sah? ce je, je med nasprotnikovimi moznimi potezami, da pojejo nasega kralja je šah.
##                # Moramo ga torej preprečiti.
##
##                # napiši funkcijo je_sah(slika, kralj_na_vrsti)
##                # figure_ki_napadajo_nasega_kralja = []
##                # for figura in figure[nasprotna_barva(na_vrsti)]:
##                #		for poteza in figura.dovoljene_poteze_iterator(slika, igra):
##                #			if poteza == (kralj[na_vrsti].x, kralj[na_vrsti].y):
##                #				figure_ki_napadajo_nasega_kralja.append(figura)
##    # ena ali več figur napada našega kralja.
##    # Če napada več figur našega kralja potem šaha z eno potezo (ki NI premik kralja) ne moremo preprečiti:
##    # if len(figure_ki_napadajo_nasega_kralja) > 1:
##    #	return True
##    # Če napada našega kralja ena figura moramo z potezo (da bo dovoljena) postaviti med kralja in napadalca figuro ali pa napadalca pojest
##    # elif len(figure_ki_napadajo_nasega_kralja) == 1:
##    #	napadalec = figure_ki_napadajo_nasega_kralja[0]
##    #	#če z potezo pojemo edinega napadalca je veljavna (ni šaha več)
##    #	if (x_k, y_k) == (napadalec.x, napadalec.y):
##    #		return False
##    #	#če napadalca z potezo ne pojemo in napadalec je konj, potem poteza ni veljavna (med kralja in konja ne moremo postaviti nič kar bi preprečilo šah)
##    #	elif napadalec.vrsta == 'konj':
##    #		return True
##    #	#če napadalca ne pojemo in ni konj, moramo figuro postaviti med napadalca in kralja.
##    #	#figura je med napadalcem in kraljem, ko je kot med vektorjem med figuro in kraljem in vektorjem med figuro in napadalcem 180 stopinj
##    #	#oz. ko je velikost v. produkta teh vektorjev enaka nič (tretjo koordinato dodamo = 0)
##    #	else:
##    #		v1 = (napadalec.x-x_k, napadalec.y-y_k, 0)
##    #		v2 = (kralj.x-x_k, kralj.y-y_k, 0)
##    #		x3, y3, z3 = cross_product(v1, v2)
##    #		if x3**2 + y2**2 + z3**2 == 0:
##    #			return False
##    # Če kralja ne napada nobena figura, moramo samo poskrbeti, da poteza ne odpre šaha.
##    # to ugotovimo tako, da izračunamo vektor med kraljem in figuro ki jo želimo premikati, premaknemo figuro
##    # in se po vektorju premikamo od kralja dokler ne naletimo na figuro ali pa konec šahovnice. Če je figura naša, je premik dovoljen
##    # Če figura ni naša in je trdnjava, lovec, ali pa kraljica potem poteza ni dovoljena
##    else:
##        v1 = (x_z - kralj.x, y_z - kralj.y)
##        normalen_v = normalen(v1)
##        if normalen_v:
##            i_premika, j_premika = normalen_v
##            # "naredimo" premik
##            igra.append(poteza)
##            figura = slika[x_z][y_z]
##            figura.premakni((x_k, y_k))
##            slika[x_z][y_z] = None
##            slika[x_k][y_k] = figura
##            figure = slika_v_figure(slika)
##            n = 1
##            while v_sahovnici((kralj.x + n * i_premika, kralj.y + n * j_premika)):
##                if slika[kralj.x + n * i_premika][kralj.y + n * j_premika] != None:
##                    if slika[kralj.x + n * i_premika][kralj.y + n * j_premika].barva == na_vrsti:
##                        return False
##                    else:
##                        if (slika[kralj.x + n * i_premika][kralj.y + n * j_premika].vrsta == 'lovec'
##                            and normalen_v in [(-1, 1), (1, 1), (-1, -1), (1, -1)]):
##                            return True
##                        elif (slika[kralj.x + n * i_premika][kralj.y + n * j_premika].vrsta == 'trdnjava'
##                              and normalen_v in [(0, 1), (0, -1), (1, 0), (-1, 0)]):
##                            return True
##                        elif slika[kralj.x + n * i_premika][kralj.y + n * j_premika].vrsta == 'kraljica':
##                            return True
##                        else:
##                            return False
##                n += 1
##            # če pridemo ven iz šahovnice brez da bi naleteli na figuro je poteza dovoljena (ni šaha)
##            return False




# sahec = sah()

# sahec.izpisi_figure_na_vrsti()
# sahec.naredi_potezo((0,1,0,2))
# sahec.izpisi_figure_na_vrsti()

# while len(sahec.vrni_vse_mozne_poteze_za_figure_na_vrsti()) != 0:
#	print(sahec.vrni_vse_mozne_poteze_za_figure_na_vrsti())
#	poteza = preberi_potezo(figure, na_vrsti, slika, igra)
#	if poteza in sahec.vrni_vse_mozne_poteze_za_figure_na_vrsti():
#		sahec.naredi_potezo(poteza)
