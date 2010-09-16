## \file testSubstitueVariables2.py
## \brief Batterie de tests pour la fonction substitueVariables()
## \package testSubstitueVariables2
##
## Teste la fonction substitueVariables()

print "test substitueVariables:" 

#--|Tests|----------------------------------------------------------------------

print "\t", substitueVariables( ['?x', 'est un', 'doctorant'],{} )
print "\t", substitueVariables( ['?x', 'est un', 'doctorant'],{'?y':'michael'} )
print "\t", substitueVariables( ['?x', 'est un', 'doctorant'],{'?x':'vincent'} )
print "\t", substitueVariables( ['foo', '?x', '?z'], 
							    {'?y':'bar','?x':'?y','?z':'45' } )
print "\t", substitueVariables( ['p', '?x'] , {'?y':'a','?x':['f','?y']} )
print "\t", substitueVariables( ['p', '?x'] , 
							    {'?y':['g','?z'], '?x':['f','?y'], '?z':['a']} )
print "\t", substitueVariables( ['p', '?x'] ,
							    {'?y':['g','?z'],'?x':['f','?y'],'?z':['?q']} )