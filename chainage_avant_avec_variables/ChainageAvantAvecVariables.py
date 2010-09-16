## \file ChainageAvantAvecVariables.py
## \brief Implementation d'un moteur d'inference avec variables.
##
## Implementation d'un moteur d'inference avant avec filtrage ou unification

#-------------------------------------------------------------------------------
print "Loading chainage_avant_avec_variables"
print "\t@version: 1.1  date: 27/06/2007 by Thomas Leaute"
print "\t@version: 1.0  date: 19/02/2007 by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------

# Modules utilises
import copy
import filtreur
import unificateur

# declare la constante echec
echec = 'ECHEC'

## Base des faits
faits = []

## Base des regles
regles = []

## Le module a utiliser
paquetage = filtreur

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
#	  regle = [ [[cond1], [cond2], ..., [condn]], [consequence] ]
#   d'ou regle[0] = [[cond1], [cond2], ..., [condn]]
#	 et regle[1] = [consequence]
#
# exemple:
#
# 	@code
#	[ [['bas-salaire', '?x'],['loyer', '?x']], ['reduc-loyer', '200', '?x'] ]
#	@endcode
#
# @param[in] conditions la liste des conditions [[cond1], [cond2], ..., [condn]]
# @param[in] consequence la consequence [consequence]
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


## Verifie que le fait passe en parametre est un declencheur de la regle
#
# Verifie que le nouveau fait passe en parametre est un declencheur de la regle,
# donnee par l'ensemble de ses conditions. Si c'est le cas, il faut verifier 
# si d'autres faits permettent de declencher la consequence de la regle.
#
# @param[in] fait un fait compose ['a', ...,'b']
# @param[in] conditions les conditions d'une regle contenant des variables ['cond1',....,'condn'], 'condi' peut aussi etre compose
# @return une liste de deux elements (qui sont chacun des listes!!!) contenant pour chaque condition satisfaite 
#		  un environnement deduit par pattern matching entre la condition et
# 		  le fait, ainsi qu'une liste des conditions restant a analyser. Le
# 		  format de retour est le suivant:
#			[
#					   [{environnement_1}, ...,{environnement_n}]
#				   , 
#			[ [cond_restant_1_1,...,cond_restant_1_k], [cond_restant_n_1,...,cond_restant_n_k]]
#				   ]
def faitSatisfaitUneCondition( fait, conditions ):  
	
	# garde les environnements dans une liste
	environnements =[]
	
	# garde une liste de conditions restantes 
	cond_restantes = []
	
	# retourne le resultat sous forme liste contenant les environnements et
	# pour chaque environnement, une liste de conditions restantes
	resultat = [ environnements, cond_restantes ]
	
	# pour chaque condition 
	for cond in conditions:		
		
		# garde une liste de conditions non remplies et obtient
		# un environnement deduit par pattern matching entre le 
		# fait et la condition 
		cond_pas_remplies = copy.deepcopy( conditions )
		environnement = paquetage.patternMatching( copy.deepcopy(fait),copy.deepcopy(cond))
		
		# si un environnement a ete trouve, l'ajoute et supprime la condition
		# statisfaite de la liste de conditions.
		if ( environnement != echec ): 
			environnements.append( environnement )
			cond_pas_remplies.remove( cond )
			cond_restantes.append( cond_pas_remplies ) 
	
	# retourne le resultat 
	return resultat


## Verife la validite de la condition en essayant toutes les substitutions 
# par les faits de la base
#
# Cette fonction verifie s'il existe dans la base des faits un fait 
# qui pourrait satisfaire la condition en essayant toutes les substitutions
# dans la liste des environnement sur tous les faits de la base des faits. Si
# c'est le cas, on stocke les environnements ainsi produits
#
# @param[in] condition la condition a verifier
# @param[in] listeEnvironnements [{...},...,{...}]
# @return la liste des environnements possibles [{},...,{}], vide si aucun
def satisfaitUneCondition ( condition, listeEnvironnements ):

	# initialise la liste des environnements possibles 
	env_possibles=[]
	
	# pour chaque environnement passe en parametre, on teste si un
	# fait particulier de la base des faits permet d'obtenir(avec cet env)
	# une nouvelle substitution, si c'est le cas, ajoute les substitutions
	# a la liste courrante
	for env in listeEnvironnements:
		for fait in faits:
			
			# obtient une substitution par pattern matching
			# entre le fait actuel et la condition 
			resultat = paquetage.patternMatching( 	copy.deepcopy(fait),
										copy.deepcopy(condition),
									   	copy.copy(env) )
									   
			# si l'environnement est valide, alors on l'ajoute 
			if ( resultat != echec ):
				env_possibles.append( resultat)   
				
	# retourne la liste des environnements possibles 
	return env_possibles


## Verifie qu'une liste de conditions peut etre verifiee par les environnements 
# existants
#
# Cette fonction s'assure que toutes les conditions passees en parametres
# peuvent etre satisfaites par la base des faits actuelle et retourne
# la liste des environnements ainsi obtenus. Si toutes les conditions de la
# regle peuvent etre ainsi satisfaites, alors on ajoutera les consequences
# dans la base des faits. Les consequences sont en fait diverses instantiations
# d'une meme consequence par diverses substitutions possibles. A noter encore
# qu'une consequence ne sera une solution que si elle n'existe pas encore dans
# la base des faits.
#
# @param conditions la liste de conditions a verifier [[],...,[]] 
# @param environnement un dictionnaire de substitutions
# @return la liste des environnements possibles [{},...,{}]; [] si aucun
def satisfaitConditions( conditions, environnement ):
	
	# construit une liste initiale avec l'environnement
	# passe en parametre
	liste_env =[ environnement ]
	
	# pour chaque condition dans la liste des conditions,
	# si la liste des environnements n'est pas vide,
	# on y ajoute les environnements qui permettent de satisfaire 
	# une des conditions 
	for cond in conditions:
		
		# s'il n'y a pas de liste des environnements, alors
		# on retourne une liste vide 
		if len(liste_env)==0:
			return liste_env
		
		# sinon, on verifie si la liste des environnements courante
		# permet de satisfaire la condition courante
		else:
			liste_env = satisfaitUneCondition( cond, liste_env )
			
	# retourne la liste des environnements ainsi obtenue 
	return liste_env


