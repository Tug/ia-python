# -*- coding: cp1252 -*-
## \file id3.py
## \brief Contient l'algorithme ID3
## \package id3
## \brief Contient l'algorithme ID3

#-------------------------------------------------------------------------------
print "Chargement du module ID3"
print "Construction d'un arbre de decision avec ID3."
print "\t@version: 1.6  date: 05/05/2008 modifie par Thomas Leaute"
print "\t@version: 1.5  date: 22/05/2007 modifie par Thomas Leaute"
print "\t@version: 1.4  date: 21/05/2007 modifie par Thomas Leaute"
print "\t@version: 1.3  date: 16/05/2007 modifie par Thomas Leaute"
print "\t@version: 1.2  date: 15/02/2007 modifie par Vincent Schickel-Zuber"
print "\t@version: 1.1  date: 01/02/2007 modifie par Bruno alves"
print "\t@version: 1.0  date: 17/05/2006 modified par l'auteur"
print "\t@author: michael.schumacher@epfl.ch"
print "\t@copyright: EPFL-IC-IIF-LIA 2006-2007"
#-------------------------------------------------------------------------------

# modules nécessaires
import math
import copy


## La liste des exemples
#
# La liste des exemples, selon le format suivant:
#	tousLesExemples ::= [ exemple1 exemple2 ... ]
#	exemple ::= [ classe valeur-attribut-1 ... valeur-attribut-n]
tousLesExemples = []

## La liste des attributs
#
# La liste des attributs (dans le meme ordre que celui des exemples)
# avec leur valeur. Format:
#	attributsEtValeurs ::= [ attribut1 attribut2 ... ]
#	attribut ::= [ nom-attribut valeur-1 .. valeur-m ]
attributsEtValeurs = []

## L'arbre de decision trouvé
#
# Contient l'arbre de décision
classification = []	


#-------------------------------------------------------------------------------
#   CALCUL DE L'ARBRE DE DECISION
#-------------------------------------------------------------------------------

