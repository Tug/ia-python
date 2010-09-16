#-------------------------------------------------------------------------------
print "Chargement du module objet et noeud pour la recherche"
print "\t@version: 1.3  date: 13/06/2007 modified by Thomas Leaute"
print "\t@version: 1.2  date: 13/02/2007 modified by Vincent Schickel-Zuber"
print "\t@version: 1.1  date: 15/01/2007 modified by Bruno Alves"
print "\t@version: 1.0  date: 24/03/2006 modified by the author"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 24/03/2006"
print "\t@copyright: EPFL-IC-IIF-LIA 2006-2007"
#-------------------------------------------------------------------------------

# modules utilises
import math
import copy


## Represente un noeud d'un graphe
#
# La classe Element correspond a un simple noeud d'un graphe. Dans ce cas
# il s'agira d'un graphe de villes. Donc un element sera une ville.
class Element:
	
	## @var nom
	## le nom de cet element 

	## @var posX
	## la position horizontale de cet element 
	
	## @var posY
	## la position verticale de cet element 
	
	## @var voisins
	## la liste des voisins attaches a celui-ci
		
	## Constructeur de la classe 
	# 
	# Initialise l'objet Element representant un noeud sur un graphe, en
	# lui associant un nom et une position sur un plan 2-D. La liste de
	# ses voisins est initialement vide
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] nom le nom a donner a cet element
	# @param[in] posX la position du noeud sur l'axe X
	# @param[in] posY la position du noeud sur l'axe Y
	# @note le parametre nom est utilise comme indentificateur est doit
	#	   pour cela etre <strong>unique</strong>!
	def __init__( self, nom, posX, posY ):
		
		## le nom de cet element 
		self.nom = nom

		## la position horizontale de cet element 
		self.posX = posX
		
		## la position verticale de cet element 
		self.posY = posY
		
		## la liste des voisins attaches a celui-ci
		self.voisins = []


	## Retourne une representation textuelle de cet element
	#
	# Cette methode retourne sous forme textuelle une representation
	# des donnees contenues dans cette classe. Ces donnees sont retournees
	# sous forme d'une chaine de caracteres au format:
	#
	# @code
	#	<nom_element,(position_x,position_y)>
	#		 voisins = { nom_voisin_1 nom_voisin_2 ... nom_voisin_n }
	# @endcode
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @return Une chaine de caracteres contenant les donnees de cet element
	def __repr__( self ):
		out = ("<%s,(%d,%d)>\n" % (self.nom, self.posX,self.posY))
		out = out + "\t voisins = {"
		for voisin in self.voisins:
			out = out + " " + voisin.nom
		out = out + " }"
		return out


	## Ajoute un nouveau voisin a la liste des voisins de cet element
	#
	# Insere un nouveau voisin en \b tete de liste des voisins de cet element. Un
	# voisin est un autre element defini par un nom et une position. Dans le
	# cas de cette simulation, un element sera une ville et les voisins aussi.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] voisin le noeud voisin a ajouter dans la liste
	def ajouteVoisin( self, voisin ):
		self.voisins.insert( 0, voisin )


	## Verifie si le nom passe en param est egal a celui de cet element
	#
	# Cette methode compare deux chaines de caracteres et teste si elles sont
	# egales. Si elles sont egales, alors le nom passe en parametre est 
	# le meme que celui de cet element.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] un_nom le nom avec lequel il faut comparer
	# @return \b True si les deux noms correspondent, \b False sinon
	def verifieNom( self, un_nom ):
		return (self.nom==un_nom)


	## Retourne la distance euclidienne separant cet objet avec celui 
	# passe en parametre
	#
	# Cette methode retourne la distance euclidienne entre ces deux
	# elements. 
	#
	# La formule de la distance euclienne est la suivante:
	# \f$\sqrt{(self.posX-objet.posX)^2+(self.posY-objet.posY)^2}\f$.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] objet un autre element avec lequel on calcule la distance
	# @return Distance euclidienne entre l'element courant et l'objet passe
	#		 en parametre. Dans le cas de cette simulation, il s'agit de
	#		 donner la distance entre deux villes 
	# @note L'operateur Python '**' designe : <em>elevation a une puissance</em>
	def distanceEuclidienne( self, objet ):
		return math.sqrt((self.posX-objet.posX)**2 + (self.posY-objet.posY)**2)


