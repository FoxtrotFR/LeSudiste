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
    frite.tempo =random.randint (tempomin,tempomax) #50/100 pour le move_right et left
    frite.speed = random.randint (speedmin,30)
    
    return frite
    
def show (liste_frites,nbr): #etat varie en focntion de la gravité (voir liste frites.look)
    x=str(int(liste_frites[nbr][1]))
    y=str(int(liste_frites[nbr][2]))
    txt="\033["+y+";"+x+"H" #placer le curseur 
    sys.stdout.write(txt)#se placer à la position du personnage 
    sys.stdout.write(liste_frites[nbr][0]) #afficher la frite

def move (liste_frites,gravite,dt,signe,up):
    for i in liste_frites :
        i[1]+=i[4]*dt*signe #appliquer la vitesse lateral signe =-1 pour right et down signe = 1 pour left
        i[2]+=(up*gravite*dt)/3 #appliquer la gravite(diminué), signe up =-1 pour une monte des frites

def fritliste(liste_frites,frite,etat):
    liste_frites.append([frite.look[etat],frite.x,frite.y, frite.tempo,frite.speed]) #rajout d'une frite 
    return liste_frites

def creation (liste_frites,speedmin,tempomin,tempomax,x,y): 
    if len(liste_frites)==0: 
        frite = create(speedmin,tempomin,tempomax,x,y)
        liste_frites=fritliste(liste_frites,frite,0) #0 correspond à  l'état de la frite, ici en diagonal   
    elif len (liste_frites)<10 and liste_frites[len(liste_frites)-1][3]==0: #creer une frite 
        frite = create(speedmin,tempomin,tempomax,x,y)
        liste_frites=fritliste(liste_frites,frite,0)
    for i in range (len(liste_frites)): #gerer la tempo et le reduire si besoin 
        if liste_frites[i][3]>0:
            liste_frites[i][3]-=1
    return liste_frites

def collision (liste_frites,liste_plateforme,players,gamover):
    deletefrite = 0
    positionfrite= 0
    for i in range (len(liste_frites)): 
		#collision avec le palyers
        if int(liste_frites[i][2])== int(players.y) and int(liste_frites[i][1])==int(players.x)+1: #si la frite touche la tete
            gamover=1
        for b in range (1,3):
            for a in range(3):
                if int(liste_frites[i][2])==int(players.y)+b and int(liste_frites[i][1])==int(players.x)+a: #si la frite touche le corps
                     gamover=1
		#collision avec le sol ou le mur
        if int (liste_frites[i][2])>=41 or int(liste_frites[i][1]<=1) or int(liste_frites[i][1]>=152 or int(liste_frites[i][2])<=9) :
            deletefrite=1
            positionfrite=i
		#collision avec plateforme
        for c in range(len(liste_plateforme)):
             if int(liste_frites[i][2])==int(liste_plateforme[c][2]) and int (liste_plateforme[c][1])<= int(liste_frites[i][1])<= int(liste_plateforme[c][1]+len(liste_plateforme[c][0])):
                deletefrite=1
                positionfrite=i
    if deletefrite==1:
        del liste_frites[positionfrite]
    return gamover,liste_frites