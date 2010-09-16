#-------------------------------------------------------------------------------
print "Chargement du module de recherche"
print "\t@version: 1.3  date: 28/06/2007 modified by Thomas Leaute"
print "\t@version: 1.2  date: 15/01/2007 modified by Vincent Schickel-Zuber"
print "\t@version: 1.1  date: 15/01/2007 modified by Bruno Alves"
print "\t@version: 1.0  date: 24/03/2006 modified by the author"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 24/03/2006"
print "\t@copyright: EPFL-IC-IIF-LIA 2006"
#-------------------------------------------------------------------------------

# modules necessaires
import libRecherche
import copy

# constante signifiant un echec
ECHEC='echec'

## Dictionnaire contenant toutes les villes
CARTE={}


#-------------------------------------------------------------------------------
# DEFINITIONS
#-------------------------------------------------------------------------------


## Exception pour le cas ou une ville n'est pas trouvee
#
# La class VILLE_PAS_TROUVEE est derivee de la classe base Exception. Elle
# est elle-meme une exception, et sert a indiquer lorsqu'une ville n'est
# pas trouvee.
class VILLE_PAS_TROUVEE(Exception):
	
	## @var nom
	# le nom de la ville recherchee
		
	## Constructeur de la classe VILLE_PAS_TROUVEE
	#
	# Initialise les parametres de la classe. Dans ce cas, une exception ne
	# contient que le nom de la ville que l'on cherche.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] nom le nom de la ville que l'on cherche et qui n'a pas
	#				ete trouvee 
	def __init__( self, nom ):
		
		## le nom de la ville recherchee
		self.nom = nom


## Represente un noeud du graphe des villes
#
# Ville est une sousclasse de la classe Element representant le noeud
# d'un graphe.
class Ville(libRecherche.Element):
	
	## Constructeur de la classe Ville 
	# 
	# Initialise la classe ville. La classe ville est une descendante de
	# Element qui definit un noeud d'un graphe.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] nom le nom de l'objet 
	# @param[in] posX la position sur l'axe X
	# @param[in] posY la position sur l'axe Y
	# @note le nom de la ville est utilise comme identificateur, il doit
	#	   pour cela etre \b unique
	def __init__ ( self, nom, posX, posY ):
		libRecherche.Element.__init__( self, nom, posX, posY )


	## Retourne une representation texte de la ville
	#
	# Cette methode retourne une representation texte des principales
	# donnees concernant la ville. L'affichage se fait selon le format:
	# @code
	# ville<nom_de_ville, x, y>
	#	voisins = { ville<...>, ville<...> }
	# @endcode
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] self pointeur vers l'objet lui-meme 
	# @return une chaine de caracteres contenant la representation texte
	def __repr__ ( self ):
		out = ("ville <%s,(%d,%d)>\n" % (self.nom, self.posX,self.posY))
		out = out+"\t voisins={"
		for voisin in self.voisins:
			out=out+" "+voisin.nom
		out = out+"}"
		return out


