import random

class Cella:
	def __init__(self, lettera):
		self.lettera = lettera
		self.chiavePosizioneOrizzontale = None
		self.occupataOrizzontale = False
		self.chiavePosizioneVerticale = None
		self.occupataVerticale = False
	
	def impostaChiavePosizione(self, chiavePosizione):
		orientamento = chiavePosizione[0]
		if orientamento == 0: self.chiavePosizioneOrizzontale = chiavePosizione
		else: self.chiavePosizioneVerticale = chiavePosizione
	
	def chiavePosizione(self, orientamento):
		if orientamento == 0: return self.chiavePosizioneOrizzontale
		return self.chiavePosizioneVerticale
	
	def impostaOccupata(self, occupazione, orientamento):
		if orientamento == 0: self.occupataOrizzontale = occupazione
		else: self.occupataVerticale = occupazione
	
	def occupata(self, orientamento):
		if orientamento == 0: return self.occupataOrizzontale
		return self.occupataVerticale
	
	def __repr__(self):
		return self.lettera

class Posizione:
	def __init__(self, coordinate, orientamento, lunghezza):
		self.coordinate = coordinate
		self.orientamento = orientamento
		self.lunghezza = lunghezza
		self.occupata = False
		self.incastri = 0
	
	def __repr__(self): 
		return "(coordinate: %s, orientamento: %d, lunghezza: %d, incastri: %d)" % (self.coordinate, 
			self.orientamento, self.lunghezza, self.incastri)

class Cruciverba:
	def __init__(self, righe, colonne, statoIniziale):
		self.righe = righe
		self.colonne = colonne
		self.griglia = []
		self.posizioni = {}
		self._inizializzaGriglia(statoIniziale)
		self._inizializzaMappaPosizioni()
		self._inizializzaCelleGriglia()
	
	def _inizializzaGriglia(self, statoIniziale):
		self.griglia = [[Cella('') for _ in range(self.colonne)] 
			for _ in range(self.righe)]
		righeStatoIniziale = statoIniziale[1:-1].split('\n')
		for r in range(self.righe):
			for c in range(self.colonne):
				cella = self.griglia[r][c]
				lettera = righeStatoIniziale[r][c]
				if lettera == '*': cella.lettera = lettera
					
	
	def _inizializzaMappaPosizioni(self):
		posizioni = self._trovaPosizioni()
		for posizione in posizioni:
			chiave = (posizione.orientamento, posizione.coordinate)
			self.posizioni[chiave] = posizione
	
	def _inizializzaCelleGriglia(self):
		posizioni = self.posizioni.values()
		for posizione in posizioni:
			self._inizializzaCellePosizione(posizione)
	
	def _inizializzaCellePosizione(self, posizione):
		chiavePosizione = (posizione.orientamento, posizione.coordinate)
		(riga, colonna) = posizione.coordinate
		for _ in range(posizione.lunghezza):
			cella = self.griglia[riga][colonna]
			cella.impostaChiavePosizione(chiavePosizione)
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
	
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
				if lunghezza > 3: 
					datiPosizioni.append((indiceInizio, lunghezza))
		return datiPosizioni
	
	def prossimaPosizioneInserimento(self, posizionePrecedente = None):
		posizioniCandidate = []
		if posizionePrecedente != None:
			posizioniCandidate = self._trovaPosizioniLibereIntersecanti(
				posizionePrecedente)
		if posizioniCandidate == []: 
			posizioniCandidate = [posizione for posizione in 
				self.posizioni.values() if not posizione.occupata]
		return Cruciverba.posizioneMigliore(posizioniCandidate)
	
	def _trovaPosizioniLibereIntersecanti(self, posizionePrecedente):
		posizioni = []
		(riga, colonna) = posizionePrecedente.coordinate
		orientamento = Cruciverba.opposto(posizionePrecedente.orientamento)
		for _ in range(posizionePrecedente.lunghezza):
			cella = self.griglia[riga][colonna]
			if not cella.occupata(orientamento):
				chiavePosizione = cella.chiavePosizione(orientamento)
				if chiavePosizione != None:
					posizioni.append(self.posizioni[chiavePosizione])
			if posizionePrecedente.orientamento == 0: colonna += 1
			else: riga += 1
		return posizioni
		
	def modelloParola(self, posizione):
		modello = []
		(riga, colonna) = posizione.coordinate
		for _ in range(posizione.lunghezza):
			lettera = self.griglia[riga][colonna].lettera
			letteraPrima = self._ottieniLetteraPrima(
				(riga, colonna), posizione.orientamento)
			letteraDopo = self._ottieniLetteraDopo(
				(riga, colonna), posizione.orientamento)
			modello.append((letteraPrima, lettera, letteraDopo))
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
		return modello
	
	def _ottieniLetteraPrima(self, coordinate, orientamento):
		(riga, colonna) = coordinate
		if orientamento == 0: riga -= 1
		else: colonna -= 1
		if riga >= 0 and colonna >= 0:
			return self.griglia[riga][colonna].lettera
		return '';
	
	def _ottieniLetteraDopo(self, coordinate, orientamento):
		(riga, colonna) = coordinate
		if orientamento == 0: riga += 1
		else: colonna += 1
		if riga < self.righe and colonna < self.colonne:
			return self.griglia[riga][colonna].lettera
		return '';
	
	def inserisciParola(self, parola, posizione):
		if posizione.occupata: raise Exception
		(riga, colonna) = posizione.coordinate
		orientamentoOpposto = Cruciverba.opposto(posizione.orientamento)
		for i in range(posizione.lunghezza):
			cella = self.griglia[riga][colonna]
			if cella.lettera == '':
				cella.lettera = parola[i]
				chiavePosizioneIntersecante = cella.chiavePosizione(
					orientamentoOpposto)
				if chiavePosizioneIntersecante != None:
					self.posizioni[chiavePosizioneIntersecante].incastri += 1
			elif cella.lettera != parola[i]: raise Exception
			cella.impostaOccupata(True, posizione.orientamento)
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
		posizione.occupata = True
	
	def rimuoviParola(self, posizione):
		if not posizione.occupata: return
		(riga, colonna) = posizione.coordinate
		orientamentoOpposto = Cruciverba.opposto(posizione.orientamento)
		for i in range(posizione.lunghezza):
			cella = self.griglia[riga][colonna]
			if not cella.occupata(orientamentoOpposto):
				cella.lettera = ''
				chiavePosizioneIntersecante = cella.chiavePosizione(
					orientamentoOpposto)
				if chiavePosizioneIntersecante != None:
					self.posizioni[chiavePosizioneIntersecante].incastri -= 1
			cella.impostaOccupata(False, posizione.orientamento)
			if posizione.orientamento == 0: colonna += 1
			else: riga += 1
		posizione.occupata = False
		
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
	
	#sbagliata
	@staticmethod
	def posizioneMigliore(posizioni):
		posizioneMigliore = None
		for posizione in posizioni:
			if posizioneMigliore == None: posizioneMigliore = posizione
			elif posizione.incastri > posizioneMigliore.incastri:
				posizioneMigliore = posizione
			elif (posizione.incastri == posizioneMigliore.incastri and
				posizione.lunghezza > posizioneMigliore.lunghezza):
				posizioneMigliore = posizione
		return posizioneMigliore
	
	def prelevaRiga(self, riga):
		return self.griglia[riga]
	
	def prelevaColonna(self, colonna):
		return [self.griglia[i][colonna] for i in range(self.righe)]
	
	@staticmethod
	def opposto(orientamento):
		return (orientamento + 1) % 2
	
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
				

