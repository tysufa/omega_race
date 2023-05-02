import pygame
from math import cos, sin, radians

pygame.init()


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, rect_centre, walls):
        super().__init__()
        self.base_image = pygame.image.load(
            "image/Kla'ed/Base/Kla'ed - Frigate - Base.png")
        # on tourne l'image vers la droite
        self.base_image = pygame.transform.rotozoom(self.base_image, -90, 1)
        self.image = self.base_image

        self.x = x
        self.y = y
        self.size = size
        # le rectangle du milieu pour les collisions
        self.rect_centre = rect_centre

        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0.2
        # la perte de vitesse lorsqu'on rebondit
        self.velocity_lost = 0.6
        self.max_velocity = 15
        self.angle = 0

        self.wall_distance = 20

        self.rect = self.image.get_rect(center=(self.x, self.y))  # pour l'affichage et la position de l'img

        self.taille_hitbox = (44, 44)
        self.hitbox = pygame.rect.Rect((self.x, self.y), self.taille_hitbox)  # pour une taille de hitbox constante

        self.alive = True

        self.anim1 = PlayerAnim(self.x, self.y, 11, 64, 50,
                                "image/Kla'ed/Engine/Kla'ed - Frigate - Engine.png", False)
        self.anim2 = PlayerAnim(self.x, self.y, 39, 64, 50,
                                "image/Kla'ed/Shield/Kla'ed - Frigate - Shield.png", True)
        self.anim3 = PlayerAnim(self.x, self.y, 8, 64, 50,
                                "image/Kla'ed/Destruction/Kla'ed - Frigate - Destruction.png", True)

        self.player_anim = pygame.sprite.Group()
        self.player_anim.add(self.anim1)
        self.player_anim.add(self.anim2)
        self.player_anim.add(self.anim3)

    def rotate(self, direction):
        if direction == "R":  # si on veut tourner vers la droite
            self.angle -= 5
        elif direction == "L":
            self.angle += 5

        # rotozoom à une meilleur qualité que rotate
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)
        self.rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle
        self.hitbox.center = self.rect.center  # on replace la hitbox

    def move(self):
        # la prochaine velocité
        new_velocity_x = (self.velocity.x + cos(radians(self.angle)))
        new_velocity_y = (self.velocity.y + sin(radians(self.angle)))

        # on change la vélicité que si elle ne dépasse pas le maximum
        if abs(new_velocity_x) < self.max_velocity:
            self.velocity.x = new_velocity_x
        if abs(new_velocity_y) < self.max_velocity:
            self.velocity.y = new_velocity_y

    def update(self):

        keys = pygame.key.get_pressed()  # on récupère la liste des touches appuyées

        for sprite in self.player_anim.sprites():
            if not sprite.stay:
                sprite.show = False  # on cache tous les sprites

        if keys[pygame.K_UP]:
            self.move()
            self.anim1.show = True  # on veut afficher l'animation des réacteurs

        if keys[pygame.K_z]:
            self.anim2.show = True  # on affiche l'animation du bouclier

        if keys[pygame.K_SPACE]:
            self.alive = False
            self.anim3.show = True

        if keys[pygame.K_RIGHT]:
            self.rotate("R")
            for sprite in self.player_anim.sprites():
                sprite.rotate("R")  # on fait tourner chaque sprite du vaisseau vers la droite

        if keys[pygame.K_LEFT]:
            self.rotate("L")
            for sprite in self.player_anim.sprites():
                sprite.rotate("L")

        # on update les coordonnées
        self.x += self.velocity.x * self.speed
        self.y -= self.velocity.y * self.speed

        self.player_anim.update()  # on update chaque sprite d'animation du joueur

        for sprite in self.player_anim.sprites():
            sprite.rect.center = (self.x, self.y)  # on change la position de chaque animation

        # on check les collisions
        self.collision_bord()
        self.collision_centre()

        # on update les positions de rect et hitbox
        self.rect.center = (self.x, self.y)
        self.hitbox.center = (self.x, self.y)


    def collision_bord(self):
        # si le haut du vaisseau dépasse le haut de l'écran
        if self.hitbox.top < self.wall_distance:
            self.hitbox.top = self.wall_distance + 1  # on se replace 1 pixel en dessous
            self.y = self.hitbox.center[1]  # on update aussi la coordonnée y car on a seulement modifié hitbox
            self.velocity.y *= -self.velocity_lost  # on inverse la direction pour rebondir et on perd de la vitesse

        if self.hitbox.bottom > self.size[1]-self.wall_distance:
            self.hitbox.bottom = self.size[1] - self.wall_distance - 1
            self.y = self.hitbox.center[1]
            self.velocity.y *= -self.velocity_lost

        if self.hitbox.left < self.wall_distance:
            self.hitbox.left = self.wall_distance + 1
            self.x = self.hitbox.center[0]
            self.velocity.x *= -self.velocity_lost

        if self.hitbox.right > self.size[0]-self.wall_distance:
            self.hitbox.right = self.size[0] - self.wall_distance - 1
            self.x = self.hitbox.center[0]
            self.velocity.x *= -self.velocity_lost

    def collision_centre(self):
        if self.hitbox.colliderect(self.rect_centre):  # si on a une collision avec le rectangle du milieu
            # si l'écart entre le haut du vaisseau et le bas du rectangle est suffisament faible
            if abs(self.hitbox.top - self.rect_centre.bottom) <= self.max_velocity * self.speed + 1:
                self.hitbox.top = self.rect_centre.bottom + 1  # on replace le vaisseau
                self.y = self.hitbox.center[1]
                self.velocity.y *= -self.velocity_lost

            if abs(self.hitbox.bottom - self.rect_centre.top) <= self.max_velocity * self.speed + 1:
                self.hitbox.bottom = self.rect_centre.top - 1
                self.y = self.hitbox.center[1]
                self.velocity.y *= -self.velocity_lost

            if abs(self.hitbox.right - self.rect_centre.left) <= self.max_velocity * self.speed + 1:
                self.hitbox.right = self.rect_centre.left - 1
                self.x = self.hitbox.center[0]
                self.velocity.x *= -self.velocity_lost

            if abs(self.hitbox.left - self.rect_centre.right) <= self.max_velocity * self.speed + 1:
                self.hitbox.left = self.rect_centre.right + 1
                self.x = self.hitbox.center[0]
                self.velocity.x *= -self.velocity_lost