## Represente un noeud d'un algorithme de recherche
#
# Ce qui differentie un noeud d'un algorithme de recherche d'un noeud 
# traditionel d'un graphe(Element), est que ce dernier ne comprend pas
# de cout. La variable cout est utile pour des algorithmes de recherche
# tels que A*.
class Noeud:

	## @var refElement
	# une reference vers l'element du graphe
	
	## @var coutC
	# le cout \f$c_{n}\f$ pour aller d'un noeud inital a un noeud n
	
	## @var coutF
	# le cout total \f$c_{n}+h_{n}\f$ pour aller d'un noeud inital a un 
	# noeud final en passant par n
		
	## Constructeur de la classe Noeud
	#
	# Initialise l'etat interne d'un noeud de recherche. Il comprend
	# notamment une reference vers un noeud du graphe, ainsi qu'un cout
	# f(n) et un cout c(n). La relation entre ces deux elements est la
	# suivante: \f[f_{n}=c_{n}+h_{n}\f]\n
	#
	#	 \f$c_{n}\f$  represente le cout pour aller du noeud initial jusqu'au
	#				noeud courant n\n
	#	\f$h_{n}\f$  represente une <strong>estimation</strong> du cout pour
	#				aller du noeud n a un noeud final\n
	#	 \f$f_{n}\f$  represente le cout total pour aller d'un noeud initial
	#				a un noeud but en passant par le noeud n !\n
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] refElement une reference a un element representant un noeud
	# @param[in] coutC le cout \f$c_{n}\f$
	# @param[in] coutF le cout total \f$c_{n}+h_{n}\f$
	def __init__( self, refElement, coutC=None, coutF=None ):

		if coutC is None:
			coutC = 0
		if coutF is None:
			coutF = 0
			
		self.refElement = refElement
		self.coutC = coutC
		self.coutF = coutF


	## Retourne une representation textuelle de cet objet
	#
	# Cette methode retourne une representant sous forme textuelle des 
	# donnees contenues dans cet objet. Ces donnes sont au format :
	#
	# @code
	# noeud<nom_du_noeud,cout_cn, cout_fn>
	# @endcode
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @return 
	def __repr__(self):
		return ("noeud <%s,%d,%d>" % ( self.refElement.nom, 
									   self.coutC, 
									   self.coutF) )


	## Teste si le noeud passe en parametre est solution
	#
	# Un noeud est une solution si son nom est le meme que celui
	# d'un noeud but. Pour rappel, le nom d'un element est <strong>unique
	# </strong>, donc, il suffit de tester la correspondance entre les noms
	# des deux elements : celui-ci et celui passe en parametre. En general,
	# l'element passe en parametre sera un noeud <em>final</em>.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] refElement l'element de reference equivalent a 
	#			la destination finale
	# @return true <=>  self est l'objet final
	def estUneSolution( self, refElement ):
		return self.refElement.nom==refElement.nom


	## Met a jour le cout \f$c_{n}\f$ du noeud passe en parametre
	#
	# Attention, la mise a jour s'effectue bien sur le noeud passe en 
	# parametre, et non pas le noeud represente par l'objet traitant
	# cette methode. Cela est tout a fait normal. Pour chaque noeud, il y
	# a 0,1, ou plusieurs successeurs. L'algorithme de recherche part du
	# premier noeud et descend selon les successeurs. Alors, pour le noeud
	# courant on a toujours un cout defini(0 pour le noeud initial). A chaque
	# successeur du noeud, on met a jour a partir du cout du noeud courant et
	# de la distance euclidienne les separant :
	#
	# \f[c_{succ} = c_{self} + \delta (succ,self)\f]
	# 
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in,out] succ le noeud a mettre a jour
	def metAJourCoutC( self, succ ):
		succ.coutC = self.coutC + self.refElement.distanceEuclidienne(
															succ.refElement )


	## Met a jour le cout \f$f_{n}=c_{n}+h_{n}\f$ du noeud passe en parametre
	#
	# Met a jour le cout total du noeud courant. Pour mettre a jour cette
	# valeur, il faut que le cout c(n) soit a jour. La partie heuristique
	# h(n) de la formule est donnee par la distance euclidienne entre le
	# noeud self et le noeud but passe en parametre.
	# Dans notre cas, self est le noeud but !!!!
	#
	# \f[f_{succ} = c_{succ} + \delta (succ,self)\f]
	# 
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in,out] succ le noeud a mettre a jour
	# @note h(n)=distance euclidienne entre self et le but
	def metAJourCoutF(self,succ):
		succ.coutF = succ.coutC + succ.refElement.distanceEuclidienne(
															self.refElement )
																	

	## Retourne tous les voisins du noeud
	#
	# Cette methode retourne tous les noeuds voisins du noeud courant
	# represente par self.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] but la ville de destination (de type Element)
	def successeurs(self,but):
		
		# construit un noeud pour chaque voisin. Remarquez que le
		# constructeur de Noeud est automatiquement appelle
		succs = map( Noeud, self.refElement.voisins )
		
		# met a jour le cout C de chaque noeud. La fonction self.metAJourCoutC
		# sera appelee automatiquement en recevant comme parametre une noeud
		# successeur
		map( self.metAJourCoutC, succs )
		
		# met a jour le cout total f(n). La fonction metAJourCoutF est
		# automatiquement appelee pour chaque successeur
		map( Noeud(but).metAJourCoutF, succs )
		
		# retourne la liste des successeurs ainsi obtenue
		return succs


