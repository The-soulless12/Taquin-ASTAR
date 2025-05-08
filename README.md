# Taquin-A-STAR
Solveur du jeu du Taquin implémenté en Python, utilisant l'algorithme A* afin de résoudre efficacement le casse-tête en optimisant le chemin vers la solution à l'aide d'une heuristique.

# Fonctionnalités
- Solveur du jeu du Taquin avec l'algorithme A*, une méthode de recherche de chemin **exacte** qui garantit de trouver la solution optimale à condition que l’heuristique utilisée soit admissible. Cette fonction heuristique estime la distance restante pour atteindre la solution et combine cette estimation avec le coût déjà parcouru pour choisir les mouvements les plus prometteurs.
- Il est possible de jouer graphiquement en cliquant directement sur les cases du Taquin.
- Il est également possible de jouer en saisissant les directions (`h`, `b`, `d`, `g` pour haut, bas, droite, gauche) puis en appuyant sur `Entrée` ou le bouton `déplacer` afin de déplacer les pièces du jeu.
- L'application permet de régénérer le Taquin afin de proposer un nouveau casse-tête à résoudre.
- Pour les Taquins de taille 2x2 et 3x3, une solution optimale est calculée, montrant la séquence de mouvements nécessaires pour résoudre le puzzle.

# Structure du Projet
- main.py : Contient le programme principal implémentant l'algorithme A* pour résoudre le jeu du Taquin avec une interface graphique interactive.

# Prérequis
- Python version 3.x
- Le package : colorama.

# Note
- Pour exécuter le projet, saisissez la commande `python main.py` dans votre terminal.
- L'algorithme A* fonctionne très bien pour des Taquins de petite taille (2x2 et 3x3) mais il y a un problème lié à la taille du Taquin pour des tailles plus grandes (4x4 et plus). En effet, l'algorithme A* peut devenir de plus en plus lourd en termes de complexité et nécessite davantage de ressources pour trouver une solution ce qui peut provoquer un plantage ou une très lente exécution en raison de **l'explosion combinatoire** du nombre d'états possibles à explorer.
- Le problème du Taquin est **un problème NP-difficile** ce qui signifie qu'il n'existe pas de méthode rapide et efficace pour le résoudre lorsque la taille du puzzle augmente. La complexité du problème croît de manière **exponentielle** avec le nombre de cases.
