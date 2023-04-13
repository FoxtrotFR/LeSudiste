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
    bg= open (background,"r")


    menu.backgroung = bg.read().splitlines()
    bg.close()
    return menu


def show (menu):
    
    
