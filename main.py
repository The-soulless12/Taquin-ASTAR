import random

def creer_taquin(taille):
    # On génére les valeurs dans le désordre
    valeurs = list(range(1, taille * taille)) + [0] 
    random.shuffle(valeurs) 
    return [valeurs[i * taille:(i + 1) * taille] for i in range(taille)]

def afficher_taquin(grille):
    taille = len(grille)
    largeur = len(str(taille * taille - 1))
    separateur = "+" + ("-" * (largeur + 2) + "+") * taille
    
    for ligne in grille:
        print(separateur)
        print("| " + " | ".join(f"{cell:>{largeur}}" if cell != 0 else " " * largeur for cell in ligne) + " |")
    print(separateur)

def main():
    taille = 4
    taquin = creer_taquin(taille)
    afficher_taquin(taquin)

if __name__ == "__main__":
    main()