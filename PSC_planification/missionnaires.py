#-------------------------------------------------------------------------------
print "Planification du probleme des missionnaires"
print "\t@version: 3.0  date: 07/06/2008 modified by Thomas Leaute"
print "\t@version: 2.1  date: 14/04/2008 modified by Thomas Leaute"
print "\t@version: 2.0  date: 03/05/2007 modified by Thomas Leaute"
print "\t@version: 1.1  date: 02/05/2007 modified by Thomas Leaute"
print "\t@version: 1.0  date: 05/03/2007 created by Vincent Schickel-Zuber"
print "\t@author: vincent.schickel-zuber@epfl.ch date: 05/03/2007"
print "\t@copyright: EPFL-IC-IIF-LIA 2007"
#-------------------------------------------------------------------------------

# Definit les types d'acteurs, avec la liste des acteurs de chaque type:
acteursB = ['B']
acteursM = ['M1','M2']
acteursC = ['C1','C2']

# Construit le probleme de planification
probleme = libPlan.ProblemeDePlanification ()

# Cree les propositions de planification
for acteur in acteursB + acteursM + acteursC:
	probleme.ajouteProposition("g("+acteur+")")
	probleme.ajouteProposition("d("+acteur+")")

# Cree les operateurs de planification
for bateau in acteursB:
	for i in range ( len(acteursM) ):
		pilote = acteursM[i]
		probleme.ajouteOperateur(libPlan.Operateur("dg("+bateau+", "+pilote+")", [ "d("+bateau+")", "d("+pilote+")" ], [ "g("+bateau+")", "g("+pilote+")" ]))
		for passager in acteursM[i+1:] + acteursC:
			probleme.ajouteOperateur(libPlan.Operateur("gd("+bateau+", "+pilote+", "+passager+")", [ "g("+bateau+")", "g("+pilote+")", "g("+passager+")" ], [ "d("+bateau+")", "d("+pilote+")", "d("+passager+")" ]))

# Ajoute les mutex de propositions
for acteur in acteursB + acteursM + acteursC:
	probleme.ajouteMutexDePropositions("d("+acteur+")", "g("+acteur+")")

# Ajoute les mutex d'operateurs 
operateurs = probleme.retourneOperateurs()
for i in range ( len(operateurs) ):
	op1 = operateurs[i]
	for op2 in operateurs[i+1:]:
		for acteur in acteursB + acteursM + acteursC:
			if (op1.aPourPrecondition("d("+acteur+")") or op1.aPourPrecondition("g("+acteur+")")) and (op2.aPourPrecondition("d("+acteur+")") or op2.aPourPrecondition("g("+acteur+")")):
				probleme.ajouteMutexDOperateurs(op1, op2)
				break

# Ajoute les contraintes initiales
for acteur in acteursB + acteursM + acteursC:
	probleme.ajouteConditionInitiale("g("+acteur+")", True)

# Ajoute les contraintes finales
for acteur in acteursB + acteursM + acteursC:
	probleme.ajouteConditionFinale("d("+acteur+")", True)

# Affiche le probleme de planification
print probleme


# Definit un plan contenant 5 etats  
solveur = PlanificateurPSC(probleme, 5)

# Implemente le PSC a partir du probleme de planification 
solveur.implementePSC()

# Affiche la liste des arcs et des noeuds dans le PSC
#solveur.affichePSC()

# Trouve la solution et l'affiche
solveur.trouveLaSolution()
