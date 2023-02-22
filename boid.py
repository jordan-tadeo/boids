import pygame

W, H = (640, 480)

class Boid:
    def __init__(self):
        self.pos = [W/2, H/2]
        self.vel = [0, 0]
        self.hdg = 33

        self.surf = pygame.Surface((12, 12))

    