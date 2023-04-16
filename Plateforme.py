# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Plateforme : pass

import sys
import random

def create (lenth,y): #ceer le type plateforme
    plateforme = Plateforme()
    plateforme.x = 152
    plateforme.y =y
    plateforme.lenth=lenth
    plateforme.look = ''
    for i in range (plateforme.lenth):
        plateforme.look+='_'
    
    
    return plateforme

def show(listeplateforme,nbr):

    x=str(int(152))
    y=str(int(listeplateforme[nbr][1]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position du personnage 

    sys.stdout.write(listeplateforme[nbr][0]) #afficher la fritte

def getlenth (plateforme): #renvoyer la longueur d'une plateforme 

    return plateforme.lenth

def getheight(plateforme): #renvoyer la hauteur d'une plateforme
    return plateforme.y 

def listeplat (listeplateforme,plateforme):
    listeplateforme.append([plateforme.look,plateforme.x,plateforme.y])
    return listeplateforme
