exec file("PSC.py")

vars = Variables()
contraintes = Contraintes()

v1=libPSC.Variable("a",[2, 3])
v2=libPSC.Variable("b",range(12))
v3=libPSC.Variable("c",range(3))
v4=libPSC.Variable("d",range(3))
v5=libPSC.Variable("e",range(12))

vars.ajouteVar(v1)
vars.ajouteVar(v2)
vars.ajouteVar(v3)
vars.ajouteVar(v4)
vars.ajouteVar(v5)
print vars

cv2= libPSC.ContrainteUnaire(v2,"<",4)
cv1v2= libPSC.ContrainteBinaire(v1,"!=",v2)
cv2v3= libPSC.ContrainteBinaire(v2,"!=",v3)
cv2v4= libPSC.ContrainteBinaire(v2,"!=",v4)
cv2v5= libPSC.ContrainteBinaire(v2,"!=",v5)
cv3v4= libPSC.ContrainteBinaire(v3,"!=",v4)
cv3v5= libPSC.ContrainteBinaire(v3,"!=",v5)
cv4v5= libPSC.ContrainteBinaire(v4,"!=",v5)
cv5v1= libPSC.ContrainteBinaire(v5,"<",v1)

contraintes.ajouteContrainte(cv2)
contraintes.ajouteContrainte(cv1v2)
contraintes.ajouteContrainte(cv2v3)
contraintes.ajouteContrainte(cv2v4)
contraintes.ajouteContrainte(cv2v5)
contraintes.ajouteContrainte(cv3v4)
contraintes.ajouteContrainte(cv3v5)
contraintes.ajouteContrainte(cv4v5)
contraintes.ajouteContrainte(cv5v1)
print contraintes

print "Fait la consistance des noeuds"
vars.consistanceDesNoeuds()
print vars

print "Fait la consistance des arcs"
contraintes.consistanceDesArcs()
print vars

sol=backtrack(0,True)
print "Solutions trouvees avec bt:=", SOLUTIONS
