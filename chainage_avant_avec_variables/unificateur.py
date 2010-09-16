## \file unificateur.py
## \brief Implementation de l'algorithme du pattern matching
## \package unificateur
## \brief Implementation de l'algorithme du pattern matching
##
## Implementation de l'algorithme du pattern matching par unification. Cette 
## version permet d'avoir des variables sur les deux propositions

#-------------------------------------------------------------------------------
print "Unificateur"
print "\t@version: 1.3  date: 20/2/2007 by Vincent Schickel-Zuber"
print "\t@version: 1.2  date: 11/2/2007 by Vincent Schickel-Zuber"
print "\t@version: 1.1  date: 11/1/2007 by Bruno Alves"
print "\t@version: 1.0  date: 17/2/2006 by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------

# constante signifiant un echec 
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
# liste substitution2. Si la variable existe deja dans substitution1, alors ca
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
# proposition recursivement.
# @note Notez que pour l'unification, les propositions peuvent avoir des
#	   variables des deux cotes. Il faut donc remplacer les variables dans
#	   les deux propositions.
#
# @param[in] pattern la proposition (contient des variables, atomes,...
#				sous forme [' ',' ', ' '] OU ' ' ou ['[]'...])
# @param[in] substitutions la liste des substitutions {a:b, c:d,...}
# @return la proposition avec les variables remplacees par leur valeurs
def substitueVariables( pattern , substitutions ):  
	if testeAtome(pattern):
		if testeVariable(pattern) and pattern in substitutions:		 
			return substitueVariables( 		
				retourneValeur(trouveSubstitution(pattern,substitutions)),
				substitutions )
	else:
		for x in pattern[:]:
			pattern.append(substitueVariables(x , substitutions))
			pattern.pop(0)			
	return pattern


## Effectue une unification entre deux propositions
#
# Le filtrage est effectue en parcourant les deux propositions en meme temps,
# en prenant deux elements, en les comparants et en construisant les 
# substitutions qui s'imposent. Par exemple:
#
# <ul>
# 	<li>prop1 = [ 'Superman', 'a', 'une', 'cape', '?z' ]</li>
# 	<li>prop2 = [ '?x', 'a', 'une', '?y', 'rouge' ]</li>
# </ul>
#
# produit { '?x':Superman, '?y':'cape', '?z':'rouge' }
#
# L'algorithme est le suivant:
#
# @code
# Unifier (pat1, pat2)
#	1. if pat1 ou pat2 est un atome:
#	3.	 Echanger pat1 et pat2 au besoin pour que pat1 soit un atome
#	4.	 if pat1 et pat2 sont identiques: return {}.
#	5.	 else if pat1 est une variable:
#	7.		 if pat1 apparait dans pat2: return echec.
#	8.		 else return la substitution {pat1:pat2}.
#   10.	 else if pat2 est une variable: return la substit. {pat2:pat1}.
#   11.	 else: return echec.
#   12. else:
#   13.	 F1 <- premier element de pat1
#   14.	 T1 <- reste de pat1
#   15.	 F2 <- premier element de pat2
#   16.	 T2 <- reste de pat2
#   17.	 Z1 <- Unifier (F1, F2)
#   18.	 if Z1 = echec: return echec
#   19.	 G1 <- remplacer les variables de T1 selon les substitutions de Z1.
#   20.	 G2 <- remplacer les variables de T2 selon les substitutions de Z1.
#   21.	 Z2 <- Unifier (G1, G2)
#   22.	 if Z2 = echec: return echec
#   23.	 return { Z1 union Z2 }
# @endcode
#
# @param[in] proposition1 une propopsition avec/sans variables
# @param[in] proposition2 une proposition avec/sans variables
# @return les substitutions si l'unification reussit: {'?x':'a',..}, 'ECHEC' 
#		 sinon
def unifier( proposition1, proposition2 ):
	
	# si les deux listes sont vides, alors on retourne
	# une liste vide
	if (proposition1 == [] and proposition2 == []):
		return {}

	# si l'une des deux listes est vide, alors on retourne
	# ECHEC
	elif (proposition1 == [] or proposition2 == []):
		return echec
	
	# si proposition1 our proposition2 est un atome
	elif testeAtome(proposition1) or testeAtome(proposition2):

		# si proposition1 n'est pas un atome, alors on
		# l'echange avec proposition2
		if not testeAtome(proposition1):
			tmp = copy.deepcopy(proposition1)
			proposition1 = copy.deepcopy(proposition2)
			proposition2 = tmp
			
		# si les deux propositions sont egales, rien a faire
		if proposition1 == proposition2:
			return {}
		
		# si proposition1 est une variable..
		if testeVariable(proposition1):
			
			# .. et est contenue dans proposition2, alors echec 
			if proposition1 in proposition2:
				return echec
			
			# ...et n'est pas dans proposition2, alors construit la substitution
			else:
				return construitSubstitution(proposition1, proposition2)
			
		# si proposition2 est une variable, alors on construit la substitution
		if testeVariable(proposition2):
			return construitSubstitution(proposition2, proposition1)
		
		# retourne echec dans tous les autres cas
		return echec
		
	else:
		f1 = proposition1[0]
		t1 = proposition1[1:]
		f2 = proposition2[0]
		t2 = proposition2[1:]
		z1 = unifier( f1, f2 )
		if ( z1==echec ):
			return echec
		g1 = substitueVariables( t1, z1 )
		g2 = substitueVariables( t2, z1 )
		z2 = unifier( g1, g2 )
		if ( z2==echec ):
			return echec
		return unionSubstitutions( z1, z2 )


## Effectue une unification entre deux propositions passees en parametres
#
# Une unification est un procede tres semblable au filtrage vu dans l'exercice
# precedent, mais dans ce cas, les deux propositions peuvent contenir des
# variables. Un unificateur est plus general qu'un filtreur, il peut dont
# faire office de filtreur et ainsi etre utilise dans le chainage avant. 
# Cependant il est absolument necessaire dans un moteur d'inference a chainage
# arriere.
#
# @param[in] proposition1 proposition 1 avec/sans variables
# @param[in] proposition2 porposition 2 avec/sans variables
# @param[in] environnement un environnement {'?x':'a',...} de depart
# @return substitution dans un dico si le filtrage reussit : {'?x':'a',...}, 
#		 'ECHEC sinon
def patternMatching(proposition1, proposition2, environnement=None):
	if environnement is None:
		environnement={}
	if environnement==echec:
		return echec
	else :
		proposition1 = substitueVariables( proposition1, environnement )
		proposition2 = substitueVariables( proposition2, environnement )
		return unionSubstitutions( environnement,
								  unifier(proposition1, proposition2) )


#-------------------------------------------------------------------------------
# BATTERIE DE TESTS
#-------------------------------------------------------------------------------

# effectue un test de substitution de variables 
exec file("testSubstitueVariables2.py")

# effectue un test d'unification
exec file("testUnifier.py")

# effectue des tests sur l'unificateur
exec file("testPatternMatching2.py")
