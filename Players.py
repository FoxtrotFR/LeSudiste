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

def players_move(players):
    #gerer deplacement player
    if players.right != 0 :
        right(players)
        players.right -=1
    elif players.left !=0 :  #bouger le players vers la gauche si la touche est appuyé
        left (players)
        players.left -= 1
    elif players.plateforme==0 and players.memoireup==0: #appliquer la gravité (0 pas sur palteforme)
        playersdown(players) 
    elif players.memoireup!=0: #faire le saut du player
        up(players)
        players.memoireup-= 1

def collision(players,listeplateforme):
    gamover=0
    players.plateforme=0 
    if int(players.y)+3== 41 : #collision avec le sol
        gamover=1
    elif int(players.y)==8 : #collision avec le  plafond 
        players.memoireup=0 #appliquer direct la gravité
    for i in listeplateforme : #collision lorsque le player est sur la plateforme(peut sauter)
        for a in range (3):
            if int(players.y)+3 == int(i[2]) and int(i[1])<=int(players.x)+a <= int( i[1]+len(i[0])): #ne plus appliquer la gravité au contact d'une plateforme
                players.plateforme=-1
            elif int(players.y)==int(i[2]) and int(i[1])<=int(players.x)+1 <= int( i[1]+len(i[0])) : #collision par desous uen plateforme
                players.memoireup=0 #si la tete touche
            for b in range (1,3): #si le corps touche
                if int (players.y)+b==int(i[2]) and int(i[1])<=int(players.x)+a <= int( i[1]+len(i[0])) : 
                    players.memoireup=0
		#collision avec un tonneau
        if i[6]==1:
            for c in range (3):
                for d in range(3):
                    if int(players.y)+c==int(i[7].y) and int(players.x)+d==int (i[7].x)+1:
                        gamover=1
    return gamover,listeplateforme

                                    