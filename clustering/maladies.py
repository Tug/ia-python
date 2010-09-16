## @package maladies Classification de maladies

## @file maladies.py Classification de maladies

#DOMAINES=[['maladies','angine-erythemateuse','angine-pultacee','angine-diphterique','appendicite','bronchite','coqueluche', 'pneumonie','rougeole','rubeole'],
#          ['fievre','non','legere','elevee'],
#          ['amygdales','normales','gonflees', 'points-blancs', 'enduit-blanc'],
#          ['ganglions','non','oui'],
#          ['gene-a-avaler','non','oui'],
#          ['mal-au-ventre','non','oui'],
#          ['toux','non','oui'],
#          ['rhume','non','oui'],
#          ['respiration','normale','genee','rapide'],
#          ['joues','normales','rouges','taches-rouges'],
#          ['yeux','normaux','larmoyants']] 

DONNEES =[['angine-erythemateuse','elevee','gonflees',    'oui','oui','non','non','non','normale','normales',     'normaux'],
		  ['angine-pultacee',     'elevee','points-blancs','oui','oui','non','non','non','normale','normales',     'normaux'],
          ['angine-diphterique',  'legere','enduit-blanc','oui','oui','non','non','non','normale','normales',     'normaux'],
          ['appendicite',         'legere','normales',    'non','non','oui','non','non','normale','normales',     'normaux'],
          ['bronchite',           'legere','normales',    'oui','non','non','oui','oui','genee',   'normales',     'normaux'],
          ['coqueluche',          'legere','normales',    'non','oui','non','oui','oui','genee',   'normales',     'normaux'],
          ['pneumonie',           'elevee','normales',    'non','non','non','oui','non','rapide', 'rouges',       'normaux'],
          ['rougeole',            'legere','normales',    'non','oui','non','oui','oui','normale','normales',     'larmoyants'],
          ['rougeole',            'legere','normales',    'non','oui','non','oui','oui','normale','taches-rouges','larmoyants'],
          ['rubeole',             'legere','normales',    'oui','non','non','non','non','normale','taches-rouges','normaux'],
          ['rubeole',             'non',   'normales',    'oui','non','non','non','non','normale','taches-rouges','normaux'],
          ['rubeole',             'non',   'normales',    'oui','non','non','non','non','normale','normales',     'normaux']]
