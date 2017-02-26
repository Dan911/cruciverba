from string import *
import string
import random
import operator
import pickle

indirizzo_file_parole = ""
indirizzo_file_definizioni = ""
num_righe_cruciverba = int(input('numero righe cruciverba:'))
num_colonne_cruciverba = int(input('numero colonne cruciverba:'))



#-----------------------------------------------------------------------
#definizione schema cruciverba allo stato iniziale

class Posizione:
	def __init__(self, coordinate, orientamento, lunghezza):
		self.coordinate = coordinate
		self.orientamento = orientamento
		self.lunghezza = lunghezza
		self.occupata = False
		self.incastri = 0
		self.parola = ''#contiene il nome della parola inserita
	
	def __repr__(self): 
		return "(coordinate: %s, orientamento: %d, lunghezza: %d, incastri: %d, parola: %s)\n" % (self.coordinate, 
			self.orientamento, self.lunghezza, self.incastri, self.parola)

class Cella:
	def __init__(self, riga, colonna):
		self.coordinate = (riga,colonna)
		self.lettera = ''
		self.occupata = 0
	
	def __repr__(self):
		return self.lettera

class Cruciverba:
	def __init__(self, righe, colonne):
		self.righe = righe
		self.colonne = colonne
		self.griglia = []	
		self.posizioni = [{},{}] # [{orizzontali}, {verticali}] la chiave data dalle coordinate, 
		self.indicePosizione = 1 # indice della definizione, parte da 1
		self._inizializzaGriglia()
		self._inizializzaCelleGriglia()
		self._inizializzaMappaPosizioni()
		self._eliminaPosizioniSuperflue()#definizioni di parole da 1 carattere, e' necessario perche' bisogna
										 #il caso in cui venga generato un rombo con un buco in mezzo
	def _inizializzaGriglia(self):
		for r in range(self.righe):
			self.griglia.append([])
			for c in range(self.colonne):
				self.griglia[r].append([])
				self.griglia[r][c] = Cella(r,c)
		#self.griglia[0][random.randint(0,self.colonne-1)].lettera = '*'
		
	def _inizializzaMappaPosizioni(self):
		posizioni = self._trovaPosizioni()	#MODIFICA: genero una posizione per volta in cui inserisco le parole
		prosegui = 0
		for posizione in posizioni:
			prosegui = 0
			#per ogni posizione da inserire controllo che nella direzione opposta a quella 
			#coordinata non sia gia' stato attribuito un indice per la definizione, se c'e' tengo lo stesso
			#altrimenti le attribuisco l'indicePosizione corrente, e incremento  indicePosizione 
			for i in self.posizioni[not(posizione.orientamento)].keys():
				if self.posizioni[not(posizione.orientamento)][i].coordinate == posizione.coordinate:
					self.posizioni[posizione.orientamento][i] = posizione
					prosegui = 1
			if not(prosegui):
				self.posizioni[posizione.orientamento][self.indicePosizione] = posizione
				self.indicePosizione += 1
	
	def _eliminaPosizioniSuperflue(self):
		#se c'e' una stessa definizione da 1 carattere in entrambi gli orientamenti (rombo) sostituire la cella con asterisco
		#poi eliminare tutte le definizioni da 1 carattere
		posizioniOrizzontali = self.posizioni[0].keys()
		posizioniVerticali = self.posizioni[1].keys()
		for i in posizioniOrizzontali:
			if self.posizioni[0][i].lunghezza == 1:
				for j in posizioniVerticali:
					if self.posizioni[1][j].lunghezza == 1:
						if self.posizioni[0][i].coordinate == self.posizioni[1][j].coordinate:
							(r,c) = self.posizioni[0][i].coordinate
							self.griglia[r][c].lettera = '*'
				del self.posizioni[0][i]
		for j in posizioniVerticali:
			if self.posizioni[1][j].lunghezza == 1:
				del self.posizioni[1][j]
				
	def _inizializzaCelleGriglia(self): # inizializza alcune caselle con asterisco, ottenendo lo stato iniziale		
		r = 0
		c = 0
		verifica = 0
		for r in range (self.righe):	
			verifica = self._generaRiga(r, 0, self.colonne)
			
			
	def _generaRiga(self, r, inizio, fine ):# pone asterisco in un posto a caso fra inizio e fine
		if inizio >= fine:
			return 0
		posizioneAsterisco = random.randint(inizio, fine)
		if posizioneAsterisco == fine: #l'asterisco e' fuori schema, quindi non c'e'
			return 0
		self.griglia[r][posizioneAsterisco].lettera = '*'
		distanza = random.randint(0, fine-1)
		self._generaRiga(r, inizio, posizioneAsterisco-distanza)
		self._generaRiga(r, posizioneAsterisco+distanza, fine)		
		
	def _trovaPosizioni(self):
		posizioniOrizzontali = self._trovaPosizioniOrizzontali()
		posizioniVerticali = self._trovaPosizioniVerticali()
		return posizioniOrizzontali + posizioniVerticali
	
	def _trovaPosizioniOrizzontali(self):
		posizioni = []
		for riga in range(self.righe):
			posizioni += self._trovaPosizioniInRiga(riga)
		return posizioni
	
	def _trovaPosizioniInRiga(self, riga):
		posizioni = []
		datiPosizioni = Cruciverba.datiPosizioniInCelle(self.prelevaRiga(riga))
		for (colonna, lunghezza) in datiPosizioni:
			coordinate = (riga, colonna)
			posizioni.append(Posizione(coordinate, 0, lunghezza))
		return posizioni
	
	def _trovaPosizioniVerticali(self):
		posizioni = []
		for colonna in range(self.colonne):
			posizioni += self._trovaPosizioniInColonna(colonna)
		return posizioni
	
	def _trovaPosizioniInColonna(self, colonna):
		posizioni = []
		datiPosizioni = Cruciverba.datiPosizioniInCelle(
			self.prelevaColonna(colonna))
		for (riga, lunghezza) in datiPosizioni:
			coordinate = (riga, colonna)
			posizioni.append(Posizione(coordinate, 1, lunghezza))
		return posizioni
		
	@staticmethod
	def datiPosizioniInCelle(celle):
		datiPosizioni = []
		indiceInizio = indiceFine = 0
		while indiceInizio < len(celle):
			indiceInizio = Cruciverba.trovaProssimoBlank(indiceFine, celle)
			if indiceInizio < len(celle):
				indiceFine = Cruciverba.trovaProssimoAsterisco(
					indiceInizio, celle)
				lunghezza = indiceFine - indiceInizio
				if lunghezza >=1: 
					datiPosizioni.append((indiceInizio, lunghezza))
		return datiPosizioni
	
	@staticmethod
	def trovaProssimoBlank(indicePartenza, celle):
		return Cruciverba.trovaProssimoCarattere('', indicePartenza, celle)
	
	@staticmethod
	def trovaProssimoAsterisco(indicePartenza, celle):
		return Cruciverba.trovaProssimoCarattere('*', indicePartenza, celle)
	
	@staticmethod
	def trovaProssimoCarattere(carattere, indicePartenza, celle):		
		i = indicePartenza
		while i < len(celle):
			if celle[i].lettera == carattere: return i
			i += 1
		return i
	
	def prelevaRiga(self, riga):
		return self.griglia[riga]
	
	def prelevaColonna(self, colonna):
		return [self.griglia[i][colonna] for i in range(self.righe)]
		
		
	def __repr__(self):
		stringa = ''
		bordo =  '+' + ''.join(['---+' for _ in range(self.colonne)]) + '\n'
		for r in range(self.righe):
			stringa += bordo
			for c in range(self.colonne):
				lettera = self.griglia[r][c].lettera
				if c == 0: stringa += '|'
				stringa += ' ' + (lettera != '' and lettera or ' ') + ' |'
			stringa += '\n'
		stringa += bordo
		return stringa