class PlayerAnim(pygame.sprite.Sprite):
    def __init__(self, x, y, frame_number, frame_size, frames_delay, image_path, stay):
        super().__init__()

        self.frame_number = frame_number
        self.frame_size = frame_size
        self.frames_delay = frames_delay
        self.image_path = image_path
        self.x = x
        self.y = y
        self.stay = stay

        # on créer une surface pour contenir notre image
        self.image = pygame.Surface((self.frame_size, self.frame_size)).convert_alpha()

        # on charge l'image qu'on affichera sur notre surface
        self.image_to_blit = pygame.image.load(self.image_path)

        # numéro du sprite à afficher
        self.frame = 0

        # on affiche l'image sur la surface
        self.image.blit(self.image_to_blit, (0, 0), (self.frame * self.frame_size, 0, self.frame_size, self.frame_size))

        # savoir si on affiche le sprite ou non
        self.show = False

        # on commence en tournant l'animation vers la droite comme le joueur
        self.angle = -90

        self.image = pygame.transform.rotate(self.image, self.angle)

        self.base_image = self.image  # l'image que l'on fera tourner pour éviter une perte de qualité de l'image

        self.rect = self.image.get_rect(center=(x, y))

        self.timer = pygame.time.get_ticks()  # le timer pour gérer le timing des animations

    def rotate(self, direction=None):
        if direction == "R":  # si on veut tourner vers la droite
            self.angle -= 5
        elif direction == "L":
            self.angle += 5

        # rotozoom à une meilleur qualité que rotate
        self.image = pygame.transform.rotozoom(self.base_image, self.angle, 1)

        # on enlève le fond noir de self.image en le rendant transparent
        self.image.set_colorkey("black")

        self.rect = self.image.get_rect(center=(self.x, self.y))  # on replace le rectangle

    def update(self):
        if not self.show:
            self.frame = -1  # on n'affiche que du noir

        self.base_image.fill("black")  # on efface l'image précédente
        # on affiche la nouvelle image
        self.base_image.blit(self.image_to_blit, (0, 0), (self.frame * self.frame_size, 0, self.frame_size, self.frame_size))
        self.rotate()  # on update à chaque tour self.image par rapport à self.base_image
        self.image.set_colorkey("black")  # on enlève le fond noir

        if pygame.time.get_ticks() - self.timer > self.frames_delay:  # savoir si on passe au sprite suivant
            self.frame += 1
            self.timer = pygame.time.get_ticks()

        if self.frame > self.frame_number:
            self.frame = 0  # on repasse à la première image
            self.show = False
