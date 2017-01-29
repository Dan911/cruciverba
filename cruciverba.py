class Cella:
	def __init__(self, lettera, inizioParolaOrizzontale, 
			inizioParolaVerticale):
		self.lettera = lettera
		self.inizioParolaOrizzontale = inizioParolaOrizzontale
		self.inizioParolaVerticale = inizioParolaVerticale
	
	def inizioParola(self, orientamento):
		if orientamento == 0: return self.inizioParolaOrizzontale
		else: return self.inizioParolaVerticale
	
	def __repr__(self):
		return self.lettera

def riempiCruciverba(cruciverba, parole, orientamento):
	posizione = posizioneInserimento(cruciverba, orientamento)
	if posizione == None:
		orientamento = opposto(orientamento)
		posizione = posizioneInserimento(cruciverba, orientamento)
		if posizione == None: return True
	modello = modelloParola(cruciverba, posizione, orientamento)
	paroleDaTentare = cercaParole(modello, parole)
	for parola in paroleDaTentare:
		inserisciParola(parola, cruciverba, posizione, orientamento)
		parole.remove(parola)
		successo = riempiCruciverba(cruciverba, parole, 
			opposto(orientamento))
		if(successo == True): return True
		rimuoviParola(modello, cruciverba, posizione, orientamento)
		parole.insert(0, parola)
	return False

def posizioneInserimento(cruciverba, orientamento):
	if orientamento == 0:
		return posizioneInserimentoOrizzontale(cruciverba)
	else: return posizioneInserimentoVerticale(cruciverba)

def posizioneInserimentoOrizzontale(cruciverba):
	for indiceRiga in range(righe(cruciverba)):
		riga = cruciverba[indiceRiga]
		indiceColonna = posizioneInserimentoInCelle(riga, 0)
		if indiceColonna != None: return (indiceRiga, indiceColonna)
	return None

def posizioneInserimentoVerticale(cruciverba):
	for indiceColonna in range(colonne(cruciverba)):
		colonna = prelevaColonna(indiceColonna, cruciverba)
		indiceRiga = posizioneInserimentoInCelle(colonna, 1)
		if indiceRiga != None: return (indiceRiga, indiceColonna)
	return None

def posizioneInserimentoInCelle(celle, orientamento):
	parolaInCorso = False
	for i in range(len(celle)-1):
		cella = celle[i]
		if cella.lettera == '*': 
			parolaInCorso = False
		elif cella.inizioParola(orientamento) == True: 
			parolaInCorso = True
		elif parolaInCorso == False and celle[i+1].lettera != '*': 
			return i
	return None

def modelloParola(cruciverba, posizione, orientamento):
	if orientamento == 0: 
		return modelloParolaOrizzontale(cruciverba, posizione)
	else: return modelloParolaVerticale(cruciverba, posizione)

def modelloParolaOrizzontale(cruciverba, posizione):
	celle = cruciverba[posizione[0]][posizione[1]:]
	return modelloParolaInCelle(celle)
	
def modelloParolaVerticale(cruciverba, posizione):
	celle = prelevaColonna(posizione[1], cruciverba)[posizione[0]:]
	return modelloParolaInCelle(celle)

def modelloParolaInCelle(celle):
	modello = []
	for cella in celle:
		if cella.lettera == '*': return "".join(modello)
		if cella.lettera == '': modello.append('.')
		else: modello.append(cella.lettera)
	return "".join(modello)

def cercaParole(modello, parole):
	risultatoRicerca = []
	for parola in parole:
		if(confrontaConModello(parola, modello) == True):
			risultatoRicerca.append(parola)
	return risultatoRicerca

def confrontaConModello(parola, modello):
	if len(parola) != len(modello): return False
	for i in range(len(modello)):
		if modello[i] == '.': continue
		if modello[i] != parola[i]: return False
	return True

def inserisciParola(parola, cruciverba, posizione, orientamento):
	if orientamento == 0: 
		inserisciParolaOrizzontale(parola, cruciverba, posizione)
	else: inserisciParolaVerticale(parola, cruciverba, posizione)

def inserisciParolaOrizzontale(parola, cruciverba, posizione):
	(riga, colonna) = posizione
	cruciverba[riga][colonna].inizioParolaOrizzontale = True
	for carattere in parola:
		cruciverba[riga][colonna].lettera = carattere
		colonna += 1

