## \file filtreur.py
## \brief Implementation de l'algorithme du filtrage.
## \package match
##
## Implementation de l'algorithme du pattern matching avec un filtrage simple. 
## Ce type de filtrage ne supporte que les variables d'un cote.

#-------------------------------------------------------------------------------
print "Filtreur"
print "\t@version: 1.5  date: 07/03/2008 modified by Thomas Leaute"
print "\t@version: 1.4  date: 27/06/2007 modified by Thomas Leaute"
print "\t@version: 1.3  date: 20/02/2007 modified by Vincent Schickel"
print "\t@version: 1.2  date: 01/07/2007 modified by Bruno Alves"
print "\t@version: 1.1  date: 10/03/2006 modified by Vincent Schickel"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 9/2/2006"
print "\t@copyright: EPFL-IC-IIF-LIA 2006-2007"
#-------------------------------------------------------------------------------

## La variable globale utilisee pour signifier un ECHEC
echec='ECHEC'


## Teste si le symbole passe en parametre est un atome
# 
# Cette fonction teste si le symbole passe en parametre est
# du meme type qu'un atome ( c-a-d ' ' )
#
# @param[in] x le symbole a tester
# @return True si le symbole x est un atome, False sinon
def testeAtome( x ):
	return type(x)==type('')


## Teste si le symbole passe en parametre est une substitution
#
# Cette fonction teste si le symbole passe en parametre est du
# meme type qu'un dictionnaire ( c-a-d {} ). Une substitution
# est de la forme {'?x':'oiseau'}.
#
# @param[in] x le symbole a tester
# @return True si le symbole x est une substitution, False sinon
def testeSubstitution( x ):
	return type(x)==type({})


## Teste si le symbole passe en parametre est une variable
#
# Cette fonction teste si le symbole x passe en parametre est
# un atome et qu'il commence par le caractere ?. Une variable
# est codee ainsi: ?x
#
# @param[in] x le symbole a tester
# @return True si le symbole x est une variable
def testeVariable( x ):
	return (testeAtome(x) and x[0]=='?')


## Retourne une substitution entre une variable et une expression
#
# Construit une substitution, en associant une variable de la forme ?x
# avec une expression, qui peut etre d'un type quelconque sans variable.
#
# @param[in] variable la variable a substituer
# @param[in] datum preposition sans variable
# @return une substitution {variable:datum}
def construitSubstitution( variable, datum ):
	return {variable:datum}


## Retourne la variable d'une substitution
#
# La variable d'une substitution est le premier element d'une paire
# {variable:valeur}. 
#
# @param[in] substitution la substitution
# @return la variable de la substitution
def retourneVariable( substitution ):
	return substitution.keys()[0]


## Retourne la valeur d'une substitution
#
# La valeur d'une substitution est le deuxieme element d'une paire
# {variable:valeur}. 
#
# @param[in] substitution la substitution
# @return la valeur de la substitution
def retourneValeur( substitution ):
	return substitution.values()[0]


## Retourne la substitution associee a une variable,
# cad: {variable:definition_de_la_variable}
#
# Cette fonction retourne une paire {variable:valeur} si elle existe,
# dans le cas contraire, elle retourne False
#
# @param[in] variable la variable dont on veut trouver une substitution
# @param[in] substitutions la liste des substitutions possibles
# @return la substitution associee a la variable si elle existe dans
#		 substitutions, sinon retourne False
def trouveSubstitution( variable, substitutions ):
	if variable in substitutions:
		return {variable:substitutions[variable]}
	else:
		return False


## Construit l'union de deux substitutions
#
# Pour construire l'union de deux substitutions, on prend chaque variable de la
# liste substitution2. Si la variable existe deja dans substitution1, alors sa
# valeur est mise a jour, sinon elle est creee avec sa valeur associee.
#
# @param[in] substitution1 la premiere substitution
# @param[in] substitution2 la deuxieme substitution
# @return substitution1 UNION substitution2; echec if substitution1 ou
#		 substitution2 ne sont pas des substitutions
def unionSubstitutions( substitution1, substitution2 ):
	if ( testeSubstitution(substitution1) and
		 testeSubstitution(substitution2) ):
		keys = substitution2.keys()
		for x in keys:
			substitution1[x]=substitution2[x]
		return substitution1;
	else:
		return echec


## Retourne la proposition avec les variables remplacees par leurs valeurs
#
# Cette methode se charge de substituer toutes les variables de la proposition
# passee en argument par leur valeur associee dans la liste des substitutions.
# Si la proposition est une <em>variable</em>, alors il suffit de retourner
# la valeur associee si elle existe, sinon, on teste chaque element de la
# proposition recursivement
#
# @param[in] pattern la proposition (contient des variables, atomes,...
#				sous forme [' ',' ', ' '] OU ' ' ou ['[]'...])
# @param[in] substitutions la liste des substitutions {a:b, c:d,...}
# @return la proposition avec les variables remplacees par leur valeurs
def substitueVariables( pattern , substitutions ):  
	if testeAtome(pattern):
		if testeVariable(pattern) and pattern in substitutions:		 
			return retourneValeur(trouveSubstitution(pattern,substitutions))
	else:
		for x in pattern[:]:
			pattern.append(substitueVariables(x , substitutions))
			pattern.pop(0)			
	return pattern


