import pygame
from pygame.locals import *
from random import randint
from math import radians,sin,cos,acos,asin,degrees

def rotate (xa,ya,xb,yb):
    """
    renvoie en degrés la rotation nescaissaire a l'objet (xa,ya) pour être tourné vers (xb,yb)
    """
    ret=degrees(acos((xb-xa)/((xb-xa)**2+(yb-ya)**2)**(1/2)))
    if asin((yb-ya)/((xb-xa)**2+(yb-ya)**2)**(1/2))<0:
        ret = -ret
    return ret

class ennemi:
    def __init__ (self,x,y,WINDOW):
        self.x=x
        self.y=y
        self.alive=True
        self.window=WINDOW#mettre la fenettre en imput pour pouvoir s'afficher

class mine(ennemi):#La mine est un cercle blanc immobile.
    def __init__ (self,x,y,WINDOW):
        super().__init__(x,y,WINDOW)
    def draw(self):
        pygame.draw.circle(self.window, (255,255,255), (self.x, self.y), 10)
    def moove(self):
        pass

class asteroid(ennemi):#l'asteroid est un cercle jaune au mouvement aléatoire
    def __init__ (self,x,y,WINDOW):
        super().__init__(x,y,WINDOW)
        self.senscos=1#multiplicateur du sens g/d. est un fix de merde temporaire pour les bugs de cette rotation
        self.rotation=randint(0,360)#rotation de l'ennemi, en degrés, 0 étant a droite
    def draw (self):
        pygame.draw.circle(self.window, (255,255,0), (self.x, self.y), 10)
    def moove(self):
        self.x+=5*(cos(radians(self.rotation)))*self.senscos#le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y+=5*(sin(radians(self.rotation)))
        if self.x+10 >= 640 or self.x-10 <= 0:
            self.senscos=-self.senscos
            #self.rotation = self.rotation + 90#suposément car cos(o+pi/2)=-cos. Ne marche cepandant pas. (décalage + bug 1fois/2
        if self.y+10 >= 480 or self.y-10 <= 0:
            self.rotation = -self.rotation#car sin est paire. fonctione.

class bull(ennemi):#le bull est un cercle vert qui s'orriente à l'apparition vers le centre de l'écran
    def __init__ (self,x,y,WINDOW):
        super().__init__(x,y,WINDOW)
        self.senscos=1#multiplicateur du sens g/d. est un fix de merde temporaire pour les bugs de cette rotation
        self.rotation=rotate(x,y,320,240)
    def draw (self):
        pygame.draw.circle(self.window, (0,255,0), (self.x, self.y), 10)
    def moove(self):
        self.x+=5*(cos(radians(self.rotation)))*self.senscos#le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y+=5*(sin(radians(self.rotation)))
        """if self.x+10 > 620 or self.x-10 < 0:
            self.senscos=-self.senscos#self.rotation = self.rotation-90#la rotation ne marche pas
        if self.y+10 >= 480 or self.y-10 <= 0:
            self.rotation = -self.rotation"""
        if self.x+10 > 640 or self.x-10 < 0 or self.y+10 >= 480 or self.y-10 <= 0:
            self.alive=False