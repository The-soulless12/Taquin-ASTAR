import random
import heapq
from colorama import Fore, Style
import tkinter as tk
from tkinter import messagebox

def creer_taquin(taille):
    while True:
        # On génère les valeurs dans le désordre
        valeurs = list(range(1, taille * taille)) + [0] 
        random.shuffle(valeurs)
        grille = [valeurs[i * taille:(i + 1) * taille] for i in range(taille)]
        
        # Vérifie si le taquin est solvable
        if est_solvable(grille) and grille != [[(i * taille + j + 1) % (taille * taille) for j in range(taille)] for i in range(taille)]:
            return grille

def transposition(valeurs, N):
    # Cette fonction calcule le nombre de transpositions dans une configuration donnée
    valeurs_new = [N if v == 0 else v for v in valeurs]  # On remplace la case vide par N
    cible = sorted(valeurs_new)
    transpositions = 0
    index_map = {val: i for i, val in enumerate(valeurs_new)}  # On cherche la losition actuelle de chaque valeur
    
    for i in range(len(valeurs_new)):
        while valeurs_new[i] != cible[i]:  # Tant que la valeur à l'index n'est pas correcte
            cible_index = index_map[cible[i]]  # L'index où la valeur correcte doit être
            valeurs_new[i], valeurs_new[cible_index] = valeurs_new[cible_index], valeurs_new[i]  # On effectue un swap
            index_map[valeurs_new[cible_index]] = cible_index  # On met à jour l'index de la valeur échangée
            index_map[valeurs_new[i]] = i  # On met à jour l'index de la valeur actuelle
            transpositions += 1  # On augmenter le compteur de transpositions
    
    return transpositions 

def permutations_case_vide(valeurs, taille):
    # Cette fonction calcule le nombre de permutations nécessaires pour déplacer la case vide jusqu'à la fin du tableau
    valeurs_new = [taille*taille if v == 0 else v for v in valeurs]
    index_vide = valeurs_new.index(taille*taille)  # On cherche la position actuelle de la case vide
    
    ligne = (index_vide) // taille
    colonne = (index_vide) % taille
    # On permute horizontalement la case vide jusqu'à la fin de sa ligne puis verticalement jusqu'à la fin de sa colonne
    return ( 2*taille- 2 - ligne - colonne)

def est_solvable(grille):
    # Cette fonction vérifie si une configuration de taquin est solvable ou pas
    taille = len(grille)
    valeurs = [grille[i][j] for i in range(taille) for j in range(taille)]
    N = taille * taille  # Valeur à utiliser pour remplacer le 0
    
    nb_transposition = transposition(valeurs, N)
    nb_permutations= permutations_case_vide(valeurs, taille)
    # Le problème est solvable si la parité de la permutation est identique à la parité de permutation la case vide
    return (nb_transposition % 2) == (nb_permutations% 2) # Il s'agit d'un XOR

def afficher_taquin(grille):
    # Affiche le taquin en mode console
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

import tkinter as tk
from tkinter import messagebox

# Création de l'interface graphique du Taquin
class TaquinApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taquin")

        self.taille = 4  # La taille du taquin
        self.taquin = creer_taquin(self.taille)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.labels = [[None for _ in range(self.taille)] for _ in range(self.taille)]
        self.create_buttons()

        self.entry = tk.Entry(self.root, font=("Courier", 14))
        self.entry.pack()

        self.submit_button = tk.Button(self.root, text="Déplacer", command=self.deplacer_utilisateur)
        self.submit_button.pack()

        # En raison de l'explosion combinatoire de l'algorithme A* et de la puissance de la machine exécutant
        # le programme, il est recommandé d'utiliser A* uniquement pour les taquins de taille 3x3.
        if self.taille <= 3:
            self.result_button = tk.Button(self.root, text="Trouver solution", command=self.trouver_solution)
            self.result_button.pack()
        self.root.bind('<Return>', self.deplacer_utilisateur_entree)

        self.root.resizable(False, False)

    def create_buttons(self):
        for i in range(self.taille):
            for j in range(self.taille):
                label = tk.Label(self.frame, text=self.taquin[i][j] if self.taquin[i][j] != 0 else '',
                                 width=4, height=2, relief="solid", font=("Courier", 14))
                label.grid(row=i, column=j, padx=5, pady=5)
                self.labels[i][j] = label
                # Ajout d'un événement de clic pour déplacer une pièce
                label.bind("<Button-1>", lambda event, x=i, y=j: self.clic_piece(x, y))
        self.update()

    def update(self):
        for i in range(self.taille):
            for j in range(self.taille):
                value = self.taquin[i][j]
                if value == 0:
                    self.labels[i][j].config(text="", bg="white")
                else:
                    self.labels[i][j].config(text=str(value), bg="lightpink")

    def clic_piece(self, i, j):
        # Trouve la position de la case vide
        x, y = trouver_case_vide(self.taquin)
        
        # Vérifie si la pièce cliquée est adjacente à la case vide
        if abs(i - x) + abs(j - y) == 1:
            self.taquin[x][y], self.taquin[i][j] = self.taquin[i][j], self.taquin[x][y]
            self.update()
            if est_termine(self.taquin):
                messagebox.showinfo("Victoire", "Félicitations, vous avez gagné !")

    def deplacer_utilisateur(self, event=None):
        direction = self.entry.get()
        if direction in ['h', 'b', 'd', 'g']:
            deplacer(self.taquin, direction)
            self.update()
            if est_termine(self.taquin):
                messagebox.showinfo("Victoire", "Félicitations, vous avez gagné !")
        else:
            self.entry.delete(0, tk.END)
        
        self.entry.delete(0, tk.END)

    def deplacer_utilisateur_entree(self, event):
        self.deplacer_utilisateur()

    def trouver_solution(self):
        solution = a_star(self.taquin)
        if solution:
            messagebox.showinfo("Solution trouvée", f"Solution : {' '.join(solution)}")
        else:
            messagebox.showinfo("Solution", "Aucune solution trouvée.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaquinApp(root)
    root.mainloop()