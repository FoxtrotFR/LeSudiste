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
    players.look = look.read()
    look.close()
    return players
    
    
def show (players):
    #se placer à la position du personnage 
    x=str(int(players.x))
    y=str(int(players.y))
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    
    #afficher le personnage 
    sys.stdout.write(players.look)
    

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