def riempiCruciverba(cruciverba, parole, posizionePrecedente = None):
	posizione = cruciverba.prossimaPosizioneInserimento(posizionePrecedente)
	"""
	fh = open('outcrux', 'a')
	fh.write(repr(posizione) + '\n' + repr(cruciverba) + '\n')
	fh.close()
	"""
	if posizione == None: return True
	modello = cruciverba.modelloParola(posizione)
	paroleDaTentare = cercaParole(modello, parole)
	posizioneSuccessiva = None
	lettereEscluse = ''
	indiceIntersezione = -1
	for (parola, _) in paroleDaTentare:
		if indiceIntersezione != -1 and (parola[indiceIntersezione] 
			in lettereEscluse): continue
		cruciverba.inserisciParola(parola, posizione)
		if posizioneSuccessiva == None:
			posizioneSuccessiva = cruciverba.prossimaPosizioneInserimento(posizione)
			indiceIntersezione = calcolaIndiceIntersezione(posizione, posizioneSuccessiva)
		#parole.remove(parola)
		if riempiCruciverba(cruciverba, parole, posizione) == True: return True
		else: lettereEscluse += parola[indiceIntersezione]
		cruciverba.rimuoviParola(posizione)
		#parole.insert(0, parola)
	return False

def calcolaIndiceIntersezione(posizioneX, posizioneY):
	if posizioneY == None: return -1
	if posizioneX.orientamento == 0:
		return posizioneY.coordinate[1] - posizioneX.coordinate[1]
	else: return posizioneY.coordinate[0] - posizioneX.coordinate[0]

def cercaParole(modello, parole):
	risultatoRicerca = []
	for parola in parole:
		punteggio = valutaParola(parola, modello)
		if punteggio != -1: risultatoRicerca.append((parola, punteggio))
	return sorted(risultatoRicerca, reverse = True, 
		key = lambda (_, punteggio): punteggio)

def valutaParola(parola, modello):
	if len(parola) != len(modello): return -1
	punteggioTotale = 0
	for i in range(len(modello)):
		punteggio = valutaAbbinamento(parola[i], modello[i])
		if punteggio == -1: return -1
		punteggioTotale += punteggio
	return punteggioTotale

def valutaAbbinamento(lettera, modello):
	(letteraPrima, letteraModello, letteraDopo) = modello
	if letteraModello != '' and letteraModello != lettera: return -1
	if letteraModello == lettera: return 0
	punteggio = 0
	if consonante(lettera):
		if letteraDopo == '*': return 0
		if vocale(letteraPrima): punteggio += 1
		if vocale(letteraDopo): punteggio += 1
	elif vocale(lettera):
		if consonante(letteraPrima): punteggio += 1
		if consonante(letteraDopo): punteggio += 1
	return punteggio

def consonante(lettera):
	return lettera in "*bcdfghjklmnpqrstvwxyz"

def vocale(lettera):
	return lettera in "*aeiou"

def ottieniListaParole():
	fh = open('paroleItaliano', 'r')
	return fh.read().split('\n')

statoInizialeCruciverba = """
-------*
------*-
----*---
*-----*-
*--*--*-
-*------
----*--*
-----*--
"""

parole = ottieniListaParole()
cruciverba = Cruciverba(8, 8, statoInizialeCruciverba)
random.shuffle(parole)
print riempiCruciverba(cruciverba, parole)
print cruciverba