## \brief Represente un noeud dans l'arbre de décision
#
# Cette classe représente un noeud dans l'arbre de décision
class Noeud:

	## \var attribut
	#
	# L'attribut de partitionnement du noeud

	## \var exemples
	#
	# La liste des exemples à classifier

	## \var enfants
	#
	# La liste des noeuds enfants de ce noeud.

	
	## Constructeur du noeud
	#
	# Initialise l'état interne du noeud, en lui passant l'attribut
	# de partionnement, les exemples à classer ainsi que la liste
	# des enfants attachés à ce noeud.
	#
	# @param[in] self référence automatique vers l'objet exécutant cette méthode
	# @param[in] attributPartition L'attribut de partitionnement du noeud.
	# @param[in] listeExemples Les exemples du noeud (s'il est terminal).
	# @param[in] enfants Les noeuds fils (s'il n'est pas terminal).
	def __init__( self, attributPartition, listeExemples, enfants ):
		self.attribut = attributPartition
		self.exemples = listeExemples
		self.enfants = enfants


	## Retourne une représentation textuelle des caractéristiques du noeud
	#
	# Cette méthode retourne une représentation textuelle de cette classe. Voici
	# un exemple de sortie:
	#
	# @code
	# ********** ARBRE DE DECISION **********
	# Partitionnement selon age
	# Valeur old
	#	Noeud terminal: classe down
	#	   ['down', 'old', 'no', 'software']
	#	   ['down', 'old', 'no', 'hardware']
	#	   ['down', 'old', 'yes', 'software']
	# Valeur midlife
	#	Partitionnement selon competition
	#	Valeur no
	#	   Noeud terminal: classe up
	#		  ['up', 'midlife', 'no', 'hardware']
	#		  ['up', 'midlife', 'no', 'software']
	#	Valeur yes
	#	   Noeud terminal: classe down
	#		  ['down', 'midlife', 'yes', 'software']
	#		  ['down', 'midlife', 'yes', 'hardware']
	# Valeur new
	#	Noeud terminal: classe up
	#	   ['up', 'new', 'no', 'hardware']
	#	   ['up', 'new', 'no', 'software']
	#	   ['up', 'new', 'yes', 'software']
	# @endcode
	#
	# @param[in] self référence automatique vers l'objet exécutant cette méthode
	# @return une chaîne de caractères contenant la représentation du noeud
	def __repr__(self):
		out = ("\n********** ARBRE DE DECISION **********\n")
		return out + self.imprimeNoeudAux("  ")
	

	## Retourne une représentation textuelle de l'arbre de décision à partir
	# du noeud courrant
	#
	# Cette méthode imprime un arbre de décision en commençant par le noeud courant
	# et en descendant dans la hiérarchie.
	#
	# @param[in] self référence automatique vers l'objet exécutant cette méthode
	# @param[in] espacement l'espacement initial pour le formattage
	# @return une chaîne de caractères contenant la représentation du noeud
	def imprimeNoeudAux( self, espacement ):

		# si le noeud est terminal, on affiche le noeud et les exemples
		if self.estTerminal():
			out = ("%s Noeud terminal : classe %s\n" %
				   ( espacement, self.retourneClasse()) )
			for ex in self.exemples:
				out = out + ("%s  %s\n" % (espacement, ex))

		# si le noeud n'est pas terminal, alors continue la descente récursive
		else:

			# indique que le noeud n'est pas terminal
			out = ("%s Partitionnement selon %s\n" %
				   (espacement, retourneNomAttribut(self.attribut)))

			# retourne la liste des valeurs de l'attribut
			valeurs = retourneValeursAttribut( self.attribut )

			# retourne la liste des successeurs
			successeurs = self.enfants

			# incrémente l'espacement pour le formattage
			nouvelEspacement = espacement + "    "

			# parcourt les successeurs jusqu'à ce qu'il n'y en ait plus
			while len(successeurs) > 0:
				if successeurs[0] != []:
					out = out + ("%s Valeur %s\n" % (espacement, valeurs[0]))
					out = out + successeurs[0].imprimeNoeudAux( nouvelEspacement )
				valeurs = valeurs[1:]
				successeurs = successeurs[1:]

		# retourne la représentation ainsi obtenue
		return out


	## Retourne la classe du noeud
	# 
	# Cette méthode indique la classe du noeud s'il est un noeud
	# terminal. Si le noeud est un noeud intermédiaire, alors celui-ci
	# n'a pas de classe.
	#
	# @param[in] self référence automatique vers l'objet exécutant cette méthode
	# @return la classe correspondant au noeud \c n s'il est terminal,
	#		 \c [] si c'est un noeud intermediaire
	def retourneClasse( self ):
		if self.estTerminal():
			return retourneClasse( self.exemples[0] )


	## Indique si le noeud est terminal ou non
	#
	# Cette méthode indique si le noeud considéré est terminal ou pas. Un
	# noeud est terminal ssi il ne possède pas d'attribut de partitionnement,
	# mais uniquement des exemples classifiés.
	#
	# @param[in] self référence automatique vers l'objet exécutant cette méthode
	# @return \b True si le noeud est terminal, \b False sinon
	def estTerminal( self ):
		return (self.attribut == [])


#-------------------------------------------------------------------------------
# INITIALISATION ET CONSULTATION DE L'ARBRE DE DECISION
#-------------------------------------------------------------------------------


## Initialise le module ID3 
#
# Cette fonction initialise le module ID3 avec les exemples \c exemples et la
# description des classes et attributs \c attrsEtValeurs.
#
# @param[in] exemples les exemples à classifier
# @param[in] attrsEtValeurs les attributs ainsi que leur valeur
def initID3( exemples, attrsEtValeurs):

	# variables globales du problème
	global tousLesExemples
	global attributsEtValeurs
	global classification

	# initialise les variables du problème
	tousLesExemples = exemples
	attributsEtValeurs = attrsEtValeurs
	classification = []

	# affiche les informations
	print( "DB : initID3 -> attributsEtValeurs : %s" % (attributsEtValeurs) )


