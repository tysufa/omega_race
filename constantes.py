FONT = "Comic Sans MS"
SIZE = (1080, 720)
WALL_DISTANCE = 10  # écart entre les murs et les bords de l'écran
BACKGROUND_IMAGE = "image/background/Space Background3.png"
GAME_MUSIC = "music/Race to Mars.mp3"
MENU_MUSIC = "music/Checking Manifest.mp3"
TITLE = "Omega Race"

PLAYER_SAFE_SPAWN_ZONE = (600, 600)

##### Menu ####
ANIMATION_SPEED = 2
ANIMATION_STARTING_OFFSET = 1000

##### Player #####
MAX_PLAYER_SPEED = 9
PLAYER_SPEED = 0.5
VELOCITY_LOST = 0.5
HITBOX_SIZE = (44, 44)
ROTATION_SPEED = 5
PLAYER_IMAGE = "image/Kla'ed/Base/Kla'ed - Frigate - Base.png"
PLAYER_INITIAL_POSITION = (130, 160)
RESPAWN_TIME = (
    50 * 9
)  # durée de l'animation de mort x nombre de frame sur l'animation de la mort
LIFE_NB = 2

FIRE_RATE = 550  # temps en millisecodes was 550
BULLET_SPEED = MAX_PLAYER_SPEED * 1.7 * PLAYER_SPEED
BULLET_SPRITESHEET = "image/Kla'ed/Projectiles/Kla'ed - Big Bullet.png"


LIGHT_GREY = (231, 229, 230)


ROCKETSHIP_SCORE = 500

###Ennemis###

###Constantes###

###Upgrades :###

LISTE_UPGRADES = [
    "tourelle_cadence+",
    "tourelle_grace-",
    "tir_vitesse+",
    "chargeur_rotation+",
    "tourelle_rocket",
]

###Asteroid###
# constantes :
ASTEROID_VITESSE = 1
ASTEROIDE_SCORE = 100

###Tir###
TIR_VITESSE_UPGRADE_MULTIPLIER = 1.5
TIR_VITESSE = 4.0

###Rocket###
ROCKET_VITESSE = 5
ROCKET_ROTATION = 4
ROCKET_ROTATION_DECAY = 0.99

###Chargeur###
CHARGEUR_SCORE = 300
CHARGEUR_ROTATION_SPEED_UPGRADE_MULTIPLIER = 1.1
CHARGEUR_ANGLE_ACCELERATION_UPGRADE_MULTIPLIER = 1.2
CHARGEUR_ROTATION_SPEED = 1.5
CHARGEUR_MIN_SPEED = 0.7
CHARGEUR_MAX_SPEED = 3
CHARGEUR_ACCELERATION = 0.1
CHARGEUR_DECELERATION = 0.1
CHARGEUR_ANGLE_ACCELERATION = 20.0  # determine la moitié de l'angle devant le chargeur dans lequel le joueur doit être pour qu'il accélère.


###Tourelle###
TOURELLE_SCORE = 400
TOURELLE_INITIAL_CLOCK_UPGRADE_MULTIPLIER = 0.60
TOURELLE_NEW_CLOCK_UPGRADE_MULTIPLIER = 0.75
TOURELLE_INITIAL_CLOCK = [
    200.0,
    300.0,
]  # fourchette du timer initial aléatoire pour le premier tir
TOURELLE_NEW_CLOCK = [
    150.0,
    250.0,
]  # fourchette du timer aléatoire pour les tirs suivants

###Miner###

MINER_CLOCK = (200, 300)
MINER_SPEED = 2
MINER_MINES = 5
MINER_SCORE = 400


###Rocketship###
ROCKETSHIP_INITIAL_CLOCK = [
    400,
    500,
]  # fourchette du timer initial aléatoire pour le premier tir
ROCKETSHIP_NEW_CLOCK = [
    250,
    400,
]  # fourchette du timer aléatoire pour les tirs suivants
ROCKETSHIP_SCORE = 500
ROCKETSHIP_ROTATION_SPEED = 1.5
ROCKETSHIP_MIN_SPEED = 0.7
ROCKETSHIP_MAX_SPEED = 2
ROCKETSHIP_ACCELERATION = 0.1
ROCKETSHIP_DECELERATION = 0.1
ROCKETSHIP_ANGLE_ACCELERATION = 20  # determine la moitié de l'angle devant le chargeur dans lequel le joueur doit être pour qu'il accélère.
ROCKETSHIP_NB_TIRS = 1


###Variables###

VARIABLES = {}


def reset():
    global VARIABLES
    VARIABLES["TIR_VITESSE"] = TIR_VITESSE
    VARIABLES["TOURELLE_INITIAL_CLOCK"] = TOURELLE_INITIAL_CLOCK.copy()
    VARIABLES["TOURELLE_NEW_CLOCK"] = TOURELLE_NEW_CLOCK.copy()
    VARIABLES["CHARGEUR_ROTATION_SPEED"] = CHARGEUR_ROTATION_SPEED
    VARIABLES["CHARGEUR_ANGLE_ACCELERATION"] = CHARGEUR_ANGLE_ACCELERATION
    VARIABLES["TOURELLE_TIR"] = "tir"
    VARIABLES["MINE_TIRS"] = 0