#------------------------------------------------------------------------
#gestione parole dizionario

class Parola:
	
	def __init__(self, nome):
		self.nome = nome
		self.lunghezza = len(nome)
		self.ricorrenze = 0
		self.definizione = ''
	
	def __str__(self):
		return "%s"%(self.nome)

	def like(self, s):#confronta la parola (self) con il modello s 	es.--sa--e (- carattere qualsiasi)'
		if self.lunghezza != len(s):
			return 0
		for i in range(self.lunghezza):
			if (s[i] in string.lowercase) or (s[i] in string.uppercase):
				if not(s[i]==self.nome[i]):
					return 0
			elif s[i]!='-':
				return 0;
			else: continue
		return 1
		
	def __len__(self):
		return self.lunghezza
		
def elencoDaFile(indirizzo): #da un file crea un elenco di parole
	f = open(indirizzo, 'r')
	elencoNomiParole = f.read().split('\r\n')
	elencoCompletoParole = []
	for i in range(len(elencoNomiParole)):
		elencoCompletoParole.append(Parola(elencoNomiParole[i]))
	f.close()
	return elencoCompletoParole

def ripartisciElencoCompletoPerLunghezza(elenco): #dall'elenco crea gruppi di parole tutte della stessa lunghezza
	partizione = {}
	for i in range(len(elenco)):		#visito l'elenco completo delle parole
		
		len_i = len(elenco[i])		#lunghezza parola i-esima dell'elenco
		 
		# popolo la partizione	NB elenco e partizione condividono lo stesso elemento, non copie
		if (partizione.has_key(len_i)):
			partizione[len_i].append(Parola(''))
			partizione[len_i][-1] = elenco[i]
		else: partizione[len_i] = [elenco[i]]
	return partizione

