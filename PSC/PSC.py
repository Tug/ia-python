## \file PSC.py
# \brief Module implementant l'algorithme du backtracking 
#		pour la resolution des problemes de contraintes
# \package PSC
# \brief Module implementant l'algorithme du backtracking 
#		pour la resolution des problemes de contraintes
#
# Chaque algorithme utilise les methodes de consistance pour eviter
# d'avoir des instanciations de valeurs qui ne sont pas compatibles
# avec les contraintes. Pour plus de details sur le fonctionnement
# des PSC, lire le chapitre 8 du livre.
#
# @see Chapitre 8 du livre

#-------------------------------------------------------------------------------
print "Chargement du module PSC"
print "\t@version: 2.0  date: 06/06/2008 modified by Thomas Leaute"
print "\t@version: 1.5  date: 28/03/2008 modified by Thomas Leaute"
print "\t@version: 1.4  date: 28/06/2007 modified by Thomas Leaute"
print "\t@version: 1.3  date: 14/02/2007 modified by Vincent Schickel"
print "\t@version: 1.2  date: 17/01/2007 modified by Bruno Alves"
print "\t@version: 1.1  date: 24/04/2006 modified by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 24/04/2006"
print "\t@copyright: EPFL-IC-IIF-LIA 2006-2007"
#-------------------------------------------------------------------------------

# modules utilises
import libPSC
import copy

## Liste de toutes les variables
VARIABLES=[]

## Liste de toutes les contraintes
CONTRAINTES=[]

## Constante retournee en cas d'echec
ECHEC='echec'

## Contient le nombre d'iterations de l'algorithme
ITERATIONS = 0

## Liste des solutions de l'algorithme
SOLUTIONS=[]


## Verifie si chaque contrainte portant sur la variable k et sur au moins une des variables
## precedentes dans PSC.VARIABLES est satisfaite
#
# @param[in] k position actuelle dans PSC.VARIABLES 
def consistanceAvecVarsPrecedentes ( k ):

	# pour chaque contrainte portant sur la variable k: 
	for c in CONTRAINTES:
		if VARIABLES[k].nom in c.vars:
		
			# si la contrainte porte aussi sur une variable precedente:
			for i in range(0, k):
				if VARIABLES[i].nom in c.vars:
				
					# si la contrainte est valide, passe a la suivante
					if c.estValide( VARIABLES[k], VARIABLES[k].valeur ):
						break
					else:
						return False
	
	# toutes les contraintes sont valides
	return True


## Affiche la solution avec quelques informations utiles
#
# Affiche tout simplement la solution en indiquant le nom de l'algorithme
# utilise, le nombre d'iterations qui ont ete necessaires pour arriver
# a la solution, le nombre de contraintes visitees et enfin, la solution
# elle-meme.
#
# @param[in] algo le nom de l'algorithme de recherche utilise
# @param[in] solution la solution trouvee jusqu'a present
def afficheSolution( algo, solution ):
	print "\t", algo, ": SOLUTION TROUVEE en", ITERATIONS, "etapes et avec", libPSC.NBCONTRAINTES, "contraintes verifiees;", "SOLUTION=", solution


## Affiche le nombre d'iterations ainsi que quelques informations utiles
#
# Affiche le nombre d'iterations avec des informations supplementaires sur
# l'algorithme utilise et la profondeur de recheche actuelle.
#
# @param[in] algo le nom de l'algorithme de recherche utilise
# @param[in] k la profondeur actuelle a laquelle on se trouve
def afficheNbIterations( algo, k ):
	print algo, ": Iteration:=", ITERATIONS, ", profondeur actuelle:=", k,"et", libPSC.NBCONTRAINTES, "contraintes verifiees"



