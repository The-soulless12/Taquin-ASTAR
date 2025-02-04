import random
import heapq
from colorama import Fore, Style

def creer_taquin(taille):
    # On génère les valeurs dans le désordre
    valeurs = list(range(1, taille * taille)) + [0] 
    random.shuffle(valeurs) 
    return [valeurs[i * taille:(i + 1) * taille] for i in range(taille)]

def afficher_taquin(grille):
    taille = len(grille)
    largeur = len(str(taille * taille - 1))
    separateur = "+" + ("-" * (largeur + 2) + "+") * taille
    
    for i, ligne in enumerate(grille):
        print(separateur)
        ligne_str = ""
        for j, cell in enumerate(ligne):
            if (i, j) in cases_cibles(grille):
                # On affiche en rouge les cases qui peuvent bouger
                cell_str = f"{cell if cell != 0 else ' ' :>{largeur}}"
                ligne_str += f"| {Fore.RED}{cell_str}{Style.RESET_ALL} "
            else:
                ligne_str += f"| {cell if cell != 0 else ' ' :>{largeur}} "
        print(ligne_str + " |")
    print(separateur)

def trouver_case_vide(grille):
    for i, ligne in enumerate(grille):
        for j, valeur in enumerate(ligne):
            if valeur == 0:
                return i, j
    return None

def deplacer(grille, direction):
    taille = len(grille)
    x, y = trouver_case_vide(grille)
    
    mouvements = {
        "b": (x - 1, y),
        "h": (x + 1, y),
        "d": (x, y - 1),
        "g": (x, y + 1)
    }
    
    if direction in mouvements:
        nx, ny = mouvements[direction]
        if 0 <= nx < taille and 0 <= ny < taille:
            grille[x][y], grille[nx][ny] = grille[nx][ny], grille[x][y]

def cases_cibles(grille):
    # On recherche les cases qui peuvent bouger en fonction de la position de la case vide
    taille = len(grille)
    x, y = trouver_case_vide(grille)
    cases = []

    mouvements = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
    for nx, ny in mouvements:
        if 0 <= nx < taille and 0 <= ny < taille:
            cases.append((nx, ny))

    return cases

def est_termine(grille):
    # Cette fonction vérifie si la grille est dans l'état final
    taille = len(grille)
    compteur = 1  
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] != 0 and grille[i][j] != compteur:
                return False
            compteur += 1
    print("\nFélicitations, vous avez gagné !\n")
    return True

def heuristique(grille):
    # Cette heuristique calcule le nombre de pièces mal placées
    taille = len(grille)
    mal_places = 0
    compteur = 1
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] != 0 and grille[i][j] != compteur:
                mal_places += 1
            compteur += 1
    return mal_places   

def generer_voisins(grille, closed_list):
    # Cette fonction va générer les grilles voisines de "grille"
    voisins = []
    directions = {'b': (-1, 0), 'h': (1, 0), 'd': (0, -1), 'g': (0, 1)} # Utile pour la génération de la séquence solution
    
    for direction, (dx, dy) in directions.items():
        grille_copy = [ligne[:] for ligne in grille]
        x, y = trouver_case_vide(grille)
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grille) and 0 <= ny < len(grille):
            grille_copy[x][y], grille_copy[nx][ny] = grille_copy[nx][ny], grille_copy[x][y]
            if tuple(tuple(ligne) for ligne in grille_copy) not in closed_list:
                voisins.append((grille_copy, direction)) 
    return voisins

def a_star(taquin):
    taille = len(taquin)
    objectif = [[(i * taille + j + 1) % (taille * taille) for j in range(taille)] for i in range(taille)] # Il s'agit de notre état final
    
    # On initialise la liste des nœuds ouverts
    open_list = []
    heapq.heappush(open_list, (heuristique(taquin), taquin, []))  # coût f(n), grille, chemin
    # On initialise la liste des nœuds fermés (les grilles déjà explorées)
    closed_list = set()

    while open_list:
        _, grille_actuelle, chemin_mouvements = heapq.heappop(open_list) # On sélectionne le nœud avec le plus faible coût total f(n)
        # Note : le _ désigne le f qui est utile pour le tri mais inutile après l'extraction
        
        if grille_actuelle == objectif:
            return chemin_mouvements
        
        closed_list.add(tuple(tuple(ligne) for ligne in grille_actuelle)) # On ajoute la grille actuelle à la liste des nœuds fermés
        
        for voisin, mouvement in generer_voisins(grille_actuelle, closed_list):
            g = len(chemin_mouvements) + 1
            h = heuristique(voisin)
            f_voisin = g + h
            if tuple(tuple(ligne) for ligne in voisin) not in closed_list:
                heapq.heappush(open_list, (f_voisin, voisin, chemin_mouvements + [mouvement]))
    
    return None

def main():
    taille = 3
    taquin = creer_taquin(taille)
    afficher_taquin(taquin)

    solution = a_star(taquin)
    if solution:
        print("\nSolution trouvée !")
        print("Séquence des mouvements :", ''.join(solution))
    else:
        print("Aucune solution trouvée.")

    while not est_termine(taquin):
        direction = input("Tapez (h ↑, b ↓, g ←, d →) ou 'q' pour quitter : ")
        if direction == 'q':
            break
        deplacer(taquin, direction)
        afficher_taquin(taquin)

if __name__ == "__main__":
    main()