def ripartisciElencoCompletoPerSimilitudine(elenco):
	# raggruppa parole simili partendo da un elenco completo in ordine alfabetico
	# precondizione: elenco in ordine alfabetico
	# il raggruppamento e' significativo solo per parole lunghe almeno 4
	# una prima passata prende una parola e la raggruppa con tutte quelle che la contengono
	# una seconda passata prende una chiave esclusa l'ultima lettera e unisce la classe con le classi
	# la cui chiave comprende la prima 
	partizione = {}	#la chiave e' la prima parola della classe in ordine alfabetico						
	i = 0
	j = 0
	while i < (len(elenco)): 			
		if len(elenco[i]) > 3:	
			partizione[elenco[i]] = [elenco[i]]
			j = i+1
			try:
				while elenco[i].nome in elenco[j].nome:
					partizione[elenco[i]].append(Parola(''))
					partizione[elenco[i]][-1] = elenco[j]	
					j += 1
				i = j
			except:
				i = j
		else: 
			partizione[elenco[i]] = [elenco[i]]
			i +=1
	#inizio seconda passata
	k = partizione.keys()
	k.sort()
	partizione2 = {}
	i = 0
	while i < len(k):
		if len(k[i]) > 3:
			partizione2[k[i]] = partizione[k[i]]
			j = i+1
			try:
				while partizione2[k[i]][0].nome[:-1] in partizione[k[j]][0].nome:
					partizione2[k[i]] += partizione[k[j]]
					j += 1
				i = j
			except:
				i = j
		else:
			partizione2[k[i]] = partizione[k[i]]
			i += 1	
	return partizione2 



def contaParolePerLunghezza(elenco): #dall'elenco conta il numero di parole di ogni lunghezza
	numParoleLunghezza = {}
	indici = elenco.keys()
	for i in range(len(indici)):
		len_i = len(elenco[indici[i]])	
		numParoleLunghezza[indici[i]]=len_i
	return numParoleLunghezza

elencoCompletoParole = elencoDaFile(indirizzo_file_parole)	#contiene tutte le parole
partizionePerLunghezza = ripartisciElencoCompletoPerLunghezza(elencoCompletoParole)	#contiene tutte le parole raggruppate per lunghezza
partizionePerSimilitudine = ripartisciElencoCompletoPerSimilitudine(elencoCompletoParole)
numParoleLunghezza = contaParolePerLunghezza(partizionePerLunghezza)	#contiene per ogni gruppo della partizione il numero di elementi totali