## Representation d'un graphe de villes
#
# Le graphe est represente par les relations de voisinage entre 
# les villes. Toutes les villes sont ajoutees dans le dictionnaire CARTE
class Villes:
	
	## Constructeur de la classe
	#
	# Instantie un attribut villes qui sera un dictionnaire avec  
	# clef=ville.nom et la valeur=objet_ville
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	def __init__( self ):
		global CARTE
		CARTE={}


	## Construit et ajoute la ville au dictionnaire villes		
	#
	# Cette methode commence par construire un noeud ville, en lui
	# indiquant son nom et sa position dans le plan. Ensuite, si
	# la ville n'existe pas encore dans le dictionnaire, elle est ajoutee
	# sous la clef ville.nom
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] nom le nom de la ville
	# @param[in] posX la position de la ville sur l'axe X
	# @param[in] posY la position de la ville sur l'axe Y
	def construitVille( self, nom, posX, posY ):
		ville = Ville(nom, posX,posY) # cree une nouvelle ville 
		# n'ajoute la ville que si elle n'existe pas encore
		if nom in CARTE:
			print "La ville", ville," existe deja dans le graphe"
		else:
			CARTE[nom]=ville
			
	## Cherche et retourne une ville associee a un nom donne
	#
	# Cette methode se contente de retourner le noeud associe au nom
	# passe en parametre, si ce nom est deja dans le dictionnaire. Si 
	# ce n'est pas le cas, alors \c chercheVille() leve une exception
	# du type VILLE_PAS_TROUVEE. Cette exception contient le nom de la
	# ville qui n'a pas ete trouvee
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] nom le nom de la ville
	# @return Un pointeur vers le noeud recherche s'il existe, -1 sinon
	# @exception Retourne une exception du type VILLE_PAS_TROUVEE pour signifier
	#			que la ville en question n'a pas ete trouvee
	def chercheVille( self, nom ):
		if nom in CARTE:
			return CARTE[nom]
		else:
			raise VILLE_PAS_TROUVEE(nom)


	## Definit une route (un arc) entre deux villes
	#
	# Un arc dans un graphe est defini par une relation de voisinage. On
	# determine s'il existe une route entre deux villes, si chacune est 
	# presente dans le liste des voisins de l'autre. Donc, pour creer
	# une route entre les deux, il suffit de les ajouter en tant que voisins
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] nom_ville1 le nom de la premiere ville
	# @param[in] nom_ville2 le nom de la deuxieme ville
	def construitRoute( self, nom_ville1, nom_ville2 ):
		try:
			# creer une route entre deux villes consiste
			# simplement a definir une relation de voisinage
			# entre deux villes voisines
			ville1 = self.chercheVille(nom_ville1)
			ville2 = self.chercheVille(nom_ville2)
			ville1.ajouteVoisin(ville2)
			ville2.ajouteVoisin(ville1)
		except VILLE_PAS_TROUVEE, e:
			print "La Ville", e.nom, "n'existe pas"


	## Imprime toutes les villes avec leurs connections(voisins)
	#
	# Imprime la liste des villes contenues dans le dictionnaire CARTE
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	def imprimeLesVilles( self ):
		for ville in CARTE:
			print CARTE[ville]


#-------------------------------------------------------------------------------
# ALGORITHMES DE RECHERCHE
#-------------------------------------------------------------------------------

## Algorithme de recherche
#
# Cette fonction de recherche permet de faire trois types de recherche:
#
# \li \c DFS pour la recherche en profondeur d'abord.
# \li \c BFS pour la recherche en largeur d'abord.
# \li \c A* pour la recherche heuristique
#
# L'algorithme de recherche est le suivant :
#
# @code
# Recherche(Noeud_depart, Noeud_but, methode)
#	1. Q <- [Noeud_depart] 
#	2. while Q non vide:
#	3.	 n <- premier(Q), Q <- reste(Q)
#	4.	 if n est un noeud but:
#	5.	   return n
#   6.	 else:
#   7.	   S <- successeurs de n
#   8.	   Q <- ajouterSuccesseurs(Q,S,methode)
#	9. return ECHEC.
# @endcode
#
# @param[in] depart ville de depart
# @param[in] but ville d'arrivee
# @param[in] methode la methode utilisee (DFS,BFS,A*)
# @return n si c'est un noeud but, ECHEC sinon
# @note Le seul changement entre les diverses methodes de recherche est la
#	   facon d'ajouter les successeurs dans Q.
#	   \li \c DFS on ajoute S+Q
#		\li \c BFS on ajoute Q+S
#		\li \c A* on ajoute Q+S et on trie par ordre croissant de \f$f_{n}\f$
def recherche( depart, but, methode ):
	
	# initialise la liste avec le noeud de depart
	Q=[libRecherche.Noeud(depart)]
	
	# initialise le compteur d'iterations
	nbIteration=1
	
	# boucle jusqu'a ce que Q soit vide
	while len(Q) > 0:
		
		# selectionne le premier noeud de la liste 
		n = Q.pop(0)
		
		# si on a une solution, on l'imprime et la retourne
		if n.estUneSolution(but):
			print "Solution a l'iteration ",nbIteration,":",n
			return n
		
		# sinon, on augmente le compteur d'iterations et on ajoute
		# les successeurs dans la liste Q selon la methode de recherche
		else:
			nbIteration+=1
			print "Iteration ", nbIteration, ":", n
			S = n.successeurs(but)
			Q = ajouteSuccesseurs(Q, S, methode)
				
	# plus de noeud dans la liste Q
	return ECHEC
				
				
