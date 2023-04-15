# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 10:58:47 2023

@author: Maxime,Clément 
"""


import sys 
import time
import select
import tty

import Frame 
import Players
import Game
import Menu

timeStep= None


def init():
    global animat, timeStep,menu
    #animation=Frame.create(color=4,x=28,y=8,filename="anim.txt")
    timeStep=0.1
    menu=Menu.create(0)

    tty.setcbreak(sys.stdin.fileno()) #modofier le fct du terminal pr recupérer les interactions clavier 
    
    

def interact():
	global  timeStep
	#gestion des evenement clavier
	
	#si une touche est appuyee
	if isData():
		c = sys.stdin.read(1)
		#if c == 'm':         
		#	quitGame()
		if c=='m' :
			Game.showbackground()
		
def isData():
	#recuperation evenement clavier
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def run():
	global timeStep,menu
	Menu.show(menu)
	sys.stdout.flush()
	#Boucle de simulation	
	while 1:
		interact()	
		time.sleep(timeStep)

##################################
#les test 
init()
run()