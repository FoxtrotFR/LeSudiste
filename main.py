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
import Frites

timeStep= None
speed= None 
gravite = None 
score = None 
compteur = None 
listefrites = None 

old_settings = termios.tcgetattr(sys.stdin)

def init():
    global timeStep, menu, game, players, ennemi, speed, gravite, score, listeplateforme, listefrites,  compteur 
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
    listeplateforme = [['______________________________________________________________________',10,25,70,0,10,4],['____________________________________________________________',90,35,60,0,0,4]]
    listefrites=[]
    compteur=0
    
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
		elif c==' ' and players.plateforme == -1 : # si la touche entré est appuyé et le players est sur une plateforme
			players.memoireup=26
			
		
def isData():
	#recuperation evenement clavier
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def run():
	global timeStep, game,speed
	#Boucle de simulation	
	while 1:
		if game.start == 0:
			interact()
			show()
		else : 
			interact()
			move()
			show()
			Game.scoreup(game,speed)	
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
			Plateforme.show(listeplateforme,i)
		for i in range(len(listefrites)):
			Frites.show(listefrites,i)
		sys.stdout.flush() # vider la mémoire tampon



def move ():
	global players, listeplateforme, timeStep, game, speed, listefrites, compteur 

	#bouger les plateformes	
	Plateforme.move(listeplateforme,speed,timeStep) 
	#gerer creation de plateforme 
	derniereplat=len(listeplateforme)-1
	if listeplateforme[derniereplat][5]<=0:
		plateforme = Plateforme.create()
		listeplateforme=Plateforme.listeplat(listeplateforme,plateforme)
	#gerer appartition et disparition de plateformes 	
	delete = 0
	position =0
	for b in range (len(listeplateforme)) :	
		if int(listeplateforme[b][1])<=0: #regarde si la plateforme arrive en bout de course et on la fait disparaitre petit à petit 
			listeplateforme[b]=Plateforme.reduire(listeplateforme, b)
			if len(listeplateforme[b][0])==0 : #on la supprime quand il y a plus rien 
				delete = 1
				position =b
		else :	
			listeplateforme[b]=Plateforme.augmenter(listeplateforme,b,speed,timeStep) #creation de la plateforme (condition dans la fct auglenter)
	if delete ==1 :
		del listeplateforme[position]		

	
	
	#gerer les collision du player
	players.plateforme=0 
	if int(players.y)+3== 41 : #collision avec le sol
		gameover()
	elif int(players.y)==8 : #collision avec le  plafond 
		players.memoireup=0 #appliquer direct la gravité
	for i in listeplateforme : #collision lorsque le player est sur la plateforme(peut sauter)
		for a in range (3):
			if int(players.y)+3 == int(i[2]) and int(i[1])<=int(players.x)+a <= int( i[1]+len(i[0])): #ne plus appliquer la gravité au contact d'une plateforme
				players.plateforme=-1
			elif int(players.y)==int(i[2]) and int(i[1])<=int(players.x)+1 <= int( i[1]+len(i[0])) : #collision par dessous une plateforme impossible 
				players.memoireup=0 #si la tete touche
			for b in range (1,3): #si le corps touche
				if int (players.y)+b==int(i[2]) and int(i[1])<=int(players.x)+a <= int( i[1]+len(i[0])) : 
					players.memoireup=0
		#collision avec un tonneau
		if i[6]==1:
			for c in range (3):
				for d in range(3):
					if int(players.y)+c==int(i[7].y) and int(players.x)+d==int (i[7].x)+1:
						gameover()
					
		

	if players.plateforme==0 and players.memoireup==0: #apliquer la gravité
		Players.playersdown(players) 
	elif players.memoireup!=0: #faire le saut du player
		Players.up(players)
		players.memoireup-=1

	
	#gerer deplacement des frites 
	if game.score>2: #si le score est atteint 
		if len(listefrites)==0: 
			frite = Frites.create()
			listefrites=Frites.fritliste(listefrites,frite,0)
		elif len (listefrites)<10 and listefrites[len(listefrites)-1][3]==0: #creer une frite 
			frite = Frites.create()
			listefrites=Frites.fritliste(listefrites,frite,0)
		for i in range (len(listefrites)):
			if listefrites[i][3]>0:
				listefrites[i][3]-=1
		Frites.move(listefrites,gravite,timeStep)
	
	#gerer les collsion des frites 
		deletefrite = 0
		positionfrite= 0
		for i in range (len(listefrites)): 
			#collision avec le palyers
			if int(listefrites[i][2])== int(players.y) and int(listefrites[i][1])==int(players.x)+1: #si la frite touche la tete
				gameover()
			for b in range (1,3):
				for a in range(3):
					if int(listefrites[i][2])==int(players.y)+b and int(listefrites[i][1])==int(players.x)+a: #si la frite touche le corps
						gameover()
			#collision avec le sol ou le mur
			if int (listefrites[i][2])==41 or int(listefrites[i][1]==0) :
				deletefrite=1
				positionfrite=i
			#collision avec plateforme
			for c in range(len(listeplateforme)):
				if int(listefrites[i][2])==int(listeplateforme[c][2]) and int (listeplateforme[c][1])<= int(listefrites[i][1])<= int(listeplateforme[c][1]+len(listeplateforme[c][0])):
					deletefrite=1
					positionfrite=i
		if deletefrite==1:
			del listefrites[positionfrite]



	#augmenter la vitesse
	speed = Game.speedup(speed)
	

	
		
def gameover (): # en cas de defaite relancer le jeu au menu
	global players, game, score 
	game.start=0
	players.y=10
	game.score = 0
	


	


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