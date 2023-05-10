import pygame
from pygame.locals import *
from random import randint
from math import radians, sin, cos, acos, asin, degrees
from constantes import *
from animation import Anim
from particles import create_particle_list


# size : 720, 480
def rotate(xa, ya, xb, yb):
    """
    renvoie en degrés la rotation nescaissaire a l'objet (xa,ya) pour être tourné vers (xb,yb)
    """
    ret = degrees(acos((xb - xa) / ((xb - xa) ** 2 + (yb - ya) ** 2) ** (1 / 2)))
    if asin((yb - ya) / ((xb - xa) ** 2 + (yb - ya) ** 2) ** (1 / 2)) < 0:
        ret = -ret
    return ret


def modulo_rot(rot):
    """
    renvoie rot [360]
    """
    if rot < 0:
        return rot + 360
    elif rot > 360:
        return rot - 360
    else:
        return rot


class Ennemy_list:  # liste des ennemis en jeu
    def __init__(self):
        self.tab = []
        self.explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.explosion_sound.set_volume(0.15)

    def update(self, player, projectiles_list, score):
        tmp = self.tab.copy()  # on copie self.ennemy_list pour pas retirer des éléments de la liste pendant qu'on bosse dessus
        a = 0  # a=nombre d'entités suprimées du tableau a ce parcours de self.ennemy_list
        for i in range(len(self.tab)):  # pour chaque entité :

            if self.tab[i].colide(player.hitbox):  # si ils touchent le joueur, on tue ce dernier.
                player.die()

            for proj in projectiles_list.sprites():  # pour chaque projectile :
                if self.tab[i].colide(proj.rect):  # si l'ennemi est en colision avec le projectile
                    player.particles = create_particle_list(15, proj.rect.x, proj.rect.y, randint(4, 6), 2, 2, 0.3, 0.5)
                    
                    self.tab[i].alive = False  # alors on tue l'ennemi
                    proj.remove(projectiles_list)  # on supprime le projectile du groupe
                    self.explosion_sound.play()
                    score += SCORE_ADD

            if self.tab[i].alive:  # si l'ennemi est vivant :
                if self.tab[i].needlist:  # les ennemis de type Chargeur sont un cas particulier, car ils ont besoin des coordonées du joueur.
                    if self.tab[i].needcord:
                        tmp=self.tab[i].move(player.x, player.y,tmp)
                    else:
                        tmp=self.tab[i].move(tmp)
                else:
                    if self.tab[i].needcord:
                        self.tab[i].move(player.x, player.y)
                    else:
                        self.tab[i].move()

            else:  # si l'ennemi n'est pas vivant :
                tmp.pop(i - a)  # on le retire de la copie de la liste d'ennemi
                a += 1  # comme on retire des éléments, il faut se décaler pour suprimer l'élément qui correspond a self.ennemy_list[i]
            if type(self.tab[i])==Asteroid :
                self.tab[i].death_anim()

        self.tab = tmp.copy()  # on transforme le tableau en sa copie vidée des ennemis morts.

        return score

    def draw(self):
        for i in range(len(self.tab)):  # pour chaque ennemi dans la liste
            if self.tab[i].alive:
                self.tab[i].draw()  # on dessine l'ennemi


class Ennemi:
    def __init__ (self,x,y,WINDOW,rect,imagepath,needcord=False,needlist=False,hitbox_size=(35,35)):
        self.alive=True #Etat
        #Position et mouvements
        self.x=x
        self.y=y

        self.needcord=needcord
        self.needlist=needlist

        # Données globales
        self.window = WINDOW  # mettre la fenettre en imput pour pouvoir s'afficher
        tu = pygame.display.get_window_size()
        self.height = tu[1]
        self.widht = tu[0]
        self.centre = rect

        # rectangles
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.base_image = self.image
        self.image_rect = self.image.get_rect(center=(self.x,self.y))
        self.hitbox = pygame.rect.Rect((x,y),hitbox_size)

    def colmurver(self):
        if self.hitbox.colliderect(self.centre):  # si on a une collision avec le rectangle du milieu
            # si l'écart entre le haut du vaisseau et le bas du rectangle est suffisament faible
            if abs(self.hitbox.top - self.centre.bottom) <= 10:
                return True

            elif abs(self.hitbox.bottom - self.centre.top) <= 10:
                return True

    def colmurhor(self):
        if self.hitbox.colliderect(self.centre):  # si on a une collision avec le rectangle du milieu
            if abs(self.hitbox.right - self.centre.left) <= 10:
                return True
            elif abs(self.hitbox.left - self.centre.right) <= 10:
                return True

    def colver (self):
        return self.y+10 >= self.height or self.y-10 <= 0

    def colhor (self):
        return self.x+10 >= self.widht or self.x-10 <= 0

    def colide(self, rect):
        return self.hitbox.colliderect(rect)


class Mine(Ennemi):  # La mine est un cercle blanc immobile.
    def __init__(self, x, y, WINDOW, rect):
        super().__init__(x, y, WINDOW, rect, "image/mine2.png")

    def draw(self):
        self.window.blit(self.image, self.image_rect)

    def move(self):
        pass


