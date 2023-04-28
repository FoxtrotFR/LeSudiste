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
import Tonneau

timeStep= None
speed= None 
gravite = None 
score = None 
listefrites = None 
intro = None
listetonneau = None 

old_settings = termios.tcgetattr(sys.stdin)

def init():
    global timeStep, menu, game, players, ennemi, speed, gravite, score, listeplateforme, listefrites, listetonneau
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
    intro=frame.read_frames("intro.txt")

    listetonneau = []
    
    tty.setcbreak(sys.stdin.fileno()) #modifier le fct du terminal pr recupérer les interactions clavier 
    
    

def interact():
	global  timeStep, game, players
	#gestion des evenements clavier
	
	#si une touche est appuyée
	if isData():
		c = sys.stdin.read(1)
		if c == 'm':         
			quitGame()	
		elif c==' ' and players.plateforme == -1 :  # si la touche entré est appuyé et le players est sur une plateforme
			players.memoireup=26
		elif c=='q' : # si la touche q est appuyéez
			players.left = 1
			players.right=0
		elif c=='d' : # si la touche d est appuyée 
			players.right = 1
			players.left=0
		elif c=='\n' : # si la touche entré est appuyée
			game.start=1
			frame.display_frames(intro,delay=5)
			while not frame.get_frame_finished(intro):
				 time.sleep(0.1)
			
		
def isData():
	# recuperation evenement clavier
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def run():
	global timeStep, game,speed,listeplateforme, listefrites,players
	#Boucle de simulation	
	while 1:
		if game.start == 0:
			interact()
			show()
		else : 
			interact()
			if game.score <10: #gravité initiale 
				move1()
			elif int(game.score)==10: #renitialisé le jeu 
				listeplateforme=[['____________________________________________________________',50,25,60,0,0,4]]
				listefrites=[]
				players.y =35 #imposer la ligne du players 
			elif game.score>10: #changer la gravité
				move2()
				
			
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
		for i in listetonneau:
			Tonneau.show(i)
		sys.stdout.flush() # vider la mémoire tampon



def move1 ():
	global players, listeplateforme, timeStep, game, speed, listefrites

	#bouger les plateformes	
	Plateforme.move(listeplateforme,speed,timeStep) 
	#gerer creation de plateforme 
	derniereplat=len(listeplateforme)-1
	if listeplateforme[derniereplat][5]<=0:
		plateforme = Plateforme.create(game.score)
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
					
		

	if players.plateforme==0 and players.memoireup==0: #appliquer la gravité
		Players.playersdown(players) 
	elif players.memoireup!=0: #faire le saut du player
		Players.up(players)
		players.memoireup-=1

	
	#gerer deplacement des frites 
	if game.score>20: #si le score est atteint 
		if len(listefrites)==0: 
			frite = Frites.create()
			listefrites=Frites.fritliste(listefrites,frite,0)
		elif len (listefrites)<10 and listefrites[len(listefrites)-1][3]==0: #creer une frite 
			frite = Frites.create()
			listefrites=Frites.fritliste(listefrites,frite,0)
		for i in range (len(listefrites)): #gerer la tempo ert le reduire si besoin 
			if listefrites[i][3]>0:
				listefrites[i][3]-=1
		Frites.move(listefrites,gravite,timeStep)
	
	#gerer les collision des frites 
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
	
def move2():
	global speed,gravite, players, listefrites, listeplateforme,game,timeStep,listetonneau
	#initialisation des variables 
	deletetonneau = 0
	positiontonneau = 0

	#gerer mouvement du players
	if players.right !=0 : #bouger le players vers la droite si la touche est appuyé
		Players.right(players)
		players.right -=1
	elif players.left !=0 :  #bouger le players vers la gauche si la touche est appuyé
		Players.left (players)
		players.left -=1

	#gerer appartition des plateformes
	dernierplatef=len(listeplateforme)-1
	if listeplateforme[dernierplatef][5]<=0:
		plateforme = Plateforme.create2()#creer les plateformes
		listeplateforme=Plateforme.listeplat(listeplateforme,plateforme)
	#bouger les plateformes
	Plateforme.move2(listeplateforme,speed,timeStep)

	#gerer les frites 
	if game.score>20:
		#creer les frites 
		if len(listefrites)==0:
			frite=Frites.create2()
			listefrites=Frites.fritliste(listefrites,frite,0)
		elif listefrites[len(listefrites)-1][3]==0:
			frite=Frites.create2()
			listefrites=Frites.fritliste(listefrites,frite,0)
		listefrites[len(listefrites)-1][3]-=1 #gerer le tempo de la derniere frite 
		Frites.move(listefrites,gravite,timeStep)
		
		#COLLISION frite 
		deletefrite = 0
		positionfrite = 0
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

	#gerer les tonneau
	if game.score>30:
		#creation des tonneau
		if len(listetonneau)==0: # si la liste est vide 
			tonneau= Tonneau.create2()
			listetonneau = Tonneau.listonneau(listetonneau,tonneau)
		derniertonneau=len(listetonneau)-1
		if listetonneau[derniertonneau].tempo==0: #baisser le tempo du dernier tonneau
			tonneau= Tonneau.create2()
			listetonneau = Tonneau.listonneau(listetonneau,tonneau)
		listetonneau[derniertonneau].tempo-=1
		for i in listetonneau:
			Tonneau.move2(i,speed,timeStep) #bouger les tonneau
		
		#collision tonneau 
		#collision avec le sol
		
		for i in range(len(listetonneau)):
			if int(listetonneau[i].y)+3==41:
				deletetonneau=1
				positiontonneau=i
		#collision tonneau
		for i in listetonneau:
			if int(i.y)+3==int(players.y) and int(i.x)==int(players.x): # si la tete est au contact du bas du tonneau
				gameover()
			#regarder si le bas du tonneau est au contact du joueur
			for a in range(1,3): # le milieur du corps et le bas
				for b in range(3): #les colones du joueur 
					for c in range(3): # la ligne du bas du tonneau
						for d in range(1,3): #les deux lignes du bas du tonneau
							if int(i.y)+d==int(players.y)+a and int(i.x)+c==int(players.x)+b:
								gameover()

	if deletetonneau==1:
		del listetonneau[positiontonneau]




	

	#COLLISION
	delete = 0
	position = 0
	#collision plateforme avec le sol 
	for i in range(len(listeplateforme)):
		if int(listeplateforme[i][2])==41:
			delete=1
			position = i
	if delete==1:
		del listeplateforme[position]
	#collision plateforme joueur 
	for i in listeplateforme:
		for a in range (3):
			if int(players.y)+a==int(i[2]) and int(i[1])<=int(players.x)+1<=int(i[1]+i[3]): #contacte avec la tete
				gameover()
			for b in range(3):
				if int(players.y)+a==int(i[2]) and int(i[1])<=int(players.x)+b<=int(i[1]+i[3]): #collision avce le corps 
					gameover()
	#collision joueur avec les murs 
	if int(players.x)<=1:
		players.x=1
		players.left=0
	elif players.x>=150:
		players.x=150
		players.right=0

	#collision frite



	#remettre à 0 les deplacements
	players.left = 0
	players.right = 0

	


	




		
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