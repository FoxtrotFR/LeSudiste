# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:00:31 2023

@author: Maxime
"""
import sys 

class Players : pass

def create( x, y,gravite,dt):
    players = Players()
    players.x = x
    players.y = y
    players.dt= dt
    players.gravite=gravite
    players.plateforme = 0
    look = open("joueur.txt", "r")
    players.look = look.read().splitlines()
    look.close()
    players.memoireup=0
    players.right =0
    players.left =0
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
    y=players.y
    players.y= y-players.gravite*players.dt
    players.memoireup -=1
    return players.y
    
def right (players) : #decaller vers la droite
    x=players.x
    players.x=x+(players.gravite*players.dt*3)
    return players.x

def left (players): #decaller le player vers la gauche 
    x=players.x
    players.x=x-(players.gravite*players.dt*3)
    return players.x 

def playersdown (players):
    y= players.y
    players.y= y+(players.gravite*players.dt)
    return players.y


   