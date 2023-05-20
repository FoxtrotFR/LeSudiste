# -*- coding: utf-8 -*-
"""
Created on Tue Apr 11 10:58:47 2023

@author: Maxime
"""

class Frites : pass

import sys
import random

def create (speedmin,tempomin,tempomax,x,y):
    frite = Frites()
    frite.x = x #143 pour right et down
    frite.y = y    #11 pour right et down
    frite.look = ['/','|',"\\"]
    frite.tempo =random.randint (tempomin,tempomax) #50/100 pour le move1
    frite.speed = random.randint (speedmin,30)
    
    return frite
    
def show (listefrites,nbr): #etat varie en focntion de la gravité (voir liste frites.look)
    x=str(int(listefrites[nbr][1]))
    y=str(int(listefrites[nbr][2]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position du personnage 
    sys.stdout.write(listefrites[nbr][0]) #afficher la frite

def move (listefrites,gravite,dt,signe):
    for i in listefrites :
        i[1]+=i[4]*dt*signe #appliquer la vitesse lateral signe =-1 pour right et down signe = 1 pour left
        i[2]+=(gravite*dt)/3 #appliquer la gravite(diminué)

def fritliste(listefrites,frite,etat):
    listefrites.append([frite.look[etat],frite.x,frite.y, frite.tempo,frite.speed]) #rajout d'une frite 
    return listefrites

def creation (listefrites,speedmin,tempomin,tempomax,x,y): 
    if len(listefrites)==0: 
        frite = create(speedmin,tempomin,tempomax,x,y)
        listefrites=fritliste(listefrites,frite,0) #0 correspond à  l'état de la frite, ici en diagonal   
    elif len (listefrites)<10 and listefrites[len(listefrites)-1][3]==0: #creer une frite 
        frite = create(speedmin,tempomin,tempomax,x,y)
        listefrites=fritliste(listefrites,frite,0)
    for i in range (len(listefrites)): #gerer la tempo et le reduire si besoin 
        if listefrites[i][3]>0:
            listefrites[i][3]-=1
    return listefrites

def collision (listefrites,listeplateforme,players,gamover):
    deletefrite = 0
    positionfrite= 0
    for i in range (len(listefrites)): 
		#collision avec le palyers
        if int(listefrites[i][2])== int(players.y) and int(listefrites[i][1])==int(players.x)+1: #si la frite touche la tete
            gamover=1
        for b in range (1,3):
            for a in range(3):
                if int(listefrites[i][2])==int(players.y)+b and int(listefrites[i][1])==int(players.x)+a: #si la frite touche le corps
                     gamover=1
		#collision avec le sol ou le mur
        if int (listefrites[i][2])==41 or int(listefrites[i][1]==0) :
            deletefrite=1
            positionfrite=i
        for i in range (5):
            if int(listefrites[i][1])==150+i: #dans le cas ou la frites touche le mur (comme il n'y a pas de position intermediare on est oblige de balayer un espace possible entre deux positions)
                deletefrite=1
                positionfrite=i
		#collision avec plateforme
        for c in range(len(listeplateforme)):
             if int(listefrites[i][2])==int(listeplateforme[c][2]) and int (listeplateforme[c][1])<= int(listefrites[i][1])<= int(listeplateforme[c][1]+len(listeplateforme[c][0])):
                deletefrite=1
                positionfrite=i
    if deletefrite==1:
        del listefrites[positionfrite]
    return gamover,listefrites