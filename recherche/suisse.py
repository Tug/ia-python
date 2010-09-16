###-------------------------------------------------------------------
##   Fichier pris depuis topo.xml de la platforme LogistAgent
##   par Radu Jurca
###-------------------------------------------------------------------


###-------------------------------------------------------------------
##   Les villes.  
###-------------------------------------------------------------------

villes=Villes()
villes.construitVille( "Lausanne", 110, 260 )
villes.construitVille( "Geneve", 40, 300 )
villes.construitVille( "Sion", 200, 300 )
villes.construitVille( "Neuchatel", 150, 170 )
villes.construitVille( "Bern", 210, 280 )
villes.construitVille( "Basel", 230, 65 )
villes.construitVille( "Fribourg", 175, 200 )
villes.construitVille( "Zurich", 340, 90 )
villes.construitVille( "Aarau", 290, 95 )
villes.construitVille( "Luzern", 320, 155 )
villes.construitVille( "St-Gallen", 455, 85 )
villes.construitVille( "Thun", 235, 210 )
print "\tVilles ajoutees"


###-------------------------------------------------------------------
##   Les routes.
###-------------------------------------------------------------------

villes.construitRoute( "Lausanne", "Geneve" )
villes.construitRoute( "Sion", "Lausanne" )
villes.construitRoute( "Neuchatel", "Lausanne" )
villes.construitRoute( "Fribourg", "Lausanne" )
villes.construitRoute( "Fribourg", "Bern" )
villes.construitRoute( "Sion", "Thun" )
villes.construitRoute( "Neuchatel", "Bern" )
villes.construitRoute( "Basel", "Bern" )
villes.construitRoute( "Zurich", "Aarau" )
villes.construitRoute( "Zurich", "Luzern" )
villes.construitRoute( "Bern", "Aarau" )
villes.construitRoute( "Bern", "Luzern" )
villes.construitRoute( "Luzern", "Aarau" )
villes.construitRoute( "St-Gallen", "Zurich" )
villes.construitRoute( "Thun", "Bern" )
villes.construitRoute( "Basel", "Zurich" )
print "\tRoutes ajoutees"


###-------------------------------------------------------------------
###                         FIN DU FICHIER
###-------------------------------------------------------------------
