#Elèves: Sophia CHABOT, Eugène LALLAIN

#Import des bibliothèques/fonctions requises
from tkinter import *
from random import randint
from math import tan,sqrt,radians

#Fonctions du jeu:
##Tracer une cible:
def draw_cible():
    global x, y
    r = lvl_scale.get()
    cible = canvas.create_polygon(x,y,x+r,y+r,x,y+2*r,x-r,y+r,tag='cible',outline="",fill='yellow')
    x = canvas.coords(cible)[0]
    y = canvas.coords(cible)[1]
##Orientation du canon et trajectoire du tir:
def tracer(k):
    global tube, bullet, x, y
    canvas.delete(tube)
    canvas.delete("traj")
    bullet = canvas.create_line(25, 435, 800, 435-775*k, fill='black', tag='traj')
    tube = canvas.create_line(25, 435, 25+30/sqrt(k**2+1), 435-k*30/sqrt(k**2+1), width=20, fill='#735F40')
    
##Verifier si le joueur gagne
def result(k):
    global cible, x, y
    contact1 = [canvas.gettags(item) for item in canvas.find_overlapping(x, y, x, y+2*lvl_scale.get())]
    contact2 = [canvas.gettags(item) for item in canvas.find_overlapping(x-lvl_scale.get(), y+lvl_scale.get(), x+lvl_scale.get(), y+lvl_scale.get())]
    if ("traj",) in contact1+contact2:
        enter["state"] = "disabled"
        win.place(x=200, y=200, width=300, height=90)
        win_score.config(text=f"Vous avez gagné en {count} essais !")
        win_score.place(x=200, y=270, width=300, height=60)

##Tirer
def tirer():
    global count
    #On vérifie que l'angle entré soit bien un nombre
    if not ent_angle.get().isdigit():
        angle_erreur.place(x=395, y=5, width=150, height=h)
        return
    angle_erreur.place(x=800, y=600)
    count+=1
    comptage.config(text="Nombre d'essais: "+str(count))
    if ent_angle.get() == "90": #tan(x) n'est pas définie pour x = 90
        k = 500
    else:
        k=tan(radians(int(ent_angle.get())))
    tracer(k)
    result(k)
    
##Relancer le jeu:
def reset():
    global count, win, win_score, x, y
    enter["state"] = "active"
    win.place(x=800, y=600)
    win_score.place(x=800, y=600)
    canvas.delete('traj','cible')
    count=0
    comptage.config(text="Nombre d'essais : 0")
    lvl.config(text="Rayon : "+str(lvl_scale.get()))
    x = randint(lvl_scale.get(), 700-lvl_scale.get())
    y = randint(h+2*m, 430-2*lvl_scale.get())
    draw_cible()    

#Fenêtre de jeu:
fenetre=Tk()
fenetre.title('CanonBall')
fenetre.geometry("800x500")
fenetre.maxsize(800, 500) 
fenetre.minsize(800, 500) 
fenetre.configure(background='#406AB0')

#Canvas:
canvas = Canvas(fenetre, width=700, height=460, bg='#99ccff')
canvas.place(x=0, y=40)

#Variables:
##Comptage d'essai réalisé:
count = 0
##Marge
m=5
##Hauteur des label
h=30
##Scale de niveau qui défini le rayon de la cible
lvl_scale = Scale(fenetre,from_=50,to=10,variable=IntVar,font=("Calibri",12),bd=0,troughcolor='#99ccff')
lvl_scale.set(30)
lvl_scale.place(x=728,y=150,width=45,height=255)
##Coordonnée de la cible (faisant en sorte qu'elle soit toujours entièrement visible):
x = randint(lvl_scale.get(), 700-lvl_scale.get())
y = randint(h+2*m, 430-2*lvl_scale.get())

#Barre d'information/Menu
##Saisie de l'angle de tir:
ask_angle = Label(fenetre, text="Entrez un angle :", font=("Calibri",12))
ask_angle.place(x=5, y=5, width=120, height=h)
ent_angle = Entry(fenetre, font=("Calibri",12))
ent_angle.place(x=130, y=5, width=60, height=h)
##Affichage si l'entrée d'angle n'est pas conforme
angle_erreur = Label(fenetre, text="Veuillez rentrer un entier!", bg="red", font=("Calibri",9,"bold"),fg="white")
##Bouton de lancement
enter = Button(fenetre, text='Go !', command=tirer, font=("Calibri",12))
enter.place(x=195, y=5, width=50, height=h)
##Bouton de replacement de la cible:
replace = Button(fenetre, text='Replacer une cible', command=reset, font=("Calibri",12,"bold"))
replace.place(x=250, y=5, width=140, height=h)
redef = Button(fenetre, text='Redéfinir', command=reset, font=("Calibri",12,"bold"))
redef.place(x=710, y=112, width=85, height=h)
##Affichage du nombre d'essai:
comptage = Label(fenetre, text="Nombre d'essais : 0", font=("Calibri",12))
comptage.place(x=550, y=5, width=150, height=h)
##Affichage du niveau
lvl = Label(fenetre, text="Rayon : "+str(lvl_scale.get()), font=("Calibri",12,"bold"),bg='#406AB0',fg='white')
lvl.place(x=710, y=80, width=85, height=h)
##Bouton quitter
quitter = Button(fenetre, text='QUITTER', command=fenetre.destroy, font=("Calibri",12))
quitter.place(x=710, y=500-h-5, width=85, height=h)

#Elements graphique du jeu
##Sol
floor = canvas.create_rectangle(0, 435, 700, 500, outline="", fill='#8BA464')
##Canon
base = canvas.create_oval(10, 420, 40, 450, outline="", fill='#735F40')
tube = canvas.create_line(25, 435, 25+30/sqrt(2), 435-30/sqrt(2), width=20, fill='#735F40')
##Affichage si le joueur gagne
win = Label(fenetre, text="Bien joué !", font=('Calibri',30,"bold"))
win_score = Label(fenetre, font=('Calibri', 12))
##Cible
draw_cible()

#Détection de la touche "Entrée" pour tirer
fenetre.bind("<Return>", lambda event: tirer())

#Lancement du gestionnaire d'évènements
fenetre.mainloop()
