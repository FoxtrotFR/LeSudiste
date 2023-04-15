# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime,Clement
"""

class Game : pass

import sys
import os

rows, columns = os.popen('stty size', 'r').read().split()



def create ():
    game = Game()
    
    
    
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



if __name__=="__main__":
   game = create()
   showbackground()