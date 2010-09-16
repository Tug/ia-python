#-------------------------------------------------------------------------------
print "Chargement du module variable et noeud pour PSC"
print "\t@version: 2.0  date: 06/06/2008 modified by Thomas Leaute"
print "\t@version: 1.8  date: 25/04/2008 modified by Thomas Leaute"
print "\t@version: 1.7  date: 28/06/2007 modified by Thomas Leaute"
print "\t@version: 1.6  date: 03/05/2007 modified by Thomas Leaute"
print "\t@version: 1.5  date: 02/05/2007 modified by Thomas Leaute"
print "\t@version: 1.4  date: 19/03/2007 modified by Vincent Schickel-Zuber"
print "\t@version: 1.3  date: 14/02/2007 modified by Vincent Schickel-Zuber"
print "\t@version: 1.2  date: 17/01/2007 modified by Bruno Alves"
print "\t@version: 1.0  date: 24/04/2006 created by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 24/04/2006"
print "\t@copyright: EPFL-IC-IIF-LIA 2006-2007"
#-------------------------------------------------------------------------------

# module utilise
import copy

## Le nombre de contraintes visitees
NBCONTRAINTES=0


## Classe modelisant une variable
#
# Une variable dans le probleme des contraintes est un objet qui peut
# prendre n'importe quelle valeur de son domaine.
class Variable:

	## \var nom
	# le nom de la variable

	## \var domaine
	# le domaine de valeurs de la variable

	## \var valeur
	# la valeur actuelle de la variable

	## \var label
	# le label de valeurs associe a la variable
	# utilise pour le forward checking
	
	
	## Constructeur de la classe
	#
	# Initialise la variable avec un nom et un domaine donnes. Sa valeur
	# initiale est fixee a \c None et son label est une copie du domaine.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] nom le nom de la variable
	# @param[in] domaine une liste de valeurs possibles pour la variable
	#
	# @note comme pour le precedent exercice (Lab5), un nom est un identifiant,
	#	   il doit donc etre \b unique
	def __init__( self, nom, domaine ):
		self.nom=nom
		self.domaine=domaine
		self.valeur=None 
		self.label=[]
		self.initLabel()

	
	## Reinitialise le contenu de l'attribut label
	#
	# Reinitialise le label comme une copie du domaine.
	#   label = domaine.clone()
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def initLabel( self ):
		self.label=copy.deepcopy(self.domaine)


	## Efface la valeur desiree du label
	#
	# Supprime la valeur d passee en parametre du label, si elle existe.
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] d la valeur du domaine a supprimer
	#
	# @see Chapitre 8.5.2 sur l'algorithme de Walz
	def enleveDuLabel( self, d ):
		if d in self.label:
			self.label.remove(d)


	## Met a jour la valeur de cette variable
	#
	# Remplace la valeur actuelle de la variable par une nouvelle valeur
	# passee en parametre.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param valeur la nouvelle valeur
	def metAJourValeur( self, valeur ):
		self.valeur=valeur   


	## Verifie que le nom de la variable correspond a celui passe en parametre
	#
	# Cette methode verifie si le nom passe en parametre est bien le nom
	# de cette variable
	# @param[in] self reference automatique vers l'instance executant cette
	#			methode.
	# @param[in] nom le nom a verifier
	# @return \b True si le nom correspond, \b False sinon
	def nomEstEgal( self, nom ):
		return self.nom==nom

		
	## Retourne la taille du domaine
	#
	# La taille du domaine est le nombre d'elements presents dans le domaine.
	# Dans cette version, le domaine doit etre fini !
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def tailleDuDomaine( self ):
		return len(self.domaine)

	## Retourne la taille du label
	#
	# La taille du label est le nombre d'elements presents dans le label.
	# Dans cette version, le label doit etre fini !
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def tailleDuLabel( self ):
		return len(self.label)

	## Retourne une representation textuelle des donnees de la classe
	#
	# Retourne une representation textuelle de la classe. Le format d'affichage
	# est le suivant:
	#
	# @code
	#   var : nom = valeur,		domaine = [val1, ..., valn]
	# @endcode
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def __repr__( self ):
		str = "var : %s \t= %s,\tdomaine = %s" % ( self.nom, self.valeur, self.domaine )
		return str


## Classe modelisant une contrainte sur une ou plusieurs variables
class Contrainte:

	## \var vars
	# Liste des noms des variables de cette contrainte

	## Constructeur de la classe
	#
	# Initialise la liste des variables
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] vars la liste des variables
	def __init__( self, vars ):
		self.vars = vars

	## Retourne la dimension de la contrainte
	#
	# Cette methode retourne la dimension de la contrainte, qui specifie
	# le nombre de variables qu'elle touche.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def dimension( self ):
		return 0


	## Teste si la contrainte est valide et respectee par les valeurs de la/
	# des variable(s) qui la compose/ent.
	#
	# Cette methode verifie si la contrainte est respectee par les valeurs
	# actuelles des variables qui la composent.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] var variable pour laquelle on veut tester une valeur
	# @param[in] val valeur de la variable a tester
	# @return \b True si la contrainte est respectee, \b False sinon
	def estValide( self, var, val ):
		return False;


	## Retourne une representation textuelle des donnees de la classe
	#
	# Retourne une representation textuelle de la classe.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	def __repr__( self ):
		str = "Contrainte : %s" %(self.vars)
		return str		



