# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Frites : pass

import sys
import random

def create ():
    frite = Frites()
    frite.x = 147
    frite.y = 15
    frite.look = ['/','|','\\']
    frite.tempo =random.randint (30,60)
    
    return frite

def show (listefrites,nbr): #etat varie en focntion de la gravité (voir liste frites.look)
    x=str(int(listefrites[nbr][1]))
    y=str(int(listefrites[nbr][2]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position du personnage 

    sys.stdout.write(listefrites[nbr][0]) #afficher la frite

def move (listefrites,speed,gravite,dt):
    for i in listefrites :
        i[1]-=speed*dt #appliquer la vitesse lateral
        i[2]+=(gravite*dt)/5 #appliquer la gravite(diminué)

def fritliste(listefrites,frite,etat):
    listefrites.append([frite.look[etat],frite.x,frite.y, frite.tempo]) #rajout d'une frite 
    return listefrites

