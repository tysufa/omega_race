import pygame

pygame.init()

W_SIZE = 720
H_SIZE = 480

window = pygame.display.set_mode((W_SIZE, H_SIZE))
pygame.display.set_caption("menu")

rect1 = pygame.rect.Rect((0, 0, 100, 100))

# création d'une font
font = pygame.font.Font(None, 32)

# création du texte
text = font.render('Test', True, "blue", "green")
text_rect = text.get_rect(center=(100, 100))


continuer = True

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    rect1.center = (720//2, 480//2)
    window.blit(text, text_rect)
    pygame.display.flip()

