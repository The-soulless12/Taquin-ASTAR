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
    directions = ['b', 'h', 'd', 'g']
        
    for direction in directions:
        grille_copy = [ligne[:] for ligne in grille]
        deplacer(grille_copy, direction)
        if tuple(tuple(ligne) for ligne in grille_copy) not in closed_list:
            voisins.append(grille_copy)
    return voisins

def a_star(taquin):
    taille = len(taquin)
    objectif = [[(i * taille + j + 1) % (taille * taille) for j in range(taille)] for i in range(taille)] # Il s'agit de notre état final
    
    # On initialise la liste des nœuds ouverts
    open_list = []
    heapq.heappush(open_list, (heuristique(taquin), taquin, []))  # (coût f(n), grille, chemin)
    # On initialise la liste des nœuds fermés (les grilles déjà explorées)
    closed_list = set()

    while open_list:
        _, grille_actuelle, chemin = heapq.heappop(open_list) # On sélectionne le nœud avec le plus faible coût total f(n)
        # Note : le _ désigne le f qui est utile pour le tri mais inutile après l'extraction
        
        if grille_actuelle == objectif:
            return chemin
        
        closed_list.add(tuple(tuple(ligne) for ligne in grille_actuelle)) # On ajoute la grille actuelle à la liste des nœuds fermés
        
        for voisin in generer_voisins(grille_actuelle, closed_list):
            g = len(chemin) + 1
            h = heuristique(voisin)
            f_voisin = g + h
            if tuple(tuple(ligne) for ligne in voisin) not in closed_list:
                heapq.heappush(open_list, (f_voisin, voisin, chemin + [voisin]))
    
    return None

def main():
    taille = 3
    taquin = creer_taquin(taille)
    afficher_taquin(taquin)

    solution = a_star(taquin)
    if solution:
        print("\nSolution trouvée !")
        for etape in solution:
            afficher_taquin(etape)
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