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

import Frame 
import Players
import Game
import Menu
import Ennemi
import Plateforme
import Frites
import Tonneau
import Scoreboard

timeStep= None 
force_gravite = None 
score = None 
listefrites = None 
intro = None
listetonneau = None 
username = None
rows, columns = os.popen('stty size', 'r').read().split()

old_settings = termios.tcgetattr(sys.stdin)

def init():
    global timeStep, menu, game, players, ennemi, force_gravite, score, listeplateforme, listefrites, listetonneau, intro,ennemi
    #animation=Frame.create(color=4,x=28,y=8,filename="anim.txt")
    timeStep=0.1
    speed = 10	
    force_gravite = 10
    score = 0
    listeplateforme=[]

    menu=Menu.create(0)
    game = Game.create(speed,score)
    players = Players.create(40,10,force_gravite,timeStep)
    ennemi = Ennemi.create (144,9)
    listeplateforme = [['______________________________________________________________________',10,25,70,0,10,4,''],['____________________________________________________________',90,35,60,0,0,4,'']]
    listefrites=[]
    intro=Frame.read_frames("intro.txt")
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
		elif c==' ' and players.plateforme == -1 and (game.gravite%2) == 1:  # si la touche entré est appuyé et le players est sur une plateforme
			players.memoireup=11
		elif c=='q' and (game.gravite%2)==0 : # si la touche q est appuyéez
			players.left = 1
			players.right=0
		elif c=='d'  and (game.gravite%2) == 0: # si la touche d est appuyée 
			players.right = 1
			players.left=0
		elif c=='\n' : # si la touche entré est appuyée
			game.start=1
			Frame.display_frames(intro,delay=0.1)
			while not Frame.get_frame_finished(intro):
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
				game.gravite=3
				listetonneau=[]
				ennemi=Ennemi.setposition(2,ennemi)
			elif game.score>Game.getscore_left(game) and game.score<Game.getscore_up(game):
				move_left()
			elif int(game.score) == Game.getscore_up(game):
				listeplateforme=[['____________________________________________________________',50,35,60,0,0,4,'']]
				listefrites=[]
				players.y =15 #imposer la ligne du players 
				game.gravite=2
			elif game.score>Game.getscore_up(game):
				move_up()
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
	global players, listeplateforme, timeStep, game, listefrites,force_gravite

	gamover=0

	#gerer creation de plateforme 
	Plateforme.creation_right_left(listeplateforme,game.score,1)
	#gerer appartition et disparition de plateformes et mouvement
	Plateforme.live_right_left(listeplateforme,game.speed,timeStep,1,-1)	

	#gerer les collision et deplacement du player
	Players.move(players,1)
	gamover,players=Players.collision(players,listeplateforme,1,gamover)				
	
	#gerer les frites 
	if game.score>20: #si le score est atteint 
		Frites.creation(listefrites,15,50,100,11,143)
		Frites.move(listefrites,force_gravite,timeStep,-1,1)
	#gerer les collision des frites
		gamover,listefrites=Frites.collision(listefrites,listeplateforme,players,gamover) 

	#si le joueur est mort
	if gamover==1:
		gameover()

	#augmenter la vitesse
	game.speed = Game.speedup(game.speed)
	
def move_down():
	global force_gravite, players, listefrites, listeplateforme,game,timeStep,listetonneau

	gamover= 0
	#gerer mouvement du players
	Players.move(players,2)
	#gerer les collision du palyers
	Players.collision(players,listeplateforme,2,gamover)

	#gerer appartition des plateformes
	dernierplatef=len(listeplateforme)-1
	if listeplateforme[dernierplatef][5]<=0:
		plateforme = Plateforme.create_down()#creer les plateformes
		listeplateforme=Plateforme.listeplat(listeplateforme,plateforme)
	#bouger les plateformes
	Plateforme.move_down(listeplateforme,game.speed,timeStep)

	#gerer les frites 
	if game.score>Game.getscore_down(game)+20:
		#création
		Frites.creation (listefrites,0,15,30,11,143)
		Frites.move(listefrites,force_gravite,timeStep,-1,1)
		#gerer les collision des frites
		gamover,listefrites=Frites.collision(listefrites,listeplateforme,players,gamover) 

	#gerer les tonneaux
	if game.score>Game.getscore_down(game)+10:
		#creation des tonneaux
		Tonneau.creation(listetonneau,game,timeStep,1)
		#collision des tonneaux
		delete_tonneau,position_tonneau,gamover = Tonneau.collision(listetonneau,players,gamover,1)
	#suppression des tonneaux
		if delete_tonneau==1:
			del listetonneau[position_tonneau]

	#collision plateforme 
	listeplateforme,gamover = Plateforme.collision_down(listeplateforme,players,gamover)
	if gamover==1:
		gameover()

	#augmenter la vitesse
	game.speed = Game.speedup(game.speed)

def move_left():
	global force_gravite, players, listefrites, listeplateforme,game,timeStep,listetonneau

	gamover=0

	#gerer collision palyers
	gamover,players=Players.collision(players,listeplateforme,3,gamover)
	#gerer le deplacement du players
	Players.move(players,3)

	#faire creation de plateforme
	Plateforme.creation_right_left(listeplateforme,game.score,3)
	Plateforme.live_right_left(listeplateforme,game.speed,timeStep,3,1) #gerer apparition et disparition de plateforme 
	
	#gerer creation des frites 
	Frites.creation(listefrites,15,50,100,7,10)
	Frites.move (listefrites,force_gravite,timeStep,1,1) #bouger les frites
	gamover,listefrites = Frites.collision(listefrites,listeplateforme,players,gamover) 

	#si le joueur est mort 
	if gamover==1:
		gameover()
	
	#augmenter la vitesse
	game.speed = Game.speedup(game.speed)

def move_up():
	global force_gravite, players, listefrites, listeplateforme,game,timeStep,listetonneau

	gamover= 0
	#gerer mouvement du players
	Players.move(players,2)
	#gerer les collision du palyers
	Players.collision(players,listeplateforme,2,gamover)

	#gerer appartition des plateformes
	dernierplatef=len(listeplateforme)-1
	if listeplateforme[dernierplatef][5]<=0:
		plateforme = Plateforme.create_up()#creer les plateformes
		listeplateforme=Plateforme.listeplat(listeplateforme,plateforme)
	#bouger les plateformes
	Plateforme.move_up(listeplateforme,game.speed,timeStep)

	#gerer les frites 
	if game.score>Game.getscore_up(game)+20:
		#création
		Frites.creation (listefrites,0,15,30,36,143)
		Frites.move(listefrites,force_gravite,timeStep,-1,-1)
		#gerer les collision des frites
		gamover,listefrites=Frites.collision(listefrites,listeplateforme,players,gamover) 

	#gerer les tonneaux
	if game.score>Game.getscore_up(game)+10:
		#creation des tonneaux
		Tonneau.creation(listetonneau,game,timeStep,2)
		#collision des tonneaux
		delete_tonneau,position_tonneau,gamover = Tonneau.collision(listetonneau,players,gamover,2)
	#suppression des tonneaux
		if delete_tonneau==1:
			del listetonneau[position_tonneau]

	#collision plateforme 
	listeplateforme,gamover = Plateforme.collision_up(listeplateforme,players,gamover)
	if gamover==1:
		gameover()

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
    init()
    run()

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