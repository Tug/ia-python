#-------------------------------------------------------------------------------
print "Loading chainage_avant_sans_variables"
print "\t@version: 2.4  date: 27/06/2007 modifie par Thomas Leaute"
print "\t@version: 2.3  date: 20/02/2007 modifie par Vincent Schickel-Zuber"
print "\t@version: 2.2  date: 10/23/2006 modifie par Vincent Schickel-Zuber"
print "\t@version: 2.1  date: 01/03/2007 modifie par Bruno Alves"
print "\t@version: 2.0  date: 12/02/2007 modifie par Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------

# Module pour la copie en profondeur
import copy

## Base des faits
faits = []

## Base des regles
regles = []


## Initialise les bases de faits et de regles
#
# Initialise la base des faits ainsi que la base des
# regles en les vidant d'abord.
def initDBs():
	del faits[:]
	del regles[:]


#-------------------------------------------------------------------------------
# FAITS
#-------------------------------------------------------------------------------

## Affiche la base des faits
#
# Affiche les faits sur la sortie standard du programme(ecran)
def afficheFaits():
	for x in faits:
		print x
		
## Ajoute un fait a la base des faits
#
# Ajoute un fait passe en parametre dans la base de faits actuelle
#
# @param[in] fait le fait a ajouter dans la base des faits
def ajouteFait( fait ):
	faits.append( fait )

		
#-------------------------------------------------------------------------------
# REGLES
#-------------------------------------------------------------------------------

## affiche la base des regles
#
# Affiche chaque regle de la base des regles sur la sortie standard
# du programme (stdout)
def afficheRegles():
	for x in regles:
		print x
		
		
## Ajoute une regle a la base des regles
#
# Ajoute une regle a la base des regles. Une regle est en fait un couple
# compose d'une seule consequence precedee d'un groupe de conditions. Une fois
# toutes les conditions reunies, la consequence peut etre ajoutee a la 
# base des faits. Le codage d'une regle est le suivant:
# 
#	  regle = [ ['cond1','cond2',...,'condn'], consequence ]
#   d'ou regle[0] = ['cond1','cond2',...,'condn']
#	 et regle[1] = consequence
#
# @param[in] conditions la liste des conditions ['toto',...,'titi']
# @param[in] consequence la consequence (un atome)
def ajouteRegle( conditions, consequence ):
	regles.append( [conditions, consequence] )

	
## Retourne les conditions d'une regle.
#
# Retourne les conditions d'une regle. Le codage des regles est decrit dans
# la documentation de la fonction ajouteRegle()
#
# @param[in] regle une regle de la base des regles
# @return la liste des conditions de la regle passee en argument
# @see ajouteRegle
def conditionsRegle( regle ):
	return regle[0]


## Retourne la consequence d'une regle
#
# Retourne la consequence d'une regle. Celle-ci correspond au deuxieme
# element d'une regle(donc d'index 1)
# @param[in] regle une regle de la base des regles
# @return la consequence de la regle passee en argument
# @see ajouteRegle
def consequenceRegle( regle ):
	return regle[1]


## Indique si un fait passe en parametre satisfait une des conditions d'une regle ou non
#
# Un fait satisfait l'une des conditions d'une regle, si le fait est
# inclus dans la liste des conditions de la regle
#
# @param[in] regle la regle a veifier
# @param[in] le_fait le fait que la condition de la regle doit contenir
# @return True si une des conditions est remplie par le_fait, False sinon 
def satisfaitUneCondition( regle, le_fait ):
	return ( le_fait in conditionsRegle(regle) )


## Indique si toutes les conditions d'une regle sont satisfaites par la base des faits
#
# Les conditions d'une regle sont satisfaites par la base des faits, si tous les
# faits constituant les conditions de la regle passee en parametre sont inclus
# dans la base des faits
#
# @param regle la regle a verifier
# @return True si toutes les conditions sont remplies par la base des faits, 
#		 False sinon
def satisfaitConditions( regle ):
	return set(conditionsRegle(regle)).issubset(set(faits))


## Effectue un chainage avant simple a partir des faits initiaux et de regles donnees
#
# La fonction de chainage avant simple deduit tous les faits possibles de
# deduire a partir des faits initiaux et des regles donnes. Une fois que les 
# consequences deduites sont inscrites dans la bases de donnees, il faudra
# de nouveau verifier si ces nouveaux faits permettent de declencher de
# nouvelles regles. Le processus se poursuit jusqu'a ce qu'il n'y ait plus
# de fait a deduire. Le pseudo-code de l'algorithme de chainage avant est le
# suivant:
#
# @code
#    1. Procedure Chainage-Simple(F,R)
#    2. Q <- faits de depart F
#    3. while Q pas vide {
#    4.	 q <- premier(Q), Q <- reste(Q)
#    5.	 if q pas dans la base de donnees then 
#    6.			ajouter q a la base de donnees et imprimer q
#    7.	 for chaque regle r de la base de regles R {
#    8.		 if q appartient conditions(r)
#    9.		  and conditions(r) est inclus dans la base de donnees
#   10.		  and conclusion(r) pas dans la base de donnees {
#   11.			 ajouter conclusion(r) en queue de Q
#   12.		 }
#   13.	 }
#   14. }
# @endcode
#
# @param[in] faitsInitiaux la liste des faits initiaux
# @param[in] regles la liste des regles
def chainageAvantSimple( faitsInitiaux, regles ):

	# copie les faits initiaux dans Q
	Q = copy.deepcopy( faitsInitiaux )

	# tant qu'il reste des faits a analyser,
	# il faut le faire...
	while len(Q)>0:

		# considere le premier fait de la liste Q
		q = Q.pop(0)

		# si le fait n'est pas encore dans la base des
		# faits, il faut l'ajouter. cela ne sera vrai
		# que lorsqu'une nouvelle consequence sera
		# inseree dans la liste Q
		if q not in faits:
			ajouteFait( q )
			print q

	# pour que la consequence d'une regle soit ajoutee
  	# dans la base des faits, il faut respecter les trois
	# conditions suivantes:
	#
		#	 1 - le fait q est une condition de la regle r
		#	 2 - les autres conditions de r sont satisfaites par
		#		 la base des faits actuelle
		#	 3 - la consequence de la regle r n'est pas encore
		#		 dans la base des faits
		for r in regles:
			if ( satisfaitUneCondition(r,q) and
				 satisfaitConditions(r) and
				 consequenceRegle(r) not in faits ):
				Q.append( consequenceRegle(r) )

		  
#
# Execution du programme
#

# Execute le fichier pour ajouter les regles et les faits dans leurs
# bases respectives
execfile( "impots.py" )

# effectue le chainage avant simple sur la liste
# des faits et des regles
chainageAvantSimple( faits, regles )

# imprime la nouvelle base des faits
print "Liste des faits deduits:"
print faits
