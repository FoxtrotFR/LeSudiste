# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:47:28 2023

@author: Maxime
"""

class Ennemi : pass

import sys 


def create (img,x,y):
    ennemi = Ennemi()
    ennemi.x= x
    ennemi.y=y
    look = open (img,"r")
    ennemi.look = look.read()
    look.close()
    return ennemi
    
def show(ennemi):
    #se placer à la position du personnage 
    x=str(int(ennemi.x))
    y=str(int(ennemi.y))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    
    #afficher le personnage 
    sys.stdout.write(ennemi.look)

    if __name__=="__main__":
        players = create()
        
