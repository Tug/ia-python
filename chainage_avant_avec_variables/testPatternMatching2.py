## \file testPatternMatching2.py
## \brief Batterie de tests pour l'unificateur
## \package testPatternMatching2
## \brief Batterie de tests pour l'unificateur
##
## Teste l'efficacite et la bonne marche de la fonction patternMatching.

print "\ntest patternMatching:" 

#-|Tests|-----------------------------------------------------------------------

print "\t", patternMatching( ['?x', 'is a', 'doctorant'], 
						 ['vincent', 'is a', 'doctorant'] )
						 
print "\t", patternMatching( ['vincent', 'is a', 'doctorant'],
						 ['?x', 'is a', 'doctorant'] )
						 
print "\t", patternMatching( ['vincent', 'is a', '?y'],
						 ['?x', 'is a', 'doctorant'] )
						 
print "\t", patternMatching( ['vincent', 'is a', 'doctorant'],
						 ['vincent', 'is a', 'doctorant'] )
						 
print "\t", patternMatching( ['vincent', 'is a', 'doctorant'],
						 ['michael', 'is a', 'doctorant'] )
						 
print "\t", patternMatching( ['foo', '?x', ['?y', 'bar', 'jean']],
						 ['foo', 'jean', ['marc', 'bar', '?z']] )
						 
print "\t", patternMatching( ['foo', '?x', ['?y', 'bar', 'jean']],
						 ['foo', 'jean', ['marc', 'bar', '?x']] ,{'?y':'marc'})
						 
print "\t", patternMatching( ['foo', '?x', ['?y', 'bar', 'paul']],
						 ['foo', 'jean', ['marc', 'bar', '?x']] ,{})
						 
print "\t", patternMatching( ['frere', '?x', '?y'],
						 ['frere', '?y', '?z'],
		   				 {'?z':'?x'} )
