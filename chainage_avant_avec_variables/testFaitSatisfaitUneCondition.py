## \file testFaitSatisfaitUneCondition.py
## \brief Batterie de tests pour la fonction faitSatisfaitUneCondition()
## \package testFaitSatisfaitUneCondition
## \brief Batterie de tests pour la fonction faitSatisfaitUneCondition()
##
## Teste la fonction faitSatisfaitUneCondition()

print "\ntest faitSatisfaitUneCondition:"

#--|Tests|----------------------------------------------------------------------

print faitSatisfaitUneCondition( ['pere','jean','paul'],
								 [['pere','?x','?y'],['pere','?y','?z']] )
print faitSatisfaitUneCondition( ['pere','jean','paul'],
								 [['fils','?x','?y'],['pere','?y','?z'],
			 					  ['mere','?x','?y']] )
print faitSatisfaitUneCondition( ['tonton','jean','paul'],
								 [['fils','?x','?y'],['pere','?y','?z'],
			 					 ['mere','?x','?y']] )
