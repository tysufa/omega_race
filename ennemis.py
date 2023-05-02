import pygame
from pygame.locals import *
from random import randint
from math import radians,sin,cos,acos,asin,degrees
#size : 720, 480
def rotate (xa,ya,xb,yb):
    """
    renvoie en degrés la rotation nescaissaire a l'objet (xa,ya) pour être tourné vers (xb,yb)
    """
    ret=degrees(acos((xb-xa)/((xb-xa)**2+(yb-ya)**2)**(1/2)))
    if asin((yb-ya)/((xb-xa)**2+(yb-ya)**2)**(1/2))<0:
        ret = -ret
    return ret

class Ennemy_list :
    def __init__ (self):
        self.tab=[]

    def update(self,playerx,playery):
        tmp = self.tab.copy()  # on copie self.ennemy_list pour pas retirer des éléments de la liste pendant qu'on bosse dessus
        a = 0  # a=nombre d'entités suprimées du tableau a ce parcours de self.ennemy_list
        for i in range(len(self.tab)):
            if self.tab[i].colide(playerx,playery,26):#si l'objet est en colision avec le joueur a 20 px près
                self.tab[i].alive=False#alors on tue l'objet
            if self.tab[i].alive:
                self.tab[i].move()
            else:
                tmp.pop(i - a)  # comme on retire des éléments, il faut se décaler pour suprimer l'élément qui correspond a self.ennemy_list[i]
                a += 1
        self.tab = tmp.copy()

    def draw (self):
        for i in range(len(self.tab)):
            if self.tab[i].alive:
                self.tab[i].draw()

    def ajouter (self,ennemi):
        tab.append(ennemi)

class Ennemi:
    def __init__ (self,x,y,WINDOW,imagepath):
        self.x=x
        self.y=y
        self.alive=True
        self.window=WINDOW#mettre la fenettre en imput pour pouvoir s'afficher
        tu=pygame.display.get_window_size()
        self.height=tu[1]
        self.widht=tu[0]
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.image_rect = self.image.get_rect(center=(self.x,self.y))
        while self.x+10>(self.widht // 2 -self.widht // 6) and self.x-10<(self.widht // 2 +self.widht // 6) and self.y+10>(self.height // 2 -self.height // 6) and self.y-10<(self.height // 2 +self.height // 6) :
            self.x=randint(10,tu[0]-10)
            self.y=randint(10,tu[1]-10)

    def colmurver (self):
        return (self.x+15>(self.widht // 2 -self.widht // 6) and self.x-15<(self.widht // 2 +self.widht // 6) and self.y+15>(self.height // 2 -self.height // 6) and self.y-15<(self.height // 2 +self.height // 6) and (self.y<(self.height // 2 -self.height // 6) or self.y>(self.height // 2 +self.height // 6)))

    def colmurhor (self):
        return (self.x+15>(self.widht // 2 -self.widht // 6) and self.x-15<(self.widht // 2 +self.widht // 6) and self.y+15>(self.height // 2 -self.height // 6) and self.y-15<(self.height // 2 +self.height // 6) and (self.x<(self.widht // 2 -self.widht // 6) or self.x>(self.widht // 2 +self.widht // 6)))

    def colver (self):
        return self.y+10 >= self.height or self.y-10 <= 0 or self.colmurver()#essayer de récuperer les dimensions de la fenètre + essayer de prendre en compte le carré central

    def colhor (self):
        return self.x+10 >= self.widht or self.x-10 <= 0 or self.colmurhor()

    def colide (self, x,y,size):
        return self.x-size<x and self.x+size>x and self.y-size<y and self.y+size>y

class mine(Ennemi):#La mine est un cercle blanc immobile.
    def __init__ (self,x,y,WINDOW):
        super().__init__(x,y,WINDOW)

    def draw(self):
        pygame.draw.circle(self.window, (255,255,255), (self.x, self.y), 10)

    def move(self):
        pass

class asteroid(Ennemi):#l'asteroid est un cercle jaune au mouvement aléatoire
    def __init__ (self,x,y,WINDOW):
        super().__init__(x,y,WINDOW,"image/Asteroid 01 - Base.png")
        self.senscos=1#multiplicateur du sens g/d. est un fix de merde temporaire pour les bugs de cette rotation
        self.rotation=randint(0,360)#rotation de l'ennemi, en degrés, 0 étant a droite
        self.angle=0

    def draw (self):
        self.window.blit(self.image,self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle

    def move(self):
        self.x+=1*(cos(radians(self.rotation)))*self.senscos#le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y+=1*(sin(radians(self.rotation)))
        if super().colhor():
            self.senscos=-self.senscos
            #self.rotation = self.rotation + 90#suposément car cos(o+pi/2)=-cos. Ne marche cepandant pas. (décalage + bug 1fois/2
        if super().colver():
            self.rotation = -self.rotation#car sin est paire. fonctione.
        self.image_rect.center=(self.x,self.y)

class bull(Ennemi):#le bull est un cercle vert qui s'orriente à l'apparition vers le centre de l'écran
    def __init__ (self,x,y,xb,yb,WINDOW,vitesse=5):
        super().__init__(x,y,WINDOW)
        self.senscos=1#multiplicateur du sens g/d. est un fix de merde temporaire pour les bugs de cette rotation
        self.rotation=rotate(x,y,xb,yb)
        self.vitesse=vitesse

    def draw (self):
        pygame.draw.circle(self.window, (0,255,0), (self.x, self.y), 10)

    def moove(self):
        self.x+=vitesse*(cos(radians(self.rotation)))*self.senscos#le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y+=vitesse*(sin(radians(self.rotation)))
        if super().colhor() or super().colver() :
            self.alive=False

class shooter(Ennemi):
    def _init__ (self,x,y,WINDOW,liste):
        super().__init__(x,y,WINDOW)
        self.liste=liste
        self.height=20
        self.width=40

    def draw(self):
        pygame.draw.rect(self.window, (255,255,0), (self.x-self.width/2, self.y-self.height/2), self.height,self.widht)
    def moove(self):
        self.x+=vitesse*(cos(radians(self.rotation)))*self.senscos#le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y+=vitesse*(sin(radians(self.rotation)))

        if super().colhor() or super().colver() :
            self.alive=False
