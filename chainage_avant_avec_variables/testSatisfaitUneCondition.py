## \file testSatisfaitUneCondition.py
## \brief Batterie de tests pour la fonction satisfaitUneCondition()
## \package testSatisfaitUneCondition
## \brief Batterie de tests pour la fonction satisfaitUneCondition()
##
## Teste la fonction satisfaitUneCondition()

print "\ntest satisfaitUneCondition:"

#--|Test|-----------------------------------------------------------------------

faits=[['a', 'and', 'b'],['b', 'and', 'b']]
print satisfaitUneCondition(['?x', 'and','b'],[{'?y':'b'}])
