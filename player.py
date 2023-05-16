import random

import pygame
from math import cos, sin, radians
from projectiles import Projectiles
from constantes import *
from animation import Anim
from particles import create_particle_list

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, rect_centre, ennemis):
        super().__init__()
        self.base_image = pygame.image.load(PLAYER_IMAGE).convert_alpha()
        # on tourne l'image vers la droite
        self.base_image = pygame.transform.rotozoom(self.base_image, -90, 1)
        self.image = self.base_image
        self.ennemis = ennemis

        self.explosion_sound = pygame.mixer.Sound("sound/explosion.wav")
        self.shooting_sound = pygame.mixer.Sound("sound/shooting.wav")
        self.bouncing_sound = pygame.mixer.Sound("sound/bouncing.wav")
        self.dissapearing_sound = pygame.mixer.Sound("sound/laser_dissapearing.wav")
        self.shooting_sound.set_volume(0.15)
        self.explosion_sound.set_volume(0.3)
        self.bouncing_sound.set_volume(1)
        self.dissapearing_sound.set_volume(0.05)

        self.x = x
        self.y = y
        # le rectangle du milieu pour les collisions
        self.rect_centre = rect_centre

        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = PLAYER_SPEED
        # la perte de vitesse lorsqu'on rebondit
        self.velocity_lost = VELOCITY_LOST
        self.max_velocity = MAX_PLAYER_SPEED
        self.angle = 0

        self.rect = self.image.get_rect(center=(self.x, self.y))  # pour l'affichage et la position de l'img

        self.hitbox = pygame.rect.Rect((self.x, self.y), HITBOX_SIZE)  # pour une taille de hitbox constante

        self.alive = True
        self.nb_life = LIFE_NB
        self.respawn = False

        self.engine_anim = Anim(self.x, self.y, 11, (64, 64), 50,
                                "image/Kla'ed/Engine/Kla'ed - Frigate - Engine.png", False)
        self.explosion_anim = Anim(self.x, self.y, 8, (64, 64), 50,
                                   "image/Kla'ed/Destruction/Kla'ed - Frigate - Destruction.png", True)

        self.player_anim = pygame.sprite.Group(self.engine_anim,
                                               self.explosion_anim)  # on créer un groupe contenant les animations du joueur

        self.projectiles = pygame.sprite.Group()  # le groupe qui contiendra les projectiles à l'écran du joueur
        self.reloading = False  # sert à tester si on peut tirer à nouveau ou non

        self.rect_ecran = pygame.rect.Rect((WALL_DISTANCE, WALL_DISTANCE), (
            SIZE[0] - WALL_DISTANCE * 2,
            SIZE[1] - WALL_DISTANCE * 2))  # on créer un rectangle qui prend toute la fenetre

        self.particles = []

    def dispawn_projectile(self, projectile):
        self.particles = create_particle_list(15, projectile.rect.x, projectile.rect.y, random.randint(6, 8), 2, 2, 0.3, 0.5)
        projectile.remove(self.projectiles)
        self.dissapearing_sound.play()

    def rotate(self, direction):
        if direction == "R":  # si on veut tourner vers la droite
            self.angle -= ROTATION_SPEED
        elif direction == "L":
            self.angle += ROTATION_SPEED

        # rotozoom à une meilleur qualité que rotate
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.rect.center  # on replace la hitbox

    def die(self):
        self.nb_life -= 1
        self.alive = False
        self.explosion_anim.show = True
        self.engine_anim.show = False
        self.death_timer = pygame.time.get_ticks()
        self.explosion_sound.play()

    def respawn_function(self):
        self.x = random.randint(WALL_DISTANCE, SIZE[0] - WALL_DISTANCE)  # même si l'on touche le mur on sera téléporté à l'intérieur de la fenetre de jeu
        self.y = random.randint(WALL_DISTANCE, SIZE[1] - WALL_DISTANCE)
        self.hitbox.center = self.x, self.y
        while self.hitbox.colliderect(self.rect_centre): # on ne veut pas respawn dans le rectangle au centre
            self.x = random.randint(WALL_DISTANCE, SIZE[0]-WALL_DISTANCE)
            self.y = random.randint(WALL_DISTANCE, SIZE[1]-WALL_DISTANCE)
            self.hitbox.center = self.x, self.y

        self.velocity.x = 0
        self.velocity.y = 0
        self.respawn = True

    def move(self):
        angle_x = cos(radians(self.angle))
        angle_y = sin(radians(self.angle))
        # la prochaine velocité
        new_velocity_x = (self.velocity.x + cos(radians(self.angle)))
        new_velocity_y = (self.velocity.y + sin(radians(self.angle)))

        # on change la vélicité que si elle ne dépasse pas le maximum
        if angle_x < 0:
            if new_velocity_x > self.max_velocity * angle_x:
                self.velocity.x = new_velocity_x
        else:
            if new_velocity_x < self.max_velocity * angle_x:
                self.velocity.x = new_velocity_x

        if angle_y < 0:
            if new_velocity_y > self.max_velocity * angle_y:
                self.velocity.y = new_velocity_y
        else:
            if new_velocity_y < self.max_velocity * angle_y:
                self.velocity.y = new_velocity_y

    def update(self, window):

        if self.reloading:  # si on est en train de "recharger" :
            if pygame.time.get_ticks() - self.time > FIRE_RATE:  # si on à dépassé le temps de recharge
                self.reloading = False  # on peut à nouveau tirer

        keys = pygame.key.get_pressed()  # on récupère la liste des touches appuyées

        for anim in self.player_anim.sprites():  # on parcours toutes les animations du joueur
            if not anim.stay:  # si on ne doit pas laisser cette animation jusqu'à la fin :
                anim.show = False  # on cache l'animation

        if self.alive:
            if keys[pygame.K_UP]:
                self.move()  # on se déplace
                self.engine_anim.show = True  # on veut afficher l'animation des réacteurs

            if keys[pygame.K_z]:
                if not self.reloading:
                    self.projectiles.add(Projectiles(self.x, self.y, self.angle, window))  # on ajoute un nouveau projectile
                    self.shooting_sound.play()
                    self.reloading = True  # on passe en rechargement
                    self.time = pygame.time.get_ticks()

            if keys[pygame.K_RIGHT]:
                self.rotate("R")
                for anim in self.player_anim.sprites():
                    anim.rotate("R")  # on fait tourner chaque sprite du vaisseau vers la droite

            if keys[pygame.K_LEFT]:
                self.rotate("L")
                for anim in self.player_anim.sprites():
                    anim.rotate("L")

            if keys[pygame.K_DOWN]:
                self.velocity.x = 0
                self.velocity.y = 0

            if keys[pygame.K_a]:
                if not self.reloading:
                    self.projectiles.add(Projectiles(self.x, self.y, self.angle, window, True))  # on ajoute un nouveau projectile
                    self.shooting_sound.play()
                    self.reloading = True  # on passe en rechargement
                    self.time = pygame.time.get_ticks()

            # on update les coordonnées
            self.x += self.velocity.x * self.speed
            self.y -= self.velocity.y * self.speed

        else:
            if pygame.time.get_ticks() - self.death_timer > RESPAWN_TIME:
                self.x = random.randint(WALL_DISTANCE, SIZE[
                    0] - WALL_DISTANCE)  # même si l'on touche le mur on sera téléporté à l'intérieur de la fenetre de jeu
                self.y = random.randint(WALL_DISTANCE, SIZE[1] - WALL_DISTANCE)
                self.hitbox.center = self.x, self.y
                while self.hitbox.colliderect(self.rect_centre):  # on ne veut pas respawn dans le rectangle au centre
                    self.x = random.randint(WALL_DISTANCE, SIZE[0] - WALL_DISTANCE)
                    self.y = random.randint(WALL_DISTANCE, SIZE[1] - WALL_DISTANCE)
                    self.hitbox.center = self.x, self.y

                self.velocity.x = 0
                self.velocity.y = 0
                self.respawn = True
            if pygame.time.get_ticks() - self.death_timer >= RESPAWN_TIME:
                self.respawn_function()

        self.player_anim.update()

        # on check les collisions
        self.collision_bord()
        self.collision_centre()

        # on update les positions de rect et hitbox
        self.rect.center = (self.x, self.y)
        self.hitbox.center = (self.x, self.y)

        for anim in self.player_anim.sprites():
            anim.rect.center = (self.x, self.y)  # on change la position de chaque animation

        self.projectiles.update(self.ennemis)

    def collision_bord(self):
        for projectile in self.projectiles.sprites():
            if projectile.rect.top < WALL_DISTANCE:
                self.dispawn_projectile(projectile)

            elif projectile.rect.bottom > SIZE[1] - WALL_DISTANCE:
                self.dispawn_projectile(projectile)

            if projectile.rect.right > SIZE[0]:
                self.dispawn_projectile(projectile)

            elif projectile.rect.left < WALL_DISTANCE:
                self.dispawn_projectile(projectile)




        bounced = False

        # si le haut du vaisseau dépasse le haut de l'écran
        if self.hitbox.top < WALL_DISTANCE:
            self.hitbox.top = WALL_DISTANCE + 1  # on se replace 1 pixel en dessous
            self.y = self.hitbox.center[1]  # on update aussi la coordonnée y car on a seulement modifié hitbox
            self.velocity.y *= -self.velocity_lost  # on inverse la direction pour rebondir et on perd de la vitesse
            bounced = True

        if self.hitbox.bottom > SIZE[1] - WALL_DISTANCE:
            self.hitbox.bottom = SIZE[1] - WALL_DISTANCE - 1
            self.y = self.hitbox.center[1]
            self.velocity.y *= -self.velocity_lost
            bounced = True

        if self.hitbox.left < WALL_DISTANCE:
            self.hitbox.left = WALL_DISTANCE + 1
            self.x = self.hitbox.center[0]
            self.velocity.x *= -self.velocity_lost
            bounced = True

        if self.hitbox.right > SIZE[0] - WALL_DISTANCE:
            self.hitbox.right = SIZE[0] - WALL_DISTANCE - 1
            self.x = self.hitbox.center[0]
            self.velocity.x *= -self.velocity_lost
            bounced = True

        if bounced:
            self.bouncing_sound.play()

    def collision_centre(self):
        for projectile in self.projectiles.sprites():
            # on fais dispawn les projectiles qui passent par le centre
            if projectile.rect.colliderect(self.rect_centre):
                self.dispawn_projectile(projectile)

        if self.hitbox.colliderect(self.rect_centre):  # si on a une collision avec le rectangle du milieu
            self.bouncing_sound.play()
            # si l'écart entre le haut du vaisseau et le bas du rectangle est suffisament faible
            if abs(self.hitbox.top - self.rect_centre.bottom) <= self.max_velocity * self.speed + 1:
                self.hitbox.top = self.rect_centre.bottom + 1  # on replace le vaisseau
                self.y = self.hitbox.center[1]
                self.velocity.y *= -self.velocity_lost

            elif abs(self.hitbox.bottom - self.rect_centre.top) <= self.max_velocity * self.speed + 1:
                self.hitbox.bottom = self.rect_centre.top - 1
                self.y = self.hitbox.center[1]
                self.velocity.y *= -self.velocity_lost

            elif abs(self.hitbox.right - self.rect_centre.left) <= self.max_velocity * self.speed + 1:
                self.hitbox.right = self.rect_centre.left - 1
                self.x = self.hitbox.center[0]
                self.velocity.x *= -self.velocity_lost

            elif abs(self.hitbox.left - self.rect_centre.right) <= self.max_velocity * self.speed + 1:
                self.hitbox.left = self.rect_centre.right + 1
                self.x = self.hitbox.center[0]
                self.velocity.x *= -self.velocity_lost