def inserisciParolaVerticale(parola, cruciverba, posizione):
	(riga, colonna) = posizione
	cruciverba[riga][colonna].inizioParolaVerticale = True
	for carattere in parola:
		cruciverba[riga][colonna].lettera = carattere
		riga += 1

def rimuoviParola(modello, cruciverba, posizione, orientamento):
	if orientamento == 0: 
		rimuoviParolaOrizzontale(modello, cruciverba, posizione)
	else: rimuoviParolaVerticale(modello, cruciverba, posizione)

def rimuoviParolaOrizzontale(modello, cruciverba, posizione):
	(riga, colonna) = posizione
	cruciverba[riga][colonna].inizioParolaOrizzontale = False
	for carattere in modello:
		if carattere == '.': cruciverba[riga][colonna].lettera = ''
		colonna += 1

def rimuoviParolaVerticale(modello, cruciverba, posizione):
	(riga, colonna) = posizione
	cruciverba[riga][colonna].inizioParolaVerticale = False
	for carattere in modello:
		if carattere == '.': cruciverba[riga][colonna].lettera = ''
		riga += 1
	
def prelevaColonna(c, cruciverba):
	return [cruciverba[r][c] for r in range(righe(cruciverba))]

def colonne(cruciverba):
	return len(cruciverba[0])

def righe(cruciverba):
	return len(cruciverba)

def opposto(orientamento):
	return (orientamento + 1) % 2

def stampaCruciverba(cruciverba):
	for riga in cruciverba:
		for cella in riga:
			print cella.lettera, '\t',
		print

def cruciverbaVuoto(righe, colonne):
	return [[Cella('', False, False) for _ in range(colonne)] 
		for _ in range(righe)]

cruciverba = cruciverbaVuoto(8,8)
cruciverba[0][7].lettera = '*'
cruciverba[1][6].lettera = '*'
cruciverba[2][4].lettera = '*'
cruciverba[3][0].lettera = '*'
cruciverba[3][6].lettera = '*'
cruciverba[4][0].lettera = '*'
cruciverba[4][3].lettera = '*'
cruciverba[4][6].lettera = '*'
cruciverba[5][1].lettera = '*'
cruciverba[6][4].lettera = '*'
cruciverba[6][7].lettera = '*'
cruciverba[7][5].lettera = '*'
parole = [
	'cariota',
	'afillo',
	'vite',
	'msg',
	'dixie',
	'ed',
	'ln',
	'ocotea',
	'gama',
	'op',
	'ovale',
	'ih',
	'cav',
	'ago',
	'afide',
	'av',
	'ritidoma',
	'ilex',
	'cal',
	'ol',
	'ilo',
	'tomento',
	'epi',
	'agama',
	'prova',
	'prove',
	'idiota',
	'maldonado',
	'alonso',
	'rossi',
	'button',
	'spazzatura',
	'riciclata',
	'piove',
	'governo'
	'ladro']
print riempiCruciverba(cruciverba, parole, 0)
print cruciverba
		
"""
def posizioneInserimentoInCelle(celle, orientamento):
	parolaInCorso = False
	for indice in len(celle):
		cella = celle[indice]
		if cella.inizioParolaOrizzontale == True: parolaInCorso = True
		if parolaInCorso == False: return (indiceRiga, indiceColonna)
		if cella.lettera == '*': parolaInCorso = False
	return None
"""

"""
def posizioneInserimentoInRiga(indiceRiga, cruciverba):
	parolaInCorso = False
	riga = cruciverba[indiceRiga]
	for indiceColonna in range(len(riga)-1):
		cella = riga[indiceColonna]
		if cella.lettera == '*': parolaInCorso = False
		elif cella.inizioParolaOrizzontale == True: parolaInCorso = True
		elif parolaInCorso == False and riga[indiceColonna + 1].lettera != '*': 
			return (indiceRiga, indiceColonna)
	return None

def posizioneInserimentoInColonna(indiceColonna, cruciverba):
	parolaInCorso = False
	colonna = prelevaColonna(indiceColonna, cruciverba)
	for indiceRiga in range(len(colonna)-1):
		cella = colonna[indiceRiga]
		if cella.inizioParolaVerticale == True: parolaInCorso = True
		if parolaInCorso == False:
			if colonna[indiceRiga + 1].lettera != '*': 
				return (indiceRiga, indiceColonna)
			else: parolaInCorso = True
		if cella.lettera == '*': parolaInCorso = False
	return None
"""			
		
		
	
