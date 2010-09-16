## \file sudoku.py
# \brief Implementation d'un exemple de probleme de contraintes sur la base
#		du fameux jeu du Sudoku
# \package sudoku
# \brief Implementation d'un exemple de probleme de contraintes sur la base
#		du fameux jeu du Sudoku

#-------------------------------------------------------------------------------
print "Chargement du probleme de sudoku"
print "\t@version: 2.0  date: 06/06/2008 modified by Thomas Leaute"
print "\t@version: 1.3  date: 25/04/2008 modified by Thomas Leaute"
print "\t@version: 1.2  date: 15/03/2007 modified by Vincent Schickel-Zuber"
print "\t@version: 1.1  date: 21/01/2007 modified by Bruno Alves"
print "\t@version: 1.0  date: 01/05/2006 modified by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 1/05/2006"
print "\t@copyright: EPFL-IC-IIF-LIA 2006-2007"
#-------------------------------------------------------------------------------

# modules utilises
import copy
import libPSC
import PSC

## Represente le symbole vide dans la grille
X = 0

## Le domaine des variables (pour un sudoku, va de 0 a 9)
DOMAINE=range(1,10)

## Contient l'enonce de depart
PROBLEME=[]

## Contient la grille du Sudoku
GRILLE=[[]]

## Nombre de colonnes dans la grille
NBCOL=9

## Nombre de lignes dans la grille
NBLGN=9

VARS = PSC.Variables()
CONTS = PSC.Contraintes()

## Taille d'une sous grille
TAILLESOUSGRILLE=3


## Retourne la position de la ss_grille correspondant a la position absolue
#
# Retourne la position de la sous-grille correspondant a la valeur absolue
# donnee en pos:
# \n
# exemple:\n
#	   pos=5 et TAILLESOUSGRILLE=3\n
# donc \c retournePosSSGrille(5) = 5/3 = 1
#
# @param[in] pos la position absolue
# @return la position de la sous-grille correspondant a la position absolue
def retournePosSSGille( pos ):
	return pos/TAILLESOUSGRILLE


## Retourne la position dans la ss_grille correspondant a la position absolue
#
# Retourne la position dans la sous-grille correspondant a la valeur absolue
# donnee en pos:
# \n
# exemple:\n
#	   pos=5 et TAILLESOUSGRILLE=3\n
# donc \c retournePosINSSGille(5) = 5%3 = 2
#
# @param[in] pos la position absolue
# @return la position dans la sous-grille correspondant a la position absolue
def retournePosINSSGille( pos ):
	return pos%TAILLESOUSGRILLE 


## Verifie si le symbole passe en parametre correspond au symbole vide
#
# Verifie si le symbole correspond au symbole vide en le testant contre
# le symbole vide X.
#
# @param[in] symbol le symbole a verifier
# @return \b True si le symbole est un symbole vide, \b False
def estVide( symbol ):
	return symbol==X


