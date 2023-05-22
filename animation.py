import pygame


class Anim(pygame.sprite.Sprite):
    def __init__(self, x, y, frame_number, frame_size, frames_delay, image_path, stay):
        super().__init__()

        self.frame_number = frame_number
        self.frame_size = frame_size
        self.frames_delay = frames_delay
        self.image_path = image_path
        self.x = x
        self.y = y
        self.stay = stay # cette variable sert à cacher certaines animations avant d'avoir atteint la dernière image

        # on créer une surface pour contenir notre image
        self.image = pygame.Surface(self.frame_size).convert_alpha()

        # on charge l'image qu'on affichera sur notre surface
        self.image_to_blit = pygame.image.load(self.image_path)

        # numéro du sprite à afficher
        self.frame = 0

        # on affiche l'image sur la surface
        self.image.blit(self.image_to_blit, (0, 0), (self.frame * self.frame_size[0], 0, self.frame_size[0], self.frame_size[1]))

        # savoir si on affiche le sprite ou non
        self.show = False

        # on commence en tournant l'animation vers la droite comme le joueur
        self.angle = -90

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
        if self.show:
            if self.frame == -1: # on passe directement à la première frame pour éviter d'afficher du noir
                self.frame = 0

            if pygame.time.get_ticks() - self.timer > self.frames_delay:  # savoir si on passe au sprite suivant
                self.frame += 1
                self.timer = pygame.time.get_ticks()

            if self.frame > self.frame_number:
                self.frame = -1
                self.show = False # on n'affiche plus l'animation
        else:
            self.frame = -1 # on passe à -1 pour n'afficher que du noir et donc ne rien afficher à l'écran

        self.base_image.fill("black")  # on efface l'image précédente
        # on affiche la nouvelle image
        self.base_image.blit(self.image_to_blit, (0, 0), (self.frame * self.frame_size[0], 0, self.frame_size[0], self.frame_size[1]))
        self.rotate()  # on update à chaque tour self.image par rapport à self.base_image
        self.image.set_colorkey("black")  # on enlève le fond noir

