#-------------------------------------------------------------------------------
# INITIALISATION
#-------------------------------------------------------------------------------
print "|+| Chargement du fichier impots" 
initDBs()

#-------------------------------------------------------------------------------
# TEST 1
#-------------------------------------------------------------------------------
print "\tAjout des faits...",
ajouteFait( 'bas-salaire' )
ajouteFait( 'loyer' )
ajouteFait( 'enfants' )
ajouteFait( 'long-trajet' )
print "\tOK"

#-------------------------------------------------------------------------------
# TEST 2
#-------------------------------------------------------------------------------
# print "\tAjout des faits...",
# ajouteFait( 'pas-d-enfants' )
# ajouteFait( 'pas-de-loyer' )
# ajouteFait( 'haut-salaire' )
# ajouteFait( 'long-trajet' )
# print "\tOK"

#-------------------------------------------------------------------------------
# AJOUT DES REGLES
#-------------------------------------------------------------------------------
print "\tAjout des regles...",
ajouteRegle( ['pas-d-enfants'], 'reduc-enfant-0' )
ajouteRegle( ['enfants'], 'reduc-enfant-100' )
ajouteRegle( ['bas-salaire'], 'reduc-loyer-200' )
ajouteRegle( ['moyen-salaire'], 'reduc-loyer-100' )
ajouteRegle( ['haut-salaire'], 'reduc-loyer-0' )
ajouteRegle( ['pas-loyer'], 'reduc-loyer-0' )
ajouteRegle( ['petit-trajet'], 'reduc-trajet-0' )
ajouteRegle( ['reduc-enfant-0', 'long-trajet'], 'reduc-trajet-100' )
ajouteRegle( ['reduc-loyer-0', 'long-trajet'], 'reduc-trajet-100' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-100', 'long-trajet'], 'reduc-trajet-50' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-200', 'long-trajet'], 'reduc-trajet-0' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-0', 'reduc-trajet-0'], 'reduc-0' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-0', 'reduc-trajet-0'], 'reduc-100' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-100', 'reduc-trajet-0'], 'reduc-100' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-100', 'reduc-trajet-0'], 'reduc-200' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-200', 'reduc-trajet-0'], 'reduc-200' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-200', 'reduc-trajet-0'], 'reduc-300' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-0', 'reduc-trajet-50'], 'reduc-50' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-0', 'reduc-trajet-50'], 'reduc-150' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-100', 'reduc-trajet-50'], 'reduc-150' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-100', 'reduc-trajet-50'], 'reduc-250' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-200', 'reduc-trajet-50'], 'reduc-250' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-200', 'reduc-trajet-50'], 'reduc-350' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-0', 'reduc-trajet-100'], 'reduc-100' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-0', 'reduc-trajet-100'], 'reduc-200' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-100', 'reduc-trajet-100'], 'reduc-200' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-100', 'reduc-trajet-100'], 'reduc-300' )
ajouteRegle( ['reduc-enfant-0', 'reduc-loyer-200', 'reduc-trajet-100'], 'reduc-300' )
ajouteRegle( ['reduc-enfant-100', 'reduc-loyer-200', 'reduc-trajet-100'], 'reduc-400' )
print "\tOK"