## Algorithme de recherche optimisee
#
# L'algorithme de recherche optimisee est tres similaire a celui d'une recherche
# normale, la grande difference etant que l'on ne visite un noeud qu'une seule 
# fois. Pour cela, on garde la liste C qui contient tous les noeuds deja
# visites. 
#
# @code
#RechercheOptimisee(Noeud_depart, Noeud_but, methode)
#	1.  Q <- [Noeud_depart] 
#	2.  C <- [] 
#	3.  while Q non vide:
#	4.	  n <- premier(Q), Q <- reste(Q)
#	5.	  if n est un noeud but:
#   6.	    return n
#   7.	  else:
#   8.	    if (n not in C and methode is not "A*") or 
#   ...(n=n' in C and f(n)<f(n') and methode is  "A*"):
#   9.		  S <- successeurs de n
#   10.		  Q <- ajouterSuccesseurs(Q,S,methode)
#   11.		  ajoute n dans C
#	12. return ECHEC
# @endcode
#
# @param[in] depart ville de depart
# @param[in] but ville d'arrivee
# @param[in] methode la methode utilisee (DFS,BFS,A*)
# @note Une variante est necessaire pour A*. En effet, un noeud peut etre 
#	   deja contenu dans la liste. Cependant, si son cout est superieur a
#	   celui trouve par un autre chemin, on met a jour celui-ci
def rechercheOptimisee(depart, but, methode):
	
	# liste initiale contenant les noeuds en cours. initialisee
	# avec le noeud de depart
	Q =[libRecherche.Noeud(depart)]
	
	# liste des noeuds deja visites 
	C = libRecherche.Noeuds()
	
	# initialise le compteur d'iterations
	nbIteration=1
	
	# itere jusqu'a ce que Q soit vide ou 
	# que l'on trouve un noeud but
	while len(Q) > 0:
		
		# extrait le premier noeud de la liste 
		n = Q.pop(0)
		
		# si celui-ci est une solution, on l'imprime et le retourne 
		if n.estUneSolution(but):
			print "Solution a l'iteration ",nbIteration,":",n
			return n
		
		# sinon, on parcourt ses successeurs en s'assurant que le noeud
		# n n'existe pas deja dans la liste ou, si c'est le cas, a un cout 
		# inferieur
		else:
			if (not C.contient(n) and methode is not "A*") or (C.contient(n) 
				and C.coutFStrictementInferieur(n) and methode is "A*")  :
				
				# affiche l'iteration en cours
				print "Iteration ", nbIteration, ":", n
				
				# incremente le compteur d'iterations
				nbIteration+=1
				
				# ajoute le noeud dans la liste des noeuds visites 
				C.ajouteNoeud( n )
				
				# ajoute ses successeurs selon la methode choisie 
				S=n.successeurs( but )
				Q=ajouteSuccesseurs( Q, S, methode )
					
	# plus d'elements dans Q
	return ECHEC


## Ajoute les successeurs S dans la liste Q
#
# Ajoute les succeseurs S a Q suivant la methode de recherche.
#
# @param[in] Q la liste initiale
# @param[in] S la liste des successeurs
# @param[in] methode la methode de recherche { DFS, BFS, A* }
def ajouteSuccesseurs(Q,S,methode):
	
	# DFS - ajoute les successeurs en tete de liste
	if methode=="DFS":
		return S+Q
	
	# BFS - ajoute les successeurs en queue de liste 
	elif methode=="BFS":
		return Q+S
	
	# A* - ajoute les successeurs en queue de liste et trie la
	#	  liste par ordre decroissant de cout 
	elif methode=="A*":
		Q = Q+S
		Q.sort(key = lambda n : n.coutF)
		return Q
	
	# La methode n'existe pas 
	else:
		print "Methode ", methode," inconnue"


#-------------------------------------------------------------------------------
# CREATION DU GRAPHE
#-------------------------------------------------------------------------------

# creation du graphe
exec file( "carte.py" )
#exec file( "suisse.py" )

# imprime la liste des villes 
villes.imprimeLesVilles()

# choisit comme ville de depart A et comme ville d'arrivee P
start=villes.chercheVille( "A" )
print "Debut=", start
fin = villes.chercheVille( "P" )
print "But=", fin

# choisit comme ville de depart Zurich et comme ville d'arrivee Geneve
#start=villes.chercheVille( "Zurich" )
#print "Debut=", start
#fin = villes.chercheVille( "Geneve" )
#print "But=", fin

# affiche les resultats des divers algorithmes de recherche 
# !! Attention !! DFS boucle indefiniment avec suisse.py !!, le mettre
# en commentaire pour tester 
print "\nRecherche avec DFS=\n", recherche( start, fin, "DFS" )
print "\nRecherche avec BFS=\n", recherche( start, fin, "BFS" )
print "\nRecherche optimisee avec BFS=\n", rechercheOptimisee( start,fin,"BFS" )
print "\nRecherche avec A*=\n", recherche( start, fin, "A*" )
print "\nRecherche optimisee avec A*=\n", rechercheOptimisee( start, fin, "A*" )
