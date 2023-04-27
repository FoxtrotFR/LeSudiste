# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Tonneau : pass

import sys

#creer le tonneau
def create (x,y,filename):
    tonneau = Tonneau()
    tonneau.x = x
    tonneau.y = y
    look=open(filename,"r")
    tonneau.look = look.read().splitlines()
    look.close()
    
    return tonneau


def show(tonneau):
    
    #afficher le tonneau ligne par ligne 
    for i in range(len(tonneau.look)):
        x=str(int(tonneau.x))
        y=str(int(tonneau.y)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)#se placer à la position du personnage 



        sys.stdout.write(tonneau.look[i]) #afficher la ligne 

def getheight(tonneau): #renvoyer la hauteur du tonneau
    return tonneau.y

#test validé
if __name__=="__main__":
    tonneau = create(10,10,"tonneau.txt")
    show(tonneau)