## Represente une liste de noeuds d'un graphe
#
# Cette classe facilite la programmation en proposant un wrapper pour une 
# liste de noeuds. Cet objet permet d'ajouter de nouveaux noeuds, permet
# de tester si un noeud est present et permet de tester si un noeud precis
# a un cout F inferieur a celui de tous les noeuds presents dans la liste 
class Noeuds:

	## @var noeuds
	# la liste contenant les noeuds d'un graphe
	
	## Constructeur de la classe
	#
	# Initialise la liste des noeuds a zero
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	def __init__( self ):
		self.noeuds=[]


	## Ajoute un noeud a la liste
	#
	# Ajoute un nouveau noeud a la liste des noeuds presente
	# 
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] noeud le noeud a ajouter 
	def ajouteNoeud( self, noeud ):
		self.noeuds.append( noeud )


	## Teste si un noeud precis est contenu dans la liste 
	#
	# Cette methode teste si un noeud est deja contenu dans la liste
	# des noeuds de la classe en testant si leurs noms sont egaux. Pour
	# rappel, un nom est \b unique.
	#
	# @param self un pointeur vers cet objet lui-meme (automatique)
	# @param noeud le noeud a verifier
	# @return \b True si le noeud est dans la liste, \b False sinon
	def contient(self,noeud):
		for n in self.noeuds:
			if n.refElement.nom==noeud.refElement.nom:
				return True
		return False


	## Teste si le noeud passe en parametre a un cout \f$f_{n}\f$ strictement inferieur 
	## a celui des noeuds presents dans la liste
	#
	# Cette methode teste si le cout \f$f_{n}\f$ du noeud passe en parametre
	# est strictement inferieur a celui des autres. Pour cela, on parcourt
	# la liste des noeuds et on teste si un noeud avec le meme nom
	# existe. Si c'est le cas et si son cout \f$f_{n}\f$ est plus grand 
	# que celui du noeud passe en parametre, alors on retourne \b True.
	#
	# @param[in] self un pointeur vers cet objet lui-meme (automatique)
	# @param[in] noeud le noeud a verifier
	# @return \b True si \f$noeud.coutF < noeuds.n.coutF\f$, \b False sinon
	def coutFStrictementInferieur( self, noeud ):
		for n in self.noeuds:
			if ( n.refElement.nom==noeud.refElement.nom and 
				noeud.coutF<n.coutF):
				return True
		return False 
