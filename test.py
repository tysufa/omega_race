import pygame
from pygame.locals import *
from ennemis import *

HAUTEUR_FENETRE = 480
LARGEUR_FENETRE = 640
WINDOW = pygame.display.set_mode( (LARGEUR_FENETRE, HAUTEUR_FENETRE) )

pygame.display.set_caption("Oh mes garce")
pygame.font.init()
fonte = pygame.font.Font(None, 30)
continuer = True
entity=[]#tableau contenant toutes les entités a update (pour l'instant juste des ennemis)
while continuer:
    pygame.time.delay(15)
    tmp=entity.copy()#on copie entity pour pas retirer des éléments de la liste pendant qu'on bosse dessus
    a=0#a=nombre d'entités suprimées du tableau a ce parcours de entity
    for i in range(len(entity)):
        if entity[i].alive:
            entity[i].moove()
            entity[i].draw()
        else :
            tmp.pop(i-a)#comme on retire des éléments, il faut se décaler pour suprimer l'élément qui correspond a entity[i]
            a+=1
    entity=tmp.copy()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                entity.append(bull(pos[0],pos[1],320,240,WINDOW))
                print(len(entity))


    pygame.display.update()
    WINDOW.fill( (0,0,0) )