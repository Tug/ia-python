#-------------------------------------------------------------------------------
print "Algorithme de clustering hierarchique"
print "\t@version: 1.2  date: 26/05/2007 modified by Thomas Leaute"
print "\t@version: 1.1  date: 25/05/2007 modified by Thomas Leaute"
print "\t@version: 1.0  date: 05/03/2007 created by Thomas Leaute"
print "\t@author: thomas.leaute _AT_ epfl.ch date: 09/05/2007"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------
## @package clusteringHierarchique Algorithme de clustering hierarchique, par single-link et complete-link

## @file clusteringHierarchique.py Algorithme de clustering hierarchique, par single-link et complete-link

exec file("distance.py")

## "single-link" ou "complete-link" 
METHODE = "" 

## liste des noeuds de dendogramme restant a fusionner
NOEUDS = [] 

##  \brief Cette classe represente un noeud dans un dendogramme de clusters
class Noeud:

	## @var profondeur 
	# \brief Profondeur du noeud dans le dendogramme
	
	## @var successeurs 
	# \brief Liste des successeurs du noeud dans le dendogramme
	
	## @var cluster 
	# \brief Cluster associe a ce noeud
	
	## \brief Constructeur
	# @param self Reference vers l'objet
	# @param p Profondeur du noeud dans le dendogramme
	# @param succ Liste des successeurs du noeud
	# @param c Cluster associe a ce noeud. Si pas precise, construit le cluster comme l'union des clusters des successeurs
	def __init__ (self, p, succ, c = None):
		self.profondeur = p
		self.successeurs = succ
		if c != None:
			self.cluster = c
		else:
			self.cluster = [ donnee for noeud in self.successeurs for donnee in noeud.cluster ]
	
	## \brief Affiche le dendogramme qui a ce noeud pour racine
	# @param self Reference vers l'objet
	# @param prefixe (optionnel) String a utiliser comme prefixe en debut de chaque ligne
	def afficheDentogramme (self, prefixe = ""):
		print prefixe + str(self.cluster)
		for i in range(0, len(self.successeurs)):
			print prefixe + "|\n" + prefixe + "|"
			trait = "---" + "".join(["---" for j in range(0, self.successeurs[i].profondeur - self.profondeur - 1)])
			marge = "".join(["   " for j in range(0, self.successeurs[i].profondeur - self.profondeur - 1)])
			if i == len(self.successeurs)-1:
				marge = "   " + marge
			else:
				marge = "|  " + marge
			print prefixe + trait
			self.successeurs[i].afficheDentogramme(prefixe + marge)
		

## \brief Initialise l'algorithme
# 
# Transforme les donnees en une liste de noeuds, chaque noeud correspondant a un cluster contenant une unique donnee
# @param methode Methode utilisee ("complete-link" ou "single-link") 
def chargeDonnees (methode):
	global NOEUDS, METHODE
	METHODE = methode
	NOEUDS = [ Noeud(len(DONNEES), [], [donnee]) for donnee in DONNEES ]


## \brief Retourne si tous les clusters ont ete fusionnes  
# @return True si et seulement si \c NOEUDS ne contient plus qu'un seul noeud
def fini ():
	return len(NOEUDS) <= 1
	
	
## \brief Distance entre deux clusters 
# 
# Consulte la valeur de \c METHODE pour decider de la methode de calcul de la distance
# @param cluster1 Premier cluster
# @param cluster2 Deuxieme cluster
# @return La distance entre \c cluster1 et \c cluster2
def distanceClusters (cluster1, cluster2):
	if METHODE == "single-link":
		return min([ distance(donnee1, donnee2) for donnee1 in cluster1 for donnee2 in cluster2 ])
	elif METHODE == "complete-link":
		return max([ distance(donnee1, donnee2) for donnee1 in cluster1 for donnee2 in cluster2 ])
	else:
		print "Methode de calcul de la distance entre clusters '" + METHODE + "' inconnue"
		return None
	
	
## \brief Fusionne les deux clusters les plus similaires dans la liste \c NOEUDS
def reviseClusters ():

	# S'il y a strictement moins de 2 noeuds :
	if len(NOEUDS) <= 1:
		return 
	
	# Sinon (plus de 2 noeuds), trouve les 2 noeuds dont les clusters sont les plus similaires :
	pairesDeNoeuds = [ [NOEUDS[i], NOEUDS[j]] for i in range(0, len(NOEUDS)-1) for j in range(i+1, len(NOEUDS)) ]
#	paireMin = argmin(pairesDeNoeuds, lambda paire: distanceClusters(paire[0].cluster, paire[1].cluster)) # pour Python 2.3 
	paireMin = min(pairesDeNoeuds, key = lambda paire: distanceClusters(paire[0].cluster, paire[1].cluster)) # pour Python 2.x, x >= 4 
				
	# Fusionne les deux clusters trouves pour former un nouveau noeud : 
	NOEUDS.remove(paireMin[0])
	NOEUDS.remove(paireMin[1])
	NOEUDS.append(Noeud(len(NOEUDS) + 1, [paireMin[0], paireMin[1]]))
				

## \brief Affiche le resultat du clustering, i.e. le dendogramme obtenu
def afficheResultat (): 
	NOEUDS[0].afficheDentogramme()


############################

# Charge la base de donnees :
#exec file("maladies.py")
exec file("profits.py")

# Initialise l'algorithme de clustering hierarchique :
chargeDonnees("single-link") 
#chargeDonnees("complete-link") 

# Lance l'agorithme de clustering :
exec file("clustering.py")
