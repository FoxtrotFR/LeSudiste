# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Frites : pass

import sys

def create (x,y,speed,img):
    frites = Frites()
    frites.x = x
    frites.y = y
    frites.speed = speed
    look = open (img, "r")
    frites.look = look.read()
    look.close()
    return frites