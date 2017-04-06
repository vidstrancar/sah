import math

def cross_product(v1, v2):
	x1, y1, z1 = v1
	x2, y2, z2 = v2
	return (y1*z2-y2*z1, x2*z1-x1*z2, x1*y2-x2*y1)

def vzporedna(v1, v2):
	x1, y1 = v1
	x2, y2 = v2
	x3, y3, z3 = cross_product((x1, y1, 0), (x2, y2, 0))
	if x3**2 + y2**2 + z3**2 == 0:
		return True
def normiraj(v1):
	x, y, z = v1
	dolzina = math.sqrt(x**2+y**2+z**2) 
	return (x/dolzina, y/dolzina, z/dolzina)
#normalen, če vzporeden enemu izmed osnovnih osmih premikov. Kateremu, sicer False
def normalen(v1):
	normalni = [(-1,1), (1,1), (-1, -1), (1, -1), (0,1), (0,-1), (1, 0), (-1, 0)]
	normiran = normiraj(v1)
	for normalen_vektor in normalni:
		if vzporedna(normiran, normalen_vektor):
			return normalen_vektor
	return False
	
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
	
def bo_sah_po_potezi(igra, slika, figure, poteza, na_vrsti, kralj): ##poteza v formatu (zacetni x, zace. y, koncni x, konc. y)
	x_z, y_z, x_k, y_k = poteza
	#če premikamo kralja, moramo poskrbeti, da ne bo pod šahom
	if slika[x_z][y_z].vrsta == 'kralj':
		igra.append(poteza)
		kralj.premakni((x_k, y_k))
		slika[x_z][y_z] = None
		slika[x_k][y_l] = kralj
		figure = slika_v_figure(slika)
		for figura in figure[nasprotna_barva(na_vrsti)]:  ## če je po potezi naš kralj med dovoljenimi premiki nasprotnih, potem smo v šahu po potezi
			for poteza in figura.dovoljene_poteze_iterator(slika, igra):
				if poteza == (kralj[na_vrsti].x, kralj[na_vrsti].y):
					return True
	#torej ne premikamo kralja.
	#ali je sah? ce je, je med nasprotnikovimi moznimi potezami, da pojejo nasega kralja je šah.
	#Moramo ga torej preprečiti.
	figure_ki_napadajo_nasega_kralja = []
	for figura in figure[nasprotna_barva(na_vrsti)]:
		for poteza in figura.dovoljene_poteze_iterator(slika, igra):
			if poteza == (kralj[na_vrsti].x, kralj[na_vrsti].y):
				figure_ki_napadajo_nasega_kralja.append(figura)
	#ena ali več figur napada našega kralja.
	#Če napada več figur našega kralja potem šaha z eno potezo (ki NI premik kralja) ne moremo preprečiti:
	if len(figure_ki_napadajo_nasega_kralja) > 1:
		return True
	#Če napada našega kralja ena figura moramo z potezo (da bo dovoljena) postaviti med kralja in napadalca figuro ali pa napadalca pojest
	elif len(figure_ki_napadajo_nasega_kralja) == 1:
		napadalec = figure_ki_napadajo_nasega_kralja[0]
		#če z potezo pojemo edinega napadalca je veljavna (ni šaha več)
		if (x_k, y_k) == (napadalec.x, napadalec.y):
			return False
		#če napadalca z potezo ne pojemo in napadalec je konj, potem poteza ni veljavna (med kralja in konja ne moremo postaviti nič kar bi preprečilo šah)
		elif napadalec.vrsta == 'konj':
			return True
		#če napadalca ne pojemo in ni konj, moramo figuro postaviti med napadalca in kralja.
		#figura je med napadalcem in kraljem, ko je kot med vektorjem med figuro in kraljem in vektorjem med figuro in napadalcem 180 stopinj
		#oz. ko je velikost v. produkta teh vektorjev enaka nič (tretjo koordinato dodamo = 0)
		else:
			v1 = (napadalec.x-x_k, napadalec.y-y_k, 0)
			v2 = (kralj.x-x_k, kralj.y-y_k, 0)
			x3, y3, z3 = cross_product(v1, v2)
			if x3**2 + y2**2 + z3**2 == 0:
				return False
	#Če kralja ne napada nobena figura, moramo samo poskrbeti, da poteza ne odpre šaha.
	#to ugotovimo tako, da izračunamo vektor med kraljem in figuro ki jo želimo premikati, premaknemo figuro
	#in se po vektorju premikamo od kralja dokler ne naletimo na figuro ali pa konec šahovnice. Če je figura naša, je premik dovoljen
	#Če figura ni naša in je trdnjava, lovec, ali pa kraljica potem poteza ni dovoljena
	else:
		v1 = (x_z-kralj.x, y_z-kralj.y)
		normalen_v = normalen(v1)
		if normalen_v:
			x_premika, y_premika = normalen_v
			#"naredimo" premik
			igra.append(poteza)
			figura = slika[x_z][y_z]
			figura.premakni((x_k, y_k))
			slika[x_z][y_z] = None
			slika[x_k][y_k] = figura
			figure = slika_v_figure(slika)		
			n = 1
			while v_sahovnici((kralj.x+n*x_premika, kralj.y+n*y_premika)): 
				if slika[kralj.x+n*x_premika][self.y+n*y_premika] != None:
					if slika[kralj.x+n*x_premika][self.y+n*y_premika].barva == na_vrsti:
						return False
					else:
						if (slika[kralj.x+n*x_premika][self.y+n*y_premika].vrsta == 'lovec'
							and normalen_v in [(-1,1), (1,1), (-1, -1), (1, -1)]):
							return True
						elif (slika[kralj.x+n*x_premika][self.y+n*y_premika].vrsta == 'trdnjava'
							and normalen_v in [(0,1), (0,-1), (1, 0), (-1, 0)]):
							return True
						elif slika[kralj.x+n*x_premika][self.y+n*y_premika].vrsta == 'kraljica':
							return True
						else:
							return False
				n+=1
			#če pridemo ven iz šahovnice brez da bi naleteli na figuro je poteza dovoljena (ni šaha)
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
		figure = slika_v_figure(slika)
		na_vrsti = self.barva
		#poiščemo kralja
		for figura in figure[na_vrsti]:
			if figura.vrsta == 'kralj':
				kralj = figura
				
		for premik in self.izracunaj_dovoljene_premike_iterator(slika, igra):
			x_koncna, y_koncna = premik
			poteza = (self.x,self.y,x_koncna,y_koncna)
			if not(bo_sah_po_potezi(igra, slika, figure, poteza, na_vrsti, kralj)): 
				yield poteza
	
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