## Classe representant une sous-grille faisant partie d'une grille
# du Sudoku
class SSGrille:

   
	## Constructeur de la classe
	#
	# Initialise la sous-grille
	#
	# Initialise l'etat interne d'une sous-grille en initialisant les
	# tableaux, les positions, en ajoutant
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param posL la position sur la ligne[0..2]
	# @param posC la position dans la colonne[0..2]
	def __init__( self, posL, posC ):
		# initialise les positions et les tables
		self.posL=posL
		self.posC=posC
		self.ssgrille=[]
		self.notPossible=[]

		# ajoute les lignes des sous-grilles
		for i in range(0,TAILLESOUSGRILLE):
			self.ssgrille.append([])

		# cree une nouvelle variable pour chaque case
		for i in range(0,TAILLESOUSGRILLE):
			for j in range(0,TAILLESOUSGRILLE):
				id="v["+str(self.posL)+","+str(self.posC)+"]["+str(i)+","+str(j)+"]"
				var = libPSC.Variable(id,DOMAINE)
				self.ssgrille[i].append(var)
				VARS.ajouteVar(var)


	## Met a jour la valeur de la variable dans la sous grille a un endroit specifique
	#
	# Cette methode met a jour la valeur de la variable donnee par sa position.
	#
	# @param[in] self reference automatique vers l'objet qui execute cette meth.
	# @param[in] valeur la valeur de la variable
	# @param[in] domaine le domaine de la variable
	# @param[in] posX la position en X
	# @param[in] posY la position en Y
	def ajouteVariable( self, valeur, domaine , posX, posY ):   
		if valeur in DOMAINE:
			self.ssgrille[posX][posY].domaine=[valeur]
			self.notPossible.append(valeur)
		else:
			self.ssgrille[posX][posY].domaine=copy.deepcopy(DOMAINE)		 


	## Retourne la coordonne absolue d'un element dans la grille
	#
	# Cette methode retourne la position absolue etant donnee une position
	# dans une sous-grille.
	#
	# @param[in] self reference automatique vers l'objet qui execute cette meth.
	# @param[in] x la position en axe x dans la sous-grille
	# @param[in] y la position en axe y dans la sous-grille
	# @return le couple (x_abolue,y_abolue)
	def positionAbolue( self, x, y ):
		posx=self.posL*TAILLESOUSGRILLE+x
		posy=self.posC*TAILLESOUSGRILLE+y
		return (posx,posy)


	## Retourne la valeur a une position donnee
	#
	# Cette methode retourne la valeur d'une variable associee a une
	# case en (posX,posY).
	#
	# @param[in] self reference automatique vers l'objet qui execute cette meth.
	# @param[in] posX la position en X
	# @param[in] posY la position en Y
	def valeur( self, posX, posY ):
		return self.ssgrille[posX][posY].valeur


	## Genere toutes les contraintes de groupes
	#
	# Cette methode genere toutes les contraintes possibles pour cette
	# sous-grille. Ces contraintes sont de la forme Xi!=Xj.
	#
	# @param[in] self reference automatique vers l'objet qui execute cette meth.
	def genereContraintesSSGrille( self ):
		for i in range(0,TAILLESOUSGRILLE):
			for j in range(0,TAILLESOUSGRILLE):				
				for k in range(i,TAILLESOUSGRILLE):
					for l in range(0,TAILLESOUSGRILLE):
						if k > i or (k == i and l > j):
							var1=self.ssgrille[i][j]
							var2=self.ssgrille[k][l]
							c=libPSC.ContrainteBinaire(var1,"!=",var2)
							CONTS.ajouteContrainte(c)


