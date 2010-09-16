## \file testInstantieVariables.py
## \brief Batterie de tests pour la fonction instantieVariables()
## \package testInstantieVariables
## \brief Batterie de tests pour la fonction instantieVariables()
##
## Teste la fonction instantieVariables()


print "\ntest instantieVariables:"

#--|Test|----------------------------------------------------------------------

print instantieVariables( ['?x',['?y', '?z']],
						  [{'?x':'X','?y':'Y'},{'?x':'X','?z':'Z'}] )