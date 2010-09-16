## \file testFiltrer.py
## \brief Tests pour la fonction filtrer().
## \package testFiltrer
## Effectue des tests sur la fonction filtrer(datum,pattern):
##
## Cette fonction permet de tester si la fonction filtrer effectue le filtrer
## correctement selon les specifications. Divers aspects sont testes:
##
##   - filtrer d'un proposition sous forme d'atome
##	- filtrer d'une position complexe(composee d'atomes)
## 	- filtrer sans variables avec propositions identiques
##	- filtrer d'une proposition complexe(avec sous-listes)
##	- filtrer avec proposition differentes
##	- filtrer avec reutilisation d'une meme variable dans pattern
print "\nTest de la fonction filtrer(datum,pattern):"

#-------------------------------------------------------------------------------
j=filtrer('vincent', '?x')
print "\t",j

#-------------------------------------------------------------------------------
a=filtrer(['vincent', 'est un', 'doctorant'],['?x', 'est un', 'doctorant'] )
print "\t", a

#-------------------------------------------------------------------------------
b=filtrer( ['vincent', 'est un', 'doctorant'],
			['?x', 'est un', '?y'] )
print "\t", b

#-------------------------------------------------------------------------------
c=filtrer( ['vincent', 'est un', 'doctorant'], 
			['vincent', 'est un', 'doctorant'] )
print "\t", c

#-------------------------------------------------------------------------------
d=filtrer(['vincent', 'est un', 'doctorant',['vincent', 'est un', 'doctorant']] 
		 ,['vincent', 'est un', 'doctorant',['vincent', 'est un', 'doctorant']])
print "\t",d

#-------------------------------------------------------------------------------
e=filtrer(['vincent', 'est un', 'doctorant'],
		['vincent', 'est un', 'doctorant',['vincent', 'est un', 'doctorant']])
print "\t",e

#-------------------------------------------------------------------------------
f=filtrer( ['vincent', 'est un', 'doctorant'] , 
		    ['paolo', 'est un', 'doctorant'])
print "\t",f

#-------------------------------------------------------------------------------
g=filtrer( ['vincent', 'est un','doctorant','paolo', 'est un', 'doctorant'],
		    ['?x', 'est un', '?y','?z', 'est un', '?v'])
print "\t",g

#-------------------------------------------------------------------------------
h=filtrer( ['vincent', 'est un', 'vincent'], ['?x', 'est un', '?x'] )
print "\t",h

#-------------------------------------------------------------------------------
i=filtrer( ['vincent', 'est un', 'doctorant'], ['?x', 'est un', '?x'] )
print "\t",i
