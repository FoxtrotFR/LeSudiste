# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:00:31 2023

@author: Maxime
"""
import time
import sys 

class Players : pass

def create(img, x, y):
    players = Players()
    players.x = x
    players.y = y
    look = open(img, "r")
    players.look = look.read().splitlines()
    look.close()
    return players
    
    
def show(players):
    #afficher le personnage ligne par ligne 
    for i in range(len(players.look)):
        x=str(int(players.x))
        y=str(int(players.y)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)   #se placer a la position du personnage 

        sys.stdout.write(players.look[i]) #afficher la ligne 

def getheight(players) : #renvoyer la hauteur du perso
    return players.y

def up(players): #sauter en hauteur 
    players.y+=30
    return players
    
def right (players) : #decaller vers la droite
    players.x+=10
    return players 

def left (players): #decaller le player vers la gauche 
    players.x-=10   
    return players  

#test validé
#seul probleme, lorsque je met des time.sleep entre les show il show tout uniquement a la fin(et pas en continue)
if __name__=="__main__":
   players = create("joueur.txt",10,10)
   show(players)
   time.spleep(1)
   right(players)
   right(players)
   show(players)
   time.sleep(1)
   left(players)
   
   show(players)
   time.sleep(1)
   up(players)
   show(players)
   