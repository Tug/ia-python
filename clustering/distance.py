#-------------------------------------------------------------------------------
print "Distance entre deux donnees"
print "\t@version: 1.1  date: 05/03/2007 modified by Thomas Leaute"
print "\t@version: 1.0  date: 05/03/2007 created by Thomas Leaute"
print "\t@author: thomas.leaute _AT_ epfl.ch date: 09/05/2007"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------
## @package distance Distance entre deux donnees

## @file distance.py Distance entre deux donnees

## \brief Distance entre deux donnees 
# 
# Retourne le nombre d'elements differents 
# @param donnee1 Premiere donnee
# @param donnee2 Deuxieme donnee
# @return La distance entre \c donnee1 et \c donnee2
def distance (donnee1, donnee2):
	dist = 0
	for i in range(0, len(donnee1)):
		if not donnee1[i] == donnee2[i]:
			dist = dist + 1
	return dist
	

## \brief Fonction argmin
# 
# Cette fonction retourne l'element d'une liste qui minimise la fonction passee en parametre. 
# Elle n'est utile que pour Python 2.3, sinon on peut utiliser la fonction min() a partir de 2.4. 
# Retourne \c None si la liste est vide. 
# @param liste Une liste dont on cherche l'element optimal
# @param fn Fonction a minimiser 
# @return L'element de la liste \c liste qui minimise la fonction \c fn
def argmin (liste, fn):
	if liste == []:
		return None
	e0 = liste[0] 
	f0 = fn(e0) 
	for e in liste[1:]:
		fe = fn(e)
		if fe < f0:
			e0 = e
			f0 = fe
	return e0