class sah:
	def __init__(self):	
		self.igra = []
		self.na_vrsti = 'bel'
		self.figure = {'bel':[kmet_bel((0,1)), kmet_bel((1,1)), kmet_bel((2,1)), kmet_bel((3,1)), kmet_bel((4,1)), kmet_bel((5,1)), kmet_bel((6,1)),
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
		self.slika = figure_v_sliko(self.figure)		
	def vrni_kralje(self):
		bele = figure['bel']
		crne = figure['crn']
		for figura in bele:
			if figura.vrsta == 'kralj':
				bel_kralj = figura
		for figura in crne:
			if figura.vrsta == 'kralj':
				crn_kralj = figura
		return {'bel': bel_kralj, 'crn':crn_kralj}
	def naredi_potezo(self, poteza):
		x_z, y_z, x_k, y_k = poteza
		self.igra.append(poteza)
		figura = slika[x_z][y_z]
		figura.premakni((x_k, y_k))
		self.slika[x_z][y_z] = None
		self.slika[x_k][y_l] = figura
		self.figure = slika_v_figure(slika)
		self.na_vrsti = nasprotna_barva(na_vrsti)
	def vrni_vse_mozne_poteze_za_figure_na_vrsti(self):
		vse_mozne_poteze = []
		for figura in self.figure[self.na_vrsti]:
			for poteza in figura.dovoljene_poteze_iterator(self.slika, self.igra):
				vse_mozne_poteze.append(poteza)
		return vse_mozne_poteze
		
		

sahec = sah()
	
while len(sahec.vrni_vse_mozne_poteze_za_figure_na_vrsti()) != 0:
	print(sahec.vrni_vse_mozne_poteze_za_figure_na_vrsti())
	poteza = preberi_potezo(figure, na_vrsti, slika, igra) ##preveri tudi če je dovoljena poteza
	if poteza in sahec.vrni_vse_mozne_poteze_za_figure_na_vrsti():
		sahec.naredi_potezo(poteza)
	
