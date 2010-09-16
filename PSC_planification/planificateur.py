#-------------------------------------------------------------------------------
print "Chargement de l'algorithme de planification par PSC"
print "\t@version: 3.0  date: 07/06/2008 modified by Thomas Leaute"
print "\t@version: 2.3  date: 31/03/2008 modified by Thomas Leaute"
print "\t@version: 2.2  date: 28/06/2007 modified by Thomas Leaute"
print "\t@version: 2.1  date: 04/05/2007 modified by Thomas Leaute"
print "\t@version: 2.0  date: 03/05/2007 modified by Thomas Leaute"
print "\t@version: 1.1  date: 02/05/2007 modified by Thomas Leaute"
print "\t@version: 1.0  date: 05/03/2007 created by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 05/03/2007"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------
import copy
import libPSC
import PSC
import libPlan


## contiennent les variables et les contraintes
VARS = PSC.Variables()
CONTS = PSC.Contraintes()

## contient la liste de tous les etats
ETATS = []


## Une contrainte d'axiome de cadre pour un etat et une proposition donnes
class ContrainteAxiomeCadre (libPSC.Contrainte):
	
	## \var varPre 
	# Variable correspondant a la proposition au debut de l'etat
	
	## \var varPost 
	# Variable correspondant a la proposition a la fin de l'etat
	
	## \var varsOp
	# Liste de variables d'operateurs ayant la proposition representee par \a varPost comme postcondition
	
	## Constructeur de la classe
	# 
	# La contrainte est la suivante : 
	# SI (\a varPre = \c False ET \a varPost = \c True) 
	# ALORS au moins une des variables dans \a varsOp est \c True
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] varPre variable correspondant a la proposition au debut de l'etat
	# @param[in] varsOp liste de variables d'operateurs ayant la proposition representee par \a varPost 
	#					comme postcondition
	# @param[in] varPost variable correspondant a la proposition a la fin de l'etat
	def __init__( self, varPre, varsOp, varPost ):
		libPSC.Contrainte.__init__(self, [varPre.nom, varPost.nom] + [ varOp.nom for varOp in varsOp ])
		self.varPre = varPre
		self.varsOp = varsOp
		self.varPost = varPost

	# Retourne la dimension de la contrainte
	def dimension( self ):
		return len( self.varsOp ) + 2

	# Teste si la contrainte est valide et respectee par les valeurs des variables qui la composent.
	def estValide( self, var, val ):
	
		# incremente le nombre de contraintes visitees
		libPSC.NBCONTRAINTES += 1
		
		# sauvegarde la valeur de la variable val avant de la modifier
		valeur = var.valeur
		var.metAJourValeur(val)
		
		valide = False
		
		# Si au moins une des variables n'est pas encore instanciee, retourne True
		for var2 in [ self.varPre, self.varPost ] + self.varsOp:
			if var2.valeur == None:
				valide = True
				break
		
		# Si toutes les variables sont intanciees, verifie que la contrainte est satisfaite
		if not valide:
		
			# Verifie si la proposition passe de False a True
			if self.varPre.valeur == False and self.varPost.valeur == True:
				
				# Verifie si au moins un des operateurs est applique
				for varOp in self.varsOp:
					if varOp.valeur == True:
						valide = True
						break
				
			else:
				valide = True
			
		# annule le changement de valeur de la variable var et retourne
		var.metAJourValeur(valeur)
		return valide
	
	
	## Propage l'assignation d'une variable de la contrainte aux autres variables non instanciees
	#
	# Etant donne qu'on a fixe une valeur pour une variable de cette contrainte, 
	# on essaie de reduire le label des autres en supprimant les valeurs inconsistantes. 
	#
	# Propagation paresseuse : appliquee seulement s'il ne reste qu'une variable non instanciee
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] var la variable qui vient d'etre instanciee
	# @return True si apres propagation, la contrainte est toujours consistante
	def propage ( self, var ):
		
		# Obtient la derniere variable non encore instanciee
		derniereVar = None
		for var2 in [ self.varPre, self.varPost ] + self.varsOp:
			if var2.valeur == None:
				if derniereVar == None:
					derniereVar = var2
				else:
					# Il reste plus d'une variable non instanciee
					return True
		
		# utilise le label de la variable derniereVar
		for l in derniereVar.label[:]:

			#verifie que la contrainte est satisfaite
			if not self.estValide( derniereVar, l ):
				# on enleve la valeur l du label
				derniereVar.enleveDuLabel(l)
		
		# la consistance est possibe <=> il reste au moins une valeur dans le label
		return len(derniereVar.label) > 0

		
	## L'algorithme REVISER n'est pas defini pour des contraintes n-aires
	def reviser ( self ):
		return False
	
	# Retourne une representation textuelle des donnees de la classe
	def __repr__(self):
		str = "Axiome de cadre : %s = False \t/\t %s \t/\t %s = True" % (self.varPre.nom, [ varOp.nom for varOp in self.varsOp ], self.varPost.nom)
		return str		


