import numpy as np
import pygame
from OpenGL.GL import *


class App:

    def __init__(self):
        pygame.init()
        pygame.display.set_mode((640, 480), pygame.OPENGL | pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()
        glClearColor(0.2, 0.2, 0.2, 1)
        self.mainloop()

    def mainloop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            glClear(GL_COLOR_BUFFER_BIT)
            pygame.display.flip()

            self.clock.tick(60)
        self.quit()

    def quit(self):
        pygame.quit()

class Triangle:
    def __init__(self):

        # x y z r g b
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vertices_count = 3



if __name__ == '__main__':
    myApp = App()