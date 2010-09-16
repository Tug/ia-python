#-------------------------------------------------------------------------------
print "Algorithme de k-means"
print "\t@version: 1.2  date: 26/06/2007 modified by Thomas Leaute"
print "\t@version: 1.1  date: 25/05/2007 modified by Thomas Leaute"
print "\t@version: 1.0  date: 05/03/2007 created by Thomas Leaute"
print "\t@author: thomas.leaute _AT_ epfl.ch date: 09/05/2007"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------
## @package kMeans Algorithme de k-means

## @file kMeans.py Algorithme de k-means

import copy
exec file("distance.py")

## Noyaux de l'iteration precedente
VIEUXNOYAUX = []

## Liste des clusters courants
CLUSTERS = []

## \brief Affiche les clusters dans un format lisible
# @param clusters Liste des clusters a afficher
def afficheClusters (clusters):
	print "*********************"
	print "Clusters :"
	for cluster in clusters:
		if len(cluster) > 0:
			print "Donnees :", cluster[0]
			for donnee in cluster[1:]:
				print "         ", donnee
	print "*********************"

## \brief Associe chaque donnee au plus proche noyau
# @param noyaux Liste des noyaux
# @return La liste des clusters. La premiere donnee de chaque cluster est son noyau.
def formeClusters (noyaux):

	# Commence avec des clusters ne contenant que leur noyau
	clusters = [[noyau] for noyau in noyaux]

	for donnee in DONNEES:
		if donnee in noyaux:
			continue # Ignore les noyaux, ils ont deja ete traites

		# Selectionne le cluster dont le noyau est le plus proche de la donnee et ajoute la donnee a ce cluster
#		cluster = argmin(clusters, lambda c: distance(donnee, c[0])) # pour Python 2.3
		cluster = min(clusters, key = lambda c: distance(donnee, c[0])) # pour Python 2.x, x >= 4
		cluster.append(donnee)
	return clusters


## \brief Recentre le noyau d'un cluster passe en parametre.
#
# Le nouveau noyau est place en tete de la liste qui represente le cluster.
# @param cluster Le cluster dont le noyau doit etre recentre
# @return Le cluster dont le noyau a ete recentre
def recentreNoyau (cluster):
#	noyau = argmin(cluster, lambda x: sum([distance(donnee, x)**2 for donnee in cluster])) # pour Python 2.3
	noyau = min(cluster, key = lambda x: sum([distance(donnee, x)**2 for donnee in cluster])) # pour Python 2.x, x >= 4
	cluster.remove(noyau)
	cluster.insert(0, noyau)
	return cluster


## \brief Affiche les noyaux dans un format lisible
# @param noyaux Liste des noyaux a afficher
def afficheNoyaux (noyaux):
	if len(noyaux) > 0:
		print "Noyaux  :", noyaux[0]
		for noyau in noyaux[1:]:
			print "         ", noyau


## \brief Affiche le resultat du clustering, i.e. la liste des clusters
def afficheResultat ():
	afficheClusters(CLUSTERS)


## \brief Initialise l'algorithme
#
# Construit la liste \c CLUSTERS. Initialement, le premier cluster contient toutes les donnees (sauf les autres noyaux)
# @param k Nombre de clusters desires
# @param listeNoyaux Liste des noyaux. Si pas specifiee, prend les k premieres donnees comme noyaux
def chargeDonnees (k, listeNoyaux = None):
	global CLUSTERS

	noyaux = listeNoyaux
	if noyaux == None:
		# Par defaut on choisit les k premieres donnees comme noyaux
		noyaux = DONNEES[0:k]
		afficheNoyaux(noyaux)

	# Initialement, par defaut, affecte toutes les donnees au premier noyau :
	CLUSTERS = [ [noyau] for noyau in noyaux ]
	for donnee in DONNEES:
		if not donnee in noyaux:
			CLUSTERS[0].append(donnee)


## \brief Retourne la liste des noyaux
# @return La liste des premiers elements de chaque cluster
def retourneNoyaux ():
	return [cluster[0] for cluster in CLUSTERS]


## \brief Retourne si la liste de clusters passee en parametre est satisfaisante, ou s'il faut continuer a iterer
# @return True si la liste des noyaux n'a pas change depuis l'iteration precedente
def fini ():
	noyaux = retourneNoyaux()
	noyaux.sort()
	VIEUXNOYAUX.sort()
	return noyaux == VIEUXNOYAUX


## \brief Boucle principale qui met a jour les clusters
def reviseClusters ():
	global VIEUXNOYAUX, CLUSTERS

	noyaux = retourneNoyaux()
	VIEUXNOYAUX = copy.deepcopy(noyaux)

	# Forme les clusters autour des noyaux :
	CLUSTERS = formeClusters(noyaux)

	# Recentre le noyau de chaque cluster :
	CLUSTERS = [recentreNoyau(cluster) for cluster in CLUSTERS]
#	afficheClusters(CLUSTERS)


############################

# Charge la base de donnees :
exec file("maladies.py")
#exec file("profits.py")

# Initialise l'algorithme de k-means :
chargeDonnees(4)

# Lance l'agorithme de clustering :
exec file("clustering.py")

