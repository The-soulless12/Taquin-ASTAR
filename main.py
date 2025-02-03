import random
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

def deplacer_taquin(grille, direction):
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

def main():
    taille = 4
    taquin = creer_taquin(taille)
    afficher_taquin(taquin)

    while True:
        direction = input("Tapez (h ↑, b ↓, g ←, d →) ou 'q' pour quitter : ")
        if direction == 'q':
            break
        deplacer_taquin(taquin, direction)
        afficher_taquin(taquin)

if __name__ == "__main__":
    main()