## Cette classe represente un etat de planification
#
# Un etat contient une liste de propositions utilisees comme pre- et postconditions, et une liste d'operateurs	
class Etat:

	## \var varInitiales 
	# dictionnaire { nom de proposition : variable de proposition }

	## \var varFinales 
	# dictionnaire { nom de proposition : variable de proposition }
	
	## \var varOperateurs 
	# dictionnaire { nom de l'operateur : variable d'operateur }

	## \var no_etat 
	# numero de cet etat
	
	## constructeur
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param no_etat le numero de l'etat [0,PlanificateurPSC.nb_etats)
	# @param props La liste des propositions de planification 
	# @param ops La liste des operateurs de planification 
	def __init__(self, no_etat, props, ops):
		self.no_etat=no_etat
		self.varInitiales = {}
		self.varFinales = {}
		self.varOperateurs = {}
		self.construitVariablesOperateurs(ops)
		self.construitVariablesPropositions(props)

	##construit une action
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param ops La liste des operateurs de planification 
	def construitVariablesOperateurs(self, ops):
		for op in ops:
			var = libPSC.Variable(op.nom + " etat " + str(self.no_etat), [True, False])
			self.varOperateurs[op.nom] = var
			VARS.ajouteVar(var)

	##construit toutes les propositions et les ajoute aux dictionnaires varInitiales et varFinales
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param props La liste des propositions de planification 
	def construitVariablesPropositions(self, props):
		if self.no_etat>0:
			self.varInitiales = ETATS[self.no_etat-1].varFinales
		for prop in props:
			var = libPSC.Variable(prop + " etat " + str(self.no_etat+1), [True, False])
			VARS.ajouteVar(var)
			self.varFinales[prop] = var
			if self.no_etat == 0:
				var = libPSC.Variable(prop + " etat 0", [True, False])
				VARS.ajouteVar(var)
				self.varInitiales[prop] = var

	## Retourne la liste des variables de propositions initiales 
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneVarInitiales(self):
		return self.varInitiales.values()

	## Retourne la variable initiale correpondant a la Proposition passee en parametre
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop Proposition dont on veut la variable initiale
	def retourneVarInitiale(self, prop):
		return self.varInitiales[prop]

	## Retourne la liste des variables de propositions finales 
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneVarFinales(self):
		return self.varFinales.values()

	## Retourne la variable finale correpondant a la Proposition passee en parametre
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prop Proposition dont on veut la variable finale
	def retourneVarFinale(self, prop):
		return self.varFinales[prop]

	## Retourne la liste des operateurs 
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def retourneOperateurs(self):
		return self.varOperateurs.values()

	## Retourne la variable correspondant a l'operateur passe en parametre
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] op l'operateur
	def retourneVarOperateur(self, op):
		return self.varOperateurs[op.nom]

	## Retourne une representation en str
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def __str__(self):
		strr = "Etat "+str(self.no_etat)+"\n"
		strr += "\t Propositions initiales :\n"
		for var in self.retourneVarInitiales():
			strr+="\t\t"+str(var)+"\n"
		
		strr += "\t Operateurs :\n"
		for op in self.retourneOperateurs():
			strr+="\t\t"+str(op)+"\n"

		strr += "\t Propositions finales :\n"
		for var in self.retourneVarFinales():
			strr+="\t\t"+str(var)+"\n"
			
		return strr
		 
		 
