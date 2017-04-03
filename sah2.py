import math

def v_sahovnici(polozaj):
	x, y = polozaj
	if 0 <= x <= 7 and 0 <= y <= 7:
		return True
	else:
		return False		
def nasprotna_barva(barva):
	if barva == 'bel':
		return 'crn'
	else:
		return 'bel'		

def figure_v_sliko(figure):  ##popravi
	slika = [[None]*8 for i in range(8)]
	for bela_figura in figure['bel']:
		if v_sahovnici((bela_figura.x, bela_figura.y)):
			slika[bela_figura.x][bela_figura.y] = bela_figura
	for crna_figura in figure['crn']:
		slika[crna_figura.x][crna_figura.y] = crna_figura
	return slika
def slika_v_figure(slika):
	figure = {'bel':[], 'crn':[]}
	for vrsta in slika:
		for element in vrsta:
			if element != None:
				if element.barva == 'bel':
					figure['bel'].append(element)
				else:
					figure['crn'].append(element)
	return figure

def preberi_potezo(figure, na_vrsti, slika, igra):
	dovoljen_vnos = False
	zacetni_x=zacetni_y=koncni_x=koncni_y=0
	while not(dovoljen_vnos):
		vnos = input(na_vrsti + ': ')
		parametri_vnosa = vnos.split(',')
		zacetni_x=int(parametri_vnosa[0])
		zacetni_y=int(parametri_vnosa[1])
		koncni_x=int(parametri_vnosa[2])
		koncni_y=int(parametri_vnosa[3])
		if (zacetni_x, zacetni_y, koncni_x, koncni_y) in vse_dovoljene_poteze(figure, slika, igra):
			dovoljen_vnos = True
	return (zacetni_x, zacetni_y, koncni_x, koncni_y)		
def narisi_sliko(slika):
	for vrstica in slika:
		vrstica = ' '
		for element in vrstica:
			if element == None:
				vrstica += 'None'
			else:
				print("tlele")
				vrstica += element.barva+element.vrsta
		print(vrstica)
	
def vse_dovoljene_poteze(figure, slika, igra): ##krasno če usposobim generator
	crne = figure['crn']
	bele = figure['bel']
	
	vse_dovoljene_potezice = []
	
	for figura in bele:
		for poteza in figura.dovoljene_poteze_iterator(slika, igra):
			vse_dovoljene_potezice.append(poteza)
	for figura in crne:
		for poteza in figura.dovoljene_poteze_iterator(slika, igra):
			vse_dovoljene_potezice.append(poteza)
	return vse_dovoljene_potezice

def bo_sah_kralj(igra, slika, figure, poteza): ##ali bo kralj pod šahom po potezi? True/False
	zacetni_polozaj, koncni_polozaj = poteza
	zacetni_x, zacetni_y = zacetni_polozaj
	koncni_x, koncni_y = koncni_polozaj
	
	figura_ki_jo_premikamo = slika[zacetni_x][zacetni_y]
	moja_barva = figura_ki_jo_premikamo.barva
	
	for figura in figure[nasprotna_barva(moja_barva)]:
		if (koncni_x, koncni_y) in figura.dovoljeni_premiki:
			return True
		else:
			return False
def bo_sah_navaden(igra, slika, figure, poteza): ##preverimo če bo šah po tem ko premaknemo figuro (razen za kralja)
	
	zacetni_polozaj, koncni_polozaj = poteza
	zacetni_x, zacetni_y = zacetni_polozaj
	koncni_x, koncni_y = koncni_polozaj
	
	figura_ki_jo_premikamo = slika[zacetni_x][zacetni_y]
	moja_barva = figura_ki_jo_premikamo.barva
	
	kralj = None
	potencialno_nevarne_figure = []
	
	for figura in figure[moja_barva]:##poiščemo našega kralja
		if figura.vrsta == 'kralj':
			kralj = figura
			
	for figura in figure[nasprotna_barva(moja_barva)]: ##poiščemo tiste nasprotne figure, ki lahko pojejo figuro, ki jo zelimo premaknit
		for premik in figura.dovoljeni_premiki:
			if premik == zacetni_polozaj:
				potencialno_nevarne_figure.append(figura)
				
	nova_slika = slika
	nova_slika[zacetni_x][zacetni_y] = None
	nova_slika[koncni_x][koncni_y] = figura_ki_jo_premikamo
	figura_ki_jo_premikamo.premakni((koncni_x, koncni_y))
	
	for figura in potencialno_nevarne_figure:
		figura.izracunaj_dovoljene_premike(nova_slika, igra.append(poteza))
		if (kralj.x, kralj.y) in figura.dovoljeni_premiki:
			return True
	return False	