## Permet de classer un set d'exemples à l'aide de l'arbre de décision
#
# Cette fonction s'appuye sur l'arbre de décision construit par la fonction
# \c construitArbreDecision(). Pour classifier les exemples, on part depuis
# le noeud \c n et on descend recursivement dans les sous-noeuds.
#
# @param[in] n le noeud d'où part la classification
def classifie( n=classification ):

	# si le noeud est vide, alors pas de classification possible
	if n == []:
		print( ">>> L'exemple ne peut être classé" )

	# si le noeud est terminal, alors on peut obtenir sa classe
	elif n.estTerminal():
		print( ">>> L'exemple est de la classe %s" % (n.retourneClasse()) )

	# sinon, il nous faut encore parcourir l'arbre de décision
	else:

		# tout d'abord on définit quelles sont les valeurs valables
		# pour l'attribut de partionnement
		attributPartition = n.attribut
		valeursPossibles = retourneValeursAttribut( attributPartition )

		# continue le test jusqu'à ce qu'on reçoive une valeur
		# valide et qu'on puisse continuer la classification
		while True:

			# affiche la valeur de l'attribut
			print( "> Valeur de l'attribut %s? " %
				  (retourneNomAttribut(attributPartition)) )

			# lit la valeur depuis le clavier
			valeur = raw_input()

			# si la valeur fait partie des valeurs possibles, alors
			# on peut continuer la classification
			if valeur in valeursPossibles:
				return classifie( n.enfants[valeursPossibles.index(valeur)] )

			# sinon, on affiche une erreur pour signaleur que la
			# valeur n'est pas valide
			print( "## Valeur %S inconnue pour l'attribut %s" %
				  (valeur, retourneNomAttribut(attributPartition)) )

			
## Construit l'arbre de decision pour les exemples de \c tousLesExemples et
# le sauvegarde dans la variable globale \c classification.
# 
# Cette fonction s'appuye sur \c construitArbreDecisionAux pour construire
# l'arbre de décision à partir des exemples donnés.
def construitArbreDecision():

	# variables globales
	global classification

	# retourne l'arbre ainsi produit
	classification = construitArbreDecisionAux( tousLesExemples,
												construitListeAttributs() )

	# affiche l'arbre de décision produit
	print( classification )


## Fonction auxiliaire de construction de l'arbre de décision
#
# Cette fonction est la fonction qui construit vraiment l'arbre de décision.
# Elle est appelée depuis \c construitArbreDecision() pour initialiser la
# création de l'arbre à partir d'un set d'exemples et une liste
# d'attributs
#
# @param[in] exemples la liste d'exemples servant à la construction de l'arbre
# @param[in] attributs la liste des attributs
# @return une branche de l'arbre de décision
def construitArbreDecisionAux( exemples, attributs ):
	
	# indique que nous construisons l'arbre de décision
	print("DB : construitArbreDecisionAux -> attributs : %s" % (attributs))	

	# s'il n'y a plus d'exemples, alors on a fini
	if exemples == []:
		return []
		
	# si les exemples sont de même classe, alors
	# on n'a plus qu'un noeud terminal
	elif memeClasse( exemples ):
		print("DB : construitArbreDecisionAux -> memeClasse ") 
		return Noeud( [], exemples, [] )

	# sinon, il reste plus d'une classe, et il faut continuer
	# à descendre dans l'arbre
	else:

		# choisit le meilleur attribut comme attribut de partition
		attributPartition = meilleurAttribut( attributs, exemples )
		print( "DB : construitArbreDecisionAux -> attribut de partition : %s"
			   % (attributPartition) )

		# garde les attributs restants
		attributsRestants = copy.deepcopy( attributs )
		attributsRestants.remove( attributPartition )
		
		print( "DB : construitArbreDecisionAux -> attributs restants : %s"
			   % (attributsRestants) )
		
		# trie les exemples en sous-listes d'après la valeur de l'attribut de partition
		sousListes = partition( exemples, attributPartition )
		
		# construit les noeuds fils en appliquant l'algorithme à chaque sous-liste
		fils = map( lambda p : construitArbreDecisionAux(p, attributsRestants), sousListes )
		
		return Noeud( attributPartition, [], fils )


#-------------------------------------------------------------------------------
# CALCUL DE L'ENTROPIE
#-------------------------------------------------------------------------------

