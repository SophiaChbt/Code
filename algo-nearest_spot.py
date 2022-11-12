from math import *
from random import randint

import matplotlib.pyplot as plt


def alea(a, b):
    x = randint(a, b)
    y = randint(a, b)
    return (x, y)
    
def centreGymnase(a, b, n):
    L = []
    for i in range(n):
        L.append(alea(a, b))
    return L

def distance(a, b):
    return sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def GPS(moi, listeGym):
    listeDist = []
    for i in listeGym:
        listeDist.append(distance(moi, i))
    return listeGym[listeDist.index(min(listeDist))]

def tri(moi, listeGym):
    listeDist = []   # listeDist = [[distance1,(x1,y1)],[distance2,(x2,y2)], ...]
    for i in listeGym:
        listeDist += [[distance(moi, i), i]]
    for i in range(len(listeDist)):
        for j in range(len(listeDist)-i-1):
            if listeDist[j][0] > listeDist[j+1][0]:
                listeDist[j], listeDist[j+1] = listeDist[j+1], listeDist[j]
    return listeDist

listeGymnase = centreGymnase(-50,50,10)
abcisse = []
ordonnee = []
for i in listeGymnase:
    abcisse.append(i[0])
    ordonnee.append(i[1])

plt.figure(dpi=100)
plt.plot(abcisse,ordonnee,'.',color='b')
plt.hsv()

moi = alea(-50,50)
plt.plot(moi[0],moi[1],'.',color='r')
plt.plot([moi[0],GPS(moi,listeGymnase)[0]],[moi[1],GPS(moi,listeGymnase)[1]],'-',color='r')

listeTri = tri(moi, listeGymnase)
for i in range(len(listeTri)):
    x = (len(listeTri)-i)/len(listeTri)
    plt.plot([moi[0],listeTri[i][1][0]],[moi[1],listeTri[i][1][1]],'--',color=(1,1,x),lw=x/2)
    cercle = plt.Circle(moi,radius=listeTri[i][0], color=(1,1,x), fill=False,lw=x)
    bx=plt.gca()
    bx.add_patch(cercle)

cercle = plt.Circle(moi,radius=distance(moi,GPS(moi,listeGymnase)), color='yellow', fill=False)
ax = plt.gca()
ax.add_patch(cercle)

plt.axis('scaled')
plt.show()


