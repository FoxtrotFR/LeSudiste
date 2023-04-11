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
    ennemi.look = look.read().splitlines()
    look.close()
    return ennemi
    
def show(ennemi):
    #separer l'ennemi en ligne 
    t= ennemi.look
    
    #afficher le personnage ligne par ligne 
    for i in range(len(ennemi.look)):
        x=str(int(ennemi.x))
        y=str(int(ennemi.y)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)#se placer à la position du personnage 



        sys.stdout.write(t[i]) #afficher la ligne 
    
    
    
      
    

if __name__=="__main__":
    ennemi = create("ennemi.txt",10,10)
    show(ennemi)
    
    