class Asteroid(Ennemi):  # l'asteroid est un cercle jaune au mouvement aléatoire
    def __init__(self, x, y, WINDOW, rect):
        super().__init__(x, y, WINDOW, rect, "image/asteroid/Asteroid 01 - Base.png")
        self.senscos = 1  # multiplicateur du sens g/d. est un fix de merde temporaire pour les bugs de cette rotation
        self.rotation = randint(1, 360)  # rotation de l'ennemi, en degrés, 0 étant a droite
        self.angle = randint(0, 360)

        self.explosion_anim = Anim(self.x, self.y, 6, (96, 96), 100,
                                   "image/asteroid/Asteroid 01 - Explode.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)

    def draw(self):
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center

    def move(self):
        self.x+=1*(cos(radians(self.rotation)))*self.senscos#le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y+=1*(sin(radians(self.rotation)))
        self.angle+=self.rotation/abs(self.rotation)
        if super().colhor() or super().colmurhor():
            self.senscos=-self.senscos
            self.x+=3*(cos(radians(self.rotation)))*self.senscos
            #self.rotation = self.rotation + 90#suposément car cos(o+pi/2)=-cos. Ne marche cepandant pas. (décalage + bug 1fois/2
        if super().colver() or super().colmurver():
            self.rotation = -self.rotation#car sin est paire. fonctione.
            self.y+=3*(sin(radians(self.rotation)))
        self.image_rect.center=(self.x,self.y)
    def death_anim(self):
        self.explosion_anim.update()
        self.explosion_anim.angle = self.angle
        self.explosion_anim.show = True
        self.image = self.explosion_anim.image


class Tir(Ennemi):
    def __init__(self, x, y, WINDOW, rect,rotation):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Weapon Effects - Projectiles/Nautolan - Bullet.png",False,False,(10,10))
        self.rotation = modulo_rot(rotation)  # rotation de l'ennemi, en degrés, 0 étant a droite
        self.anim=Anim(self.x,self.y,7,(9,12),100,"image/Nautolan/Weapon Effects - Projectiles/Nautolan - Bullet.png",False)
    def draw(self):
        self.anim.update()
        self.anim.angle =  270 - self.rotation
        self.anim.show = True
        self.image = self.anim.image
        self.window.blit(self.image, self.image_rect)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center



        pygame.draw.rect(self.window,"red",self.hitbox,1)

    def move(self):
        self.x+=5*(cos(radians(self.rotation)))#le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y+=5*(sin(radians(self.rotation)))
        if super().colhor() or super().colmurhor() or super().colver() or super().colmurver():
            self.alive=False
        self.image_rect.center=(self.x,self.y)

class Chargeur(Ennemi):  # le Chargeur est un cercle vert qui s'orriente à l'apparition vers le centre de l'écran
    def __init__(self, x, y, WINDOW, rect):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Designs - Base/Nautolan Ship - Frigate - Base.png",True,False)
        self.senscos = 1  # multiplicateur du sens g/d. est un fix de merde temporaire pour les bugs de cette rotation
        self.rotation = 0
        self.vitesse = 1

    def draw(self):
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, 270 - self.rotation, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        #pygame.draw.rect(self.window,"red",self.hitbox,1)

    def move(self, x, y):
        self.rotation = modulo_rot(self.rotation)
        self.x += self.vitesse * (cos(radians(self.rotation))) * self.senscos  # le *senscos ne devrait pas être nécéssaire mais bon pour l'instant
        self.y += self.vitesse * (sin(radians(self.rotation)))
        objectif = modulo_rot(rotate(self.x, self.y, x, y))
        calcul = modulo_rot(objectif - self.rotation)
        if calcul > 0 and calcul < 180:
            self.rotation += +0.7
        else:
            self.rotation += -0.7
        if calcul < 10 or calcul > 350:
            self.vitesse = 2
        else:
            self.vitesse = 0.7
        if super().colver() :
            self.rotation = -self.rotation
        if super().colhor() :
            self.rotation = self.rotation + 90

class Tourelle(Ennemi):
    def __init__(self, x, y, WINDOW,rect):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Designs - Base/Nautolan Ship - Support - Base.png",True,True)
        self.rotation = 0
        self.clock=randint(50,150)
    def draw(self):
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, 270 - self.rotation, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
    def move(self,x,y,liste):
        self.rotation=rotate(self.x,self.y,x,y)
        if self.clock==0:
            liste.append(Tir(self.x,self.y, self.window, self.centre,self.rotation))
            self.clock=140
        self.clock+=-1
        return liste

class Rocketship(Ennemi):
    def __init__(self, x, y, WINDOW,rect):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Designs - Base/Nautolan Ship - Torpedo Ship.png",True,True)
        self.rotation = 0
        self.clock=randint(50,150)
    def draw(self):
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, 270 - self.rotation, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
    def move(self,x,y,liste):
        self.rotation=rotate(self.x,self.y,x,y)
        if self.clock==0:
            liste.append(Tir(self.x,self.y, self.window, self.centre,self.rotation))
            self.clock=70
        self.clock+=-1
        return liste