def confronto1(modello):#confronta il modello con tutte le parole del gruppo di lunghezza uguale
	k=len(modello)
	paroleCompatibili=[]
	try:
		for i in range(len(partizionePerLunghezza[k])):
			if partizionePerLunghezza[k][i].like(modello):
				paroleCompatibili=paroleCompatibili+[partizionePerLunghezza[k][i]]
				print paroleCompatibili[-1]
		if paroleCompatibili==[]:
			print "nessuna parola compatibile trovata"
		return paroleCompatibili
	except:
		print "modello non compatibile col dizionario"
	
def confronto2(modello, dizionario):#confronta il modello con tutte le parole di un dizionario (elenco)					
	paroleCompatibili=[]
	for i in range(len(dizionario)):
		if dizionario[i].like(modello):
			paroleCompatibili=paroleCompatibili+[dizionario[i]]
			print paroleCompatibili[-1]
	if paroleCompatibili==[]:
		print "nessuna parola compatibile trovata"
	return paroleCompatibili

#-----------------------------------------------------------------------
#riempimento schema (riempire le celle con le lettere, poi inserire la parola completa nell'apposito
#						campo della Posizione)

#-----------------------------------------------------------------------


c = Cruciverba(num_righe_cruciverba, num_colonne_cruciverba) 	

print c
print c.posizioni[0].items()
print c.posizioni[1].items()

#-----------------------------------------------------------------------
#aggiornamento definizioni parole

	#- le definizioni per ogni parola sono salvate in un file 
	#- il file contiene un dizionario con tutte le parole della lista come chiave e le definizioni tutte vuote
	#- le definizioni vengono aggiunte al cruciverba solo a fine riempimento
	#- se non c'e' la definizione per una parola, la si aggiunge al file
	#- le definizioni sono stringhe di caratteri lunghe massimo 80 caratteri
	#- man mano che si creeranno i cruciverba, si inseriranno nel file le definizioni delle parole usate
	
	#eventuali miglioramenti successivi:
	#(- ogni parola puo' avere fino a tre diverse definizioni, ne viene scelta una a caso)
	#(- per ogni parola utilizzata: se non si hanno definizioni se ne fa aggiungere una all'amministratore
	#  se si hanno meno di tre definizioni ma almeno una si fa scegliere all'amministratore se ne vuole
	#  aggiungere altre o usare quelle gia' presenti)

def aggiorna_definizioni(indirizzo):
	file_definizioni = open(indirizzo,"r+")
	dizionario_definizioni = pickle.load(f) 	#dizionario con chiave la parola e valore la definizione
	file_definizioni.close()

	parole_orizzontali = []
	parole_verticali = []
	
	posizioni_orizzontali = c.posizioni[0].items()
	posizioni_verticali = c.posizioni[1].items()
	
	for i in range(len(posizioni_orizzontali)):
		parole_orizzontali += posizioni_orizzontali[i].parola

	for i in range(len(posizioni_verticali)):
		parole_verticali += posizioni_verticali[i].parola

	for i in range(len(parole_orizzontali)):
		parola = parole_orizzontali[i]
		if(dizionario_definizioni[parola] == ''):
			dizionario_definizioni[parola] = raw_input("inserire una definizione per %s: "%parola)
		else: continue
	
	for i in range(len(parole_verticali)):
		parola = parole_verticali[i]
		if(dizionario_definizioni[parola] == ''):
			dizionario_definizioni[parola] = raw_input("inserire una definizione per %s: "%parola)
		else: continue

	file_definizioni = open(indirizzo,"w")
	pickle.dump(dizionario_definizioni, file_definizioni)
	file_definizioni.close()


aggiorna_definizioni(indirizzo_file_definizioni)
#-----------------------------------------------------------------------