## Instantie la consequence d'une regle 
# 
# Cette fonction utilise la liste des environnements trouves par pattern
# matching afin d'obtenir une liste de faits possibles. Un fait s'obtient 
# en substituant les variables de la proposition par les substitutions donnees
# dans la liste des environnements. Cependant, ces instances ne seront ajoutees 
# que si elles sont une solution au probleme.
#
# @param[in] proposition la proposition
# @param[in] listeEnvironnements la liste des environnements [{},....,{}]
# @return une liste de nouveau faits ['fait1',...,'fait2']
def instantieVariables( proposition, listeEnvironnements ):
	
	# initialise la liste des faits 
	liste_faits=[]
	
	# pour chaque environnement dans la liste des environnements,
	# on ajoute les faits deduits par substitution des variables
	# dans la proposition
	for env in listeEnvironnements:
		liste_faits.append( 
				paquetage.substitueVariables( copy.deepcopy(proposition),
									  	  copy.deepcopy(env)) )
									  
	# retourne la liste des faits ainsi obtenue
	return liste_faits


## Effectue un chainage avant avec variables 
#
# Le moteur d'inference a chainage avant avec variables permet dorenavant de 
# traiter les regles contenant des variables. Le moteur utilise le procede 
# du pattern matching pour faire les correspondances entre les faits et les conditions,
# en essayant les substitutions possibles qui font correspondre les deux
# propositions.
# 
# @code
# ChainageAvantAvecVariables(faits-initiaux, regles)
#	 1. Q <- faits-initiaux
#	 2. while Q pas vide:
#	 3.	 q <- premier(Q), Q <- reste(Q)
#	 4.	 if q pas dans la base des faits:
#	 5.		 ajouter q a la base de faits
#	 6.		 imprimer q 
#	 7.	 for each regle r de regles:
#	 8.		 if c=conditions(r) and filtrage(q,c)!= echec:
#	 9.			 for ( each environnement deduit de  filtrage(q,c):
#	10.				 environnements2 <- retourne les environnements deduits 
#   ...	  des conditions restantes de r  tout en respectant environnement
#	11.				 n <- instancie la conclusion de r tout en respectant 
#   ...	  environnements2 
#	12.				 if n pas dans la base des faits:
#	13.					 ajouter n en queue de Q 
#   
# @endcode
#
# @param[in] regles les regles a verifer
# @param[in] faits_initiaux les faits initiaux
# @return la liste des faits deduits
def chainageAvantAvecVariables( regles, faits_initiaux ):
	
	# 1. fait une copie des faits initiaux 
	Q = copy.deepcopy(faits_initiaux)
	
	# 2. tant qu'il reste des faits a traiter, on 
	#	continue
	while len(Q)>0:
		
		# 3-4. on obtient le prochain fait
		q = Q.pop(0)
		
		# 5-7. si le fait pas dans la base des faits, alors
		# on l'ajoute et on l'imprime 
		if q not in faits:
			ajouteFait(q)
			print q
			
		# 8. pour chaque regle
		for r in regles:
			
			# 9. si le fait satisfait les conditions de la regle r, c'est
			#	a dire, s'il produit une liste d'environnements valables...
			resultat = faitSatisfaitUneCondition( q, conditionsRegle(r) )
			
			# 10. pour chaque environnement deduit par le pattern matching,
			environnement = resultat[0]
			cond_restant = resultat[1]
			for i in range( len(environnement) ):
				
				# 11. obtient la liste des environnements deduits des conditions 
				#	 restantes
				env   = environnement[i]
				conds = cond_restant[i]
				envs2 = satisfaitConditions( conds, env )
				if len(envs2)>0:
					
					# 12. instantie la conclusion de r tout en repectant les
					#	 environnements dans envs2
					instances = instantieVariables( consequenceRegle(r), envs2 )
					
					# 13. pour chaque instance dans la liste des instances,
					#	 si inst n'est pas dans la base des faits, on l'ajoute dans la queue
					for inst in instances:
						if inst not in faits:
							Q.append( inst )


#-------------------------------------------------------------------------------
# BATTERIE DE TESTS
#-------------------------------------------------------------------------------

# effectue des tests sur la fonction faitSatisfaitUneCondition
exec file( "testFaitSatisfaitUneCondition.py" )

# effectue des tests sur la fonction satisfaitUneCondition
exec file( "testSatisfaitUneCondition.py" )

# effectue des tests sur la fonction satisfaitConditions
exec file( "testSatisfaitConditions.py" )

# effectue des tests sur la fonction instantieVariables
exec file( "testInstantieVariables.py" )

# effectue des tests en essayant un nouveau fichier d'impots 
exec file( "impots2.py" )

# effectue un chainage avant avec filtrage.
chainageAvantAvecVariables( regles, faits )
