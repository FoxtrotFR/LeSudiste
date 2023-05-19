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
import os

import frame 
import Players
import Game
import Menu
import Ennemi
import Plateforme
import Frites
import Tonneau
import Scoreboard

timeStep= None 
gravite = None 
score = None 
listefrites = None 
intro = None
listetonneau = None 
username = None
rows, columns = os.popen('stty size', 'r').read().split()

old_settings = termios.tcgetattr(sys.stdin)

def init():
    global timeStep, menu, game, players, ennemi, gravite, score, listeplateforme, listefrites, listetonneau, intro,ennemi
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
    listeplateforme = [['______________________________________________________________________',10,25,70,0,10,4,''],['____________________________________________________________',90,35,60,0,0,4,'']]
    listefrites=[]
    intro=frame.read_frames("intro.txt")
    listetonneau = []
    
    
    tty.setcbreak(sys.stdin.fileno()) #modifier le fct du terminal pr recupérer les interactions clavier 
    
    

def interact():
	global  timeStep, game, players,intro
	#gestion des evenements clavier
	
	#si une touche est appuyée
	if isData():
		c = sys.stdin.read(1)
		if c == 'm':         
			quitGame()	
		elif c==' ' and players.plateforme == -1 and game.gravite == 1:  # si la touche entré est appuyé et le players est sur une plateforme
			players.memoireup=11
		elif c=='q' and game.gravite==2 : # si la touche q est appuyéez
			players.left = 1
			players.right=0
		elif c=='d'  and game.gravite == 2: # si la touche d est appuyée 
			players.right = 1
			players.left=0
		elif c=='\n' : # si la touche entré est appuyée
			game.start=1
			frame.display_frames(intro,delay=0.1)
			while not frame.get_frame_finished(intro):
				 time.sleep(0.1)
			
		
def isData():
	# recuperation evenement clavier
	return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def run():
	global timeStep, game,listeplateforme, listefrites,players,listetonneau,ennemi
	#Boucle de simulation	
	is_menu_active = True  # Variable pour contrôler l'affichage du menu
    # Boucle de simulation
	while 1:
		if game.start == 0:
			if is_menu_active:  # Afficher le menu uniquement lorsque nécessaire
				show()
				is_menu_active = False  # Désactiver l'affichage du menu après l'avoir montré une fois
			interact()  # Afficher le jeu à chaque itération même lorsque le menu est actif
		else : 
			interact()
			if game.score <Game.getscore_down(game): #gravité initiale 
				move_right()
			elif int(game.score)== Game.getscore_down(game): #renitialisé le jeu 
				listeplateforme=[['____________________________________________________________',50,25,60,0,0,4,'']]
				listefrites=[]
				players.y =35 #imposer la ligne du players 
				game.gravite=2
			elif game.score>Game.getscore_down(game) and game.score<Game.getscore_left(game): #changer la gravité
				move_down()
			elif int(game.score)==Game.getscore_left(game):
				listefrites =[]
				listeplateforme = [['______________________________________________________________________',80,25,70,71,10,4,''],['______________________________________________________________________',10,35,70,71,10,4,''],['',0,38,70,0,10,4,'']]
				players.x=140
				players.y=10
				game.gravite=1
				listetonneau=[]
				ennemi=Ennemi.setposition(2,ennemi)
			elif game.score>Game.getscore_left(game):
				move3()
				
			
			show()
			Game.scoreup(game,game.speed)	
			time.sleep(timeStep)


def show ():
	global ennemi,players, game, menu,listeplateforme, rows, columns
	if int(columns) < 80 or int(rows) < 20:
		print("\033[31mMettre en Plein Ecran\033[0m")
	else:
		if game.start == 0 :
			Menu.show(menu)
			sys.stdout.flush() # vider la mémoire tampon

		elif game.start==1:
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



def move_right():
	global players, listeplateforme, timeStep, game, listefrites

	gamover=0

	#bouger les plateformes	
	Plateforme.move(listeplateforme,game.speed,timeStep) 
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
			listeplateforme[b]=Plateforme.augmenter(listeplateforme,b,game.speed,timeStep) #creation de la plateforme (condition dans la fct augmenter)
	if delete ==1 :
		del listeplateforme[position]		

	#gerer les collision et deplacement du player
	Players.move(players,1)
	gamover,players=Players.collision(players,listeplateforme,1,gamover)				
	
	#gerer les frites 
	if game.score>20: #si le score est atteint 
		Frites.creation(listefrites,15,50,100)
		Frites.move(listefrites,gravite,timeStep)
	#gerer les collision des frites
		gamover,listefrites=Frites.collision(listefrites,listeplateforme,players,gamover) 

	#si le joueur est mort
	if gamover==1:
		gameover()

	#augmenter la vitesse
	game.speed = Game.speedup(game.speed)
	
