FONT = "Comic Sans MS"
SIZE = (1080, 720)
WALL_DISTANCE = 10 # écart entre les murs et les bords de l'écran
BACKGROUND_IMAGE = "image/background/Space Background.png"
GAME_FONT = "Comic Sans MS"
GAME_MUSIC = "music/Race to Mars.mp3"
MENU_MUSIC = "music/Checking Manifest.mp3"
TITLE = "Omega Race"

PLAYER_SAFE_SPAWN_ZONE = (600,600)


##### Player #####
MAX_PLAYER_SPEED = 10
PLAYER_SPEED = 0.5
VELOCITY_LOST = 0.5
HITBOX_SIZE = (44, 44)
ROTATION_SPEED = 5
PLAYER_IMAGE = "image/Kla'ed/Base/Kla'ed - Frigate - Base.png"
PLAYER_INITIAL_POSITION = (130, 160)
RESPAWN_TIME = 50 * 9 # durée de l'animation de mort x nombre de frame sur l'animation de la mort
LIFE_NB = 2

FIRE_RATE = 600 # temps en millisecodes
BULLET_SPEED = MAX_PLAYER_SPEED * 1.3 * PLAYER_SPEED
BULLET_SPRITESHEET = "image/Kla'ed/Projectiles/Kla'ed - Big Bullet.png"


LIGHT_GREY = (231, 229, 230)


ROCKETSHIP_SCORE = 500

###Ennemis###

###Asteroid###
ASTEROID_VITESSE=1
ASTEROIDE_SCORE = 100
###Tir###
TIR_VITESSE=4

###Chargeur###
CHARGEUR_ROTATION_SPEED=1.5
CHARGEUR_MIN_SPEED=0.7
CHARGEUR_MAX_SPEED=3
CHARGEUR_ACCELERATION=0.1
CHARGEUR_DECELERATION=0.1
CHARGEUR_ANGLE_ACCELERATION = 15 #determine la moitié de l'angle devant le chargeur dans lequel le joueur doit être pour qu'il accélère.
CHARGEUR_SCORE = 300

###Tourelle###
TOURELLE_INITIAL_CLOCK=(50,150)#fourchette du timer initial aléatoire pour le premier tir
TOURELLE_NEW_CLOCK=(100,150)#fourchette du timer aléatoire pour les tirs suivants
TOURELLE_SCORE = 400

###Miner###
MINER_CLOCK=(200,300)
MINER_SPEED=1
MINER_SCORE=400