## Effectue un filtrage entre deux propositions
#
# Le filtrage est effectue en parcourant les deux propositions en meme temps,
# en prenant deux elements, en les comparant et en construisant les 
# substitutions qui s'imposent. Par exemple:
#
# <ul>
# 	<li>prop1 = [ 'Superman', 'a', 'une', 'cape', 'rouge' ]</li>
# 	<li>prop2 = [ '?x', 'a', 'une', '?y', 'rouge' ]</li>
# </ul>
#
# produit { '?x':Superman, '?y':'cape' }
#
# L'algorithme est le suivant:
#
# @code
#  1. function FILTRER( datum, pattern )
#  2.   if pattern est [] et datum est []: return {}
#  3.   if pattern est [] ou datum est []: return ECHEC
#  4.   if pattern est un atome:
#  5.	   if datum et pattern sont identiques: return {}
#  6.	   if pattern est une variable: return {pattern : datum}
#  7.	   return ECHEC
#  8.   if datum est un atome: return ECHEC
#  9.   F1 <- premier element de datum, T1 <- reste de datum
# 10.   F2 <- premier element de pattern, T2 <- reste de pattern
# 11.   Z1 <- FILTRER(F1,F2)
# 12.   if Z1 = ECHEC: return ECHEC
# 13.   G1 <- T1
# 14.   G2 <- remplacer les variables de T2 par les substitutions de Z1
# 15.   Z2 <- FILTRER(G1,G2)
# 16.   if Z2 = ECHEC: return ECHEC
# 17.   return { Z1 union Z2 }
# @endcode
#
# @param datum la propopsition <strong>sans</strong> variable
# @param pattern la proposition <strong>avec</strong> variables
# @return les substitutions si le filtrage a reussi: {'?x':'a',..}, 'ECHEC' sinon
def filtrer( datum, pattern ):

	# si les deux listes sont vides, alors on retourne
	# une liste vide
	if (pattern == [] and datum == []):
		return {}

	# si l'une des deux listes est vide, alors on retourne
	# ECHEC
	elif (pattern == [] or datum == []):
		return echec

	# si pattern est un atome, 
	elif testeAtome(pattern):

		# et si les deux propositions sont identiques, alors
		# pas de substitution
		if (pattern==datum):
			return {}

		# si pattern est une variable, alors trouve une
		# substitution
		elif testeVariable(pattern):
			return construitSubstitution(pattern,datum)

		# sinon, le filtrage echoue
		else :
			return echec

	# si datum est un atome et pattern *n'est pas* un atome, alors
	# il y a ECHEC
	elif testeAtome(datum):
		return echec

	# sinon, on peut filtrer les deux propositions sans probleme
	else:
		f1=datum[0]			# premier element	
		t1=datum[1:]		# le reste de la liste 
		f2=pattern[0]
		t2=pattern[1:]
		z1=filtrer(f1,f2)
		if z1==echec: return echec
		g1=t1
		g2=substitueVariables(t2, z1)
		z2= filtrer(g1,g2)
		if z2==echec: return echec
		return unionSubstitutions(z1,z2)		


## Effectue un filtrage en tenant compte d'une liste de substitutions
# initiale
#
# Cette fonction effectue un filtrage sur deux propositions. Cette
# fonction peut prendre en argument un environnement initial. Un
# environnement initial est une liste de substitutions. Le resultat
# final est l'union de l'environnement initial avec les substitutions
# donnees par le filtrage
#
# @param pattern une proposition pouvant contenir des variables
# @param datum la proposition <strong>sans</strong> variables
# @param environnement une liste initiale de substitutions
# @return filtre(proposition,datum) si OK, ECHEC sinon	
def patternMatching( datum, pattern, environnement=None ):
	if environnement is None:
		environnement={}
	if environnement==echec:
		return echec
	else :
		pattern = substitueVariables(pattern,environnement)
		return unionSubstitutions(environnement,filtrer(datum,pattern))

#-------------------------------------------------------------------------------
# BATTERIE DE TESTS
#-------------------------------------------------------------------------------

# effectue des tests sur la fonction substitueVariables
exec file( "testSubstitueVariables.py" )

# effectue des tests sur la fonction filtrer
exec file( "testFiltrer.py" )

# effectue des tests sur la fonction patternMatching
exec file( "testPatternMatching.py" )
