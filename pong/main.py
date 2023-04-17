import pygame

pygame.init()

window = pygame.display.set_mode((720, 480))

continuer = True

raquette1 = pygame.rect.Rect((30, 30, 15, 120))
raquette2 = pygame.rect.Rect((720-30, 30, 15, 120))
ball = pygame.rect.Rect((100, 100, 30, 30))
ball_vx = 4
ball_vy = 4

clock = pygame.time.Clock()

while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        raquette1.y += 5
    if keys[pygame.K_UP]:
        raquette1.y -= 5
    if keys[pygame.K_z]:
        raquette2.y -= 5
    if keys[pygame.K_s]:
        raquette2.y += 5

    if ball.x < 15 or ball.x > 720-15:
        ball_vx = -ball_vx
    if ball.y < 15 or ball.y > 480-15:
        ball_vy = -ball_vy

    if ball.colliderect(raquette1):
        ball_vx = -ball_vx
    if ball.colliderect(raquette2):
        ball_vx = -ball_vx

    if ball.bottom == raquette2.top or ball.bottom == raquette1.top:
        print("test")

    ball.x += ball_vx
    ball.y += ball_vy

    window.fill("black")
    pygame.draw.rect(window, "white", raquette1)
    pygame.draw.rect(window, "white", raquette2)
    pygame.draw.circle(window, "white", ball.center, 15)
    pygame.draw.rect(window, "white", ball, width=2)

    pygame.display.flip()

    clock.tick(60)
