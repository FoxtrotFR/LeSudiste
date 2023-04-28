# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Tonneau : pass

import sys
import random

#creer le tonneau
def create (lenthplat,y):
    tonneau = Tonneau()
    lenthplat=lenthplat-18+151
    tonneau.x = random.randint(165,lenthplat)
    tonneau.y = y-2
    look=open("tonneau.txt","r")
    tonneau.look = look.read().splitlines()
    look.close()
    
    return tonneau

def create2():
    tonneau=Tonneau()
    tonneau.x=random.randint(1,149)
    tonneau.y=8
    tonneau.tempo=random.randint(5,15)
    look=open("tonneau.txt","r")
    tonneau.look = look.read().splitlines()
    look.close()

    return tonneau

def listonneau(listetonneau,tonneau):
    listetonneau.append(tonneau)
    return listetonneau
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

def move(tonneau,speed,dt):
    tonneau.x-=speed*dt

def move2(tonneau,speed,dt):
    tonneau.y+=(speed*dt)/3




