# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Plateforme : pass

import sys

def create (x,y,lenth): #ceer le type plateforme
    plateforme = Plateforme()
    plateforme.x = x
    plateforme.y = y
    plateforme.lenth=lenth
    plateforme.look = ''
    
    return plateforme

def show(plateforme):
    for i in range (plateforme.lenth):
        plateforme.look+='_'

    x=str(int(plateforme.x))
    y=str(int(plateforme.y))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position du personnage 

    sys.stdout.write(plateforme.look) #afficher la fritte

#test validé
if __name__=="__main__":
    plateforme = create(40,10,10)
    show(plateforme)