## Retourne le meilleur attribut à choisir dans la liste disponible
#
# Cette fonction retourne le meilleur attribut dans la liste des attributs.
# Pour ce faire, cette fonction retourne l'attribut dont l'entropie est la
# plus faible.
#
# @param[in] attributs la liste des attributs
# @param[in] exemples la liste des exemples
# @return l'attribut ayant la plus faible entropie
def meilleurAttribut( attributs, exemples ):

	# indique ce qu'on fait
	print( "DB : meilleurAttribut -> attributs : %s" % (attributs) )
	
	# trouve l'entropie minimale
	entropieAttributs = [entropie(a,exemples) for a in attributs]
	return attributs[retourneIndiceMinimum(entropieAttributs)]




## Retourne l'entropie totale pour l'attribut passé en paramètre.
#
# Cette fonction calcule et retourne l'entropie totale pour l'attribut
# d'indice \c attribut, a savoir: H(C|A) = H(C|attribute).
#
# @param[in] attribut l'indice de l'attribut dont on cherche l'entropie
# @param[in] exemples la liste des exemples sur laquelle on calcule l'entropie
def entropie( attribut, exemples ):

	# calcule l'entropie pour chaque attribut 
	liste = [ P_Aj(attribut,x,exemples)*H_C_Aj(attribut,x,exemples)
			 for x in retourneValeursPossiblesAttribut(attribut,exemples)]

	# calcule la somme
	res = sum(liste)
	
	# affiche l'entropie	
	print( "DB : entropie -> res : %s" % (res) )
	
	# retourne le résultat
	return res


## Retourne l'entropie conditionnelle de l'attribut passé en paramètre pour
# une certaine valeur.
#
# Cette fonction calcule l'entropie conditionnelle pour l'attribut \c attribut
# ayant comme valeur d'attribut \c valeur, en d'autres termes :
#	  H(C|Aj) = H(C|attribute=value).
#
# @param[in] attribut l'indice de l'attribut
# @param[in] valeur la valeur de l'attribut
# @param[in] exemples la liste des exemples sur laquelle calculer l'entropie
def H_C_Aj( attribut, valeur, exemples ):

	# ajoute les probabilités
	return - sum([ calculeXlogX(P_Ci_Aj(c,attribut,valeur,exemples)) for c in retourneClassesPossibles(exemples) ])


## Calcule x * log_2(x)
#
# Cette méthode calcule x * log_2(x). Retourne 0 si x == 0. 
#
# @param[in] x la variable 
def calculeXlogX( x ):

	# si x est nul, alors retourne 0
	if x == 0:
		return 0		
	# sinon, retourne x * log(x,2)
	else:
		return x * math.log(x,2)


## Calcule la probabilité P(Ci|Aj) = P(class-value|attribute=value)
#
# Cette fonction calcule la probabilite que la valeur de la classe soit
# \c classe lorsque \c attribut vaut \c valeur, en d'autres
# termes : P(Ci|Aj) = P(class-value|attribute=value).
#
# @param[in] classe la nom de la classe
# @param[in] attribut l'indice de l'attribut
# @param[in] valeur la valeur de l'attribut
# @param[in] exemples la liste des exemples sur laquelle on calcule la probabilité.
def P_Ci_Aj( classe, attribut, valeur, exemples ):
	return nombreOccurencesCond(classe,attribut,valeur,exemples) /float(
		nombreOccurences(attribut,valeur,exemples))


## Retourne la probabilité P_Aj
#
# Cette fonction retourne la probabilité que la valeur de l'attribut
# d'indice \c attribut soit \c valeur. Cette probabilité est tout simplement
# le nombre d'exemples dont l'attribut \c attribut a la valeur \c valeur,
# divisé par le nombre d'exemples de la liste \c exemples.
#
# @param[in] attribut l'attribut cherché
# @param[in] valeur la valeur de l'attribut
# @param[in] exemples la liste des exemples
# @return la probabilité P_Aj
def P_Aj( attribut, valeur, exemples ):
	return nombreOccurences(attribut, valeur, exemples) / float(len(exemples))



#-------------------------------------------------------------------------------
# EXEMPLES
#-------------------------------------------------------------------------------

