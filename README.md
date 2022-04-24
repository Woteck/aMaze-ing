# aMaze-ing

###Utilisation
```
Clique-droit : Supprime une barrière à la grille.
Clique-gauche : Ajoute une barrière à la grille

A : Application & visualisation de l'algorithme A*
Z : Application & visualisation de l'algorithme Breadth First Search.
C : Création d'un nouveau labyrinthe.
V : Réinitialisation le labyrinthe.
```

###Description
Nous utilisons la librairie pygame pour visualiser notre labyrinthe.

Le projet est constitué d'un fichier Python principal (maze.py) ainsi que ses modules dans le dossier app.
Les principales classes de maze.py sont Spot, Grid, et Interface.
Une instance de la classe Interface permet de faire le lien entre l'utilisateur et le programme. On y retrouve la gestion des évènements de l'utilisateur, la création d'un instance de la classe Grid, l'affichage de la grille (Grid).
La classe Grid peut être interprêtée comme une 'liste 2D' : elle permet de gérer tous les éléments contenus à l'intérieur grâce à des méthodes. Tous les éléments de cette 'liste 2D' sont des instances de Spot. Cette classe permet de contrôler facilement un point de la grille (couleur, voisins, coordonnées dans la grille).
De plus, les algorithmes de résolutions du labyrinthe sont dans app/algorithms.py et la génération d'un nouveau labyrinthe se fait grâce à app/maze_generator.py


###Fonctionnement / Lien avec les graphes.
Chaque instance de la classe Spot possèdent ses propres coordonnées par rapport à l'Interface, sa couleur, et ses voisins.
En effet, la classe possède la méthode Spot.update_neighbors() qui permet d'actualiser sa liste de voisin par rapport à la grille. Ainsi, chaque instance Spot possède une liste de ses voisins (haut, bas gauche, droite) et nous pouvons modéliser un graphe. Grâce à cela, nous pouvons utiliser des algorithmes de recherche sur des graphes : A* et Breadth First Search contenus dans app/algorithms.py