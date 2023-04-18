# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 10:58:47 2023

@author: Maxime,Clément 
"""


import sys 
import time
import select
import tty
import termios

import frame 
import Players
import Game
import Menu
import Ennemi
import Plateforme

timeStep= None
speed= None 
gravite = None 
score = None 

old_settings = termios.tcgetattr(sys.stdin)

def init():
    global timeStep, menu, game, players, ennemi, speed, gravite, score, listeplateforme
    #animation=Frame.create(color=4,x=28,y=8,filename="anim.txt")
    timeStep=0.1
    speed = 10	
    gravite = 10
    score = 0
    listeplateforme=[]

    menu=Menu.create(0)
    game = Game.create(speed,score)
    players = Players.create(40,10,gravite,timeStep)
    ennemi = Ennemi.create (144,9)
    listeplateforme = [['______________________________________________________________________',10,25,70,0],['______________________________________________________________________',70,35,70,0]]
    

    tty.setcbreak(sys.stdin.fileno()) #modifier le fct du terminal pr recupérer les interactions clavier 
    
    

def interact():
	global  timeStep, game, players
	#gestion des evenement clavier
	
	#si une touche est appuyee
	if isData():
		c = sys.stdin.read(1)
		if c == 'm':         
			quitGame()
		elif c=='\n' : # si la touche entré est appuyé
			game.start=1
		elif c==' ' : # si la touche entré est appuyé
			players.memoireup=30
			
		
def isData():
	#recuperation evenement clavier
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def run():
	global timeStep, game
	#Boucle de simulation	
	while 1:
		interact()
		move()
		show()
		Game.speedup(game)
		Game.scoreup(game)	
		time.sleep(timeStep)


def show ():
	global ennemi,players, game, menu,listeplateforme
	if game.start == 0 :
		Menu.show(menu)
		sys.stdout.flush() # vider la mémoire tampon

	if game.start==1:
		Game.showscore(game)
		Players.show(players)
		Ennemi.show(ennemi)
		for i in range (len(listeplateforme)):
			if 0<=listeplateforme[i][1] and listeplateforme[i][1]<154:
				Plateforme.show(listeplateforme,i)
		sys.stdout.flush() # vider la mémoire tampon



def move ():
	global players, listeplateforme, timeStep, speed
	#gerer creation de plateforme 
	if len(listeplateforme)<3:
		plateforme = Plateforme.create()
		listeplateforme=Plateforme.listeplat(listeplateforme,plateforme)
		

	#gerer appartition et disparition de plateformes 
	for b in range (len(listeplateforme)) :	
		if int(listeplateforme[b][1])==0: #regarde si la plateforme arrive en bout de course et on la fait disparaitre petit à petit 
			
			listeplateforme[b]=Plateforme.reduire(listeplateforme, b)
			if len(listeplateforme[b][0])==0: #on la supprime quand il y a plus rien dedans 

				del listeplateforme[b]  
		else :
			
			listeplateforme[b]=Plateforme.augmenter(listeplateforme,b,speed,timeStep) #creation de la plateforme (condition dans la fct auglenter)
			

	
	#gerer les collision du player
	players.plateforme=0 
	if int(players.y)+3== 41 : #collision avec le sol
		gameover()
	elif int(players.y)==8 : #collision avec le  plafond 
		players.memoireup=0
	for i in listeplateforme :
		for a in range (3):
			if int(players.y)+3 == int(i[2]) and int(i[1])<=int(players.x)+a <= int( i[1]+len(i[0])): #ne plus appliquer la gravité au contact d'une plateforme
				players.plateforme=-1

	if players.plateforme==0 and players.memoireup==0: #apliquer la gravité
		Players.playersdown(players) 
	elif players.memoireup!=0: #faire le saut du player
		Players.up(players)
		players.memoireup-=1
	Plateforme.move(listeplateforme,speed,timeStep) #bouger les plateformes
	

	
		
def gameover (): # en cas de defaite relancer le jeu au menu
	global players, game, score 
	game.start=0
	players.y=10
	game.score = 0
	game.speed=1
	


	


def quitGame():	
	
	#restoration parametres terminal
	global old_settings
	
	
	sys.stdout.write("\033[37m") #couleur ecriture en blanc
	sys.stdout.write("\033[40m") # couleur du fond noir 
	
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
	sys.exit()
	

##################################
#les test 
init()
run()