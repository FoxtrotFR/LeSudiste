# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:00:31 2023

@author: Maxime, Clément
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

def get_y(players) : #renvoyer la hauteur du perso
    return players.y

def get_x(players):
    return players.x

def set_x(players,x):
    players.x=x
    return players

def set_y(players,y):
    players.y=y
    return players

def set_memoireup (players,number):
    players.memoireup=number
    return players

def set_left(players,left):
    players.left=left
    return players

def set_right(players,right):
    players.right=right
    return players

def up_down(players,signe): #sauter en hauteur ou appliquer la gravite
    y = get_y(players)
    y= y+(players.gravite*players.dt)*signe
    set_y(players,y)
    return players.y
    
def right_left (players,signe) : #decaller vers la droite et la gauche
    x = get_x(players)
    x=x+(players.gravite*players.dt*3)*signe
    set_x(players,x)
    return players.x

def collision(players,liste_plateforme,gravite,gamover):
    if (gravite%2) ==1:
        players.plateforme=0 #appliquer direct la gravite 
        if int(players.y)+3== 41 : #collision avec le sol
            gamover=1
        elif int(players.y)==8 : #collision avec le  plafond 
            players.memoireup=0 #appliquer direct la gravité
            
        for i in liste_plateforme : #collision lorsque le player est sur la plateforme(peut sauter)
            for a in range (3):
                if int(players.y)+3 == int(i[2]) and int(i[1])<=int(players.x)+a <= int( i[1]+len(i[0])): #ne plus appliquer la gravité au contact d'une plateforme
                    players.plateforme=-1
                elif int(players.y)==int(i[2]) and int(i[1])<=int(players.x)+1 <= int( i[1]+len(i[0])) : #collision par dessous une plateforme impossible 
                    players.memoireup=0 #si la tete touche
                for b in range (1,3): #si le corps touche
                    if int (players.y)+b==int(i[2]) and int(i[1])<=int(players.x)+a <= int( i[1]+len(i[0])) : 
                        players.memoireup=0
            if gravite == 1:
		        #collision avec un tonneau
                if i[6]==1:
                    for c in range (3):
                        for d in range(3):
                            if int(players.y)+c==int(i[7].y) and int(players.x)+d==int (i[7].x)+1:
                                gamover=1
    elif (gravite%2) == 0:
        #collision joueur avec les murs 
        if players.x>=150:
            set_x(players,150)
            set_right(players,0)
        elif players.x<=1:
            set_x(players,1)
            set_left(players,0)  
    return gamover,players

def move(players,gravite) :
    #gerer deplacement player
    if players.plateforme==0 and players.memoireup==0 and (gravite%2)==1: #appliquer la gravité (0 pas sur palteforme)
        up_down(players,1) 
    elif players.memoireup!=0 and (gravite%2) == 1: #faire le saut du player
        up_down(players,-1)
        players.memoireup-=1
    elif players.right !=0  and (gravite%2) == 0: #bouger le players vers la droite si la touche est appuyée
        right_left(players,1)
        players.right -=1
    elif players.left !=0  and (gravite%2) == 0:  #bouger le players vers la gauche si la touche est appuyée
        right_left (players,-1)
        players.left -=1
    return players
       