class Figura:
	def __init__(self, polozaj, barva):
		self.ziv = True
		self.barva = barva
		self.x, self.y = polozaj
		self.vektorji_premika = []		
	def izracunaj_dovoljene_premike_iterator(self, slika, igra): ##vraca tocke(na sahovnici) na katere se lahko premaknemo z to figuro
		for x_premika, y_premika in self.vektorji_premika:
			n = 1
			while v_sahovnici((self.x+n*x_premika, self.y+n*y_premika)): 
				if slika[self.x+n*x_premika][self.y+n*y_premika] == None:
					yield((self.x+n*x_premika, self.y+n*y_premika))
				else:
					if slika[self.x+n*x_premika][self.y+n*y_premika].barva != self.barva:
						yield((self.x+n*x_premika, self.y+n*y_premika))
					break
				n+=1
	def pojej(self):
		self.ziv = False
		self.x *= -1
		self.y *= -1
	def premakni(self, koncna_lokacija): ##mogoče da bi naredili preverjanje veljavnosti poteze tukaj???
		x_koncen, y_koncen = koncna_lokacija
		self.x = x_koncen
		self.y = y_koncen
	def	dovoljene_poteze_iterator(self, slika, igra):
		x = self.x
		y = self.y
		for premik in self.izracunaj_dovoljene_premike_iterator(slika, igra):
			x_koncna, y_koncna = premik
			yield (x,y,x_koncna,y_koncna)
	
class kraljica(Figura):
	def __init__(self, polozaj, barva):
		Figura.__init__(self, polozaj, barva)
		self.vrsta = 'kraljica'
		self.vektorji_premika = [(-1,1), (1,1), (-1, -1), (1, -1), (0,1), (0,-1), (1, 0), (-1, 0)]
class lovec(Figura):
	def __init__(self, polozaj, barva):
		Figura.__init__(self, polozaj, barva)
		self.vrsta = 'lovec'
		self.vektorji_premika = [(-1,1), (1,1), (-1, -1), (1, -1)]
class konj(Figura):
	def __init__(self, polozaj, barva):
		Figura.__init__(self, polozaj, barva)
		self.vrsta = 'konj'
		self.vektorji_premika = [(1,2), (-1,2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1)]
	def dovoljeni_premiki_iterator(self, slika, igra):
		for x_premika, y_premika in self.vektorji_premika:
			if v_sahovnici((self.x+x_premika, self.y+y_premika)): 
				if slika[self.x+x_premika][self.y+y_premika] == None:
					yield((self.x+x_premika, self.y+y_premika))
				elif slika[self.x+x_premika][self.y+y_premika].barva != self.barva:
					yield((self.x+x_premika, self.y+y_premika))
class trdnjava(Figura):
	def __init__(self, polozaj, barva):
		Figura.__init__(self, polozaj, barva)
		self.vrsta = 'trdnjava'
		self.premaknjen = False
		self.vektorji_premika = [(0,1), (0,-1), (1, 0), (-1, 0)]
	def premakni(self, koncna_lokacija): ##mogoče da bi naredili preverjanje veljavnosti poteze tukaj???
		x_koncen, y_koncen = koncna_lokacija
		self.premaknjen = True
		self.x = x_koncen
		self.y = y_koncen
class kralj(Figura):
	def __init__(self, polozaj, barva):
		Figura.__init__(self, polozaj, barva)		
		self.sah_mat = False
		self.barva = barva
		self.vrsta = 'kralj'
		self.premaknjen = False
		self.vektorji_premika = [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1, 0), (-1,1)]
	def dovoljeni_premiki_iterator(self, slika, igra): ##dodamo kot parameter še vse veljavne poteze nasprotnih, za preverjanje saha
		for x_premika, y_premika in self.vektorji_premika:
			if v_sahovnici((self.x+x_premika, self.y+y_premika)): 
				if slika[self.x+x_premika][self.y+y_premika] == None:
					yield((x_premika, y_premika))
				elif slika[self.x+x_premika][self.y+y_premika].barva != self.barva:
					yield((x_premika, y_premika))
	def premakni(self, koncna_lokacija): ##mogoče da bi naredili preverjanje veljavnosti poteze tukaj???
		x_koncen, y_koncen = koncna_lokacija
		self.premaknjen = True
		self.x = x_koncen
		self.y = y_koncen
class kmet_bel(Figura):
	def __init__(self, polozaj):
		Figura.__init__(self, polozaj, 'bel')
		self.vrsta = 'kmet'
		self.vektorji_premika = [(0,1),(0,2),(1,1),(-1,1)]
	def premakni(self, koncna_lokacija): ##mogoče da bi naredili preverjanje veljavnosti poteze tukaj???
		x_koncen, y_koncen = koncna_lokacija
		self.premaknjen = True
		self.x = x_koncen
		self.y = y_koncen
	def dovoljeni_premiki_iterator(self, slika, igra): ##dodaj en passeu, poglej ce povzroci sah, zamenjati kmeta za kraljico, pot do slike
		for x_premika, y_premika in self.vektorji_premika:
			if v_sahovnici((self.x+x_premika, self.y+y_premika)):
				if (x_premika, y_premika) == (0,1) and slika[self.x+0][self.y+1] == None:
					yield((self.x+0, self.y+1))
				if (x_premika, y_premika) == (0,2) and slika[self.x+0][self.y+2] == None and not(self.premaknjen):
					yield((self.x+0, self.y+2))
				if (x_premika, y_premika) == (1,1) and slika[self.x+1][self.y+1] != None and slika[self.x+1][self.y+1].barva != self.barva:
					yield((self.x+1, self.y+1))
				if (x_premika, y_premika) == (-1,1) and slika[self.x-1][self.y+1] != None and slika[self.x-1][self.y+1].barva != self.barva:
					yield((self.x-1, self.y+1))
