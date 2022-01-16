# Brief Dabases
_(juste en dessous des badges sympatiques à placer)_

Ceci est un mini projet réalisé dans le cadre de la promo Dev IA par Simplon de Cannes.


### Pré-requis

 - Pyton > 3.6
 - MySQL

### Installation

Premièrement, clonez le répo, soit avec un gestionnaire, soit avec la commande : ``git clone https://github.com/malatia/Brief_db_final`` .
Ensuite, je conseille d'ouvrir le projet avec VScode et de créer un envrionnement virutel. 
Si vous êtes sous VScode voilà les étapes pour créer l'envrionnement : 
Si le terminal ne s'ouvre pas automatiquement : Dans les menus en haut aller dans "Terminal" -> "New Terminal". Puis 
 - Sous windows : ``python -m venv .venv`` et ensuite ``.venv/Scripts/activate``
 - Sous linux : ``python3 -m venv .venv`` et ensuite ``source .venv/bin/activate``
 Si tout s'est bien passé, vous devriez voir " (venv) " au début des lignes de votre terminal à présent.
 
 A partir de là on va tout simplement installer les dépendances nécessaires avec : ``python -m pip install -r requirements.txt`` , si vous êtes sous linux rempaclez "python" par "python3". 

Vous êtes normalement maintenant prêts à créer la base de données. 

Ouvrez le fichier "db_create.py" et sur les dans les variables "user", "passw", et "db_name", indiquez les informations de la base de données MySQL dans laquelle vous voulez créer les tables. Si jamais vous vous connectez à distance(donc pas en localhost), ou sur un port autre que celui par défaut, indiquez le en ligne 106.

Une fois cela fait, vous pouvez run le fichier "db_create.py".


## Démarrage

Maintenant, il suffit de lancer le fichier "run.py". Et vous pourrez vous connecter à l'adresse 127.0.0.1:5000 pour accéder au site!

## Explications du site

En gros le site à trois fonctionnalités d'accès à la base de données. 
  - On peut choisir une seule table, dans ce cas-ci, on aura un diagramme camambert représentant la distribution des différentes valeurs au sein de cette table. On peut également voir et cliquer sur les valeurs uniques de la table.
  - On peut chosir deux tables, dans ce cas-ci, on aura un scatterplot qui permettra de voir les associations existant entre les différentes valeurs au sein de ces deux tables. On peut également voir et cliquer sur les valeurs uniques des tables.
  - Enfin, si on clique sur une valeur unique d'une table, on obtient un tableau représentant toutes les lignes concernées par cette valeur
