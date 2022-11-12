# ELEVES: Sophia CHABOT, Eugene LALLAIN; CLASSE: 1ereGr2

# Import des bibliothèques/fonctions requises
from copy import deepcopy
from tkinter import *

# Definition des fonctions du jeu
def initialisation(n): # Renvoie un tableau de 15x15    
    tab = []
    for i in range(n): ## Boucle qui rajoute n ligne aux tableau
        line = []
        for j in range(n): ## Boucle qui rajoute n éléments à chaque ligne
            line = line + ['.']
        tab = tab + [line]
    return tab

def affichage(tab): # Affiche le tableau
    canvas.delete('cell') ## Supression des cases existantes s'il y en a
    l = 600/len(tab) ## Calcule la largeur des cases selon la taille du tableau
    for i in range(len(tab)):
        for j in range(len(tab)):
            if tab[i][j] == 'X':
                canvas.create_rectangle(l*j, l*i, l*(j+1), l*(i+1), outline="black", fill='black',tag='cell')
            else:
                canvas.create_rectangle(l*j, l*i, l*(j+1), l*(i+1), outline="black", fill='white',tag='cell')

def init_carre(tab): # Place 9 cellules vivantes au milieu du tableau
    for i in range(3):
        for j in range(3):
            tab[round((len(tab)-3)/2)+i][round((len(tab)-3)/2)+j] = 'X'

def init_diag(tab): # Place des cellules vivantes sur les diagonales (en X)
    for i in range(len(tab)):
        tab[i][i] = 'X'
        tab[i][len(tab[i])-i-1] = 'X'

def init_croix(tab): # Place des cellules en croix (+)
    for i in range(len(tab)):
        tab[i][round((len(tab)-1)/2)] = 'X'
    for i in range(len(tab)):
        tab[round((len(tab)-1)/2)][i] = 'X'

def set_mode(m): # Choix de situation de base
    global tab
    canvas.delete('cell') ## Supression des cases existantes s'il y en a
    tab = initialisation(size_scale.get())
    if m == "Carré":
        init_carre(tab)
    if m == "Diagonales en X":
        init_diag(tab)
    if m == "Croix en +":
        init_croix(tab)
    affichage(tab)

def draft(t): # Renvoie un tableau avec un cadre de case morte (evite les tests)
    tab2 = t
    n = len(tab)
    # On rajoute une case aux extrémité de chaque ligne:
    for i in range(n):
        tab2[i]=['.']+t[i]+['.'] 
    # Rajout de lignes entières en haut et en bas du tableau:
    tab2 = [['.']*(n+2)] + tab2 + [['.']*(n+2)]
    return tab2

def compare(tab1,tab2): # Compare 2 tableau en enlevant les case de test à la deepcopy
    for i in range(len(tab1)):
        ligne = []
        for j in range(1,len(tab1[i])-1):
            ligne = ligne + [tab1[i][j]]
        tab1[i] = ligne
    if tab1 == tab2:
        stop = True
    else:
        stop = False 
    return stop

def compte(t,ligne,colonne): # Comptage de cases vivantes
    # On défini d'abord l'ensemble des cellules qui en entourent une:
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
        if i == 'X':
            count += 1
    return count

def next_generation(tab): # Calcul de l'evolution de la colonie
    global arret
    copie = deepcopy(tab)
    t = draft(copie)
    for i in range(len(tab)): ## Analyse par ligne
        for j in range(len(tab)): ## Analyse par élément de chaque ligne
            ## Analyse et evolution pour chaque cellule
            if t[i+1][j+1] == 'X' and compte(t,i+1,j+1) != 3:
                tab[i][j] = '.'
            elif compte(t,i+1,j+1) == 2 or compte(t,i+1,j+1) == 3:
                tab[i][j] = 'X'
    arret = compare(copie,tab)

def jeu_de_la_vie(): # Affichage des génération de la colonie
    global arret
    next_generation(tab)
    affichage(tab)
    if arret == False:
        canvas.delete('msg') ## Supprime les messages de fin du jeu s'il y en a
    if arret == True: ## Affiche quand la colonie n'évolue plus
        fond = canvas.create_rectangle(0,275,600,325,outline='black',fill='black',tag='msg')
        msg = canvas.create_text(300,300,fill='white',text="La colonie n'évolue plus!",font=("Times",16),tag='msg')
        arret = False

# Fenêtre de jeu:
fen = Tk()
fen.title('Jeu de la Vie')
fen.geometry("600x670")
fen.maxsize(600, 700) 
fen.minsize(600, 700) 
fen.configure(background='#4F4F4F')

# Titre:
title = Label(fen,text="Jeu de la Vie", font=("Times New Roman",22), bg='black', fg='white')
title.place(x=0,y=0,width=600, height=50)

# Reglage de la taille de la grille:
size_label = Label(fen,text="Taille de la grille: ", font=("Times",12), bg='black', fg='white')
size_label.place(x=150,y=60,width=120,height=30)
size_scale = Scale(fen,orient='horizontal',from_=5,to=30,variable=IntVar,bg='#4F4F4F',troughcolor='black',fg='white',bd=0,highlightthickness=0)
size_scale.set(15)
size_scale.place(x=280,y=58,width=200,height=30)

# Canvas:
canvas = Canvas(fen, width=600, height=600, bg='white')
canvas.place(x=0, y=100, width=600, height=600)

# Choix de mode d'initialisation:
modelist = ["Initial","Carré","Diagonales en X","Croix en +"]
variable = StringVar(fen)
variable.set(modelist[0])
mode = OptionMenu(fen,variable, *modelist, command=set_mode)
mode.config(font=("Times",12), bg='black', fg='white', highlightthickness=0)
mode.place(x=10,y=60,width=130,height=30)

# Initialisation de la grille:
tab = initialisation(size_scale.get())
arret = False
n = len(tab)
affichage(tab)

# Lancement du jeu par un bouton:
generate = Button(fen, text='Next', command=jeu_de_la_vie, font=("Times",12), bg='black', fg='white')
generate.place(x=490, y=60, width=100, height=30)

# Lancement du gestionnaire d'évènements
fen.mainloop()