def move_down():
	global gravite, players, listefrites, listeplateforme,game,timeStep,listetonneau

	gamover= 0
	#gerer mouvement du players
	Players.move(players,2)
	#gerer les collision du palyers
	Players.collision(players,listeplateforme,2,gamover)

	#gerer appartition des plateformes
	dernierplatef=len(listeplateforme)-1
	if listeplateforme[dernierplatef][5]<=0:
		plateforme = Plateforme.create2()#creer les plateformes
		listeplateforme=Plateforme.listeplat(listeplateforme,plateforme)
	#bouger les plateformes
	Plateforme.move2(listeplateforme,game.speed,timeStep)

	#gerer les frites 
	if game.score>Game.getscore_down(game)+20:
		#création
		Frites.creation (listefrites,0,15,30)
		Frites.move(listefrites,gravite,timeStep)
		#gerer les collision des frites
		gamover,listefrites=Frites.collision(listefrites,listeplateforme,players,gamover) 

	#gerer les tonneaux
	if game.score>Game.getscore_down(game)+10:
		#creation des tonneaux
		Tonneau.creation(listetonneau,game,timeStep)
		#collision des tonneaux
		delete_tonneau,position_tonneau,gamover = Tonneau.collision(listetonneau,players,gamover)
	#suppression des tonneaux
		if delete_tonneau==1:
			del listetonneau[position_tonneau]

	#collision plateforme 
	listeplateforme,gamover = Plateforme.collision_down(listeplateforme,players,gamover)
	if gamover==1:
		gameover()

	#augmenter la vitesse
	game.speed = Game.speedup(game.speed)

def move3():
	global gravite, players, listefrites, listeplateforme,game,timeStep,listetonneau

	#bouger les plateformes 
	Plateforme.move3(listeplateforme,game.speed,timeStep)

	
	#gerer collision palyers
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
	
	#gerer le deplacement du players
	if players.plateforme==0 and players.memoireup==0: #appliquer la gravité
		Players.playersdown(players) 
	elif players.memoireup!=0: #faire le saut du player
		Players.up(players)
		players.memoireup-=1

	#faire creation de plateforme
	derniereplat=len(listeplateforme)-1
	if listeplateforme[derniereplat][5]<=0: #regarder si le trou est  egal à 0 et donc creer une nouvelle plateforme 
		plateforme = Plateforme.create3()
		listeplateforme=Plateforme.listeplat(listeplateforme,plateforme)
	
	
	#gerer apparition et disparition de plateforme 
	delete = 0
	position =0
	for b in range (len(listeplateforme)) :	
		if int(listeplateforme[b][1])+int(listeplateforme[b][3])>153: #regarde si la plateforme arrive en bout de course et on la fait disparaitre petit à petit 
			listeplateforme[b]=Plateforme.reduire3(listeplateforme,b)
			if len(listeplateforme[b][0])==0 : #on la supprime quand il y a plus rien 
				delete = 1
				position = b
		else :	
			listeplateforme[b]=Plateforme.augmenter3(listeplateforme,b,game.speed,timeStep) #creation de la plateforme (condition dans la fct augmenter)
	if delete ==1 :
		del listeplateforme[position]

	

	
	#augmenter la vitesse
	game.speed = Game.speedup(game.speed)
	

			
def disable_echo():
    # Sauvegarder la configuration actuelle des paramètres du terminal
    global old_settings
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

def enable_echo():
    global old_settings
    # Restaurer la configuration des paramètres du terminal
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    
		
def gameover():
    global players, game, username
    game.start = 2
    enable_echo() 
    Menu.menu_gameover(int(game.score))
    disable_echo() 
    game.start = 0
    players.y = 10
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


'''
rows, columns = os.popen('stty size', 'r').read().split()

    if int(columns) < 80 or int(rows) < 20:
        print("\033[31mMettre en Plein Ecran\033[0m")
'''