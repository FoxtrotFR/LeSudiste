# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
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
    

def show(listeplateforme,nbr):
    x=str(int(listeplateforme[nbr][1]))
    y=str(int(listeplateforme[nbr][2]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position de la plateforme
    sys.stdout.write(listeplateforme[nbr][0]) #afficher la plateforme
    if listeplateforme[nbr][6]==1 and listeplateforme[nbr][7].x<150:
        if listeplateforme[nbr][7].x<=1: #supprimer le tonneau 
            listeplateforme[nbr][6]=2 
        else :
            Tonneau.show(listeplateforme[nbr][7]) #afficher le tonneau

def listeplat (listeplateforme,plateforme):
    listeplateforme.append([plateforme.look,plateforme.x,plateforme.y,plateforme.lenth,plateforme.taille, plateforme.trou,plateforme.tonneau,plateforme.ton]) #liste de 8 elements 
    return listeplateforme

def move_right_left(listeplateforme,speed,timeStep,signe):
    for i in listeplateforme :
        i[1]+=speed*timeStep*signe #signe =-1 pour right et signe = 1 pour left
        if signe==-1:
            if i[6]==1: #bouger le tonneau s'il y en a un
                Tonneau.move(i[7],speed,timeStep)

def move_down(listeplateforme,speed,dt):
    for i in listeplateforme :
        i[2]+=(speed/3)*dt   
        if i[5]>0:#plateforme.trou(la tempo)
            i[5]-=(speed/3)*dt   

def reduce_left(listeplateforme,nbr):
    #reduire la taile de plateforme pour la fiare disparaitre 
    diminution = listeplateforme[nbr][1]+listeplateforme[nbr][3]-152
    listeplateforme[nbr][0]=''
    listeplateforme[nbr][3]-=diminution
    for i  in range (int(listeplateforme[nbr][3])):
        listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
    return listeplateforme[nbr]

def increase_left(listeplateforme, nbr,speed, dt):
    if int(listeplateforme[nbr][3])>len(listeplateforme[nbr][0]): #0: plateforme.look et 3 : plateforme.lenth
        rajout = int(listeplateforme[nbr][1])
        listeplateforme[nbr][1] = listeplateforme[nbr][1]-rajout #sauvegarder la virgule (eviter que els plateformes s'ecartent avec le tps)
        for i in range (int(rajout)):
            listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
    else:
        listeplateforme[nbr][5]-= speed*dt #reduire le trou pour la nouvelle plateforme 
    return listeplateforme[nbr]


def reduce_right(listeplateforme,nbr) : 
    #reduire la taille de la plateforme afin qu'elle disparaisse
    diminution = -listeplateforme[nbr][1] #valeur de x negative (indique le depassement de cbm de carre de cette derniere)
    if len(listeplateforme[nbr][0])>0: #voir si inutile 
        listeplateforme[nbr][0]=''
    listeplateforme[nbr][3]-=diminution
    for i in range (int(listeplateforme[nbr][3])): #regenere une plateforme de la bonne taille 
        listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
    listeplateforme[nbr][1]=0 #remet x à 0
    return listeplateforme[nbr]
    

def increase_right(listeplateforme, nbr,speed, dt):
    if int(listeplateforme[nbr][4])<=listeplateforme[nbr][3]: #4: plateforme.taille et 3 : plateforme.lenth
        listeplateforme[nbr][4]+= speed*dt
        rajout =int (listeplateforme[nbr][4]- len(listeplateforme[nbr][0]))
        for i in range (rajout):
            listeplateforme[nbr][0]=listeplateforme[nbr][0]+'_'
    else:
        listeplateforme[nbr][5]-= speed*dt #reduire le trou pour la nouvelle plateforme 
        listeplateforme[nbr][4] = listeplateforme[nbr][3]

    return listeplateforme[nbr]

def collision_down (listeplateforme,players,gamover):
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
            if int(Players.get_y(players))+a==int(i[2]) and int(i[1])<=int(Players.get_x(players))+1<=int(i[1]+i[3]): #contacte avec la tete
                gamover=1
            for b in range(3):
                if int(Players.get_y(players))+a==int(i[2]) and int(i[1])<=int(Players.get_x(players))+b<=int(i[1]+i[3]): #collision avce le corps 
                    gamover=1
    return listeplateforme, gamover

def creation_right_left(listeplateforme,score,gravite):
    derniereplat=len(listeplateforme)-1
    if listeplateforme[derniereplat][5]<=0:
        if gravite==1:
            plateforme = create_right_left(score,gravite)
        elif gravite==3:
            plateforme= create_right_left(score,gravite)
        listeplateforme=listeplat(listeplateforme,plateforme)  
    return listeplateforme

def live_right_left(listeplateforme,timeStep,speed,gravite,signe):
    move_right_left(listeplateforme,speed,timeStep,signe) #bouger les plateformes
    delete = 0
    position =0
    for b in range (len(listeplateforme)) :	
        if (int(listeplateforme[b][1])<=0 and gravite==1) or (int(listeplateforme[b][1])+int(listeplateforme[b][3])>153 and gravite==3): #regarde si la plateforme arrive en bout de course et on la fait disparaitre petit à petit 
            if gravite ==1:
                listeplateforme[b]=reduce_right(listeplateforme, b)
            elif gravite == 3:
                listeplateforme[b]=reduce_left(listeplateforme, b)
            if len(listeplateforme[b][0])==0 : #on la supprime quand il y a plus rien 
                delete = 1
                position =b
        else :
            if gravite == 1:
                listeplateforme[b]=increase_right(listeplateforme,b,speed,timeStep) #creation de la plateforme (condition dans la fct augmenter)
            elif gravite == 3:
                listeplateforme[b]=increase_left(listeplateforme,b,speed,timeStep) #creation de la plateforme (condition dans la fct augmenter)
    if delete ==1 :
        del listeplateforme[position]
    return listeplateforme
