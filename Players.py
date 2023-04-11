# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:00:31 2023

@author: Maxime
"""

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
    #separer l'ennemi en ligne 
    t= players.look
    
    #afficher le personnage ligne par ligne 
    for i in range(len(players.look)):
        x=str(int(players.x))
        y=str(int(players.y)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)#se placer à la position du personnage 



        sys.stdout.write(t[i]) #afficher la ligne 

def getheight(players) : #renvoyer la hauteur du perso
    return players.y

def up(players): #sauter en hauteur 
    players.y+=30
    return players
    
def right (players) : #décaller vers la 
    players.x+=30
    return players 

def left (players): #
    players.x-=30
    return players 

# test validé 
#if __name__=="__main__":
#   players = create("joueur.txt",10,10)
#   show(players)