## Classe modelisant une contrainte unaire
#
# Une contrainte unaire correspond a une restriction sur les valeurs possibles
# d'une variable, de la forme x > 0, y = 5, etc..
#
# @remarks Cette classe est une sous-classe de Contrainte, elle implemente
#		  donc toutes les fonctions de base de celle-ci.
class ContrainteUnaire(Contrainte):

	## \var ref
	# la valeur de reference avec laquelle la valeur
	# de la variable est comparee
	
	## \var op
	# l'operation a effectuer entre les deux valeurs

	## \var refVar
	# une reference a la variable de la contrainte unaire
	
	## Constructeur de la classe
	#
	# Initialise la contrainte unaire avec une valeur de reference, une
	# reference vers la variable de la contrainte ainsi qu'un operateur
	# de comparaison entre les deux
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] ref valeur de reference pour la comparaison
	# @param[in] op un operateur possible entre \f$<\f$, \f$\leq\f$, \f$=\f$ et \f$!=\f$
	# @param[in] refVar reference sur la variable a utiliser
	def __init__( self, refVar, op, ref ):
		Contrainte.__init__(self, [refVar.nom])
		self.ref=ref
		self.op=op
		self.refVar=refVar

	## Retourne la dimension de la contrainte(unaire=1).
	#
	# @copydoc Contrainte::dimension()
	# @remarks La dimension d'une contrainte unaire est 1.
	def dimension( self ):
		return 1

	## Teste si la contrainte est valide et respectee par la valeur de la variable
	#
	# @copydoc Contrainte::estValide()
	# @remarks La contrainte unaire est respectee si l'operateur applique
	#		  aux deux operandes \c refVar et \c ref retourne \b True.
	def estValide( self, var, val ):

		# incremente le nombre de contraintes visitees
		global NBCONTRAINTES
		NBCONTRAINTES += 1
		
		# sauvegarde la valeur actuelle de la variable var
		# avant de la modifier
		valeur = var.valeur
		var.metAJourValeur(val)
			
		valide = False

		# si l'operateur est 'plus-petit-que', alors
		if (self.op == "<"):
			valide = self.refVar.valeur < self.ref

		# si l'operateur est 'plus-petit-ou-egal', alors
		elif (self.op == "<="):
			valide = self.refVar.valeur <= self.ref

		# si l'operateur est 'egal', alors
		elif (self.op == "=="):
			valide = self.refVar.valeur == self.ref

		 # si l'operateur est 'different', alors
		elif (self.op == "!="):
			valide = self.refVar.valeur != self.ref

		# sinon indique que l'operateur n'est pas implemente
		else:
			print "|-| Operateur", self.op, "non implemente"
		
		# annule le changement de valeur de la variable var et retourne
		var.metAJourValeur(valeur)
		return valide


	# Retourne une representation textuelle des donnees de la classe
	def __repr__(self):
		str = "Contrainte : %s %s %s" % ( self.refVar.nom, self.op, self.ref )
		return str



## Classe modelisant une contrainte binaire
#
# Une contrainte binaire est representee dans un graphe par un
# arc allant d'un noeud source(noeud de depart) a un noeud de
# destination(noeud d'arrivee). Cette contrainte est souvent de
# la forme v1<v2, v1==v2, v1>v2, etc...

