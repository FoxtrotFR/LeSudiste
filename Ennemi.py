# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:47:28 2023

@author: Maxime
"""

class Ennemi : pass

import sys 


def create (x,y):
    ennemi = Ennemi()
    ennemi.x= x
    ennemi.y=y
    look = open ("ennemi.txt","r")
    ennemi.look = look.read().splitlines()
    look.close()
    return ennemi
    
def show(ennemi):
    
    #afficher le personnage ligne par ligne 
    for i in range(len(ennemi.look)):
        x=str(int(ennemi.x))
        y=str(int(ennemi.y)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)#se placer à la position du personnage 
        sys.stdout.write("\033[91m" + ennemi.look[i] + "\033[0m") # afficher la ligne en rouge
    
    
    
def setposition_x(x,ennemi):
    ennemi.x=x
    return ennemi
def setposition_y(y,ennemi):
    ennemi.y=y
    return ennemi