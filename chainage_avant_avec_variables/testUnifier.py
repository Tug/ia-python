## \file testUnifier.py
## \brief Batterie de tests pour l'unificateur
## \package testUnifier
##
## Teste l'efficacite et la bonne marche de la methode d'unification.

print "test fonction unifier:" 

#--|Tests|----------------------------------------------------------------------

print "\t", unifier( ['?x', 'is a', 'doctorant'], 
					['vincent', 'is a', 'doctorant'] )
					
print "\t", unifier( ['vincent', 'is a', 'doctorant'],
					['?x', 'is a', 'doctorant'] )
					
print "\t", unifier( ['vincent', 'is a', '?y'],
					['?x', 'is a', 'doctorant'] )
					
print "\t", unifier( ['vincent', 'is a', 'doctorant'],
					['vincent', 'is a', 'doctorant'] )
					
print "\t", unifier( ['vincent', 'is a', 'doctorant'],
					['micheal', 'is a', 'doctorant'] )
					
print "\t", unifier( ['foo', '?x', ['?y', 'bar', 'jean']],
					['foo', 'jean', ['marc', 'bar', '?z']] )
					
print "\t", unifier( ['foo', '?x', ['?y', 'bar', 'jean']],
					['foo', 'jean', ['marc', 'bar', '?x']] )
					
print "\t", unifier( ['foo', '?x', ['?y', 'bar', 'paul']],
					['foo', 'jean', ['marc', 'bar', '?x']] )
					
print "\t", unifier( ['p', '?x', ['f', '?y']],['p', ['f','a'], '?x'] )
