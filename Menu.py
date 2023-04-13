# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Menu : pass

import Game
import sys

#creer le menu
def create (background, scoreboard):
    menu = Menu()
    menu.name = "LE SUDISTE"
    menu.jouer = "Appuyer sur entré pour jouer"
    menu.scoreboard = scoreboard
    bg=open(background,"r")
    menu.background = bg.read().splitlines()
    bg.close()

    return menu


def show (menu):
    #afficher le fond
    Game.showbackground(menu) 

    #Afficher le name à l'endroit donné 
    x=str(60)
    y=str(5)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position du nom 
    sys.stdout.write(menu.name) #afficher le nom



#test 
if __name__=="__main__":
   menu = create("background.txt",0)
   show(menu)
    
