# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Frites : pass

import sys

def create (x,y,speed):
    frites = Frites()
    frites.x = x
    frites.y = y
    frites.speed = speed
    frites.look = ['/','|','\\']
    
    return frites

def show (frites,etat): #etat varie en focntion de la gravité (voir liste frites.look)
    x=str(int(frites.x))
    y=str(int(frites.y))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position du personnage 

    sys.stdout.write(frites.look[etat]) #afficher la fritte


#test validé
#if __name__=="__main__":
#    frites = create(10,10,0)
#    show(frites,1)
    