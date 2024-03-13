FONT = "Comic Sans MS"
SIZE = (1080, 720)
WALL_DISTANCE = 10 # écart entre les murs et les bords de l'écran
BACKGROUND_IMAGE = "image/background/Space Background3.png"
GAME_MUSIC = "music/Race to Mars.mp3"
MENU_MUSIC = "music/Checking Manifest.mp3"
TITLE = "Omega Race"

PLAYER_SAFE_SPAWN_ZONE = (600,600)


##### Player #####
MAX_PLAYER_SPEED = 9
PLAYER_SPEED = 0.5
VELOCITY_LOST = 0.5
HITBOX_SIZE = (44, 44)
ROTATION_SPEED = 5
PLAYER_IMAGE = "image/Kla'ed/Base/Kla'ed - Frigate - Base.png"
PLAYER_INITIAL_POSITION = (130, 160)
RESPAWN_TIME = 50 * 9 # durée de l'animation de mort x nombre de frame sur l'animation de la mort
LIFE_NB = 2

FIRE_RATE = 550 # temps en millisecodes was 550
BULLET_SPEED = MAX_PLAYER_SPEED * 1.7 * PLAYER_SPEED
BULLET_SPRITESHEET = "image/Kla'ed/Projectiles/Kla'ed - Big Bullet.png"


LIGHT_GREY = (231, 229, 230)


ROCKETSHIP_SCORE = 500

###Ennemis###

###Upgrades :###
LISTE_UPGRADES=["tourelle_cadence+","tourelle_grace-","tir_vitesse+"]

###Asteroid###
#constantes :
ASTEROID_VITESSE=1
ASTEROIDE_SCORE = 100
#variables :

###Tir###
#constantes :
#variables :
TIR_VITESSE_UPGRADE_MULTIPLIER=1.5
###Rocket###
ROCKET_VITESSE=5
ROCKET_ROTATION=4
ROCKET_ROTATION_DECAY=0.99
#constantes :
#variables :


###Chargeur###
CHARGEUR_ROTATION_SPEED=1.5
CHARGEUR_MIN_SPEED=0.7
CHARGEUR_MAX_SPEED=3
CHARGEUR_ACCELERATION=0.1
CHARGEUR_DECELERATION=0.1
CHARGEUR_ANGLE_ACCELERATION = 20 #determine la moitié de l'angle devant le chargeur dans lequel le joueur doit être pour qu'il accélère.
CHARGEUR_SCORE = 300
#constantes :
#variables :


###Tourelle###
#constantes :
TOURELLE_SCORE = 400
TOURELLE_INITIAL_CLOCK_UPGRADE_MULTIPLIER=0.60
TOURELLE_NEW_CLOCK_UPGRADE_MULTIPLIER=0.75
#variables :
TOURELLE_INITIAL_CLOCK=[200,300]#fourchette du timer initial aléatoire pour le premier tir
TOURELLE_NEW_CLOCK=[150,250]#fourchette du timer aléatoire pour les tirs suivants

###Miner###
MINER_CLOCK=(200,300)
MINER_SPEED=2
MINER_MINES=5
MINER_SCORE=400
#constantes :
#variables :


###Rocketship###
ROCKETSHIP_INITIAL_CLOCK=[400,500]#fourchette du timer initial aléatoire pour le premier tir
ROCKETSHIP_NEW_CLOCK=[250,400]#fourchette du timer aléatoire pour les tirs suivants
ROCKETSHIP_SCORE = 500
ROCKETSHIP_ROTATION_SPEED=1.5
ROCKETSHIP_MIN_SPEED=0.7
ROCKETSHIP_MAX_SPEED=2
ROCKETSHIP_ACCELERATION=0.1
ROCKETSHIP_DECELERATION=0.1
ROCKETSHIP_ANGLE_ACCELERATION = 20 #determine la moitié de l'angle devant le chargeur dans lequel le joueur doit être pour qu'il accélère.
ROCKETSHIP_NB_TIRS=1
#constantes :
#variables :