## La classe representant le planning par modelisation PSC
class PlanificateurPSC:

	## \var probleme 
	# Le probleme de planification a resoudre

	## \var nb_etats 
	# Le nombre d'etats dans le plan, c'est a dire la longeur du plan
	
	## constructeur
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	# @param[in] prob Le probleme de planification 
	# @param[in] nb_etats nombre d'etats
	def __init__(self, prob, nb_etats):
		self.probleme = prob
		self.nb_etats=nb_etats
		del ETATS[:]
		
	## construit tous les etats de la planification
	# Quand cette methode retourne, la liste globale ETATS doit etre rangee par ordre croissant du numero d'etat. 
	# @param[in] self reference automatique sur l'objet qui execute cette methode			
	def contruitEtats(self):
		print "|+|Construction des Etats "
		for i in range(0,self.nb_etats):
			print "\tConstruction de l'etat : "+str(i)
			etat= Etat(i, self.probleme.retournePropositions(), self.probleme.retourneOperateurs())
			ETATS.append(etat)

	## Implemente les contraintes de mutex de propositions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def implementeMutexDePropositions (self): 
		for mutex in self.probleme.retourneMutexDePropositions():
			for etat in ETATS:
				CONTS.ajouteContrainte( libPSC.ContrainteBinaire(etat.retourneVarInitiale(mutex[0]), "NAND", etat.retourneVarInitiale(mutex[1])) )
				if etat.no_etat==(self.nb_etats-1):
					CONTS.ajouteContrainte( libPSC.ContrainteBinaire(etat.retourneVarFinale(mutex[0]), "NAND", etat.retourneVarFinale(mutex[1])) )
		
	## Implemente les contraintes de mutex d'operateurs
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def implementeMutexDOperateurs (self): 
		for mutex in self.probleme.retourneMutexDOperateurs():
			for etat in ETATS:
				CONTS.ajouteContrainte( libPSC.ContrainteBinaire(etat.retourneVarOperateur(mutex[0]), "NAND", etat.retourneVarOperateur(mutex[1])) )
		
	## Implemente les contraintes correspondant aux conditions initiales et finales:
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def implementeConditionsInitialesEtFinales (self):
		for cond in self.probleme.retourneConditionsInitiales():
			var = ETATS[0].retourneVarInitiale(cond[0])
			CONTS.ajouteContrainte( libPSC.ContrainteUnaire(var, "==", cond[1]) )
		for cond in self.probleme.retourneConditionsFinales():
			var = ETATS[self.nb_etats-1].retourneVarFinale(cond[0])
			CONTS.ajouteContrainte( libPSC.ContrainteUnaire(var, "==", cond[1]) )
			
	## Implemente les contraintes de pre- et postconditions
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def implementePreEtPostconditions(self):
		for et in ETATS:
			for op in self.probleme.retourneOperateurs():
				for pre in op.retournePreconditions():
					CONTS.ajouteContrainte( libPSC.ContrainteBinaire(et.retourneVarOperateur(op), "->", et.retourneVarInitiale(pre)) )
				for post in op.retournePostconditions():
					CONTS.ajouteContrainte( libPSC.ContrainteBinaire(et.retourneVarOperateur(op), "->", et.retourneVarFinale(post)) )
						
	## ajoute les contraintes d'axiomes de cadre
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def implementeAxiomesDeCadre (self):
		for et in ETATS:
			for prop in self.probleme.retournePropositions():
				
				# Genere la liste des variables d'operateurs qui ont prop comme postcondition
				varsOp = [ et.retourneVarOperateur(op) for op in self.probleme.retourneOperateurs() 
														if op.aPourPostcondition(prop) ]
				
				c = ContrainteAxiomeCadre( et.retourneVarInitiale(prop), varsOp, et.retourneVarFinale(prop) )
				CONTS.ajouteContrainte(c)
				

	## Implemente le PSC a partir du probleme de planification
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def implementePSC (self):
		self.contruitEtats()
		afficheEtats()
		self.implementeMutexDePropositions()
		self.implementeMutexDOperateurs()
		self.implementeConditionsInitialesEtFinales()
		self.implementePreEtPostconditions()
		self.implementeAxiomesDeCadre()
		

	## Affiche les variables et les contraintes	   
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def affichePSC(self):
		print VARS.__repr__()
		print CONTS.__repr__()
		afficheNombreVarsEtContraintes()
	
	## Trouve la solution en utilsant le Forward Checking
	# @param[in] self reference automatique sur l'objet qui execute cette methode
	def trouveLaSolution(self):
		
		# consistance des noeuds + arcs
		print "|+| Fait la consistance des noeuds"
		VARS.consistanceDesNoeuds()
		print "|+| Fait la consistance des arcs"
		CONTS.consistanceDesArcs()
		afficheEtats()

		afficheNombreVarsEtContraintes()
		print "|+| Applique l'heuristique Variable Ordering"
		PSC.variableOrdering()
		
		print "|+| Applique le Forward Checking"
#		sol = PSC.backtrack(0, False)
		sol = PSC.forwardChecking(0, False, True)
		if sol!=PSC.ECHEC:
			afficheUneSolutionPossible()
		else:
			print "|-| Aucune solution trouvee"


## Affiche la solution trouvee
def afficheUneSolutionPossible():
	print "|+| Solution trouvee:=\n"
	for et in ETATS:
		print et
			
## Affiche les etats
def afficheEtats():
	for et in ETATS:
		print et

## Affiche le nombre de Variabless et de Contraintes
def afficheNombreVarsEtContraintes():
	print "|+| Nombre de Variables :"+str(VARS.retourneNbVars())
	print "|+| Nombre de Contraintes	:"+str(CONTS.retourneNbContraintes())
	
exec file("missionnaires.py")