## Classe gerant la liste des variables PSC.VARIABLES
#
# Cette classe est une sorte de wrapper pour l'object PSC.VARIABLES facilitant
# la manipulation de celui-ci. Les fonctions disponibles peuvent ajouter
# ou obtenir une variables donnee. D'autres fonctions avancees permettent
# d'appliquer la consistance des noeuds a toutes les variables ou d'initialiser
# une instance des variables presentes.
class Variables:

	## Constructeur de classe
	#
	# Initialise le tableau de variables en l'effacant.
	#
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode.
	def __init__( self ):
		del VARIABLES[:]


	## Retourne une variable d'apres son nom
	#
	# Retourne une variable dont le nom correspond au nom passe en parametre.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] nom le nom de la variable que l'on cherche
	# @return une reference a la variable recherchee si celle-ci existe, \c None sinon
	def retourneVar( self, nom ):
		for var in VARIABLES:
			if var.nomEstEgal( nom ):
				return var
		return None


	## Ajoute une nouvelle variable a la liste des variables
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] var la variable a ajouter dans la liste
	def ajouteVar( self, var ):
		VARIABLES.append( var )


	## Applique la consistance des noeuds
	#
	# Cette methode applique la consistance des noeuds pour chaque
	# variable de la liste. 
	# La methode de consistance consiste a supprimer du domaine toutes les
	# valeurs qui violent les contraintes unaires. Pour cela, il suffit d'iterer
	# sur la liste des contraintes unaires, et verifier si chacune est verifiee 
	# par toutes les valeurs possibles de la variable sur laquelle elle porte. 
	# Dans le cas contraire, cette valeur est supprimee du domaine. 
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @see Chapitre 8.5.1 du livre
	# @warning lors de l'iteration des valeurs du domaine, il faut bien
	#		  faire \b attention a iterer sur une copie du domaine, car
	#		  on ne peut pas supprimer des valeurs d'une liste et continuer
	#		  a iterer sur celle-ci
	def consistanceDesNoeuds( self ):
	
		# pour chaque contrainte unaire
		for c in CONTRAINTES:
			if c.dimension() == 1:
			
				# pour chaque valeur du domaine de la variable
				for d in c.refVar.domaine[:]:
	
					# si la contrainte n'est pas satisfaite, supprime la valeur
					if not c.estValide( c.refVar, d ) :
						c.refVar.domaine.remove(d)
													
	
	## Retourne le nombre de variables
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def retourneNbVars(self):
		return len(VARIABLES)

	## Retourne une representation textuelle des donnees des variables
	#
	# Retourne une representation de toutes les variables ajoutees dans la
	# liste PSC.VARIABLES. Le format d'affichage est:
	#
	# @code
	# Vars:
	#   var1.__repr__()
	#   var2.__repr__()
	#   ...
	#   varn.__repr__()
	# @endcode
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @return une chaine de caracteres contenant une representation de la classe
	def __repr__( self ):
		str = "Vars:\n"
		for var in VARIABLES:
			str += "\t" + var.__repr__() + "\n"
		return str


## Classe gerant la liste des contraintes PSC.CONTRAINTES
#
# Cette classe assure la gestion de la liste PSC.CONTRAINTES. Pour assurer la
# consistance, cette classe propose des methodes pour acceder aux contraintes,
# mais aussi pour appliquer la consistance des arcs a chacune.
class Contraintes:

	## Constructeur de la classe
	#
	# Initialise la liste des contraintes PSC.CONTRAINTES
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def __init__( self ):
		del CONTRAINTES[:]


	## Ajoute une contrainte dans la liste des contraintes
	#
	# Ajoute la contrainte passee en parametre dans PSC.CONTRAINTES.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] c la contrainte que l'on cherche a ajouter
	def ajouteContrainte( self, c ):
		CONTRAINTES.append(c)


	## Applique la consistance des arcs
	#
	# Cette methode est une application directe de l'algorithme REVISER
	# vu en cours. Sa base theorique prend en compte le fait que pour une
	# valeur v du domaine de xi, il se peut qu'il n'y ait pas de valeur
	# dans le domaine qui soit consistante avec les contraintes en xi et xj. Dans ce cas,
	# l'algorithme REVISER supprime v de xi. Cependant, l'appliquer une fois
	# ne suffit pas. En effet, il se peut, comme cet algorithme modifie le domaine de xi,
	# que cette modification entraine l'inconsistance avec d'autres contraintes etant valides dans le passe.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @note Regarder le chapitre 8.5.2 du cours pour de plus amples informations
	# sur le fonctionnement de l'algorithme de Waltz et REVISER
	def consistanceDesArcs( self ):
		refaire=False
		for c in CONTRAINTES:
			if c.dimension()==2 and c.reviser():
				refaire = True
		if refaire:
			self.consistanceDesArcs()
			
	## Retourne le nombre de contraintes
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def retourneNbContraintes(self):
		return len(CONTRAINTES)
	
	
	## Retourne une representation textuelle des donnees des contraintes
	#
	# Retourne une representation des toutes les contraintes ajoutees dans la
	# liste PSC.CONTRAINTES. Le format d'affichage est:
	#
	# @code
	# Contraintes:
	#   c1.__repr__()
	#   c2.__repr__()
	#   ...
	#   cn.__repr__()
	# @endcode
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @return une chaine de caracteres contenant une representation de la classe
	def __repr__( self ):
		str = "Contraintes:\n"
		for c in CONTRAINTES:
			str += "\t1. "+ c.__repr__() + "\n"
		return str


