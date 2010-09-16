## \file testPatternMatching.py
## \brief Tests pour la fonction de "pattern Matching" patternMatching().
## \package testPatternMatching
## Teste la fonction de pattern Matching patternMatching(datum, proposition, env)
##
## Cette module effectue des tests sur divers aspects du pattern Matching. Les
## aspects les plus importants sont qu'il faut tenir en compte d'un environement
## initial comprenant une serie de substitutions. Il faut par ailleurs que
## le pattern Matching puisse trouver les substitutions avec des propositions
## complexe, sans boucler(dans le cas ou pattern contient plusieurs fois la
## meme variable) et en ajoutant bien toutes les substitutions possibles.
print "\nTest de la fonction patternMatching(daum,proposition,env):"

#-------------------------------------------------------------------------------
a=patternMatching( ['vincent', 'est un', 'doctorant'],['?x', 'est un', 'doctorant'] )
print "\t",a

#-------------------------------------------------------------------------------
b=patternMatching( ['vincent', 'est un', 'doctorant'],['?x', 'est un', '?y'] )
print "\t",b

#-------------------------------------------------------------------------------
a=patternMatching( ['vincent', 'est un', 'doctorant'] , 
		 ['vincent', 'est un', 'doctorant'] )
print "\t",a

#-------------------------------------------------------------------------------
b=patternMatching( ['vincent', 'est un', 'doctorant'],['?x', 'est un', '?x'])
print "\t",b

#-------------------------------------------------------------------------------
f=patternMatching( ['foo', 'jean', ['marc', 'bar', 'jean']],
		 ['foo', '?x', ['?y', 'bar', '?x']])
print "\t",f

#-------------------------------------------------------------------------------
g=patternMatching( ['foo', 'jean', ['marc', 'bar', 'paul']],
		 ['foo', '?x', ['?y', 'bar', '?x']] )
print "\t",g

#-------------------------------------------------------------------------------
c=patternMatching( ['vincent', 'est un', 'doctorant'],
		 ['?x', 'est un', 'doctorant'], 
		 {'?y':'doctorant'} )
print "\t",c

#-------------------------------------------------------------------------------
c=patternMatching( ['vincent', 'est un', 'doctorant'],
		 ['?x', 'est un', '?y'] , 
		 {'?y':'doctorant'} )
print "\t",c

#-------------------------------------------------------------------------------
d=patternMatching( ['vincent', 'est un', 'doctorant'], 
		 ['?x', 'est un','doctorant'], 
		'ECHEC' )
print "\t",d

#-------------------------------------------------------------------------------
e=patternMatching( 'vincent','?x',  'ECHEC' )
print "\t",e

#-------------------------------------------------------------------------------
e=patternMatching( 'vincent', '?x',{} )
print "\t",e


