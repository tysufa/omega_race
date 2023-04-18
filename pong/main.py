import pygame
from time import time

pygame.init()

window = pygame.display.set_mode((720, 480))

continuer = True

size_raquette = [15, 60]
raquette1 = pygame.rect.Rect((30, 30), size_raquette)
raquette2 = pygame.rect.Rect((720 - 30, 30), size_raquette)
ball = pygame.rect.Rect((100, 100, 37, 37))
chad = pygame.image.load("chad(1).png")
nerdge = pygame.image.load("nerdge-removebg-preview.png")
ball_vx = 7
ball_vy = 7



# création d'une font
font = pygame.font.Font(None, 100)

# création du texte
text1 = "LLL"
text = font.render(text1, True, "red")
text_rect = text.get_rect(center=(720//2-200, 480//2))
affiche_text = False

#pygame.mixer.Channel(0).play(pygame.mixer.music.load("chad.mp3"))
#pygame.mixer.Channel(1).play(pygame.mixer.Sound("L.mp3"))

pygame.mixer.music.load("chad.mp3")
t = pygame.mixer.Sound("L.mp3")
pygame.mixer.music.play()
pygame.mixer.music.set_volume(1)
pygame.mixer.music.play(10)
v_raquette = 3

clock = pygame.time.Clock()

while continuer:
    text = font.render(text1, True, "red")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        if raquette1.bottom < 480:
            raquette1.y += v_raquette
    if keys[pygame.K_UP]:
        if raquette1.top > 0:
            raquette1.y -= v_raquette
    if keys[pygame.K_s]:
        if raquette2.bottom < 480:
            raquette2.y += v_raquette
    if keys[pygame.K_z]:
        if raquette2.top > 0:
            raquette2.y -= v_raquette



    if ball.x < 15 or ball.x > 720 - 30:
        pygame.mixer.music.pause()
        affiche_text = True
        text1 += "LL"
        t.play(100)
        ball_vx = -ball_vx
        ball.center = (720//2, 480//2)
        v_raquette *= 2
        ball_vy *= 2
        ball_vx *= 2
        size_raquette[1] *= 1.5
        size_raquette[1] *= 1.5
        raquette1 = pygame.rect.Rect((30, 30), size_raquette)
        raquette2 = pygame.rect.Rect((720 - 30, 30), size_raquette)

    if ball.y < 15 or ball.y > 480 - 30:
        ball_vy = -ball_vy

    if abs(ball.bottom - raquette1.top) < 10 and abs(30 - ball.x) < 10:
        ball_vy = -ball_vy

    if abs(ball.bottom - raquette2.top) < 10 and abs(720 - 30 - ball.x) < 10:
        ball_vy = -ball_vy

    if abs(ball.top - raquette1.bottom) < 10 and abs(30 - ball.x) < 10:
        ball_vy = -ball_vy

    if abs(ball.bottom - raquette2.top) < 10 and abs(720 - 30 - ball.x) < 10:
        ball_vy = -ball_vy

    if ball.colliderect(raquette1):
        ball_vx = -ball_vx
    if ball.colliderect(raquette2):
        ball_vx = -ball_vx

    ball.x += ball_vx
    ball.y += ball_vy

    window.blit(chad, (0, 0))
    pygame.draw.rect(window, "white", raquette1)
    pygame.draw.rect(window, "white", raquette2)
    pygame.draw.circle(window, "white", ball.center, 15)
    window.blit(nerdge, ball)
    if affiche_text:
        window.blit(text, text_rect)
        pygame.mixer.music.set_volume(1)

    pygame.display.flip()

    clock.tick(60)