## Retourne la valeur de l'attribut donné en paramètre pour l'exemple donné.
#
# Cette fonction retourne la valeur de l'attribut d'indice \c attribut dans
# l'exemple \c exemple. Un exemple est une liste de la forme:
#
# @code
# exemple = [ 'nom-classe', 'valeur-attribut1', ..., 'valeur-attributn']
# @endcode
#
# @param[in] exemple l'exemple dont on veut la valeur de l'attribut
# @param[in] attribut l'indice de l'attribut dont on cherche la valeur
# @return la valeur de l'attribut pour l'exemple passé en paramètre.
def retourneValeurAttribut( exemple, attribut ):
	return exemple[attribut]


## Retourne la classe de l'exemple passé en paramètre.
#
# Cette fonction retourne la classe d'un \c exemple. Cette classe est tout
# simplement le premier élément de la liste \c exemple.
#
# @param[in] exemple l'exemple dont on cherche la classe
# @return le nom de la classe à laquelle l'exemple appartient
def retourneClasse( exemple ):
	return exemple[0]


#-------------------------------------------------------------------------------
# OPERATIONS SUR UNE LISTE D'EXEMPLES
#-------------------------------------------------------------------------------

## Partitionne les exemples selon les valeur de l'attribut
#
# Retourne une liste dont chaque element est une liste des exemples
# avec un valeur commune pour \c attribut. Cette liste contient pour chaque
# valeur d'attribut \e vi un liste d'exemples dont la valeur est \e vi.
#
# @param[in] exemples la liste des exemples à partitionner
# @param[in] attribut l'attribut pivot qui sert au partitionnement
# @return un liste de sous-listes d'exemples partitionnés par valeur d'attrib.
def partition( exemples, attribut ):
	# partionne les exemples
	res = [ [e for e in exemples if retourneValeurAttribut(e, attribut)==v]
			for v in retourneValeursAttribut(attribut) ]
  
	# affiche la partition
	print( "DB : 000000000000000000000 partition -> res : %s" % (res) )
	
	# retourne la partition
	return res
	

## Indique si tous les exemples passés en paramètre appartiennent à la même
# classe.
#
# Cette fonction indique si les exemples passés dans la liste \c exemples
# appartiennent ou non à la même classe. Elle procède en dénombrant les classes 
# possibles parmi les exemples. Si le nombre est \b 1,
# alors cela signifie que les exemples font partie d'une même classe
#
# @param[in] exemples la liste des exemples dont on veut savoir s'ils sont
#					 de la même classe
# @return \b True si tous les exemples sont de la même classe, \b False sinon
def memeClasse( exemples ):
	res = len( retourneClassesPossibles(exemples) ) == 1
	print( "DB : -- memeClasse -> retourneClassesPossibles(examples) %s" %
		   (retourneClassesPossibles(exemples)) )
	print( "DB : -- memeClasse -> res %s" % (res))
	return res


## Retourne la liste de toutes les valeurs pour un certain attribut
#
# Cette fonction retourne une liste de toutes les valeurs possibles
# pour l'attribut d'indice \c attribut que l'on trouve dans les
# exemples de la liste \c exemples.
#
# @param[in] attribut l'indice de l'attribut dont on cherche les valeur
# @param[in] exemples la liste des exemples dans laquelle on cherche
# @return une liste contenant toutes les valeurs possibles de l'attribut
def retourneValeursPossiblesAttribut( attribut, exemples ):
	res = []
	for ex in exemples:
		valeur = retourneValeurAttribut( ex, attribut )
		if not valeur in res:
			res = [valeur] + res		
	return res


## Retourne la liste de toutes les classes possibles de la liste des exemples
#
# Cette fonction parcourt les exemples et cherche toutes les classes
# que l'on peut extraire à partir de cette liste.
#
# @param[in] exemples la liste des exemples à parcourir
# @return la liste des classes possibles à partir des exemples
def retourneClassesPossibles( exemples ):
	res = retourneValeursPossiblesAttribut(0, exemples)
	return res


