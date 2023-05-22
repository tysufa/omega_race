import pygame
from math import sin, cos, radians, degrees, asin, acos
from constantes import *
from animation import Anim


class Projectiles(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, window, rocket=False):
        super().__init__()
        self.x, self.y = x, y
        self.x_init, self.y_init = x, y
        self.direction = direction%360
        self.rocket = rocket
        self.window = window
        if not rocket:
            self.bullet_anim = Anim(self.x, self.y, 3, (8, 16), 50,
                                    BULLET_SPRITESHEET, True)
        else:
            self.bullet_anim = Anim(self.x, self.y, 5, (16, 32), 50,
                                    "image/Nautolan/Weapon Effects - Projectiles/Nautolan - Rocket.png", True)

        self.image = self.bullet_anim.image


        self.bullet_anim.angle = self.direction-90 # l'angle de la balle est dans la direction du joueur -90 degrées pour la tourner vers la droite comme le joueur au début de la partie


        self.hitbox = pygame.rect.Rect((self.x, self.y), (10, 10))
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.velocity = [cos(radians(self.direction)) * BULLET_SPEED, sin(radians(self.direction)) * BULLET_SPEED]

    def update(self, ennemis):
        if self.rocket:
            self.get_direction(ennemis)
            self.velocity[1] = cos(radians(self.bullet_anim.angle)) * BULLET_SPEED
            self.velocity[0] = -sin(radians(self.bullet_anim.angle)) * BULLET_SPEED


        self.bullet_anim.show = True # on veut être sur d'afficher l'animation même une fois fini

        self.bullet_anim.update() # on update l'animation du tir

        self.image = self.bullet_anim.image # l'image actuelle du tir devient l'image de l'animation en cours

        self.x += self.velocity[0] # on update la position x et y en fonction de la vélocité
        self.y -= self.velocity[1]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.hitbox.center = self.rect.center

    def rotation(self, xa, ya, xb, yb):
        """
        renvoie en degrés la rotation nescaissaire a l'objet (xa,ya) pour être tourné vers (xb,yb)
        """
        ret = degrees(acos((xb - xa) / ((xb - xa) ** 2 + (yb - ya) ** 2) ** (1 / 2)))
        if asin((yb - ya) / ((xb - xa) ** 2 + (yb - ya) ** 2) ** (1 / 2)) < 0:
            ret = -ret
        return ret

    def get_direction(self, ennemis):
        self.direction = self.direction%360
        angle_min = 180 # si l'angle minimum est supérieur au champs de vision on ira tout droit

        center_square = pygame.rect.Rect((0, 0, SIZE[0] // 3, SIZE[1] // 3))
        angle_min = self.rotation(self.hitbox.x, self.hitbox.y, ennemis[0].x, ennemis[0].y)
        pos = ennemis[0].x, ennemis[0].y


        #print(angle_min-self.direction%180, self.direction%180)

        # angle1 correspond à l'écart en angle entre le vaisseau et le point (100, 100) compris entre 0 et 180°
        #angle1 = 180 - abs(180-abs(abs(self.rotation(self.x, self.y, 100, 100))-self.direction))

        # angle2 = 180 - abs(180-abs(abs(self.rotation(self.x, self.y, 600, 100))-self.direction))

        if angle_min < 70 and False: # si l'ennemi est dans le "champ de vision"

            # pos = pygame.mouse.get_pos()
            pygame.draw.line(self.window, "orange", (self.x, self.y), (pos[0], pos[1]))

            self.bullet_anim.angle = self.bullet_anim.angle%360

            objectif = self.rotation(self.x, self.y, pos[0],pos[1])%360

            calcul_dirrection = (objectif + self.bullet_anim.angle)%360-90


            if calcul_dirrection > 0 and calcul_dirrection < 180:
                self.bullet_anim.angle += 3
                self.direction += 3
            else:
                self.bullet_anim.angle -= 3
                self.direction -= 3
