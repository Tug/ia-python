## \file testSubstitueVariables.py
## \brief Tests de substitutions pour la fonction substitueVariables().
## \package testSubstitueVariables
##
## Effectue des tests sur la fonction de substitutions de variables.
##
## Cette fonction effectue une serie de tests afin de determiner si la fonction
## substitueVariables fait les substitutions necessaires.

print "\nTest de la fonction substitueVariables(pattern,substitutions):" 

# substitutions
print "\t",substitueVariables(['?x', 'est un', 'doctorant'] , {})
print "\t",substitueVariables(['?x', 'est un', 'doctorant'] , {'?y':'michael'})
print "\t",substitueVariables(['?x', 'est un', 'doctorant'] , 		{'?x':'vincent','?y':'michael','?z':'paolo'})
print "\t",substitueVariables(['?w', 'est un', 'doctorant'] , {'?x':'vincent','?y':'michael','?z':'paolo'})
print "\t",substitueVariables(['?x', 'et', '?z', 'sont', 'doctorants'] , {'?x':'vincent','?y':'michael','?z':'paolo'})
print "\t",substitueVariables(['?x', 'est un', ['?x']] , {'?x':'vincent','?y':'michael','?z':'paolo'})
print "\t",substitueVariables(['?x', 'est un', ['?a']] , {'?x':'vincent','?y':'michael','?z':'paolo'})
print "\t",substitueVariables('?x', 
		{'?x':'vincent','?y':'michael','?z':'paolo'})
print "\t",substitueVariables('doctorant', 
		{'?x':'vincent','?y':'michael','?z':'paolo'})