import sys
import os

#le module Animation gere le type abstrait de donnee animation
#un animation est un film ascii affiche dans un terminal

def create(color,x,y,filename):
	
	#creation animat
	animation=dict()
	animation["color"]=color
	animation["x"]=x
	animation["y"]=y
	animation["on"]=False

	#recuperation du film
	myfile = open(filename, "r")
	chaine=myfile.read()

	#separation des frames
	frames=chaine.split("frame\n")
	
	animation["frames"]=[]
	for f in frames:
		animation["frames"].append(f.split("\n"))
	
	animation["timeLeft"]=None
	animation["duration"]=3

	print("animation=\n")
	print(animation["frames"])

	return animation


def setOn(a,state=True):
	if(state==True):
		a["on"]=True
		a["timeLeft"]=a["duration"]
	else:
		a["on"]=False
		a["timeLeft"]=None
		
		
def getOn(a):
	return(a["on"])

def getCurrentFrameIndex(a):
	tl=a["timeLeft"]
	d=float(a["duration"])
	nf=float(len(a["frames"]))
	
	step=d/nf
	index=int((d-tl)/step)
	
	if index >(len(a["frames"])-1):
		index=(len(a["frames"])-1)
	return index

def show(a,dt) : 
	
	if(getOn(a)==False):
		return
	
	a["timeLeft"]=a["timeLeft"]-dt
	
	if a["timeLeft"] <= 0:
		setOn(a,False)
		return
	
	#couleur fond noire
	sys.stdout.write("\033[40m")
	
	#couleur animation
	c=a["color"]
	txt="\033[37m"
	#txt="\033[3"+str(c%7+1)+"m"
	sys.stdout.write(txt)
	
	#affichage de la frame
	
	#selectFrame
	i=getCurrentFrameIndex(a)

	#pour chaque ligne
	for j in range(0,len(a["frames"][i])):
		#on se place a la position de l animat dans le terminal
		x=str(int(a["x"]))
		y=str(int(a["y"])+j)
		txt="\033["+y+";"+x+"H"
		sys.stdout.write(txt)
		
		sys.stdout.write(a["frames"][i][j])
		sys.stdout.write("\n")

	