## Algorithme de backtracking simple
#
# Le principe de l'algorithme est de tenter d'assigner une valeur a chaque variable
# dans la liste PSC.VAR. A chaque assignation, on verifie que toutes le contraintes
# liant la variable courante avec les variables deja instanciees sont satisfaites. 
# Sinon, on procede a un backtrack pour essayer une autre valeur. 
#
# @param[in] k la profondeur de la recherce (commence a 0)
# @param[in] toutesLesSolutions si \b True alors cherche TOUTES les solutions,
#			sinon s'arrete a la premiere (valeur par defaut)
# @param[in] initialise initialise les variables globales ITERATIONS et SOLUTIONS
# @return instances contenant la solution \e ou echec si aucune solution trouvee
# @see Chapitre 8.4.1 du livre
def backtrack( k, toutesLesSolutions=None, initialise=None ):

	# l'algorithme utilise est le backtracking
	algo="bt"

	# variables globales
	global ITERATIONS
	global SOLUTIONS

	# faut-il ajouter toutes les solutions ?
	if toutesLesSolutions==None:
		toutesLesSolutions=False

	# faut-il initialiser les variables ?
	if initialise==None or initialise==True:
		ITERATIONS=0
		SOLUTIONS=[]
		libPSC.NBCONTRAINTES=0
		initialise=False

	# incremente le nombre d'iterations et affiche les
	# informations du nombre de noeuds visites, etc...
	ITERATIONS += 1;
	afficheNbIterations( algo, k )

	# si k>nombre-variables, alors on a une solution
	# a la profondeur ou l'on se trouve.
	if k >= len(VARIABLES):

		# affiche la solution et l'ajoute dans la liste SOLUTIONS
		solution = {}
		for var in VARIABLES:
			solution[var.nom] = var.valeur
		afficheSolution( algo, solution )
		SOLUTIONS.append( solution )

		# s'il ne faut pas garder toutes les solutions, on peut
		# quitter l'algorithme a cette etape. La recursion sera
		# deroulee et l'algorithme termine.
		if not toutesLesSolutions:
			return SOLUTIONS

	# sinon, il faut continuer la recherche
	else:

		# obtient la k-ieme variable
		var = VARIABLES[k]

		# pour chaque valeur du domaine...
		for d in var.domaine:

			# ... teste la variable avec la valeur d
			var.metAJourValeur(d)

			# verifie si cette valeur d est consistante avec 
			# toutes les contraintes portant sur la variable k
			# et sur au moins une des variables 0..k-1 
			if consistanceAvecVarsPrecedentes(k):

				# continue l'algorithme sur la variable k+1
				reste = backtrack( k+1, toutesLesSolutions, initialise )
				if reste!= ECHEC:
					return reste

	# si l'on arrive ici, cela signifie que les valeurs pour les variables 0 a k-1 ne sont consistantes
	# avec aucune valeur possible pour la variable k. 
	var.metAJourValeur(None)
	return ECHEC			
