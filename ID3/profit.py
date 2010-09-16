# -*- coding: cp1252 -*-
## \file profit.py
## \brief Estimation du profit d'une entreprise informatique.
## \package profit
## \brief Estimation du profit d'une entreprise informatique.


# initialise ID3
initID3( [['down',  'old',  'no', 'software'],
		  ['down','midlife','yes','software'],
		  ['up',  'midlife','no', 'hardware'],
		  ['down','old',    'no', 'hardware'],
		  ['up',  'new',    'no', 'hardware'],
		  ['up',  'new',    'no', 'software'],
		  ['up',  'midlife','no', 'software'],
		  ['up',  'new',    'yes','software'],
		  ['down','midlife','yes','hardware'],
		  ['down','old',    'yes','software']],
		 [['profit', 'down','up'],
		  ['age', 'old', 'midlife', 'new'],
		  ['competition', 'no', 'yes'],
		  ['type', 'software', 'hardware']] )
		  

# construit l'arbre de décision		  
construitArbreDecision()