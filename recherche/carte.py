###-------------------------------------------------------------------
##   Les villes.  
###-------------------------------------------------------------------
villes=Villes()
villes.construitVille("A", 0, 16)
villes.construitVille("B", 5, 13)
villes.construitVille("C", 0, 10)
villes.construitVille("D", 5, 8)
villes.construitVille("E", 11, 18)
villes.construitVille("F", 15, 13)
villes.construitVille("G", 29, 18)
villes.construitVille("H", 26, 0)
villes.construitVille("I", 12, 10)
villes.construitVille("J", 17, 7)
villes.construitVille("K", 11, 3)
villes.construitVille("L", 22, 16)
villes.construitVille("M", 25, 12)
villes.construitVille("N", 24, 6)
villes.construitVille("O", 20, 0)
villes.construitVille("P", 5, 0)
print "\tVilles ajoutees"


###-------------------------------------------------------------------
##   Les routes.
###-------------------------------------------------------------------

villes.construitRoute("A","B")
villes.construitRoute("A","E")
villes.construitRoute("B","C")
villes.construitRoute("B","E")
villes.construitRoute("B","D")
villes.construitRoute("C","D")
villes.construitRoute("C","P")
villes.construitRoute("D","I")
villes.construitRoute("D","K")
villes.construitRoute("E","F")
villes.construitRoute("E","L")
villes.construitRoute("F","I")
villes.construitRoute("F","L")
villes.construitRoute("F","M")
villes.construitRoute("G","H")
villes.construitRoute("G","L")
villes.construitRoute("G","M")
villes.construitRoute("I","J")
villes.construitRoute("J","K")
villes.construitRoute("J","N")
villes.construitRoute("K","O")
villes.construitRoute("K","P")
villes.construitRoute("M","N")
villes.construitRoute("N","O")
villes.construitRoute("B","I")
villes.construitRoute("B","F")
villes.construitRoute("P","O")
print "\tRoutes ajoutees"
###-------------------------------------------------------------------
###                         FIN DU FICHIER
###-------------------------------------------------------------------
