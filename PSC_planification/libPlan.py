#-------------------------------------------------------------------------------
print "Chargement de la librairie de definition de problemes de planification"
print "\t@version: 3.0  date: 10/06/2008 modified by Thomas Leaute"
print "\t@version: 2.1  date: 28/06/2007 modified by Thomas Leaute"
print "\t@version: 2.0  date: 03/05/2007 modified by Thomas Leaute"
print "\t@version: 1.1  date: 02/05/2007 modified by Thomas Leaute"
print "\t@version: 1.0  date: 05/03/2007 created by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 05/03/2007"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------
import libPSC
import PSC

## Un operateur de planification 
class Operateur:

	## \var nom 
	# Le nom de l'operateur 
	
	## \var preconditions 
	# Liste des preconditions de l'operateur

	## \var postconditions 
	# Liste des postconditions de l'operateur (qui doivent etre vraies apres son execution) 

	##Constructeur
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] str Chaine de caracteres representant l'operateur 
	# @param[in] pre Liste de preconditions de type Proposition
	# @param[in] post Liste de postconditions de type Proposition
	def __init__(self, str, pre, post):
		self.nom = str
		self.preconditions = pre
		self.postconditions = post

	## Retourne si la proposition passee en parametre est une precondition
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop Proposition dont on veut savoir si elle est une precondition 
	def aPourPrecondition (self, prop):
		return prop in self.preconditions
	
	## Retourne la liste des preconditions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retournePreconditions (self):
		return self.preconditions

	## Retourne si la proposition passee en parametre est une postcondition
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop Proposition dont on veut savoir si elle est une postcondition 
	def aPourPostcondition (self, prop):
		return prop in self.postconditions

	## Retourne la liste des postconditions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retournePostconditions (self):
		return self.postconditions

	## retourne une representation en String
	# @param[in] self reference automatique sur l'objet qui execute cette methode	
	def __repr__(self):
		return self.nom
	

## Cette classe represente un probleme de planification, avec des propositions, des operateurs, des conditions initiales et finales, et des mutex de propositions
class ProblemeDePlanification: 

	## \var operateurs 
	# Liste d'operateurs de planification
	
	## \var propositions 
	# Liste de propositions de planification
	
	## \var condIni 
	# Liste de conditions initiales de la forme [ [prop1, bool1], [prop2, bool2], ... ]
	
	## \var condFin 
	# Liste de conditions finales de la forme [ [prop1, bool1], [prop2, bool2], ... ]
	
	## \var mutexDeProp 
	# Liste des mutex entre paires de propositions 
	
	## \var mutexDOperateurs 
	# Liste des mutex entre paires d'operateurs  
	
	## Constructeur
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def __init__ (self):
		self.operateurs = []
		self.propositions = []
		self.condIni = []
		self.condFin = []
		self.mutexDeProp = []
		self.mutexDOperateurs = []
	
	## Ajoute un operateur de planification
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] op Operateur a ajouter
	def ajouteOperateur (self, op):
		self.operateurs.append(op)

	## Retourne la liste d'operateurs
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneOperateurs (self):
		return self.operateurs 
		
	## Ajoute une proposition de planification
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop Proposition a ajouter
	def ajouteProposition (self, prop):
		self.propositions.append(prop)
	
	## Retourne la liste de propositions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retournePropositions (self):
		return self.propositions 
		
	## Ajoute une condition initiale
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop Proposition sur laquelle porte la condition initiale
	# @param[in] bool Valeur booleenne que doit prendre la Proposition au debut du plan
	def ajouteConditionInitiale (self, prop, bool):
		self.condIni.append([prop, bool])
	
	## Retourne les conditions initiales 
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneConditionsInitiales (self):
		return self.condIni

	## Ajoute une condition finale
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop Proposition sur laquelle porte la condition finale
	# @param[in] bool Valeur booleenne que doit prendre la Proposition a la fin du plan
	def ajouteConditionFinale (self, prop, bool):
		self.condFin.append([prop, bool])

	## Retourne les conditions finales 
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneConditionsFinales (self):
		return self.condFin

	## Ajoute un mutex entre deux propositions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop1 Premiere Proposition
	# @param[in] prop2 Deuxieme Proposition
	def ajouteMutexDePropositions (self, prop1, prop2): 
		self.mutexDeProp.append([prop1, prop2])

	## Retourne les mutex entre paires de propositions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneMutexDePropositions (self): 
		return self.mutexDeProp

	## Ajoute un mutex entre deux operateurs
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] op1 Premier Operateur
	# @param[in] op2 Deuxieme Operateur
	def ajouteMutexDOperateurs (self, op1, op2): 
		self.mutexDOperateurs.append([op1, op2])

	## Retourne les mutex entre paires d'operateurs
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneMutexDOperateurs (self): 
		return self.mutexDOperateurs

	## Affiche la liste des propositions et des operateurs, les conditions initiales et finales, et les mutex de propositions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def __repr__(self):
		out = "\nProbleme de planification :\n"
		out += "Propositions : " + str(self.propositions) + "\n"
		out += "Operateurs :" + str(self.operateurs) + "\n"
		out += "Conditions initiales :" + str(self.condIni) + "\n"
		out += "Conditions finales :" + str(self.condFin) + "\n"
		out += "Mutex de propositions :" + str(self.mutexDeProp) + "\n"
		out += "Mutex d'operateurs :" + str(self.mutexDOperateurs) + "\n"
		return out
	
