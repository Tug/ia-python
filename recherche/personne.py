#################################################################################
## @version: 1.0  date: 27/03/2006 modified by the author"
## @author: vincent.schickel-zuber@epfl.ch date: 24/03/2006"
## @copyright: EPFL-IC-IIF-LIA 2006"
#################################################################################
class Personne:
	def __init__(self,nom,age):
		self.nom = nom
		self.age = age
		
	def anniversaire(self):
		self.age+=1

class Retourner:
	def __init__(self, object):
		self.object = object

	def __getattr__(self, name):
		def proxy(*args, **kwds):
			getattr(self.object, name)(*args, **kwds)
			return self.object
		return proxy
	
class Etudiant(Personne):
	
	def __init__(self,nom,age,section):
		Personne.__init__(self,nom,age) # heritage
		self.section=section

	def __str__(self):
		out = "Etudiant %s a %d ans et est en section: %s\n" % (self.nom, self.age,self.section)
		return out

	def changeSection(self, nouvelleSection):
		self.section=nouvelleSection

etudiants=[]

def afficheEtudiants():
	print "Liste des etudiants:\n"
	for etud in etudiants:
		print "\t", etud
		
toto = Etudiant("Toto",23,"SSC")
print toto
toto.anniversaire()
toto.changeSection("INF")
print toto

titi = Etudiant("Titi",22,"SSC")
tata = Etudiant("Tata",25,"SSC")

etudiants=[toto,titi,tata]
print etudiants.sort(key = lambda e : e.age)

etudiants=[toto,titi,tata]
etudiants = Retourner(etudiants).sort(key = lambda e : e.age)
afficheEtudiants()
