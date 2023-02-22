import pygame
import math

W, H = (640, 480)

boid_size = (32, 32)

class Boid:
    def __init__(self):
        self.pos = [W/2, H/2]
        self.vel = [0, 0]
        self.hdg = 0

        self.surf = pygame.Surface((boid_size[0]*math.sqrt(2), boid_size[1]*math.sqrt(2)))

    