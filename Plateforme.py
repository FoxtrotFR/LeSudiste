# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime, Clément
"""

class Plateforme : pass

import Tonneau
import Players
import sys
import random

def create_right_left (score,gravite): #ceer le type plateforme
    plateforme = Plateforme()
    plateforme.y =random.randint (32,39)  #position en y de la plateforme 
    plateforme.lenth=random.randint (80,100) #taille total de la plateforme 
    plateforme.look = ''
    plateforme.taille =0 #taille actuel de plateforme 
    if gravite ==1 : 
        plateforme.x = 151
        plateforme.trou = random.randint(3,7) #taille de trou qui suit la plateforme 
        if score>40:
            plateforme.tonneau = random.randint (1,4)
        else : plateforme.tonneau = 2
        if plateforme.tonneau ==1: 
            plateforme.ton=Tonneau.create(plateforme.lenth,plateforme.y) #creer le tonneau 
        else :
            plateforme.ton = ''
    elif gravite ==3:
        plateforme.trou = random.randint(1,6) #taille de trou qui suit la plateforme 
        plateforme.x=0
        plateforme.tonneau=2
        plateforme.ton=''
    return plateforme

def create_down():
    plateforme = Plateforme()
    plateforme.x = random.randint (1,152)
    plateforme.y =10  #position en y de la plateforme 
    plateforme.lenth = random.randint (50,70) #taille total de la plateforme 
    while plateforme.x+plateforme.lenth >153:
        plateforme.lenth-=2
    plateforme.look = ''
    for i in range (plateforme.lenth):
        plateforme.look= plateforme.look+'_'
    plateforme.trou=random.randint(10,20)
    plateforme.tonneau=2
    plateforme.ton=''
    plateforme.taille=0
    return plateforme 
def create_up():
    plateforme = Plateforme()
    plateforme.x = random.randint (1,152)
    plateforme.y = 40  #position en y de la plateforme 
    plateforme.lenth = random.randint (50,70) #taille total de la plateforme 
    while plateforme.x+plateforme.lenth >153:
        plateforme.lenth-=2
    plateforme.look = ''
    for i in range (plateforme.lenth):
        plateforme.look= plateforme.look+'_'
    plateforme.trou=random.randint(10,20)
    plateforme.tonneau=2
    plateforme.ton=''
    plateforme.taille=0
    return plateforme 

def show(liste_plateforme,nbr):
    x=str(int(liste_plateforme[nbr][1]))
    y=str(int(liste_plateforme[nbr][2]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position de la plateforme
    sys.stdout.write(liste_plateforme[nbr][0]) #afficher la plateforme
    if liste_plateforme[nbr][6]==1 and liste_plateforme[nbr][7].x<150:
        if liste_plateforme[nbr][7].x<=1: #supprimer le tonneau 
            liste_plateforme[nbr][6]=2 
        else :
            Tonneau.show(liste_plateforme[nbr][7]) #afficher le tonneau

def listeplat (liste_plateforme,plateforme):
    liste_plateforme.append([plateforme.look,plateforme.x,plateforme.y,plateforme.lenth,plateforme.taille, plateforme.trou,plateforme.tonneau,plateforme.ton]) #liste de 8 elements 
    return liste_plateforme

def move_right_left(liste_plateforme,speed,timeStep,signe):
    for i in liste_plateforme :
        i[1]+=speed*timeStep*signe #signe =-1 pour right et signe = 1 pour left
        if signe==-1:
            if i[6]==1: #bouger le tonneau s'il y en a un
                Tonneau.move(i[7],speed,timeStep)

def move_up_down(liste_plateforme,speed,dt,signe):
    for i in liste_plateforme :
        i[2]+=(speed/3)*dt*signe  
        if i[5]>0:#plateforme.trou(la tempo)
            i[5]-=(speed/3)*dt   

def reduce_left(liste_plateforme,nbr):
    #reduire la taile de plateforme pour la fiare disparaitre 
    diminution = liste_plateforme[nbr][1]+liste_plateforme[nbr][3]-152
    liste_plateforme[nbr][0]=''
    liste_plateforme[nbr][3]-=diminution
    for i  in range (int(liste_plateforme[nbr][3])):
        liste_plateforme[nbr][0]=liste_plateforme[nbr][0]+'_'
    return liste_plateforme[nbr]

def increase_left(liste_plateforme, nbr,speed, dt):
    if int(liste_plateforme[nbr][3])>len(liste_plateforme[nbr][0]): #0: plateforme.look et 3 : plateforme.lenth
        rajout = int(liste_plateforme[nbr][1])
        liste_plateforme[nbr][1] = liste_plateforme[nbr][1]-rajout #sauvegarder la virgule (eviter que els plateformes s'ecartent avec le tps)
        for i in range (int(rajout)):
            liste_plateforme[nbr][0]=liste_plateforme[nbr][0]+'_'
    else:
        liste_plateforme[nbr][5]-= speed*dt #reduire le trou pour la nouvelle plateforme 
    return liste_plateforme[nbr]


def reduce_right(liste_plateforme,nbr) : 
    #reduire la taille de la plateforme afin qu'elle disparaisse
    diminution = -liste_plateforme[nbr][1] #valeur de x negative (indique le depassement de cbm de carre de cette derniere)
    liste_plateforme[nbr][0]=''
    liste_plateforme[nbr][3]-=diminution
    for i in range (int(liste_plateforme[nbr][3])): #regenere une plateforme de la bonne taille 
        liste_plateforme[nbr][0]=liste_plateforme[nbr][0]+'_'
    liste_plateforme[nbr][1]=0 #remet x à 0
    return liste_plateforme[nbr]
    

def increase_right(liste_plateforme, nbr,speed, dt):
    if int(liste_plateforme[nbr][4])<=liste_plateforme[nbr][3]: #4: plateforme.taille et 3 : plateforme.lenth
        liste_plateforme[nbr][4]+= speed*dt
        rajout =int (liste_plateforme[nbr][4]- len(liste_plateforme[nbr][0]))
        for i in range (rajout):
            liste_plateforme[nbr][0]=liste_plateforme[nbr][0]+'_'
    else:
        liste_plateforme[nbr][5]-= speed*dt #reduire le trou pour la nouvelle plateforme 
        liste_plateforme[nbr][4] = liste_plateforme[nbr][3]

    return liste_plateforme[nbr]

def collision_up_down (liste_plateforme,players,gamover,sens):
    delete = 0
    position = 0
	#collision plateforme avec le sol 
    if sens == 0:
        for i in range(len(liste_plateforme)):
            if int(liste_plateforme[i][2])>=41:
                delete=1
                position = i
    if sens == 1:
        for i in range(len(liste_plateforme)):
            if int(liste_plateforme[i][2])<=9:
                delete=1
                position = i
    if delete==1:
        del liste_plateforme[position]
	#collision plateforme joueur 
    for i in liste_plateforme:
        for a in range (3):
            if int(Players.get_y(players))+a==int(i[2]) and int(i[1])<=int(Players.get_x(players))+1<=int(i[1]+i[3]): #contacte avec la tete
                gamover=1
            for b in range(3):
                if int(Players.get_y(players))+a==int(i[2]) and int(i[1])<=int(Players.get_x(players))+b<=int(i[1]+i[3]): #collision avce le corps 
                    gamover=1
    return liste_plateforme, gamover

def creation_right_left(liste_plateforme,score,gravite):
    derniereplat=len(liste_plateforme)-1
    if liste_plateforme[derniereplat][5]<=0:
        if gravite==1:
            plateforme = create_right_left(score,gravite)
        elif gravite==3:
            plateforme= create_right_left(score,gravite)
        liste_plateforme=listeplat(liste_plateforme,plateforme)  
    return liste_plateforme

def live_right_left(liste_plateforme,timeStep,speed,gravite,signe):
    move_right_left(liste_plateforme,speed,timeStep,signe) #bouger les plateformes
    delete = 0
    position =0
    for b in range (len(liste_plateforme)) :	
        if (int(liste_plateforme[b][1])<=0 and gravite==1) or (int(liste_plateforme[b][1])+int(liste_plateforme[b][3])>153 and gravite==3): #regarde si la plateforme arrive en bout de course et on la fait disparaitre petit à petit 
            if gravite ==1:
                liste_plateforme[b]=reduce_right(liste_plateforme, b)
            elif gravite == 3:
                liste_plateforme[b]=reduce_left(liste_plateforme, b)
            if len(liste_plateforme[b][0])==0 : #on la supprime quand il y a plus rien 
                delete = 1
                position =b
        else :
            if gravite == 1:
                liste_plateforme[b]=increase_right(liste_plateforme,b,speed,timeStep) #creation de la plateforme (condition dans la fct augmenter)
            elif gravite == 3:
                liste_plateforme[b]=increase_left(liste_plateforme,b,speed,timeStep) #creation de la plateforme (condition dans la fct augmenter)
    if delete ==1 :
        del liste_plateforme[position]
    return liste_plateforme
