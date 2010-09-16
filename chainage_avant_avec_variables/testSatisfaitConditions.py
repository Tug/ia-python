## \file testSatisfaitConditions.py
## \brief Batterie de tests pour la fonction satisfaitConditions()
## \package testSatisfaitConditions
## \brief Batterie de tests pour la fonction satisfaitConditions()
##
## Teste la fonction satisfaitConditions()

print "\ntest satisfaitConditions:"

#--|Tests|----------------------------------------------------------------------

faits=[['a', 'and', 'b'],['b', 'and', 'b']]
print satisfaitConditions( [['?x', 'and','?y'],['?x', 'and','?x']],{'?y':'b'} )

faits=[['a', 'and', 'b'],['b', 'and', 'b']]
print satisfaitConditions( [['?z', 'and','?y'],['?x', 'and','?z']],{'?y':'b'} )

faits=[['a', 'and', 'b'],['b', 'and', 'c']]
print satisfaitConditions( [['?x', 'and','?y'],['?x', 'and','?x']],{'?y':'b'} )