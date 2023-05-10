import random

class Particle:
    def __init__(self, x, y, radius, velo_max_x , velo_max_y, max_dispawn_time, min_dispawn_time):
        self.x = x
        self.y = y
        self.radius = radius
        self.velocity_x = random.uniform(-velo_max_x, velo_max_x)
        self.velocity_y = random.uniform(-velo_max_y, velo_max_y)
        self.despawn_time = random.uniform(max_dispawn_time, min_dispawn_time)

    def update(self):
        if self.radius >= 0:
            self.radius -= self.despawn_time
            self.x += self.velocity_x
            self.y += self.velocity_y
            if self.x < 0: # si l'on dessine un cercle à gauche de l'écran des bugs graphiques apparaissent
                self.x = 0
