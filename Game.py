# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime,Clement
"""

class Game : pass

import Players

import sys
import os

rows, columns = os.popen('stty size', 'r').read().split()



def create (speed,score):
    game = Game()

    game.name = "Retrouvez le pastis"
    game.name_x = 60
    game.name_y = 5

    game.score = score
    game.start =0
    game.speed=speed
    
    
    return game

def showbackground(): #afficher le fond 

    #ouvir le fichier et le lire 
    bg=open("background.txt","r")
    background = bg.read().splitlines()
    bg.close()

    if int(columns) < 80 or int(rows) < 20:
        print("\033[31mMettre en Plein Ecran\033[0m")
    else:
        for i in range(len(background)):
            x=str(0)
            y=str(0+i)
            txt="\033["+y+";"+x+"H" #placer le curseur 
            sys.stdout.write(txt)   #se placer a la position du personnage 

            sys.stdout.write(background[i]) #afficher la ligne 

def showscore (game):

    showbackground()  #153 colones et 41 lignes (dont 3 lignes au dessu sans rien)
    #Afficher le titre à l'endroit donné 
    x=str(game.name_x)
    y=str(game.name_y)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position du titre 
    sys.stdout.write(game.name) #afficher le titre

    #Affichage du score 
    for i in range (5): 
        x=str(130)
        y=str(int(3)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)   #se placer a la position de la bare  
        sys.stdout.write("|") #afficher la barre

    x=str(138)  #afficher le mot "score"
    y=str(4)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position 
    sys.stdout.write("score :") #afficher 

    x=str(141) #afficher le score 
    y=str(6)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position du score 
    sys.stdout.write(str(int(game.score))) #afficher

def scoreup (game):
    game.score+=(game.speed*0.1)

def speedup(game):
    game.speed+=0.1


