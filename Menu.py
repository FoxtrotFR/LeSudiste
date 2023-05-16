# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Menu : pass

import Game
import sys
import Scoreboard

scoreboard = Scoreboard.create_from_csv(csv_filename="./test.csv", score_column_number=1)
username=""

#creer le menu
def create ( scoreboard,regles="regles.txt"):
    menu = Menu()
    menu.name = "LE SUDISTE"
    menu.name_y=5
    menu.name_x=71

    menu.jouer = "Appuyer sur entrer pour commencer le jeu"
    menu.jouer_x=80
    menu.jouer_y=15

    menu.scoreboard = scoreboard

    #ouvrir les regles pour les afficher 
    regle=open(regles,"r")
    menu.regles = regle.read().splitlines()
    regle.close()
    menu.regles_x= 80
    menu.regles_y=25

    return menu


def show (menu):
    #afficher le fond
    Game.showbackground()  #153 colones et 41 lignes (dont 3 lignes au dessu sans rien)

    #Affichage Scoreboard
    top_scores = Scoreboard.get_top_scores(scoreboard)
    top_player_names = Scoreboard.get_top_scores_name(scoreboard)
    x = str(int(menu.jouer_x)-45)
    y = str(int(menu.jouer_y)-1)
    txt = "\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    sys.stdout.write("SCOREBOARD")
    for i in range(len(top_scores)):
        x = str(int(menu.jouer_x)-50)
        y = str(int(menu.jouer_y)+i)
        txt = "\033["+y+";"+x+"H"  # placer le curseur
        sys.stdout.write(txt)  # se placer à la position du score et du nom
        sys.stdout.write(str(i+1) +".  " + top_player_names[i] + " : " + str(top_scores[i]))

    #Afficher le name à l'endroit donné 
    x=str(menu.name_x)
    y=str(menu.name_y)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position du nom 
    sys.stdout.write(menu.name) #afficher le nom

    #afficher les regles 
    for i in range(len(menu.regles)):
        x=str(int(menu.regles_x))
        y=str(int(menu.regles_y)+i)
        txt="\033["+y+";"+x+"H" #placer le curseur 
        sys.stdout.write(txt)   #se placer a la position du nom

        sys.stdout.write(menu.regles[i]) #afficher la ligne

    #afficher "appuyer sur entre pour commencer le jeu
    x=str(menu.jouer_x)
    y=str(menu.jouer_y)
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)   #se placer a la position du nom 
    sys.stdout.write(menu.jouer) #afficher le nom

    #afficher le curseur a la fin du jeu
    y=str(42)
    x=str(0)
    txt="\033["+y+";"+x+"H" #placer le curseur
    sys.stdout.write(txt)   #se placer a la position du nom 


def menu_gameover(score):
    global username
    Game.showbackground()
    x=str(71)
    y=str(5)
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    sys.stdout.write("LE SUDISTE")
    x=str(71)
    y=str(15)
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    sys.stdout.write("\033[91mGAME OVER\033[0m")
    x=str(48)
    y=str(17)
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    sys.stdout.write("Bravo, Tu as bien joué, tu as fait \033[93m" + str(score) + "\033[0m, C'est un beau score !")
    x=str(55)
    y=str(20)
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    sys.stdout.write("Tape ton pseudo pour sauvegarder ton score :")
    x=str(60)
    y=str(22)
    txt="\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    sys.stdout.write("Pseudo : ")
    user_text = input()  # Demande à l'utilisateur de saisir le texte
    x = str(70)
    y = str(22)
    txt = "\033["+y+";"+x+"H"
    sys.stdout.write(txt)
    sys.stdout.write(user_text)  # Affiche le texte saisi par l'utilisateur
    #Curseur Fin de BackGround
    y=str(42)
    x=str(0)
    txt="\033["+y+";"+x+"H" #placer le curseur
    sys.stdout.write(txt)   #se placer a la position du nom 
    return user_text



print(username)
#test 
if __name__=="__main__":
   menu_gameover(500)
    