## Retourne le nombre d'exemples dont l'attribut vaut une certaine valeur
#
# Cette fonction retourne le nombre d'exemples de la liste \c exemples dont
# la valeur de l'attribut d'indice \c attribut vaut \c valeur.
#
# @param[in] attribut l'indice de l'attribut
# @param[in] valeur la valeur de l'attribut
# @param[in] exemples la liste des exemples à parcourir
# @return le nombre d'exemples de même valeur que \c valeur
def nombreOccurences( attribut, valeur, exemples ):
	res = 0
	for ex in exemples:
		if retourneValeurAttribut(ex,attribut) == valeur:
			res = res + 1
	return res
	
	
## Retourne le nombre d'exemples respectant une condition particulière.
#
# Cette fonction retourne le nombre d'exemples d'\c exemples appartenant à la
# classe \c classe et qui ont \c valeur comme valeur de l'attribut d'index
# \c attribut.
#
# @param[in] classe le nom de classe
# @param[in] attribut l'indice de l'attribut
# @param[in] valeur la valeur de l'attribut
# @param[in] exemples la liste des exemples
# @return le nombre d'exemples respectant la condition
def nombreOccurencesCond( classe, attribut, valeur, exemples ):
	res = 0
	for ex in exemples:
		if ( retourneClasse(ex) == classe ) and ( retourneValeurAttribut(
			ex,attribut) == valeur ):
			res = res + 1
	return res



#-------------------------------------------------------------------------------
#   UTILITAIRES
#-------------------------------------------------------------------------------

## Retourne la liste de toutes les valeurs possibles de l'attribut
# d'index \c attribut.
#
# Cette fonction retourne la liste de toutes les valeurs possible pour un
# attribut donné. Les valeurs d'un attribut sont stockées dans une liste dont
# le premier élément est le nom de l'attribut. Donc, pour obtenir les valeurs,
# il suffit de retourner les éléments de 1 à
# len(\c attributsEtValeurs[attribut])
#
# @param[in] attribut l'indice de l'attribut
# @return une liste de valeurs correspondant à l'attribut d'indice \c attribut
def retourneValeursAttribut( attribut ):
	return attributsEtValeurs[attribut][1:]


## Retourne la liste des index des attributs, i.e. une liste de \c actuel a
# \c dernier-1.
#
# Cette fonction crée une liste d'indices correspondant à chaque élément
# de la liste \c attributsEtValeurs.
#
# @param[in] actuel l'indice de l'attribut courant
# @param[in] dernier l'indice du dernier attribut
# @return une liste d'indices pour chaque attribut
def construitListeAttributs( actuel=1, dernier=-1 ):
	if dernier == -1:
		dernier = len(attributsEtValeurs)
	if actuel < dernier:
		return range(actuel,dernier)
	else:
		return []


## Retourne le nom de l'attribut d'index \c attribut.
#
# Cette fonction retourne, dans la liste des attributs et de leur valeur,
# le nom de l'attribut correspondant à l'indice \c attribut. Le codage de la
# liste \c attributsEtValeurs est le suivant :
#
# @code
# attributEtValeur = [ 'nom_attribut', 'valeur_1', ..., 'valeur_n' ]
# attributsEtValeurs = [ attributEtValeur[0], ...., attributEtValeur[m] ]
# @endcode
#
# Le nom de l'attribut \c attribut se trouve donc en
# \c attributsEtValeurs[attribut][\b 0].
#
# @param[in] attribut l'indice de l'attribut dont on cherche le nom
# @return le nom de l'attribut d'indice \c attribut
def retourneNomAttribut( attribut ):
	return attributsEtValeurs[attribut][0]


## Retourne l'index de la plus petite valeur de la liste \c liste.
#
# Cette fonction cherche parmi tous les éléments de la liste \c liste passée
# en paramètre <em>le plus petit</em> et retourne sa position 
#
# @param[in] liste la liste dans laquelle l'on doit chercher
# @return l'indice du plus petit élément de la liste
def retourneIndiceMinimum( liste ):
	print( "DB : retourneIndiceMinimum -> l : %s" % (liste) )
	return liste.index( min(liste) )


#-------------------------------------------------------------------------------
# BATTERIE DE TESTS
#-------------------------------------------------------------------------------
exec file( 'maladie.py' )
exec file( 'profit.py' )