"""
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
parole = parole + ['dando', 'inizio', 'alla', 'biografia', 'del', 'mio', 'eroe,', 'aleksej', 'f\xc3\xabdorovi\xc4\x8d', 'karamazov,', 'mi', 'trovo', 'in', 'un', 'certo', 'imbarazzo.', 'e', 'cio\xc3\xa8:', 'anche', 'se', 'chiamo', 'il', 'tuttavia,', 'io', 'stesso', 'sono', 'consapevole', 'che', 'egli', 'non', '\xc3\xa8', 'affatto', 'grande', 'uomo,', 'quindi', 'gi\xc3\xa0', 'prevedo', 'inevitabili', 'domande', 'di', 'questo', 'genere:', 'cosa', 'notevole', 'lo', 'avete', 'eletto', 'a', 'vostro', 'eroe?', 'ha', 'fatto', 'tanto', 'notevole?', 'chi', 'conosce', 'per', 'quale', 'ragione?', 'perch\xc3\xa9', 'io,', 'lettore,', 'dovrei', 'perdere', 'tempo', 'ad', 'apprendere', 'i', 'fatti', 'della', 'sua', 'vita?', 'l\xe2\x80\x99ultima', 'domanda', 'la', 'pi\xc3\xb9', 'inesorabile', 'quanto', 'posso', 'solo', 'rispondere', 'questo:', '\xe2\x80\x9cforse', 'capirete', 'da', 'voi', 'leggendo', 'romanzo\xe2\x80\x9d.', 'se,', 'una', 'volta', 'letto', 'romanzo,', 'capiste', 'concordaste', 'sul', 'sia', 'davvero', 'persona', 'dico', 'con', 'rammarico', 'avverr\xc3\xa0', 'proprio', 'questo.', 'personalmente', 'ritengo', 'degno', 'nota,', 'ma', 'dubito', 'seriamente', 'riuscire', 'dimostrarlo', 'al', 'lettore.', 'protagonista,', 'protagonista', 'vago,', 'indefinito.', 'resto,', 'forse,', 'un\xe2\x80\x99era', 'come', 'nostra,', 'sarebbe', 'strano', 'pretendere', 'chiarezza', 'dalla', 'gente.', 'per\xc3\xb2', 'abbastanza', 'certa:', 'strana,', 'persino', 'eccentrico.', 'stranezza', 'l\xe2\x80\x99eccentricit\xc3\xa0', 'danneggiano,', 'diano', 'diritto', 'all\xe2\x80\x99attenzione,', 'soprattutto', 'quando', 'tutti', 'tentano', 'mettere', 'insieme', 'particolari', 'trovare', 'qualche', 'valore', 'comune', 'nella', 'confusione', 'generale.', 'mentre', 'l\xe2\x80\x99eccentrico,', 'maggior', 'parte', 'dei', 'casi,', 'elemento', 'particolare,', 'isolato.', 'forse', 'cos\xc3\xac?', 'ecco:', 'sarete', 'd\xe2\x80\x99accordo', 'questa', 'mia', 'ultima', 'tesi', 'risponderete', '\xe2\x80\x9cnon', 'cos\xc3\xac\xe2\x80\x9d', 'oppure', 'sempre', 'cos\xc3\xac\xe2\x80\x9d,', 'allora,', 'permesso,', 'sentirei', 'incoraggiato', 'riguardo', 'eroe', 'f\xc3\xabdorovi\xc4\x8d.', 'giacch\xc3\xa9', 'eccentrico', 'sempre\xe2\x80\x9d', 'ma,', 'contrario,', 'accade', 'pure', 'stesso,', 'oserei', 'dire,', 'porti', 'dentro', 's\xc3\xa9', 'nocciolo', 'tutto,', 'resto', 'degli', 'uomini', 'epoca', 'n\xe2\x80\x99\xc3\xa8', 'temporaneamente', 'allontanato', 'ragione,', 'investito', 'raffica', 'vento...', 'comunque', 'avrei', 'dovuto', 'lasciarmi', 'andare', 'queste', 'dichiarazioni', 'estremamente', 'banali', 'confuse', 'cominciare', 'nel', 'semplice', 'modi,', 'senza', 'tanti', 'preamboli:', 'libro', 'piacer\xc3\xa0,', 'verr\xc3\xa0', 'letto.', 'guaio', 'ho', 'due', 'romanzi', 'soltanto', 'biografia.', 'romanzo', 'principale', 'secondo:', 'l\xe2\x80\x99attivit\xc3\xa0', 'ai', 'nostri', 'giorni,', 'momento', 'attuale.', 'invece,', 'primo', 'avuto', 'luogo', 'ben', 'tredici', 'anni', 'fa', 'propriamente', 'prima', 'giovinezza', 'eroe.', 'fare', 'meno', 'esso', 'molte', 'cose', 'secondo', 'sarebbero', 'comprensibili.', 'impaccio', 'iniziale', 'si', 'complica', 'ulteriormente:', 'biografo,', 'potrebbe', 'essere', 'eccessivo', 'cos\xc3\xac', 'modesto', 'indefinito,', 'potrei', 'uscirmene', 'giustificare', 'tale', 'arroganza', 'mia?', 'smarrito', 'tentativo', 'risolvere', 'tali', 'quesiti,', 'deciso', 'sorvolare', 'su', 'essi', 'cercare', 'risoluzione', 'alcuna.', 's\xe2\x80\x99intende,', 'lettore', 'perspicace', 'avr\xc3\xa0', 'indovinato', 'pezzo', 'qui', 'volevo', 'parare', 'sin', 'dall\xe2\x80\x99inizio,', 'sar\xc3\xa0', 'irritato', 'me', 'l\xe2\x80\x99inutile', 'spreco', 'sterili', 'parole', 'prezioso.', 'dar\xc3\xb2', 'risposta', 'precisa', 'proposito:', 'sprecato', 'prezioso', 'gentilezza,', 'calcolo:', '\xe2\x80\x9calmeno', 'ci', 'aveva', 'avvertiti', 'tempo\xe2\x80\x9d,', 'diranno.', 'contento', 'spaccato', 'racconti', '\xe2\x80\x9cferma', 'restando', 'sostanziale', 'unit\xc3\xa0', 'tutto\xe2\x80\x9d:', 'dopo', 'aver', 'racconto,', 'potr\xc3\xa0', 'valutare', 'valga', 'pena', 'tentare', 'secondo.', 'naturalmente,', 'obblighi', 'nessuno', 'abbandonare', 'seconda', 'pagina', 'racconto', 'aprirlo', 'mai', 'pi\xc3\xb9.', 'sapete,', 'esistono', 'lettori', 'sensibili', 'vorranno', 'assolutamente', 'portare', 'termine', 'lettura', 'incorrere', 'nell\xe2\x80\x99errore', 'giudizio', 'imparziale;', 'critici', 'russi,', 'esempio,', 'fra', 'questi.', 'ecco,', 'davanti', 'persone', 'genere,', 'sento', 'cuore', 'leggero:', 'nonostante', 'tutta', 'loro', 'delicatezza', 'buona', 'fede,', 'fornisco', 'pretesto', 'legittimo', 'episodio', 'romanzo.', 'concludo', 'premessa.', 'pienamente', 'superflua,', 'dal', 'stata', 'scritta,', 'rimanga', 'pure.\ne', 'adesso', 'lavoro.\n\n\nparte', 'prima\n\n\n\n\nlibro', '\xe2\x80\xa2', 'storia', 'famigliola\n\n\ni', 'f\xc3\xabdor', 'pavlovi\xc4\x8d', 'karamazov\n\naleksej', 'karamazov', 'era', 'terzo', 'figlio', 'proprietario', 'terriero', 'nostro', 'distretto,', 'assai', 'noto', 'suoi', 'tempi', '(e', 'ancor', 'oggi', 'ricordato', 'noi)', 'tragica', 'oscura', 'fine,', 'avvenuta', 'esattamente', 'parler\xc3\xb2', 'debito.', 'adesso,', '\xe2\x80\x9cproprietario', 'terriero\xe2\x80\x9d', '(come', 'chiamava', 'noi,', 'vita', 'abitato', 'quasi', 'propriet\xc3\xa0),', 'dir\xc3\xb2', 'tipo', 'strano,', 'quelli', 'tuttavia', 'incontrano', 'spesso,', 'abietta', 'depravata,', 'balorda,', 'quei', 'balordi,', 'per\xc3\xb2,', 'sanno', 'gestire', 'egregiamente', 'propri', 'affarucci', 'e,', 'pare,', 'quelli.', 'pavlovi\xc4\x8d,', 'cominciato', 'nulla;', 'propriet\xc3\xa0', 'modestissima,', 'correva', 'qua', 'l\xc3\xa0', 'pranzare', 'tavola', 'altrui,', 'ingegnava', 'parassita,', 'eppure', 'trapasso', 'gli', 'trovarono', 'centomila', 'rubli', 'contanti,', 'contempo', 'continuato', 'uno', 'dissennati', 'scavezzacolli', 'tutto', 'distretto.', 'ripeto', 'ancora:', 'tratta', 'stupidit\xc3\xa0', '-', 'questi', 'intelligente', 'scaltra', 'dissennatezza,', 'giunta', 'nazionale.\nsi', 'sposato', 'volte', 'tre', 'figli:', 'maggiore,', 'dmitrij', 'f\xc3\xabdorovi\xc4\x8d,', 'moglie,', 'altri', 'due,', 'ivan', 'aleksej,', 'seconda.', 'moglie', 'apparteneva', 'nobile', 'stirpe,', 'ricca', 'famosa,', 'anch\xe2\x80\x99essi', 'proprietari', 'terrieri', 'miusov.', 'dilungher\xc3\xb2', 'troppo', 'spiegare', 'accadde', 'ragazza', 'dote,', 'bella', 'oltre', 'quelle', 'intelligenze', 'vivaci', 'rare', 'nostra', 'generazione,', 'trovavano', 'precedente,', 'abbia', 'potuto', 'sposare', 'nullit\xc3\xa0,', '\xe2\x80\x9cscorfano\xe2\x80\x9d,', 'allora', 'chiamavano', 'tutti.', 'conosciuto', 'infatti', 'fanciulla', 'appartenente', 'penultima', 'generazione', '\xe2\x80\x9cromantica\xe2\x80\x9d,', 'alcuni', 'misterioso', 'amore', 'signore,', 'avrebbe', 'tranquillissimamente', 'qualunque', 'momento,', 'fin\xc3\xac', 'inventarsi', 'sola', 'ostacoli', 'insormontabili,', 'gett\xc3\xb2', 'fiume', 'profondo', 'rapido', 'ripa', 'alta', 'scoscesa,', 'precipizio,', 'vi', 'per\xc3\xac', 'decisamente', 'causa', 'delle', 'proprie', 'fisime,', 'poter', 'assomigliare', 'all\xe2\x80\x99ofelia', 'shakespeare;', 'anzi,', 'quel', 'ella', 'notato', 'vagheggiato', 'tempo,', 'fosse', 'stato', 'pittoresco,', 'suo', 'posto', 'prosaica', 'riva', 'pianeggiante,', 'suicidio', 'avvenuto.', 'vero,', 'c\xe2\x80\x99\xc3\xa8', 'credere', 'russa,', 'durante', 'le', 'ultime', 'o', 'generazioni,', 'siano', 'verificati', 'pochi', 'episodi', 'questo,', 'simili', 'analogamente,', 'l\xe2\x80\x99azione', 'adelaida', 'ivanovna', 'miusova', 'dubbio', 'un\xe2\x80\x99eco', 'suggestioni', 'altrui', 'dell\xe2\x80\x99esasperazione', 'mente', 'prigioniera.', 'voluto', 'affermare', 'l\xe2\x80\x99indipendenza', 'femminile,', 'andar', 'contro', 'convenzioni', 'sociali,', 'dispotismo', 'parenti', 'famiglia,', 'compiacente', 'fantasia', 'l\xe2\x80\x99aveva', 'convinta,', 'poniamo,', 'istante,', 'malgrado', 'fama', 'coraggiosi', 'ironici', 'quell\xe2\x80\x99era', 'transizione', 'verso', 'migliori,', 'altro', 'tristo', 'buffone', 'nulla', 'lato', 'piccante', 'matrimonio', 'fu', 'preceduto', 'rapimento,', 'lusing\xc3\xb2', 'molto', 'ivanovna.', 'canto', 'suo,', 'oltremodo', 'predisposto', 'azioni', 'genere', 'propria', 'posizione', 'sociale,', 'ardeva', 'desiderio', 'far', 'carriera', 'costo,', 'l\xe2\x80\x99idea', 'legarsi', 'famiglia', 'mani', 'dote', 'allettante', 'lui.', 'all\xe2\x80\x99amore', 'reciproco,', 'pare', 'ce', 'ne', 'affatto,', 'n\xc3\xa9', 'fidanzata,', 'lui,', 'bellezza', 'ivanovna,', 'caso', 'l\xe2\x80\x99unico', 'uomo', 'sensualissimo', 'corso', 'esistenza,', 'pronto', 'correre', 'dietro', 'istantaneamente', 'ogni', 'gonnella,', 'minimo', 'segno', 'incoraggiamento.', 'quella', 'donna', 'dunque', 'l\xe2\x80\x99unica', 'nessun', 'effetto', 'sulla', 'sensualit\xc3\xa0.\nsubito', 's\xe2\x80\x99avvide', 'immediatamente', 'provare', 'disprezzo', 'nient\xe2\x80\x99altro', 'nei', 'confronti', 'marito,', 'cosicch\xc3\xa9', 'conseguenze', 'delinearono', 'straordinaria', 'rapidit\xc3\xa0.', 'avesse', 'accettato', 'fretta', 'compiuto,', 'assegnato', 'fuggitiva,', 'coniugi', 'ebbe', 'estremo', 'disordine', 'eterne', 'scenate.', 'raccontava', 'giovane', 'sposa', 'dimostrato', 'animo', 'incomparabilmente', 'ed', 'elevato', 'quale,', 'noto,', 'arraff\xc3\xb2', 'd\xe2\x80\x99un', 'sol', 'colpo', 'soldi,', 'venticinquemila', 'rubli,', 'subito', 'li', 'ricevuti,', 'lei', 'fossero', 'letteralmente', 'volatilizzati.', 'piccolo', 'villaggio', 'casa', 'citt\xc3\xa0', 'bella,', 'costituivano', 'cerc\xc3\xb2', 'lungo', 'mezzi', 'farli', 'intestare', 'nome,', 'atto', 'opportuno,', 'probabilmente', 'riuscito,', 'foss\xe2\x80\x99altro,', 'diciamo', 'cos\xc3\xac,', 'ripugnanza', 'ispirava', 'continuamente', 'consorte', 'sue', 'vergognose', 'suppliche', 'estorsioni,', 'nonch\xc3\xa9', 'stanchezza', 'emotiva', 'levarselo', 'torno.', 'fortuna,', 'mise', 'mezzo', 'pose', 'freno', 'piovra.', 'sa', 'sposi', 'erano', 'frequenti', 'litigi,', 'dice,', 'picchiare,', 'bens\xc3\xac', 'focosa,', 'audace,', 'carnagione', 'olivastra,', 'insofferente', 'dotata', 'forza', 'fisica.', 'abbandon\xc3\xb2', 'scappando', 'seminarista,', 'morto', 'fame', 'faceva', 'l\xe2\x80\x99istitutore,', 'lasciando', 'alle', 'cure', 'marito', 'figlioletto', 'mitja', 'anni.', 'batter', 'd\xe2\x80\x99occhio', 'install\xc3\xb2', 'intero', 'harem', 'continue', 'bisbocce', 'gozzoviglie,', 'negli', 'intervalli', 'andava', 'giro', 'governatorato', 'piangere', 'lamentarsi', 'incontrava', 'abbandonato', 'ivanovna;', 'inoltre,', 'coniugale', 'coniuge', 'vergognato', 'menzionare.', 'sembrava', 'gratificasse', 'lusingasse', 'recitare', 'ridicola', 'oltraggiato,', 'arrivava', 'dipingere', 'forti', 'tinte', 'sventura.', '\xc2\xabverrebbe', 'abbiate', 'promozione,', 'apparite', 'soddisfatto,', 'dolore\xc2\xbb,', 'dicevano', 'prendevano', 'giro.', 'molti', 'addirittura', 'aggiungevano', 'mostrarsi', 'rinnovata', 'veste', 'buffone,', 'apposta,', 'ridere', 'pi\xc3\xb9,', 'fingeva', 'notare', 'comicit\xc3\xa0', 'situazione.', 'sa,', 'ingenuamente.', 'finalmente', 'riusc\xc3\xac', 'scoprire', 'tracce', 'fuggitiva.', 'poveretta', 'risult\xc3\xb2', 'trovarsi', 'pietroburgo,', 'dov\xe2\x80\x99era', 'approdata', 'seminarista', 'data', 'completa', 'emancipazione.', 'dette', 'raggiungere', 'nemmeno', 'lui', 'sapeva', 'bene', 'perch\xc3\xa9.', 'dire', 'partito,', 'preso', 'decisione', 'ritenne', 'avere', 'pieno', 'diritto,', 'farsi', 'po\xe2\x80\x99', 'coraggio', 'viaggio,', 'ubriacarsi', 'ritegno.', 'punto', 'ricevette', 'notizia', 'morte', 'quest\xe2\x80\x99ultima', 'pietroburgo.', 'morta,', 'soffitta,', 'all\xe2\x80\x99improvviso,', 'alcune', 'voci', 'tifo,', 'altre', 'fame.', 'apprese', 'ubriaco.', 'dice', 'messo', 'strada', 'levando', 'cielo', 'gioia,', 'gridasse:', '\xc2\xabora,', 'lascia', 'tuo', 'servo', 'vada', 'pace!\xc2\xbb.', 'altri,', 'singhiozzava', 'bambino,', 'forte,', 'guardarlo,', 'l\xe2\x80\x99avversione', 'suscitava.', 'pu\xc3\xb2', 'darsi', 'benissimo', 'vere', 'tutte', 'versioni,', 'cio\xc3\xa8,', 'rallegrasse', 'liberazione', 'piangesse', 'liberatrice.', 'generale', 'uomini,', 'farabutti,', 'ingenui', 'sempliciotti', 'generalmente', 'creda.', 'noi', 'pure,', 'resto.\n\n\nii', 'sbarazza', 'figlio\n\nnaturalmente', 'facile', 'figurarsi', 'educatore', 'padre', 'potesse', 'genere.', 'comportamento', 'quello', 'poteva', 'aspettare:', 'disinteress\xc3\xb2', 'maniera', 'assoluta', 'bambino', 'cattiveria', 'ragione', 'risentimento', 'coniugale,', 'semplicemente', 'dimenticato.', 'frattempo', 'importunava', 'lacrime', 'piagnistei', 'trasform\xc3\xb2', 'antro', 'depravazione;', 'fedele', 'casa,', 'grigorij,', 'prese', 'mitja,', 'soli', 'anni,', 'sotto', 'tutela', 'prendersi', 'cura', 'cambiato', 'camicina.', 'inoltre', 'che,', 'materni', 'parvero', 'essersi', 'dimenticati', 'nonno,', 'cio\xc3\xa8', 'signor', 'miusov,', 'tra', 'vivi;', 'nonna', 'rimasta', 'vedova', 'trasferitasi', 'mosca,', 'gravemente', 'malata,', 'sorelle', 'sposate,', 'anno', 'tocc\xc3\xb2', 'vivere', 'grigorij', 'abitare', 'nell\xe2\x80\x99izba', 'servit\xc3\xb9.', 'pap\xc3\xa0', '(difatti', 'ignorare', 'esistenza),', 'senz\xe2\x80\x99altro', 'rispedito', 'nell\xe2\x80\x99izba,', 'poich\xc3\xa9', 'd\xe2\x80\x99impedimento', 'nelle', 'gozzoviglie.', 'torn\xc3\xb2', 'parigi', 'cugino', 'defunta', 'p\xc3\xabtr', 'aleksandrovi\xc4\x8d', 'seguito', 'visse', 'all\xe2\x80\x99estero,', 'ancora', 'spiccava', 'miusov', 'cultura,', 'vissuto', 'capitale', 'all\xe2\x80\x99estero', 'gusti', 'europei', 'vita,', 'fine', 'diventato', 'liberale', '\xe2\x80\x9840', '\xe2\x80\x9850.', 'rapporti', 'liberali', 'epoca,', 'russia', 'conosceva', 'proudhon', 'bakunin', 'amava', 'particolar', 'modo', 'ricordare', 'raccontare,', 'oramai', 'pellegrinaggi,', 'giorni', 'rivoluzione', 'febbraio', '\xe2\x80\x9848', 'parigi,', 'alludendo', 'poco', 'agli', 'scontri', 'sulle', 'barricate.', 'ricordi', 'felici', 'giovinezza.', 'garantiva', 'indipendente,', 'circa', 'mille', 'anime', 'vecchie', 'misurazioni.', 'magnifica', 'tenuta', 'trovava', 'porte', 'cittadina', 'confinava', 'terre', 'rinomato', 'monastero,', 'aleksandrovi\xc4\x8d,', 'dagli', 'giovinezza,', 'l\xe2\x80\x99assegnazione', 'dell\xe2\x80\x99eredit\xc3\xa0,', 'intrapreso', 'interminabile', 'pesca', 'taglio', 'bosco,', 'so', 'precisione,', 'ritenuto', 'dovere', 'cittadino', 'illuminata', '\xe2\x80\x9cclericali\xe2\x80\x9d.', 'appreso', 'ricordava', 'interesse,', 'avendo', 'saputo', 'dell\xe2\x80\x99esistenza', 'egli,', 'sdegno', 'giovanile', 's\xe2\x80\x99immischi\xc3\xb2', 'faccenda.', 'occasione', 'incontr\xc3\xb2', 'pavlovi\xc4\x8d.', 'comunic\xc3\xb2', 'piedi', 'desiderato', 'occuparsi', 'dell\xe2\x80\x99educazione', 'bambino.', 'raccont\xc3\xb2', 'caratteristico,', 'parlare', 'l\xe2\x80\x99aria', 'capisce', 'stia', 'parlando', 'meraviglia', 'angolo', 'casa.', 'esagerato,', 'doveva', 'pur', 'qualcosa', 'vero.', 'realt\xc3\xa0,', 'am\xc3\xb2', 'fingere,', 'mettersi', 'all\xe2\x80\x99improvviso', 'inattesa', 'peggio,', 'alcun', 'motivo,', 'anzi', 'danno', 'persona,', 'presente', 'caso.', 'caratteristica,', 'tipica', 'grandissimo', 'numero', 'persone,', 'intelligenti,', 'condusse', 'faccenda', 'fervore', 'nominato', 'tutore', '(congiuntamente', 'pavlovi\xc4\x8d),', 'visto', 'madre', 'rimasti', 'piccola', 'tenuta,', 'podere.', 'trasfer\xc3\xac', 'grado,', 'sistemato', 'assicurato', 'redditi', 'propriet\xc3\xa0,', 'affrett\xc3\xb2', 'partire', 'periodo,', 'ecco', 'affid\xc3\xb2', 'zia', 'nobildonna', 'moscovita.', 'vivendo', 'permanentemente', 'dimentic\xc3\xb2', 'colp\xc3\xac', 'immaginazione', 'pot\xc3\xa9', 'dimenticare', 'vita.', 'moscovita', 'mor\xc3\xac', 'pass\xc3\xb2', 'figlie', 'maritate.', 'nido', 'quarta', 'volta.', 'star\xc3\xb2', 'dilungarmi', 'toccher\xc3\xa0', 'raccontare', 'primogenito', 'pavlovi\xc4\x8d;', 'limiter\xc3\xb2', 'informazioni', 'strettamente', 'necessarie', 'conto,', 'quali', 'impossibile', 'dare', 'romanzo.\nin', 'luogo,', 'figli', 'crescere', 'convinzione', 'possedere', 'patrimonio', 'raggiunto', 'maggiore', 'et\xc3\xa0,', 'indipendente.', 'un\xe2\x80\x99adolescenza', 'scapestrato:', 'termin\xc3\xb2', 'ginnasio,', 'iscrisse', 'scuola', 'militare,', 'and\xc3\xb2', 'finire', 'caucaso,', 'prest\xc3\xb2', 'servizio,', 'batt\xc3\xa9', 'duello,', 'degradato,', 'prestar', 'gozzovigli\xc3\xb2', 'parecchio', 'scialacqu\xc3\xb2', 'somma', 'relativamente', 'consistente.', 'cominci\xc3\xb2', 'ricevere', 'denaro', 'et\xc3\xa0', 'fino', 'contrasse', 'debiti.', 'conobbe', 'padre,', 'volta,', 'quand\xe2\x80\x99era', 'maggiorenne,', 'venne', 'dalle', 'nostre', 'parti', 'apposta', 'chiarire', 'questione', 'beni.', 'genitore', 'piacque', 'affatto;', 'trattenne', 'part\xc3\xac', 'furia', 'riuscito', 'spillargli', 'sommetta', 'accordo', 'all\xe2\x80\x99ulteriore', 'riscossione', 'proventi', '(fatto', 'nota)', 'sapere', 'reddito', 'valore.', 'accorse', 'occorre', 'tenerlo', 'mente)', 'un\xe2\x80\x99idea', 'sbagliata', 'esagerata', 'contento,', 'via', 'certi', 'calcoli', 'mente.', 'concluse', 'superficiale,', 'violento,', 'passionale,', 'insofferente,', 'scavezzacollo', 'bastato', 'arraffare', 'calmarsi,', 'breve', 'periodo.', 'sfruttare', 'cavava', 'piccole', 'elargizioni,', 'saltuari', 'invii', 'quattro', 'tardi,', 'persa', 'pazienza,', 'ricomparve', 'definire', 'genitore,', 'inaspettatamente,', 'meraviglia,', 'possedeva', 'bel', 'niente,', 'difficile', 'conti,', 'ricevuto', 'contanti', 'l\xe2\x80\x99intero', 'controvalore', 'genitore;', 'quest\xe2\x80\x99altro', 'affare,', 'intraprendere', 'quell\xe2\x80\x99altra', 'occasione,', 'esigere', 'via.', 'rimase', 'esterrefatto,', 'subodor\xc3\xb2', 'menzogna,', 'l\xe2\x80\x99inganno,', 'perse', 'controllo', 's\xc3\xa9.', 'circostanza', 'port\xc3\xb2', 'catastrofe', 'cui', 'esposizione', 'costituisce', 'l\xe2\x80\x99argomento', 'introduttivo', 'o,', 'meglio', 'esteriore.', 'passare', 'devo', 'fratelli', 'dove', 'venuti', 'fuori.\n\niii', 'letto\n\nsbarazzatosi', 'quattrenne', 'presto', 'spos\xc3\xb2', 'dur\xc3\xb2', 'otto', 'pesc\xc3\xb2', 'consorte,', 'sof', '\xe2\x80\x98ja', 'giovane,', 'passato', 'appalto', 'societ\xc3\xa0', 'ebreo.', 'sebbene', 'gozzovigliasse,', 'bevesse', 'desse', 'smetteva', 'investire', 'concludeva', 'successo', 'ovviamente,', 'scrupoli.', 'figlia', 'oscuro', 'diacono', 'orfana', 'dall\xe2\x80\x99infanzia;', 'cresciuta', 'benefattrice,', 'educatrice', 'despota,', 'l\xe2\x80\x99illustre', 'vegliarda', 'vorochov.', 'conosco', 'dettagli,', 'sentito', 'avevano', 'tolto', 'mite,', 'placida,', 'umile', 'educanda', 'cappio', 'appeso', 'chiodo', 'ripostiglio,', 'riusciva', 'sopportare', 'carattere', 'bisbetico', 'eterni', 'rimproveri', 'vecchia,', 'cattiva', 'tiranneggiava', 'intollerabilmente', 'prossimo', 'noia.', 'chiese', 'mano', 'ragazza,', 'raccolsero', 'cacciarono', 'matrimonio,', 'propose', 'fuga', 'all\xe2\x80\x99orfanella.', '\xc3\x88', 'molto,', 'probabile', 'stessa', 'mondo', 'conto.', 'accadeva', 'poi', 'capire', 'ragazzina', 'sedici', 'preferito', 'annegarsi', 'piuttosto', 'continuare', 'benefattrice?', 'poverina', 'cambi\xc3\xb2', 'benefattrice', 'benefattore.', 'ottenne', 'neanche', 'becco', 'quattrino', 'generalessa', 'mont\xc3\xb2', 'furie,', 'maledisse', 'entrambi;', 'programmato', 'ottenere', 'nulla,', 'sedotto', 'esclusivamente', 'dell\xe2\x80\x99innocente', 'soprattutto,', 'aria', 'innocente', 'fascino', 'particolare', 'lascivo', 'depravato', 'estimatore', 'volgare', 'femminile.', '\xc2\xabquegli', 'occhietti', 'innocenti', 'tagliarono', 'l\xe2\x80\x99anima', 'lama', 'rasoio\xc2\xbb,', 'solito', 'ghigno', 'ripugnante.', 'motivo', 'attrazione', 'lasciva.', 'alcuna', 'ricompensa,', 'fece', 'tante', 'cerimonie', 'sfruttando', 'ella,', '\xe2\x80\x9cin', 'torto\xe2\x80\x9d', 'dinanzi', '\xe2\x80\x9ctolta', 'cappio\xe2\x80\x9d', 'sfruttando,', 'mitezza', 'umilt\xc3\xa0', 'lei,', 'calpest\xc3\xb2', 'elementari', 'regole', 'decenza', 'matrimoniale.', 'presenza', 'c\xe2\x80\x99era', 'andirivieni', 'donne', 'malaffare', 'organizzavano', 'orge.', 'nota', 'caratteristica', 'moralista', 'cupo,', 'ottuso', 'testardo,', 'odiato', 'precedente', 'padrona', 'nuova', 'padrona,', 'difendeva', 'litigava', 'inammissibile', 'servo;', 'disperse', 'un\xe2\x80\x99orgia', 'svergognate', 'convenute.', 'disgraziata', 'donna,', 'vissuta', 'terrore', 'piccola,', 'specie', 'malattia', 'nervosa', 'femminile', 'riscontra', 'frequenza', 'popolino,', 'campagna,', 'male,', 'vengono', 'chiamate', 'klikusi.', 'malattia,', 'provocava', 'terribili', 'attacchi', 'isterici,', 'malata', 'perdeva', 'ragione.', 'diede', 'bambini,', 'aleksej:', 'tardi.', 'mor\xc3\xac,', 'possa', 'sembrare', 'serb\xc3\xb2', 'ricordo', 'sogno,', 's\xe2\x80\x99intende.', 'madre,', 'bambini', 'capit\xc3\xb2', 'praticamente', 'sorte', 'toccata', 'primo,', 'mitja:', 'furono', 'completamente', 'abbandonati', 'andarono', 'vissero', 'izba.', 'l\xc3\xac', 'trov\xc3\xb2', 'vecchia', 'dispotica', 'generalessa,', 'cresciuto', 'madre.', 'vivi', 'capace', 'l\xe2\x80\x99offesa', 'subita.', 'lunghi', 'dettagliate', 'notizie', '\xe2\x80\x9csophie\xe2\x80\x9d,', 'ammalata', 'dell\xe2\x80\x99ignominia', 'circondava,', 'parassiti', 'detto', 'voce:', '\xc2\xabben', 'sta,', 'dio', 'l\xe2\x80\x99ha', 'punita', 'ingratitudine\xc2\xbb.\nesattamente', 'mesi', 'sof\xe2\x80\x99ja', 'apparve', 'personalmente,', 'dritta', 'mezz\xe2\x80\x99oretta,', 'combin\xc3\xb2', 'belle.', 'sera.', 'rivisto', 'quegli', 'present\xc3\xb2', 'alticcio.', 'dicono', 'spiegazione,', 'appena', 'vide', 'assest\xc3\xb2', 'all\xe2\x80\x99istante', 'sonori', 'ceffoni', 'coi', 'fiocchi,', 'tir\xc3\xb2', 'ciuffo', 'capelli', 'dall\xe2\x80\x99alto', 'basso;', 'poi,', 'parola,', 'diresse', 'dai', 'bambini.', 'bast\xc3\xb2', 'un\xe2\x80\x99occhiata', 'accorgersi', 'lavati', 'biancheria', 'sporca;', 'bianco,', 'schiaffo', 'portato', 'entrambi', 'com\xe2\x80\x99erano,', 'avvolse', 'coperta,', 'sedere', 'carrozza', 'citt\xc3\xa0.', 'accett\xc3\xb2', 'schiavo', 'devoto,', 'profer\xc3\xac', 'accompagnava', 'signora', 'carrozza,', 'inchino', 'disse,', 'grave,', '\xc2\xabdio', 'l\xe2\x80\x99avrebbe', 'ricompensata', 'orfanelli\xc2\xbb.', '\xc2\xabma', 'tu', 'rimani', 'babbeo!\xc2\xbb,', 'gridato', 'allontanandosi.', 'considerato', 'l\xe2\x80\x99intera', 'faccenda,', 'trattava', 'buon', 'affare', 'consentendo', 'formalmente', 'affidare', 'l\xe2\x80\x99educazione', 'rifiut\xc3\xb2', 'sottostare', 'condizione.', 'schiaffi', 'l\xe2\x80\x99episodio', 'citt\xc3\xa0.\nsuccesse', 'poco,', 'testamento', 'disposto', 'testa', 'piccini', '\xc2\xabper', 'educazione', 'affinch\xc3\xa9', 'soldi', 'spesi', 'loro,', 'bastassero', 'sino', 'simile', 'elargizione', 'gente', 'qualcuno', 'voglia', 'sborsasse', 'lui\xc2\xbb', 'testamento,', 'conteneva', 'espresso', 'originale.', 'l\xe2\x80\x99erede', 'vecchietta,', 'rivel\xc3\xb2', 'onesta,', 'maresciallo', 'nobilt\xc3\xa0', 'governatorato,', 'efim', 'petrovi\xc4\x8d', 'polenov.', 'capito', 'all\xe2\x80\x99istante,', 'attraverso', 'scambio', 'lettere', 'cavato', 'l\xe2\x80\x99istruzione', 'stessi', '(sebbene', 'rifiutato', 'apertamente,', 'casi', 'tirava', 'lunghe,', 'lasciava', 'sentimentalismi),', 'orfani', 'affezion\xc3\xb2', 'famiglia.', 'prego', 'prendere', 'dall\xe2\x80\x99inizio.', 'giovani', 'dovevano', 'grati', 'ricevute,', 'petrovi\xc4\x8d,', 'generosit\xc3\xa0', 'umanit\xc3\xa0', 'incontrarsi.', 'lasciato', 'eredit\xc3\xa0', 'ragazzi,', 'toccarli,', 'giunti', 'trovassero', 'raddoppiato', 'interessi,', 'garant\xc3\xac', 'un\xe2\x80\x99istruzione', 'spese;', 'sicuramente', 'invest\xc3\xac', 'ciascuno', 'rubli.', 'dilungher\xc3\xb2,', 'dettagliato', 'infanzia', 'segnaler\xc3\xb2', 'circostanze', 'principali.', 'ivan,', 'cresceva', 'adolescente', 'tetro', 'chiuso', 'timido,', 'all\xe2\x80\x99et\xc3\xa0', 'dieci', 'crescevano', 'estranea', 'grazie', 'favori', 'ribrezzo', 'parlare,', 'ragazzo', 'presto,', '(almeno', 'dicevano),', 'rivelare', 'un\xe2\x80\x99attitudine', 'allo', 'studio', 'brillante', 'fuori', 'comune.', 'come,', 'esattezza,', 'separ\xc3\xb2', 'circa,', 'ginnasio', 'mosca', 'pensione', 'pedagogo', 'esperto', 'famoso,', 'amico', 'petrovi\xc4\x8d.', 'accaduto,', '\xc2\xaba', 'smania', 'buone', 'azioni\xc2\xbb', 'entusiasta', 'all\xe2\x80\x99idea', 'capacit\xc3\xa0', 'geniali', 'educato', 'istitutore', 'geniale.', 'geniale', 'vivi,', 'giovanotto,', 'terminato', 'all\xe2\x80\x99universit\xc3\xa0.', 'dato', 'disposizioni', 'chiare,', 'personale', 'tiranna', 'raddoppiata', 'interessi', 'rispetto', 'iniziali', 'tirata', 'lunghe', 'diverse', 'formalit\xc3\xa0', 'ritardi,', 'pertanto', 'primi', 'd\xe2\x80\x99universit\xc3\xa0', 'giovanotto', 'serie', 'ristrettezze', 'costretto,', 'provvedere', 'mantenimento', 'contemporaneamente', 'dedicarsi', 'studio.', 'volle', 'contatto', 'epistolare,', 'orgoglio,', 'confronti,', 'freddo', 'senso', 'suggeriva', 'paparino', 'vero', 'appoggio.', 'caso,', 'd\xe2\x80\x99animo', 'lavorare,', 'dapprima', 'lezioni', 'private', 'venti', 'copeche,', 'correndo', 'redazioni', 'giornali', 'consegnare', 'articoletti', 'righe', 'sugli', 'incidenti', 'stradali', 'firmati', '\xe2\x80\x9cun', 'testimone\xe2\x80\x9d.', 'scritti', 'stile', 'interessante', 'arguto', 'diventarono', 'popolari,', 'dimostr\xc3\xb2', 'superiorit\xc3\xa0,', 'pratica', 'intellettuale,', 'masse', 'studenti', 'sessi,', 'eternamente', 'bisognosi', 'sfortunati,', 'soliti', 'bazzicare', 'mattina', 'sera', 'presso', 'portoni', 'riviste', 'citt\xc3\xa0,', 'incapaci', 'escogitare', 'niente', 'solite', 'richieste', 'trascrizioni', 'traduzioni', 'francese.', 'entrato', 'redazioni,', 'contatti', 'esse,', 'ultimi', 'universit\xc3\xa0', 'pubblicare', 'recensioni', 'promettenti', 'libri', 'dedicati', 'disparati', 'argomenti', 'specialistici,', 'conquistare', 'certa', 'notoriet\xc3\xa0', 'circoli', 'letterari.', 'comunque,', 'nell\xe2\x80\x99ultimo', 'periodo', 'casualmente', 'attirare', 'un\xe2\x80\x99attenzione', 'improvvisa', 'cerchia', 'gran', 'lunga', 'vasta', 'lettori,', 'moltissime', 'notarono', 'impressero', 'curiosa.', 'studi', 'universitari', 'accingeva', 'l\xe2\x80\x99estero', 'duemila', 'pubblic\xc3\xb2,', 'importanti,', 'articolo', 'attir\xc3\xb2', 'l\xe2\x80\x99attenzione', 'addetti', 'lavori,', 'proposito', 'argomento', 'essergli', 'familiare,', 'laureato', 'scienze', 'naturali.', 'l\xe2\x80\x99articolo', 'riguardava', 'dibattuta', 'dovunque', 'periodo:', 'tribunali', 'ecclesiastici.', 'esame', 'opinioni', 'espresse', 'merito,', 'espose', 'opinione.', 'ci\xc3\xb2', 'colpiva', 'maggiormente', 'quell\xe2\x80\x99articolo', 'tono', 'singolare', 'conclusione.', 'intanto,', 'clericali', 'fermamente', 'convinti', 'l\xe2\x80\x99autore', 'loro.', 'eppure,', 'accanto', 'quelli,', 'cominciarono', 'applaudire', 'sostenitori', 'civili', 'atei.', 'fin', 'perspicaci', 'decretarono', 'farsa', 'irriverente,', 'presa', 'menziono', 'penetr\xc3\xb2', 'tempestivamente', 'monastero', 'ecclesiastici', 'riscuoteva', 'largo', 'interesse;', 'produsse', 'caotica', 'confusione.', 'nome', 'dell\xe2\x80\x99autore,', 'interesse', 'nativo', '\xc2\xabproprio', 'pavlovi\xc4\x8d\xc2\xbb.', 'carne', 'ossa', 'vivo', 'parti.\nper', 'venuto', 'noi?', 'ponevo', 'inquietudine.', 'spiegarmi', 'all\xe2\x80\x99ultimo,', 'visita', 'fatale,', 'passo', 'portata.', 'istruito,', 'dall\xe2\x80\x99aria', 'orgogliosa', 'avveduta,', 'comparisse', 'indecorosa,', 'stampo,', 'ignorato,', 'incontrato', 'degnato', 'attenzione', 'denaro,', 'glielo', 'chiesto,', 'temuto', 'figli,', 'potessero', 'venire', 'giorno', 'chiedergli', 'soldi.', 'stabilisce', 'tal', 'fatta,', 'vive', 'mese', 'altro,', 'vanno', 'd\xe2\x80\x99amore', 'd\xe2\x80\x99accordo,', 'immaginare.', 'quest\xe2\x80\x99ultimo', 'meravigli\xc3\xb2', 'me,', 'altri.', 'parlato', 'prima,', 'lontano', 'parente', 'visitare', 'soggiorno', 'definitivamente', 'stabilito.', 'meravigliarsi', 'dest\xc3\xb2', 'intenso', 'dispiacere,', 'parecchi', 'battibecchi', 'intellettuali.', '\xc2\xabegli', 'orgoglioso\xc2\xbb,', 'diceva', '\xc2\xabsapr\xc3\xa0', 'procurarsi', 'necessari', 'serve', 'stare', 'qui?', 'chiaro', 'glieli', 'darebbe.', 'ama', 'bere', 'bagordi,', 'intanto', 'vecchio', 'd\xe2\x80\x99accordo!\xc2\xbb.', 'verit\xc3\xa0,', 'palese', 'influenza', 'vecchio;', 'dargli', 'ascolto,', 'perfidamente,', 'capriccioso;', 'comportarsi', 'decente...\n']
"""
	