## Classe definissant la grille, qui est faite de 9 sous-grilles
#
# Cette classe propose des methodes sympathiques pour aider dans la
# creation et la specification d'un probleme de Sudoku. Cette classe
# gere l'initialisation de la grille a partir des donnees d'un probleme
# contenues dans \c PROBLEME. Elle permet entre autres de retourner
# une representation sous forme texte de la grille
class Grille:	

	## Constructeur de la classe
	#
	# Fait un appel automatique a la fonction d'initialisation interne init()
	#
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode. 
	def __init__( self ):
		self.init()


	## Initialise la grille avec le contenu du probleme
	#
	# Cette methode initialise une grille complete en creant les tableaux
	# necessaires et en placant dedans les donnees du probleme contenues
	# dans \c PROBLEME
	# 
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode. 
	def init(self):
	
		# efface la grille
		del GRILLE[:]
		
		# ajoute les sous grilles
		for i in range(0,TAILLESOUSGRILLE):
			GRILLE.append([])

		# remplit la grille de sous-grilles
		ssgrillecol=0
		ssgrillelgn=0			
		for i in range(0,TAILLESOUSGRILLE):
			for j in range(0,TAILLESOUSGRILLE):
				GRILLE[i].append(SSGrille(i,j))
		

		# remplit les sous-grilles
		ssgrillecol=0
		ssgrillelgn=0
		for i in range(0,NBLGN):
			ssgrillecol=0
			if i>0 and i%TAILLESOUSGRILLE==0:
				ssgrillelgn+=1
			for j in range(0,NBCOL):
				if j>0 and j%TAILLESOUSGRILLE==0:
					ssgrillecol+=1
				if not (PROBLEME[i][j]==X):
					GRILLE[retournePosSSGille(i)][retournePosSSGille(j)].ajouteVariable(PROBLEME[i][j],[PROBLEME[i][j]],retournePosINSSGille(i),retournePosINSSGille(j))
				else:
					GRILLE[retournePosSSGille(i)][retournePosSSGille(j)].ajouteVariable(PROBLEME[i][j],DOMAINE,retournePosINSSGille(i),retournePosINSSGille(j))
	  

	## Retourne la grille sous forme textuelle
	#
	# Cette methode retourne une representation de la grille sous forme
	# textuelle. Voici un exemple de sortie de cette fonction:
	#
	# @code
	#   9 0 0 0 0 0 0 0 2 
	#	3 0 7 1 0 0 4 0 8 
	#	0 1 0 0 5 4 0 6 0 
	#	0 0 1 0 0 0 0 7 0 
	#	0 0 4 0 0 0 9 0 0 
	#	0 2 0 0 0 0 8 0 0 
	#	0 8 0 3 2 0 0 4 0 
	#	7 0 3 0 0 6 2 0 1 
	#	4 0 0 0 0 0 0 0 5
	# @endcode
	#
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode.
	# @return une chaine de caracteres contenant une grille sous forme textuelle
	def __str__( self ):
		ssgrillecol=0
		ssgrillelgn=0
		ligne=""
		for i in range(0,NBLGN):
			ssgrillecol=0
			if i>0 and i%TAILLESOUSGRILLE==0:
				ssgrillelgn+=1
			ligne+="\t"
			for j in range(0,NBCOL):
				if j>0 and j%TAILLESOUSGRILLE==0:
					ssgrillecol+=1
				ligne+=str(GRILLE[retournePosSSGille(i)][retournePosSSGille(j)].valeur(retournePosINSSGille(i),retournePosINSSGille(j)))+" "	
			ligne+="\n"
		return ligne


	## Retourne une variable se trouvant a une position en valeur absolue
	#
	# Cette methode retourne simplement la variable lie a une certaine position
	# dans la grille globale.
	#
	# @param[in] posX la position absolue X
	# @param[in] posY la position absolue Y
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode. 
	def retourneVariable( self, posX, posY ):
		var=GRILLE[retournePosSSGille(posX)][retournePosSSGille(posY)].ssgrille[retournePosINSSGille(posX)][retournePosINSSGille(posY)]
		return var


	## Genere toutes les contraintes de lignes
	#
	# Genere toutes les contraintes liees a une ligne. Ces contraintes
	# sont generalement qu'il ne faut pas qu'il y ait deux fois le meme
	# numero sur la meme ligne. Ce qui veut dire que pour une ligne donnee,
	# il doit y avoir une fois tous les numeros de 1 a 9.
	#
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode. 
	def genereContraintesLignes( self ):
		for i in range(0,NBCOL):
			for j in range(0,NBLGN):
				for k in range(j+1,NBLGN):
					var1=self.retourneVariable(j,i)
					var2=self.retourneVariable(k,i)
					c=libPSC.ContrainteBinaire(var1,"!=",var2)
					CONTS.ajouteContrainte(c)
					
					
	## Genere toutes les contraintes de colonne
	#
	# Genere toutes les contraintes liees a une colonne. Ces contraintes
	# sont generalement qu'il ne faut pas qu'il y ait deux fois le meme
	# numero sur la meme colonne. Ce qui veut dire que pour une colonne,
	# donnee il doit y avoir une fois tous les numeros de 1 a 9.
	#
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode. 
	def genereContraintesColonnes( self ):
		for i in range(0,NBLGN):
			for j in range(0,NBCOL):
				for k in range(j+1,NBCOL):
					var1=self.retourneVariable(i,j)
					var2=self.retourneVariable(i,k)
					c=libPSC.ContrainteBinaire(var1,"!=",var2)
					CONTS.ajouteContrainte(c)					


	## Genere toutes les contraintes de sous-grille
	#
	# Cette methode genere toutes les contraintes liees a une
	# sous-grille. Ces contraintes sont en general qu'il ne faut
	# pas qu'il y ait deux fois le meme nombre dans la meme
	# sous-grille.
	#
	# @param[in] self pointeur automatique vers l'instance executant cette
	#				 methode. 
	def genereContraintesSSGrilles( self ):
		for i in range(0,TAILLESOUSGRILLE):
			for j in range(0,TAILLESOUSGRILLE):
				GRILLE[i][j].genereContraintesSSGrille()


