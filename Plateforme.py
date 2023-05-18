# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Plateforme : pass

import Tonneau
import sys
import random

def create (score): #ceer le type plateforme
    plateforme = Plateforme()
    plateforme.x = 151
    plateforme.y =random.randint (32,39)  #position en y de la plateforme 
    plateforme.lenth=random.randint (80,100) #taille total de la plateforme 
    plateforme.look = ''
    plateforme.taille =0 #taille actuel de plateforme 
    plateforme.trou = random.randint(3,7) #taille de trou qui suit la plateforme 
    if score>40:
        plateforme.tonneau = random.randint (1,4)
    else : plateforme.tonneau = 2
    if plateforme.tonneau ==1: 
        plateforme.ton=Tonneau.create(plateforme.lenth,plateforme.y) #creer le tonneau 
    else :
        plateforme.ton = ''

    return plateforme

def create2():
    plateforme = Plateforme()
    plateforme.x = random.randint (1,152)
    plateforme.y =10  #position en y de la plateforme 
    plateforme.lenth = random.randint (50,70) #taille total de la plateforme 
    while plateforme.x+plateforme.lenth >153:
        plateforme.lenth-=2

    plateforme.look = ''
    for i in range (plateforme.lenth):
        plateforme.look= plateforme.look+'_'
    plateforme.trou=random.randint(10,20)
    plateforme.tonneau=2
    plateforme.ton=''
    plateforme.taille=0
    return plateforme 

def create3 (): #ceer le type plateforme
    plateforme = Plateforme()
    plateforme.y =random.randint (32,39)  #position en y de la plateforme 
    plateforme.lenth=random.randint (60,80) #taille total de la plateforme 
    plateforme.x = 0
    plateforme.look = ''
    plateforme.taille =0 #taille actuel de plateforme 
    plateforme.trou = random.randint(4,9) #taille de trou qui suit la plateforme 
    plateforme.tonneau = 2
    plateforme.ton = ''

    return plateforme
    

def show(listeplateforme,nbr):

    x=str(int(listeplateforme[nbr][1]))
    y=str(int(listeplateforme[nbr][2]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position de la plateforme

    sys.stdout.write(listeplateforme[nbr][0]) #afficher la plateforme

    if listeplateforme[nbr][6]==1 and listeplateforme[nbr][7].x<150:
        if listeplateforme[nbr][7].x<=1: #supprimer le tonneau 
            listeplateforme[nbr][6]=2 
        else :
            Tonneau.show(listeplateforme[nbr][7]) #afficher le tonneau





def listeplat (listeplateforme,plateforme):
    listeplateforme.append([plateforme.look,plateforme.x,plateforme.y,plateforme.lenth,plateforme.taille, plateforme.trou,plateforme.tonneau,plateforme.ton]) #liste de 8 elements 
    return listeplateforme




def move(listeplateforme,speed,dt):
    for i in listeplateforme :
        i[1]-=speed*dt
        if i[6]==1: #bouger le tonneau s'il y en a un
            Tonneau.move(i[7],speed,dt)

def move2(listeplateforme,speed,dt):
    for i in listeplateforme :
        i[2]+=(speed/3)*dt   
        if i[5]>0:#plateforme.trou(la tempo)
            i[5]-=(speed/3)*dt   

def move3(listeplateforme,speed,dt):
    for i in listeplateforme:
        i[1]+=speed*dt

def reduire3(listeplateforme,nbr):
    #reduire la taile de plateforme pour la fiare disparaitre 
    diminution = listeplateforme[nbr][1]+listeplateforme[nbr][3]-152
    listeplateforme[nbr][0]=''
    listeplateforme[nbr][3]-=diminution
    for i  in range (int(listeplateforme[nbr][3])):
        listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
    return listeplateforme[nbr]

def augmenter3(listeplateforme, nbr,speed, dt):
    if int(listeplateforme[nbr][3])>len(listeplateforme[nbr][0]): #4: plateforme.taille et 3 : plateforme.lenth
        
        rajout = int(listeplateforme[nbr][1])
        
        for i in range (int(rajout)):
            listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
        listeplateforme[nbr][1]=0
    else:
        listeplateforme[nbr][5]-= speed*dt #reduire le trou pour la nouvelle plateforme 
    

    return listeplateforme[nbr]


def reduire (listeplateforme,nbr) : 
    #reduire la taille de la plateforme afin qu'elle disparaisse
    diminution = -listeplateforme[nbr][1] #valeur de x negative (indique le depassement de cbm de carre de cette derniere)
    if len(listeplateforme[nbr][0])>0: #voir si inutile 
        listeplateforme[nbr][0]=''
    listeplateforme[nbr][3]-=diminution
    for i in range (int(listeplateforme[nbr][3])): #regenere une plateforme de la bonne taille 
        listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
    listeplateforme[nbr][1]=0 #remet x à 0
    return listeplateforme[nbr]
    

def augmenter(listeplateforme, nbr,speed, dt):
    if int(listeplateforme[nbr][4])<=listeplateforme[nbr][3]: #4: plateforme.taille et 3 : plateforme.lenth
        listeplateforme[nbr][4]+= speed*dt
        rajout =int (listeplateforme[nbr][4]- len(listeplateforme[nbr][0]))
        for i in range (rajout):
            listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
    else:
        listeplateforme[nbr][5]-= speed*dt #reduire le trou pour la nouvelle plateforme 
        listeplateforme[nbr][4] = listeplateforme[nbr][3]

    return listeplateforme[nbr]
