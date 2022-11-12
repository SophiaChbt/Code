# Import des bibliotheques requises
from copy import deepcopy

def initialisation(n): # Renvoie un tableau de 15x15
    tab = []
    for i in range(n):
        line = []
        for j in range(n):
            line = line + ['. ']
        tab = tab + [line]
    return tab

def affichage(tab): # Affiche le tableau
    for i in range(len(tab)):
        line = ""
        for j in range(len(tab[i])):
            line += str(tab[i][j])
        print(line)

def init_carre(tab): # Place 9 cellules vivantes au milieu du tableau
    for i in range(3):
        for j in range(3):
            tab[round((len(tab)-3)/2)+i][round((len(tab)-3)/2)+j] = 'X '

def init_diag(tab): # Place des cellules vivantes sur les diagonales (en X)
    for i in range(len(tab)):
        tab[i][i] = 'X '
        tab[i][len(tab[i])-i-1] = 'X '

def init_croix(tab): # Place des cellules en croix (+)
    for i in range(len(tab)):
        tab[i][round((len(tab[i])-1)/2)] = 'X '
    for i in range(len(tab[1])):
        tab[round((len(tab)-1)/2)][i] = 'X '

def draft(tab): # Renvoie un tableau avec un cadre de case morte en plus
    n = len(tab)
    tab2 = tab
    for i in range(0,n):
        tab2[i]=['. ']+tab[i]+['. ']
    tab2 = [['. ']*(n+2)] + tab2 + [['. ']*(n+2)]
    return tab2

def compare(tab1,tab2): # Compare 2 tableau en enlevant les case de test à la deepcopy
    global arret
    for i in range(len(tab1)):
        ligne = []
        for j in range(1,len(tab1[i])-1):
            ligne = ligne + [tab1[i][j]]
        tab1[i] = ligne
    if tab1 == tab2:
        arret = True

def compte(t,ligne,colonne): # Comptage de cases vivantes
    entourage = [t[ligne-1][colonne-1],
                 t[ligne-1][colonne],
                 t[ligne-1][colonne+1],
                 t[ligne][colonne-1],
                 t[ligne][colonne+1],
                 t[ligne+1][colonne-1],
                 t[ligne+1][colonne],
                 t[ligne+1][colonne+1]]
    count = 0
    for i in entourage:
        if i == 'X ':
            count += 1
    return count

def next_generation(tab): # Calcul des génération de la colonie
    global arret    
    copie = deepcopy(tab)
    t = draft(copie)
    for i in range(n):
        for j in range(n):
            if t[i+1][j+1] == 'X ' and compte(t,i+1,j+1) != 3:
                    tab[i][j] = '. '
            elif compte(t,i+1,j+1) == 2 or compte(t,i+1,j+1) == 3:
                tab[i][j] = 'X '
    compare(copie,tab)

def jeu_de_la_vie(): # Calcul et affichage des générations
    global arret
    arret = False
    while arret == False:
        if input("n for Next Generation: ")=="n":
            next_generation(tab)
            affichage(tab)
    if arret == True:
        print("La colonie n'évolue plus, entrez 'jeu_de_la_vie()' pour recommencer le jeu :D")

#Initialisation de la grille
n = int(input("Choisissez la taille de la grille: "))
tab = initialisation(n)
copie = deepcopy(tab)
affichage(tab)

#Choix d'initialisation de colonie
print("Comment voulez-vous initialiser la colonie?")
print("  1.carré")
print("  2.diagonales en X")
print("  3.croix en +")
mode = input("ENTREZ CHIFFRE: ")
if mode == "1":
    init_carre(tab)
if mode == "2":
    init_diag(tab)
if mode == "3":
    init_croix(tab)
affichage(tab)

#Lancement du jeu
jeu_de_la_vie()