# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Menu : pass

import sys

#creer le menu
def create (gamename, regle, scoreboard):
    menu = Menu()
    menu.name = gamename
    menu.regle = regle
    menu.scoreboard = scoreboard
    
    return menu