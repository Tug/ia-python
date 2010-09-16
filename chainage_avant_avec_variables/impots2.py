

##initialise la DB
print "|+| Chargement du fichier impots2" 
initDBs()

##ajoute des faits
print "\tAjout des faits",
ajouteFait(['add','0','0','0','0'])
ajouteFait(['add','100','100','0','0'])
ajouteFait(['add','100','0','100','0'])
ajouteFait(['add','200','100','100','0'])
ajouteFait(['add','200','0','200','0'])
ajouteFait(['add','300','100','200','0'])
ajouteFait(['add','50','0','0','50'])
ajouteFait(['add','150','100','0','50'])
ajouteFait(['add','150','0','100','50'])
ajouteFait(['add','250','100','100','50'])
ajouteFait(['add','250','0','200','50'])
ajouteFait(['add','350','100','200','50'])
ajouteFait(['add','100','0','0','100'])
ajouteFait(['add','200','100','0','100'])
ajouteFait(['add','200','0','100','100'])
ajouteFait(['add','300','100','100','100'])
ajouteFait(['add','300','0','200','100'])
ajouteFait(['add','400','100','200','100'])

##Paul
ajouteFait(['bas-salaire', 'Paul'])
ajouteFait(['loyer', 'Paul'] )
ajouteFait(['enfants', 'Paul'])
ajouteFait(['long-trajet', 'Paul'])

##Marc
ajouteFait(['moyen-salaire', 'Marc'])
ajouteFait(['loyer', 'Marc'] )
ajouteFait(['enfants', 'Marc'])
ajouteFait(['long-trajet', 'Marc'])

##Jean
ajouteFait(['haut-salaire', 'Jean'])
ajouteFait(['pas-de-loyer', 'Jean'] )
ajouteFait(['pas-d-enfants', 'Jean'])
ajouteFait(['long-trajet', 'Jean'])

print "\tOK"
##afficheFaits()

##ajoute des regles
print "\tAjout des regles",

##Reduction enfants
ajouteRegle([['pas-d-enfants', '?x']],['reduc-enfant', '0','?x'])
ajouteRegle([['enfants', '?x']],['reduc-enfant', '100','?x'])

##Reduction loyer
ajouteRegle([['bas-salaire', '?x'],['loyer', '?x']],['reduc-loyer', '200', '?x'])
ajouteRegle([['moyen-salaire', '?x'],['loyer', '?x']],['reduc-loyer', '100', '?x'])
ajouteRegle([['haut-salaire', '?x'],['loyer', '?x']],['reduc-loyer', '0', '?x'])
ajouteRegle([['bas-salaire', '?x'],['loyer', '?x']],['reduc-loyer', '200', '?x'])
ajouteRegle([['pas-de-loyer', '?x']],['reduc-enfant', '0','?x'])

##Reduction transport
ajouteRegle([['petit-trajet', '?x']],['reduc-trajet', '0', '?x'])
ajouteRegle([['reduc-enfant', '0','?x'],['long-trajet', '?x']],['reduc-trajet', '100', '?x'])
ajouteRegle([['reduc-loyer', '0','?x'],['long-trajet', '?x']],['reduc-trajet', '100', '?x'])
ajouteRegle([['reduc-enfant', '100','?x'],['reduc-loyer', '100', '?x'],['long-trajet', '?x']],['reduc-trajet', '50', '?x'])
ajouteRegle([['reduc-enfant', '100','?x'],['reduc-loyer', '200', '?x'],['long-trajet', '?x']],['reduc-trajet', '0', '?x'])

##Reduction totale
ajouteRegle([['reduc-enfant', '?a','?x'],['reduc-loyer', '?b', '?x'],['reduc-trajet','?c', '?x'],['add','?res','?a','?b','?c'] ],['reduc', '?res', '?x'])
print "\tOK"
##afficheRegles()

##Nouveau faits deduits
##['reduc-loyer', '200', 'Paul']
##['reduc-enfant', '100', 'Paul']
##['reduc-loyer', '100', 'Marc']
##['reduc-enfant', '100', 'Marc']
##['reduc-enfant', '0', 'Jean']
##['reduc-trajet', '0', 'Paul']
##['reduc-trajet', '50', 'Marc']
##['reduc-trajet', '100', 'Jean']
##['reduc', '300', 'Paul']
##['reduc', '250', 'Marc']