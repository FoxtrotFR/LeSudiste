# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Plateforme : pass

import sys
import random

def create (): #ceer le type plateforme
    plateforme = Plateforme()
    plateforme.x = 153
    plateforme.y =random.randint (25,40)
    plateforme.lenth=40
    plateforme.look = ''
    plateforme.taille =0

    

    return plateforme


def show(listeplateforme,nbr):

    x=str(int(listeplateforme[nbr][1]))
    y=str(int(listeplateforme[nbr][2]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position de la plateforme

    sys.stdout.write(listeplateforme[nbr][0]) #afficher la plateforme

def getlenth (plateforme): #renvoyer la longueur d'une plateforme 
    return plateforme.lenth

def getheight(plateforme): #renvoyer la hauteur d'une plateforme
    return plateforme.y 

def listeplat (listeplateforme,plateforme):
    listeplateforme.append(['',plateforme.x,plateforme.y,plateforme.lenth,plateforme.taille])
    return listeplateforme

def move(listeplateforme,speed,dt):
    for i in listeplateforme :
        i[1]-=speed*dt

def reduire (listeplateforme,nbr) : 
    #reduire la taille de la plateforme afin qu'elle disparaisse
    listeplateforme[nbr][3]-=1
    listeplateforme[nbr][0]=''
    for i in range (listeplateforme[nbr][3]):
        listeplateforme[nbr][0]=listeplateforme[nbr][0]+ '_' 
        #modifier la valeur de x
    listeplateforme[nbr][1]+=1 
    return listeplateforme[nbr]
    

def augmenter(listeplateforme, nbr,speed, dt):
    listeplateforme[nbr][4]+= speed*dt
    if len(listeplateforme[nbr][0])<listeplateforme[nbr][3] and listeplateforme[nbr][4]>=1: #augmenter la taille de plateforme pour la faire apparaitre
        for i in range(int(listeplateforme[nbr][4])):
            listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
            listeplateforme[nbr][4]-=1
        
    return listeplateforme[nbr]