class kmet_crn(Figura):
	def __init__(self, polozaj):
		Figura.__init__(self, polozaj, 'crn')
		self.vrsta = 'kmet'
		self.vektorji_premika = [(0,-1),(0,-2),(-1,-1),(1,-1)]
	def premakni(self, koncna_lokacija): ##mogoče da bi naredili preverjanje veljavnosti poteze tukaj???
		x_koncen, y_koncen = koncna_lokacija
		self.premaknjen = True
		self.x = x_koncen
		self.y = y_koncen
	def dovoljeni_premiki_iterator(self, slika, igra): ##dodaj en passeu, poglej ce povzroci sah, zamenjati kmeta za kraljico, pot do slike
		for x_premika, y_premika in self.vektorji_premika:
			if v_sahovnici((self.x+x_premika, self.y+y_premika)):
				if (x_premika, y_premika) == (0,1) and slika[self.x+0][self.y+1] == None:
					yield((self.x+0, self.y+1))
				if (x_premika, y_premika) == (0,2) and slika[self.x+0][self.y+2] == None and not(self.premaknjen):
					yield((self.x+0, self.y+2))
				if  (x_premika, y_premika) == (1,1) and slika[self.x+1][self.y+1] != None and slika[self.x+1][self.y+1].barva != self.barva:
					yield((self.x+1, self.y+1))
				if (x_premika, y_premika) == (-1,1) and slika[self.x-1][self.y+1] != None and slika[self.x-1][self.y+1].barva != self.barva:
					yield((self.x-1, self.y+1))
	
figure = {'bel':[kmet_bel((0,1)), kmet_bel((1,1)), kmet_bel((2,1)), kmet_bel((3,1)), kmet_bel((4,1)), kmet_bel((5,1)), kmet_bel((6,1)),
				kmet_bel((7,1)),
				lovec((2, 0), 'bel'), lovec((5, 0), 'bel'),
				trdnjava((0,0), 'bel'), trdnjava((7,0), 'bel'),
				konj((1,0), 'bel'), konj((6,0), 'bel'),
				kraljica((3,0), 'bel'), 
				kralj((4,0), 'bel')],
		  'crn':[kmet_crn((0,6)), kmet_crn((1,6)), kmet_crn((2,6)), kmet_crn((3,6)), kmet_crn((4,6)), kmet_crn((5,6)), kmet_crn((6,6)),
				kmet_crn((7,6)),
				lovec((0,4), 'crn'), lovec((5,7), 'crn'),
				konj((1,7), 'crn'), konj((6,7), 'crn'),
				trdnjava((0,7), 'crn'), trdnjava((7,7), 'crn'),
				kraljica((3,7), 'crn'), 
				kralj((4,7), 'crn')]} 	
			
## dodaj .sah kralju
 
slika = figure_v_sliko(figure)
igra = []
na_vrsti = 'bel'

bele = figure['bel']
crne = figure['crn']


bel_kralj = crn_kralj = None

#poiscemo kralje()oh god...)
for figura in bele:
	if figura.vrsta == 'kralj':
		bel_kralj = figura
for figura in crne:
	if figura.vrsta == 'kralj':
		crn_kralj = figura
		
while not(bel_kralj.sah_mat) and not(crn_kralj.sah_mat):
	#print(vse_dovoljene_poteze(figure, slika, igra))
	poteza = preberi_potezo(figure, na_vrsti, slika, igra) ##preveri tudi če je dovoljena poteza
	igra.append(poteza)
	zacetni_x, zacetni_y, koncni_x, koncni_y = poteza
	
	for figura in figure[na_vrsti]:
		if figura.x == zacetni_x and figura.y == zacetni_y:
			figura.premakni((koncni_x, koncni_y))
			
	slika = figure_v_sliko(figure)
	narisi_sliko(slika)
	
	for figura in bele:
		if figura.vrsta == 'kralj':
			bel_kralj = figura
	for figura in crne:
		if figura.vrsta == 'kralj':
			crn_kralj = figura
	
	na_vrsti = nasprotna_barva(na_vrsti)


#print('Bele: ')
#for crna_figura in figure['crn']:
#	print('(',crna_figura.x,',',crna_figura.y,')')
#	crna_figura.izracunaj_dovoljene_premike(slika, [])
#	for premik in crna_figura.dovoljeni_premiki:
#		x_premika, y_premika = premik
#		print('\t(', x_premika, ',', y_premika, ')')
#
#print('Črne: )
#for bela_figura in figure['bel']:
#	print('(',bela_figura.x,',',bela_figura.y,')')	
#	bela_figura.izracunaj_dovoljene_premike(slika, [])
#	for premik in bela_figura.dovoljeni_premiki:
#		x_premika, y_premika = premik
#		print('\t(', x_premika, ',', y_premika, ')')
#

#print(bo_sah(igra, slika, figure, ((3,1),(3,2))))		
