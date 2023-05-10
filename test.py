import pygame
import random

pygame.init()

window = pygame.display.set_mode((720, 480))

bg = pygame.image.load("image/background/Space Background.png")
circle = pygame.image.load("circle.png")
player = pygame.image.load("player.png")
circle = pygame.transform.scale(circle, (200, 200))

continuer = True

clock = pygame.time.Clock()


def circle_surf(color, radius):
    surf = pygame.surface.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey("black")
    return surf


while continuer:

    window.blit(bg, (0,0))
    window.fill((0, 0, 0), special_flags=pygame.BLEND_RGB_SUB)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    pos = pygame.mouse.get_pos()
    r = 15 * 4
    window.blit(player, (pos[0]-40, pos[1]-40))
    # window.blit(circle_surf((100, 100, 100), r), (pos[0] - r, pos[1] - r), special_flags=pygame.BLEND_RGB_ADD)
    # window.blit(circle_surf((50, 50, 50), r*3), (pos[0] - r*3, pos[1] - r*3), special_flags=pygame.BLEND_RGB_ADD)

    window.blit(circle, (pos[0]-100, pos[1]-100), special_flags=pygame.BLEND_RGB_ADD)

    pygame.display.flip()

    clock.tick(60)
