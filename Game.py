# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime,Clement
"""

class Game : pass

import sys


def create (filename):
    game = Game()
    
    bg=open(filename,"r")
    game.background = bg.read().splitlines()
    bg.close()
    
    return game

def showbackground(game): #afficher le fond 

    for i in range(len(game.background)):
        x=str(0)
        y=str(0+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)   #se placer a la position du personnage 

        sys.stdout.write(game.background[i]) #afficher la ligne 



if __name__=="__main__":
   game = create("background.txt")
   showbackground(game)