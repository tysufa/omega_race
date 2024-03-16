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

def passe_par_milieu(xa, ya, xb, yb,marge=10):
    rect=pygame.rect.Rect((0, 0, SIZE[0] // 3+marge, SIZE[1] // 3+marge))
    rect.center = (SIZE[0] // 2, SIZE[1] // 2)
    return len(rect.clipline((xa,ya),(xb,yb)))!=0


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
    def __init__(self,upgrades={}):
        self.tab = []
        self.explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.explosion_sound.set_volume(0.15)
        self.particle_list = []
        self.tempo = pygame.time.get_ticks()
        self.only_bullet = False
        self.screenshake = 0
        self.upgrades=upgrades
        if(self.upgrades=={}):
            for up in LISTE_UPGRADES :
                self.upgrades[up]=False

    def update(self, player, projectiles_list, score):
        tmp = self.tab.copy()  # on copie self.ennemy_list pour pas retirer des éléments de la liste pendant qu'on bosse dessus
        a = 0  # a=nombre d'entités suprimées du tableau a ce parcours de self.ennemy_list
        self.only_bullet = True
        for par in self.particle_list:
            par.update()
        for i in range(len(self.tab)):  # pour chaque entité :
            if not self.tab[i].is_bullet:
                self.only_bullet = False

            for proj in projectiles_list.sprites():  # pour chaque projectile :
                if self.tab[i].shield:
                    if self.tab[i].hitbox.colliderect(proj.rect):
                        self.tab[i].shield=False
                        proj.remove(projectiles_list)  # on supprime le projectile du groupe
                elif self.tab[i].colide(proj.rect) and self.tab[i].alive:  # si l'ennemi est en colision avec le projectile
                    self.particle_list = create_particle_list(15, proj.rect.x, proj.rect.y, randint(4, 6), 2, 2, 0.3, 0.5)
                    self.tab[i].alive = False
                    self.screenshake = 10 # on secoue l'écran pendant 10 frames
                    if not self.tab[i].is_bullet:
                        self.explosion_sound.play()
                        score += self.tab[i].score_value
                        proj.remove(projectiles_list)  # on supprime le projectile du groupe
                    self.tempo = pygame.time.get_ticks()

            if self.tab[i].alive:  # si l'ennemi est vivant :
                if self.tab[i].killbox.colliderect(player.hitbox) and player.alive:  # si ils touchent le joueur, on tue ce dernier.
                    player.die()
                if type(self.tab[i])==Miner:
                    if self.tab[i].mines<1:
                        self.tab[i].alive=False
                        tmp.append(Chargeur(self.tab[i].x,self.tab[i].y,self.tab[i].window,self.tab[i].centre))
                        self.particle_list = create_particle_list(50, self.tab[i].x, self.tab[i].y, randint(9, 12), 3, 3, 0.5, 0.8)
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
                if type(self.tab[i])==Mine:
                    for i in range(VARIABLES["MINE_TIRS"]):
                            liste.append(Rocket(self.x,self.y, self.window, self.centre,(360/VARIABLES["MINE_TIRS"])*i))
                if pygame.time.get_ticks() - self.tempo > self.tab[i].explosion_anim.frame_number * self.tab[i].explosion_anim.frames_delay:
                    tmp.pop(i - a)  # on le retire de la copie de la liste d'ennemi
                    a += 1  # comme on retire des éléments, il faut se décaler pour suprimer l'élément qui correspond a self.ennemy_list[i]
                self.tab[i].death_anim()


        self.tab = tmp.copy()  # on transforme le tableau en sa copie vidée des ennemis morts.

        return score

    def gestion_upgrades(self):
        global VARIABLES
        if self.upgrades["tourelle_cadence+"]:
            VARIABLES["TOURELLE_NEW_CLOCK"][0]*=TOURELLE_NEW_CLOCK_UPGRADE_MULTIPLIER
            VARIABLES["TOURELLE_NEW_CLOCK"][1]*=TOURELLE_NEW_CLOCK_UPGRADE_MULTIPLIER
            self.upgrades["tourelle_cadence+"]=False
        if self.upgrades["tourelle_grace-"]:
            VARIABLES["TOURELLE_INITIAL_CLOCK"][0]*=TOURELLE_INITIAL_CLOCK_UPGRADE_MULTIPLIER
            VARIABLES["TOURELLE_INITIAL_CLOCK"][1]*=TOURELLE_INITIAL_CLOCK_UPGRADE_MULTIPLIER
            self.upgrades["tourelle_grace-"]=False
        if self.upgrades["tir_vitesse+"]:
            VARIABLES["TIR_VITESSE"]*=TIR_VITESSE_UPGRADE_MULTIPLIER
            self.upgrades["tir_vitesse+"]=False
        if self.upgrades["chargeur_rotation+"]:
            VARIABLES["CHARGEUR_ROTATION_SPEED"]*=CHARGEUR_ROTATION_SPEED_UPGRADE_MULTIPLIER
            VARIABLES["CHARGEUR_ANGLE_ACCELERATION"]*=CHARGEUR_ANGLE_ACCELERATION_UPGRADE_MULTIPLIER
            self.upgrades["chargeur_rotation+"]=False
        if (VARIABLES["TOURELLE_TIR"] == "tir" and self.upgrades["tourelle_rocket"]):
            VARIABLES["TOURELLE_TIR"] = "rocket"
        if (VARIABLES["MINE_TIRS"] == "tir" and self.upgrades["mine_shrapnel"]):
            VARIABLES["MINE_TIRS"] = 5

    def draw(self):
        for i in range(len(self.tab)):  # pour chaque ennemi dans la liste
            self.tab[i].draw()  # on dessine l'ennemi


class Ennemi:
    def __init__ (self,x,y,WINDOW,rect,imagepath,needcord=False,needlist=False,hitbox_size=(35,35)):
        #Etat
        self.alive=True
        self.dying=False
        #Position et mouvements
        self.x=x
        self.y=y
        self.needcord=needcord
        self.needlist=needlist

        # Données globales
        self.window = WINDOW  # mettre la fenettre en imput pour pouvoir s'afficher
        self.centre = rect

        # rectangles
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.base_image = self.image
        self.image_rect = self.image.get_rect(center=(self.x,self.y))
        self.hitbox = pygame.rect.Rect((x,y),(hitbox_size[0]+10,hitbox_size[1]+10))
        self.killbox =  pygame.rect.Rect((x,y),(max(hitbox_size[0]-10,1),max(hitbox_size[1]-10,1)))#hitbox qui tue le joueur

        self.shield=False
        self.is_bullet = False
        self.score_value = 0


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
        return self.y+self.hitbox.height/2 >= SIZE[1] or self.y-self.hitbox.height/2 <= 0

    def colhor (self):
        return self.x+self.hitbox.width/2 >= SIZE[0] or self.x-self.hitbox.width/2 <= 0

    def colide(self, rect):
        return self.hitbox.colliderect(rect)


class Mine(Ennemi):  # La mine est un cercle blanc immobile.
    def __init__(self, x, y, WINDOW, rect):
        super().__init__(x, y, WINDOW, rect, "image/mine/mine1.png",False,False,(30,30))
        self.score_value=50

        self.anim= Anim(self.x, self.y, 1, (32, 32), 400,
                                   "image/mine/mines2.png", True)

        #pour l'animation de mort:
        self.explosion_anim = Anim(self.x, self.y, 8, (64, 64), 50,
                                   "image/Nautolan/Destruction/Nautolan Ship - Bomber.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)

    def draw(self):
        if self.alive:
            self.anim.update()
            self.anim.show = True
            self.image = self.anim.image
        self.window.blit(self.image, self.image_rect)
        #pygame.draw.rect(self.window,"red",self.hitbox,1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        self.killbox.center = self.image_rect.center
    def move(self):
        pass

    def death_anim(self):#ce serait bien d'uniformiser les self.angle et self.rotation pour en faire une méthode du super
        self.explosion_anim.update()
        self.explosion_anim.angle =randint(0,360)
        self.explosion_anim.show = True
        self.image = self.explosion_anim.image

class Asteroid(Ennemi):  # l'asteroid est un cercle jaune au mouvement aléatoire
    def __init__(self, x, y, WINDOW, rect):
        super().__init__(x, y, WINDOW, rect, "image/asteroid/Asteroid 01 - Base.png")
        self.rotation = randint(1, 360)  # rotation de l'ennemi, en degrés, 0 étant a droite
        self.angle = randint(0, 360)

        #pour l'animation de mort:
        self.explosion_anim = Anim(self.x, self.y, 6, (96, 96), 50,
                                   "image/asteroid/Asteroid 01 - Explode.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)

        self.score_value = ASTEROIDE_SCORE

    def draw(self):
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        self.killbox.center = self.image_rect.center

    def move(self):
        self.rotation=self.rotation%360#on mets la rotation modulo 360 pour assurer le bon fonctionement de la trigonométrie
        self.x+=ASTEROID_VITESSE*(cos(radians(self.rotation)))
        self.y+=ASTEROID_VITESSE*(sin(radians(self.rotation)))
        if self.rotation !=0:
            self.angle+=self.rotation/abs(self.rotation)
        if super().colhor() or super().colmurhor():
            self.rotation=180-self.rotation
            self.x+=3*(cos(radians(self.rotation)))
        if super().colver() or super().colmurver():
            self.rotation = -self.rotation
            self.y+=3*(sin(radians(self.rotation)))
        self.image_rect.center=(self.x,self.y)

    def death_anim(self):#ce serait bien d'uniformiser les self.angle et self.rotation pour en faire une méthode du super
        self.explosion_anim.update()
        self.explosion_anim.angle = self.angle
        self.explosion_anim.show = True
        self.image = self.explosion_anim.image


class Tir(Ennemi):
    def __init__(self, x, y, WINDOW, rect,rotation):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Weapon Effects - Projectiles/Nautolan - Bullet.png",False,False,(10,10))
        self.rotation = modulo_rot(rotation)  # rotation de l'ennemi, en degrés, 0 étant a droite
        self.anim=Anim(self.x,self.y,7,(9,12),100,"image/Nautolan/Weapon Effects - Projectiles/Nautolan - Bullet.png",False)
        self.is_bullet = True

        #pour pas que le jeu implose:
        self.explosion_anim = Anim(self.x, self.y, 0, (64, 64), 0,
                                   "image/Nautolan/Destruction/Nautolan Ship - Frigate.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)

    def draw(self):
        self.anim.update()
        self.anim.angle =  270 - self.rotation
        self.anim.show = True
        self.image = self.anim.image
        self.window.blit(self.image, self.image_rect)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        self.killbox.center = self.image_rect.center

    def move(self):
        self.x+=VARIABLES["TIR_VITESSE"]*(cos(radians(self.rotation)))
        self.y+=VARIABLES["TIR_VITESSE"]*(sin(radians(self.rotation)))
        if super().colhor() or super().colmurhor() or super().colver() or super().colmurver():
            self.alive=False
        self.image_rect.center=(self.x,self.y)

    def death_anim(self):
        pass

class Rocket(Ennemi):
    def __init__(self, x, y, WINDOW, rect,rotation):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Weapon Effects - Projectiles/Nautolan - Rocket.png",True,False,(10,10))
        self.rotation = modulo_rot(rotation)  # rotation de l'ennemi, en degrés, 0 étant a droite
        self.anim=Anim(self.x,self.y,4,(16,32),100,"image/Nautolan/Weapon Effects - Projectiles/Nautolan - Rocket.png",False)
        self.is_bullet = True

        #pour pas que le jeu implose:
        self.explosion_anim = Anim(self.x, self.y, 0, (64, 64), 0,
                                   "image/Nautolan/Destruction/Nautolan Ship - Frigate.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)
        self.rotation_vitesse=ROCKET_ROTATION

    def draw(self):
        self.anim.update()
        self.anim.angle =  270 - self.rotation
        self.anim.show = True
        self.image = self.anim.image
        self.window.blit(self.image, self.image_rect)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        self.killbox.center = self.image_rect.center

    def move(self, x, y):
        self.rotation = modulo_rot(self.rotation)
        objectif = modulo_rot(rotate(self.x, self.y, x,y))
        calcul_dirrection = modulo_rot(objectif - self.rotation)
        #pour tourner dans le bon sens:
        if calcul_dirrection > 0 and calcul_dirrection < 180:
            self.rotation += +self.rotation_vitesse
        else:
            self.rotation += -self.rotation_vitesse
        #pour accelerer si l'objectif est en vue et ralentir sinon:
        #on effectue enfin le mouvement
        self.x += ROCKET_VITESSE * (cos(radians(self.rotation)))
        self.y += ROCKET_VITESSE * (sin(radians(self.rotation)))
        self.rotation_vitesse*=ROCKET_ROTATION_DECAY
        if super().colhor() or super().colmurhor() or super().colver() or super().colmurver():
            self.alive=False

    def death_anim(self):
        pass

class Chargeur(Ennemi):
    def __init__(self, x, y, WINDOW, rect,shield=False):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Designs - Base/Nautolan Ship - Frigate - Base.png",True,False)
        self.engine_anim=Anim(self.x,self.y,6,(64,64),50,"image/Nautolan/Engine Effects/Nautolan Ship - Frigate - Engine Effect.png",False)
        self.engine_anim.show=False
        self.rotation = randint(0,360)
        self.vitesse = 1
        self.objectif=(x,y)
        self.score_value = CHARGEUR_SCORE

        #pour l'animation de mort:
        self.explosion_anim = Anim(self.x, self.y, 8, (64, 64), 50,
                                   "image/Nautolan/Destruction/Nautolan Ship - Frigate.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)

        #sheild:
        self.shield=shield
        self.shield_anim=Anim(self.x,self.y,35,(63,63),50,"image/Nautolan/Shields/Nautolan Ship - Frigate - Shield.png",False)

        self.hitbox.center = (self.x,self.y)

    def draw(self):
        if self.shield:
            self.shield_anim.show=True
        else:
            self.shield_anim.show=False
        if self.alive:
            self.image = pygame.transform.rotozoom(self.base_image, 270 - self.rotation, 1)
            self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
            self.hitbox.center = self.image_rect.center
            self.engine_anim.angle= 270 - self.rotation
            if self.vitesse>1.5:
                self.engine_anim.show=True
            self.engine_anim.update()
            self.window.blit(self.engine_anim.image, self.image_rect)
            self.killbox.center = self.image_rect.center
            self.shield_anim.angle= 270 - self.rotation
            self.shield_anim.update()
        self.window.blit(self.shield_anim.image, self.image_rect)
        self.window.blit(self.image, self.image_rect)
        #pygame.draw.rect(self.window,"red",self.hitbox,1)

    def colisions(self):
        if super().colmurhor() and super().colmurver():
            self.rotation = -self.rotation-90
            if self.y<SIZE[1]//2:
                self.y+=-5
            else:
                self.y+=+5
            if self.x<SIZE[0]//2:
                self.x+=-5
            else:
                self.x+=+5
        if super().colver():
            self.rotation = -self.rotation
        if super().colmurver():
            self.rotation = -self.rotation
            if self.y<SIZE[1]//2:
                self.y+=-5
            else:
                self.y+=+5
        if super().colhor():
            self.rotation = self.rotation + 90
        if super().colmurhor():
            self.rotation = self.rotation + 90
            if self.x<SIZE[0]//2:
                self.x+=-5
            else:
                self.x+=+5

    def choix_objectif(self,x,y):
        if not passe_par_milieu(self.x,self.y,x,y,40):#si on a une ligne de vue directe sur le joueur:
            self.objectif=(x,y)#on se dirige vers lui
        else :#si on ne peut pas acceder au joueur:
            if self.x<SIZE[0]//2+SIZE[0]//6 and self.x>SIZE[0]//2-SIZE[0]//6 and x<SIZE[0]//2+SIZE[0]//6 and x>SIZE[0]//2+-SIZE[0]//6: # le joueur et l'ennemi sont a l'opposé du rect:
                if self.x<SIZE[0]//2:#on sort de ce coté du rect, en passant par le plus proche
                    self.objectif=(self.x-10, self.y)
                else:
                    self.objectif=(self.x+10, self.y)
            elif self.y<SIZE[1]//2+SIZE[1]//6 and self.y>SIZE[1]//2-SIZE[1]//6 and y<SIZE[1]//2+SIZE[1]//6 and y>SIZE[1]//2-SIZE[1]//6: # le joueur et l'ennemi sont a l'opposé du rect:
                if self.y<SIZE[1]//2:#on sort de ce coté du rect, en passant par le plus proche
                    self.objectif=(self.x, self.y-10)
                else:
                    self.objectif=(self.x, self.y+10)
            elif not passe_par_milieu(self.x,self.y,self.x,y) and not passe_par_milieu(self.x,self.y,x,self.y):#si on à accés aux deux points :
                if not passe_par_milieu(x,y,self.x,y):#on prends celui des deux qui donne accés au joueur
                    self.objectif=(self.x,y)
                else:
                    self.objectif=(x,self.y)
            elif not passe_par_milieu(self.x,self.y,self.x,y):#sinon, si on peut, on se mets de façon a partager le x ou le y du joueur
                self.objectif=(self.x,y)
            elif not passe_par_milieu(self.x,self.y,x,self.y):
                self.objectif=(x,self.y)

    def move(self, x, y):
        self.choix_objectif(x,y)
        self.rotation = modulo_rot(self.rotation)
        objectif = modulo_rot(rotate(self.x, self.y, self.objectif[0],self.objectif[1]))
        calcul_dirrection = modulo_rot(objectif - self.rotation)
        #pour tourner dans le bon sens:
        if calcul_dirrection > 0 and calcul_dirrection < 180:
            self.rotation += +VARIABLES["CHARGEUR_ROTATION_SPEED"]
        else:
            self.rotation += -VARIABLES["CHARGEUR_ROTATION_SPEED"]
        #pour accelerer si l'objectif est en vue et ralentir sinon:
        if calcul_dirrection < VARIABLES["CHARGEUR_ANGLE_ACCELERATION"] or calcul_dirrection > 360-VARIABLES["CHARGEUR_ANGLE_ACCELERATION"]:
            self.vitesse +=CHARGEUR_ACCELERATION
        else:
            self.vitesse +=-CHARGEUR_DECELERATION
        #on limite la vitesse
        if self.vitesse >CHARGEUR_MAX_SPEED:
            self.vitesse=CHARGEUR_MAX_SPEED
        if self.vitesse<CHARGEUR_MIN_SPEED:
            self.vitesse=CHARGEUR_MIN_SPEED
        #on effectue enfin le mouvement
        self.x += self.vitesse * (cos(radians(self.rotation)))
        self.y += self.vitesse * (sin(radians(self.rotation)))
        self.colisions()

    def death_anim(self):
        self.explosion_anim.update()
        self.explosion_anim.angle = 270-self.rotation
        self.explosion_anim.show = True
        self.image = self.explosion_anim.image

class Tourelle(Ennemi):
    def __init__(self, x, y, WINDOW,rect,shield=False):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Designs - Base/Nautolan Ship - Turret - Base.png",True,True,(32,32))
        self.rotation = 0
        self.clock=randint(round(VARIABLES["TOURELLE_INITIAL_CLOCK"][0]),round(VARIABLES["TOURELLE_INITIAL_CLOCK"][1]))
        self.score_value = TOURELLE_SCORE

        self.base_image = pygame.transform.scale(self.base_image, (80, 80))

        #sheild:
        self.shield=shield
        self.shield_anim=Anim(self.x,self.y,9,(80,80),50,"image/Nautolan/Shields/Nautolan Ship - Bomber - Shield - Copie.png",False)

        self.hitbox.center = (self.x,self.y)

        #pour l'animation de mort:
        self.explosion_anim = Anim(self.x, self.y, 8, (64, 64), 50,
                                   "image/Nautolan/Destruction/Nautolan Ship - Bomber.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)

    def draw(self):
        if self.shield:
            self.shield_anim.show=True
        else:
            self.shield_anim.show=False
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, 270 - self.rotation, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        self.killbox.center = self.image_rect.center
        self.shield_anim.angle= 270 - self.rotation
        self.shield_anim.update()
        self.window.blit(self.shield_anim.image, self.image_rect)

    def move(self,x,y,liste):
        self.rotation=rotate(self.x,self.y,x,y)
        if self.clock<1 and not passe_par_milieu(self.x,self.y,x,y,20) :
            if (VARIABLES["TOURELLE_TIR"]=="rocket"):
                liste.append(Rocket(self.x,self.y, self.window, self.centre,self.rotation))
            else:
                liste.append(Tir(self.x,self.y, self.window, self.centre,self.rotation))
            self.clock=randint(round(VARIABLES["TOURELLE_NEW_CLOCK"][0]),round(VARIABLES["TOURELLE_NEW_CLOCK"][1]))
        self.clock+=-1
        return liste

    def death_anim(self):
        self.explosion_anim.update()
        self.explosion_anim.angle = self.rotation
        self.explosion_anim.show = True
        self.image = self.explosion_anim.image

class Miner(Ennemi):
    def __init__(self, x, y, WINDOW, rect):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Designs - Base/Nautolan Ship - Support - Base.png",False,True)
        self.rotation = randint(0,360)
        self.mines=MINER_MINES
        self.vitesse=0
        self.objectifx=0
        self.objectify=0
        self.destination()
        self.clock=randint(MINER_CLOCK[0],MINER_CLOCK[1])
        self.score_value = MINER_SCORE

        self.base_image = pygame.transform.scale(self.base_image, (80, 80))

        #pour l'animation de mort:
        self.explosion_anim = Anim(self.x, self.y, 8, (64, 64), 50,
                                   "image/Nautolan/Destruction/Nautolan Ship - Support.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)

    def draw(self):
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, 90 - self.rotation, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        self.killbox.center = self.image_rect.center

    def destination(self):
        self.objectifx=randint(40, SIZE[0] - 40)
        self.objectify=randint(40, SIZE[1] - 40)
        i=0
        while passe_par_milieu(self.x,self.y,self.objectifx,self.objectify,20) and i<10:
            self.objectifx=randint(40, SIZE[0] - 40)
            self.objectify=randint(40, SIZE[1] - 40)
            i+=1
        if i==10:
            if self.x<SIZE[0] - 40:
                self.objectifx=self.x+10
            elif self.x>40:
                self.objectifx=self.x-10


    def move(self,liste):
        if abs(self.x-self.objectifx)<10 and abs(self.y-self.objectify)<10:
            self.destination()
            self.clock-=10
        if self.mines>0:
            if self.clock<1:
                liste.append(Mine(self.x-20*(cos(radians(self.rotation))),self.y-20*(sin(radians(self.rotation))), self.window, self.centre))
                self.mines-=1
                self.clock=randint(MINER_CLOCK[0],MINER_CLOCK[1])
        self.clock+=-1
        self.rotation = modulo_rot(self.rotation)
        self.x += self.vitesse * (cos(radians(self.rotation)))
        self.y += self.vitesse * (sin(radians(self.rotation)))
        objectif = modulo_rot(rotate(self.x, self.y, self.objectifx, self.objectify))
        calcul = modulo_rot(objectif - self.rotation)
        if calcul < 10 or calcul > 350:
            self.vitesse += 0.1
        else:
            self.vitesse=0
        if self.vitesse>MINER_SPEED:
            self.vitesse=MINER_SPEED
        if calcul > 0 and calcul < 180:
            self.rotation += +2
        else:
            self.rotation += -2
        return liste

    def death_anim(self):
        self.explosion_anim.update()
        self.explosion_anim.angle = self.rotation
        self.explosion_anim.show = True
        self.image = self.explosion_anim.image

class Rocketship(Ennemi):
    def __init__(self, x, y, WINDOW,rect):
        super().__init__(x, y, WINDOW, rect, "image/Nautolan/Designs - Base/Nautolan Ship - Torpedo Ship.png",True,True)
        self.rotation = 0
        self.vitesse=0
        self.objectif=(x,y)
        self.clock=randint(ROCKETSHIP_INITIAL_CLOCK[0],ROCKETSHIP_INITIAL_CLOCK[1])
        self.score_value = ROCKETSHIP_SCORE

        #pour l'animation de mort:
        self.explosion_anim = Anim(self.x, self.y, 8, (64, 64), 50,
                                   "image/Nautolan/Destruction/Nautolan Ship - Support.png", True)
        self.anim_group = pygame.sprite.Group(self.explosion_anim)
    def draw(self):
        self.window.blit(self.image, self.image_rect)
        self.image = pygame.transform.rotozoom(self.base_image, 270 - self.rotation, 1)
        self.image_rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.image_rect.center
        self.killbox.center = self.image_rect.center

    def colisions(self):
        if super().colmurhor() and super().colmurver():
            self.rotation = -self.rotation-90
            if self.y<SIZE[1]//2:
                self.y+=-5
            else:
                self.y+=+5
            if self.x<SIZE[0]//2:
                self.x+=-5
            else:
                self.x+=+5
        if super().colver():
            self.rotation = -self.rotation
        if super().colmurver():
            self.rotation = -self.rotation
            if self.y<SIZE[1]//2:
                self.y+=-5
            else:
                self.y+=+5
        if super().colhor():
            self.rotation = self.rotation + 90
        if super().colmurhor():
            self.rotation = self.rotation + 90
            if self.x<SIZE[0]//2:
                self.x+=-5
            else:
                self.x+=+5

    def choix_objectif(self,x,y):
        if not passe_par_milieu(self.x,self.y,x,y,40):#si on a une ligne de vue directe sur le joueur:
            self.objectif=(self.x,self.y)#on bouge pas
        else :#si on ne peut pas acceder au joueur:
            if self.x<SIZE[0]//2+SIZE[0]//6 and self.x>SIZE[0]//2-SIZE[0]//6 and x<SIZE[0]//2+SIZE[0]//6 and x>SIZE[0]//2+-SIZE[0]//6: # le joueur et l'ennemi sont a l'opposé du rect:
                if self.x<SIZE[0]//2:#on sort de ce coté du rect, en passant par le plus proche
                    self.objectif=(self.x-10, self.y)
                else:
                    self.objectif=(self.x+10, self.y)
            elif self.y<SIZE[1]//2+SIZE[1]//6 and self.y>SIZE[1]//2-SIZE[1]//6 and y<SIZE[1]//2+SIZE[1]//6 and y>SIZE[1]//2-SIZE[1]//6: # le joueur et l'ennemi sont a l'opposé du rect:
                if self.y<SIZE[1]//2:#on sort de ce coté du rect, en passant par le plus proche
                    self.objectif=(self.x, self.y-10)
                else:
                    self.objectif=(self.x, self.y+10)
            elif not passe_par_milieu(self.x,self.y,self.x,y) and not passe_par_milieu(self.x,self.y,x,self.y):#si on à accés aux deux points :
                if not passe_par_milieu(x,y,self.x,y):#on prends celui des deux qui donne accés au joueur
                    self.objectif=(self.x,y)
                else:
                    self.objectif=(x,self.y)
            elif not passe_par_milieu(self.x,self.y,self.x,y):#sinon, si on peut, on se mets de façon a partager le x ou le y du joueur
                self.objectif=(self.x,y)
            elif not passe_par_milieu(self.x,self.y,x,self.y):
                self.objectif=(x,self.y)

    def move(self, x, y,liste,particules=[]):
        self.clock+=-1
        if not passe_par_milieu(self.x,self.y,x,y,40):#si on a une ligne de vue directe sur le joueur:
            self.objectif=(x,y)
            self.rotation = modulo_rot(self.rotation)
            objectif = modulo_rot(rotate(self.x, self.y, self.objectif[0],self.objectif[1]))
            calcul_dirrection = modulo_rot(objectif - self.rotation)
            #pour tourner dans le bon sens:
            if calcul_dirrection > 0 and calcul_dirrection < 180:
                self.rotation += +ROCKETSHIP_ROTATION_SPEED
            else:
                self.rotation += -ROCKETSHIP_ROTATION_SPEED
            #puis on tire
            if self.clock<1 and (calcul_dirrection < ROCKETSHIP_ANGLE_ACCELERATION or calcul_dirrection > 360-ROCKETSHIP_ANGLE_ACCELERATION):
                self.clock=randint(ROCKETSHIP_NEW_CLOCK[0],ROCKETSHIP_NEW_CLOCK[1])
                for i in range(ROCKETSHIP_NB_TIRS):
                    liste.append(Rocket(self.x,self.y, self.window, self.centre,self.rotation+(360/ROCKETSHIP_NB_TIRS)*i))
        else :
            self.choix_objectif(x,y)
            self.rotation = modulo_rot(self.rotation)
            objectif = modulo_rot(rotate(self.x, self.y, self.objectif[0],self.objectif[1]))
            calcul_dirrection = modulo_rot(objectif - self.rotation)
            #pour tourner dans le bon sens:
            if calcul_dirrection > 0 and calcul_dirrection < 180:
                self.rotation += +ROCKETSHIP_ROTATION_SPEED
            else:
                self.rotation += -ROCKETSHIP_ROTATION_SPEED
            #pour accelerer si l'objectif est en vue et ralentir sinon:
            if calcul_dirrection < ROCKETSHIP_ANGLE_ACCELERATION or calcul_dirrection > 360-ROCKETSHIP_ANGLE_ACCELERATION:
                self.vitesse +=ROCKETSHIP_ACCELERATION
            else:
                self.vitesse +=-ROCKETSHIP_DECELERATION
            #on limite la vitesse
            if self.vitesse >ROCKETSHIP_MAX_SPEED:
                self.vitesse=ROCKETSHIP_MAX_SPEED
            if self.vitesse<ROCKETSHIP_MIN_SPEED:
                self.vitesse=ROCKETSHIP_MIN_SPEED
            #on effectue enfin le mouvement
            self.x += self.vitesse * (cos(radians(self.rotation)))
            self.y += self.vitesse * (sin(radians(self.rotation)))
            self.colisions()
        return liste

    def death_anim(self):
        self.explosion_anim.update()
        self.explosion_anim.angle = self.rotation
        self.explosion_anim.show = True
        self.image = self.explosion_anim.image