## Initialise le jeu (la grille) et trouve la solution 
#
# Lance la resolution du probleme en prenant comme entree l'algorithme
# de resolution et la grille dont on cherche la solution. La fonction
# se chargera ensuite de la creation des contraintes de grille, de ligne
# de colonne et de sous-grille.
#
# @param[in] algo l'algorithme a utiliser pour la resolution du probleme
# @param[in] grille la grille preexistante que l'on souhaite resoudre.
#			Deux grilles sont disponibles \e A et \e B. \e A est de
#			faible difficulte, tandis que \e B est difficile.
def run( algo, grille ):

	# des bugs, oops, debug
	print "|+| Chargement du probleme"
	
	# variable globales
	global PROBLEME
	
	# allez-vous choisir la facile grille A ?
	if grille=="A":
		PROBLEME=[[9,X,X,X,X,X,X,X,2], 
			   [3,X,7,1,X,X,4,X,8],
			   [X,1,X,X,5,4,X,6,X],
			   [X,X,1,X,X,X,X,7,X],
			   [X,X,4,X,X,X,9,X,X],
			   [X,2,X,X,X,X,8,X,X],
			   [X,8,X,3,2,X,X,4,X],
			   [7,X,3,X,X,6,2,X,1],
			   [4,X,X,X,X,X,X,X,5]]
			   
	# ou la diabolique grille B ?
	elif grille=="B":
		PROBLEME=[[X,X,X,X,X,X,X,X,X], 
				[X,X,7,8,3,X,9,X,X],
				[X,X,5,X,X,2,6,4,X],
				[X,X,2,6,X,X,X,7,X],
				[X,4,X,X,X,X,X,8,X],
				[X,6,X,X,X,3,2,X,X],
				[X,2,8,4,X,X,5,X,X],
				[X,X,X,X,9,6,1,X,X],
				[X,X,X,X,X,X,X,X,X]]
			   
	# ou encore une autre ?
	else:
		print "|-| Grille" , grille, "non definie"
	
	# variables globales
	global VARS
	global CONTS
	
	# obtient les variables et contraintes du PSC
	VARS = PSC.Variables()
	CONTS = PSC.Contraintes()
	
	# initialisation de la grille
	print "|+| Initialisation de la grille"
	grille = Grille()

	# ajout des contraintes liees a la grille
	print "|+| Ajoute les contraintes"
	grille.genereContraintesLignes()
	grille.genereContraintesColonnes()
	grille.genereContraintesSSGrilles()
	
	# consistance des noeuds
	print "|+| Fait la consistance des noeuds"	
	VARS.consistanceDesNoeuds()
	##print VARS

	# consistance des arcs
	print "|+| Fait la consistance des arcs"
	CONTS.consistanceDesArcs()
	##print CONTS
	
	# re-ordonne les noeuds
	PSC.variableOrdering()
		
	# choisit l'algorithme a executer
	if algo=="FC":
		sol=PSC.forwardChecking( 0, False, True )
	else:
		sol=PSC.backtrack( 0, False, True )
	   
	# imprime la grille une fois l'algorithme lance
	print grille

	
#-------------------------------------------------------------------------------
# SIMULATION
#-------------------------------------------------------------------------------
run( "FC", "B" )