# @remarks Cette classe est une sous-classe de Contrainte, elle implemente
#		  donc toutes les fonctions de base de celle-ci.
class ContrainteBinaire(Contrainte):

	## \var op
	# l'operateur de comparaison entre les deux variables

	## \var refVar1
	# une reference vers la premiere variable de la contrainte

	## \var refVar2
	# une reference vers la deuxieme variable de la contrainte
	
	## Constructeur de la classe
	#
	# Initialise les variables de depart et d'arrivee, ainsi
	# que l'operateur utilise pour la comparaison.
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] op un operateur parmi \f$\ne\f$ ou \f$\equiv\f$
	# @param[in] refVar1 reference vers la variable 1
	# @param[in] refVar2 reference vers la variable 2
	def __init__( self, refVar1, op, refVar2 ):
		Contrainte.__init__(self, [refVar1.nom, refVar2.nom])
		self.refVar1=refVar1
		self.op=op
		self.refVar2=refVar2


	## Retourne la dimension de la contrainte (binaire=2).
	#
	# @copydoc Contrainte::dimension()
	# @remarks La dimension d'une contrainte binaire est 2.
	def dimension( self ):
		return 2	


	## Teste si la contrainte est valide et respectee par les valeurs des variables qui la composent.
	#
	# @copydoc Contrainte::estValide()
	# @remarks La contrainte binaire est respectee si l'operateur applique
	#		  aux deux operandes \c refVar1 et \c refVar2 retourne \b True.
	def estValide( self, var, val ):

		# incremente le nombre de contraintes visitees
		global NBCONTRAINTES
		NBCONTRAINTES += 1
		
		# sauvegarde la valeur actuelle de la variable var
		# avant de la modifier 
		valeur = var.valeur
		var.metAJourValeur(val)
			
		valide = False

		# si l'operateur est 'pas-egal', alors...
		if (self.op == "!="):
			valide = self.refVar1.valeur != self.refVar2.valeur

		# si l'operateur est 'egal', alors...
		elif (self.op == "=="):
			valide = self.refVar1.valeur == self.refVar2.valeur

		# si l'operateur est 'plus-petit-que', alors...
		elif (self.op == "<"):
			valide = self.refVar1.valeur < self.refVar2.valeur

		# si l'operateur est 'NAND' (pour des variables booleennes), alors...
		elif (self.op=="NAND"):
			valide = not (self.refVar1.valeur == True and self.refVar2.valeur == True) 

		# si l'operateur est l'implication logique (pour des variables booleennes), alors...
		elif (self.op == "->"):
			valide = (self.refVar1.valeur == False or self.refVar2.valeur == True)

		# sinon, indique que l'operateur n'est pas implemente
		else:
			print "|-| Operateur", self.op, "non implemente"

		# annule le changement de valeur de la variable var et retourne
		var.metAJourValeur(valeur)
		return valide


	## Teste si la contrainte est satisfaite pour au moins une valeur dans
	# le domaine de la variable passee en parametre
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] var la variable dont on veut tester si une valeur de domaine convient
	# @return \b True si la contrainte est possible pour au moins une des
	#		 valeurs de D2, \b False sinon
	def estPossible( self, var ):

		# si la variable n'a pas de valeur possible, alors la
		# contrainte ne peut trivialement pas etre satisfaite
		if len(var.domaine)==0 :
			return False

		# pour chaque valeur du domaine de la variable:
		for d in var.domaine:

			# retourne True si au moins une valeur convient pour cette valeur d
			if self.estValide( var, d ):
				return True

		# Aucune valeur pour la variable ne convient
		return False


	## Applique l'algorithme REVISER
	#
	# Pour chaque variable, pour chaque valeur v dans le domaine de cette variable,
	# verifie s'il existe une valeur possible pour la deuxieme variable 
	# qui satisfasse la contrainte ; sinon, supprime v du domaine. 
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @note Regarder le chapitre 8.5.2 du cours pour de plus amples informations
	# sur le fonctionnement de l'algorithme de Waltz et REVISER
	def reviser ( self ):
		modifiee = False
		for paire in [ [self.refVar1, self.refVar2], [self.refVar2, self.refVar1] ]:
		
			# pour chaque valeur du domaine de la premiere variable
			for x in paire[0].domaine[:]:
			
				# on met a jour la valeur de la variable
				paire[0].metAJourValeur(x)
			
				# si cette contrainte n'est pas possible,
				# alors...
				if not self.estPossible(paire[1]):
			
					# ...on supprime la valeur du domaine
					paire[0].domaine.remove(x)
	
					# cependant il faut reviser a nouveau, car on
					# a peut-etre invalide d'autres contraintes
					modifiee = True

			paire[0].metAJourValeur(None)
			
		return modifiee
	
	
	## Propage l'assignation d'une variable de la contrainte a l'autre variable non instanciee
	#
	# Etant donne qu'on a fixe une valeur pour une variable de cette contrainte, 
	# on essaie de reduire le label de la deuxieme en supprimant les valeurs inconsistantes. 
	#
	# @param[in] self reference automatique vers l'instance executant cette
	#				 methode.
	# @param[in] var la variable qui vient d'etre instanciee
	# @return True si apres propagation, la contrainte est toujours consistante
	def propage ( self, var ):
	
		# trouve la variable encore non instanciee
		var2 = self.refVar1
		if var == self.refVar1:
			var2 = self.refVar2
		
		# utilise le label de la variable var2
		for l in var2.label[:]:

			#verifie que la contrainte est satisfaite
			if not self.estValide( var2, l ):
				# on enleve la valeur l du label
				var2.enleveDuLabel(l)
		
		# la consistance est possibe <=> il reste au moins une valeur dans le label
		return len(var2.label) > 0
		
	
	
	# Retourne une representation textuelle des donnees de la classe
	def __repr__(self):
		str = "Contrainte : %s %s %s" % (self.refVar1.nom, self.op, self.refVar2.nom)
		return str		
