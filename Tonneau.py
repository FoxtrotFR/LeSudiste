# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Tonneau : pass

import sys
import random

import Players

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

def creation (listetonneau,game,timeStep):
    if len(listetonneau)==0: # si la liste est vide 
        tonneau= create2()
        listetonneau = listonneau(listetonneau,tonneau)
    derniertonneau=len(listetonneau)-1
    if listetonneau[derniertonneau].tempo==0: #baisser le tempo du dernier tonneau
        tonneau = create2()
        listetonneau = listonneau(listetonneau,tonneau)
    listetonneau[derniertonneau].tempo-=1
    for i in listetonneau:
        move2(i,game.speed,timeStep) #bouger les tonneau
    return listetonneau

def collision (listetonneau,players,gamover):
    position_tonneau = 0
    delete_tonneau = 0
    #collision du tonneau avec le sol (le supprimer)
    for i in range(len(listetonneau)):
        if int(listetonneau[i].y)+3==41:
            position_tonneau=i
            delete_tonneau=1
                          
	#collision tonneau avec le players
    for i in listetonneau:
        if int(i.y)+3==int(Players.get_y(players)) and int(i.x)+1==int(Players.get_x(players)): # si la tete est au contact du bas du tonneau
            gamover=1
		#regarder si le bas du tonneau est au contact du joueur
        for a in range(1,3): # le milieur du corps et le bas
            for b in range(3): #les colones du joueur 
                for c in range(3): # la ligne du bas du tonneau
                    for d in range(1,3): #les deux lignes du bas du tonneau
                        if int(i.y)+d==int(Players.get_y(players))+a and int(i.x)+c==int(Players.get_x(players))+b:
                            gamover=1
    return delete_tonneau,position_tonneau,gamover


