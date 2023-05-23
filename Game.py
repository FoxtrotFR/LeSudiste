# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023
@author: Maxime,Clement
"""

class Game : pass


import sys
import os




def create (speed,score):
    game = Game()

    game.name = "\033[33mRetrouvez le pastis\033[0m"
    game.name_x = 60
    game.name_y = 5
    game.gravite=1 #donner la gravite (on commence par la gravite initiale )
    game.score = score
    game.start =0
    game.speed=speed
    game.score_right = 0
    game.score_down = 50
    game.score_left = 100
    game.score_up = 150
    game.rotation = 200 #le score a partir du quel il faut changer de gravite
    
    return game

def getscore(game):
    return game.score

def getscore_right (game):
    return game.score_right

def getscore_down (game):
    return game.score_down

def getscore_left (game):
    return game.score_left

def getscore_up (game):
    return game.score_up

def setscore_right(game):
    game.score_right= game.score_right+game.rotation+game.speed
    return game.score_right

def setscore_down(game):
    game.score_down= game.score_down+game.rotation+game.speed
    return game.score_down

def setscore_left(game):
    game.score_left= game.score_left+game.rotation+game.speed
    return game.score_left

def setscore_up(game):
    game.score_up= game.score_up+game.rotation+game.speed
    return game.score_up

def showbackground(): #afficher le fond 

    #ouvir le fichier et le lire 
    bg=open("background.txt","r")
    background = bg.read().splitlines()
    bg.close()

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

def scoreup (game,speed):
    game.score+=(speed*0.05)

def speedup(speed):
    speed+=0.01
    return speed


