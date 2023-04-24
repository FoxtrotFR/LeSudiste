# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Plateforme : pass

import Tonneau
import sys
import random

def create (): #ceer le type plateforme
    plateforme = Plateforme()
    plateforme.x = 151
    plateforme.y =random.randint (32,39)  #position en y de la plateforme 
    plateforme.lenth=random.randint (60,80) #taille total de la plateforme 
    plateforme.look = ''
    plateforme.taille =0 #taille actuel de plateforme 
    plateforme.trou = random.randint(3,8) #taille de trou qui suit la plateforme 
    plateforme.tonneau = 1 #random.randint (1,4)
    if plateforme.tonneau ==1: 
        plateforme.ton=Tonneau.create(plateforme.lenth,plateforme.y) #creer le tonneau 
    else :
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
    listeplateforme.append(['',plateforme.x,plateforme.y,plateforme.lenth,plateforme.taille, plateforme.trou,plateforme.tonneau,plateforme.ton]) #liste de 8 elements 
    return listeplateforme

def move(listeplateforme,speed,dt):
    for i in listeplateforme :
        i[1]-=speed*dt
        if i[6]==1: #bouger le tonneau s'il y en a un
            Tonneau.move(i[7],speed,dt)
        

def reduire (listeplateforme,nbr) : 
    #reduire la taille de la plateforme afin qu'elle disparaisse
    if len(listeplateforme[nbr][0])>0:
        listeplateforme[nbr][3]+=listeplateforme[nbr][1] #enleve x a la taille de la plateforme 
    listeplateforme[nbr][0]=''
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
