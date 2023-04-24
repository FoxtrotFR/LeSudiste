# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Menu : pass

import Game
import sys

#creer le menu
def create ( scoreboard,regles="regles.txt"):
    menu = Menu()
    menu.name = "LE SUDISTE"
    menu.name_y=5
    menu.name_x=71

    menu.jouer = "Appuyer sur entrer pour commencer le jeu"
    menu.jouer_x=80
    menu.jouer_y=15

    menu.scoreboard = scoreboard

    #ouvrir les regles pour les afficher 
    regle=open(regles,"r")
    menu.regles = regle.read().splitlines()
    regle.close()
    menu.regles_x= 80
    menu.regles_y=25

    return menu


def show (menu):
    #afficher le fond
    Game.showbackground()  #153 colones et 41 lignes (dont 3 lignes au dessu sans rien)

    #Afficher le name à l'endroit donné 
    x=str(menu.name_x)
    y=str(menu.name_y)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position du nom 
    sys.stdout.write(menu.name) #afficher le nom

    #afficher les regles 
    for i in range(len(menu.regles)):
        x=str(int(menu.regles_x))
        y=str(int(menu.regles_y)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)   #se placer a la position du nom

        sys.stdout.write(menu.regles[i]) #afficher la ligne

    #afficher "appuyer sur entre pour commencer le jeu
    x=str(menu.jouer_x)
    y=str(menu.jouer_y)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position du nom 
    sys.stdout.write(menu.jouer) #afficher le nom

    #afficher le curseur a la fin du jeu
    y=str(42)
    x=str(0)
    txt="\033["+y+";"+x+"H" #placer le curseur
    sys.stdout.write(txt)   #se placer a la position du nom 



#test 
if __name__=="__main__":
   menu = create(0)
   show(menu)
    
