import pygame
import math

W, H = (640, 480)

boid_size = (16, 18)
max_speed = 2

class Boid:
    def __init__(self):
        self.pos = [W/2, H/2]
        
        self.hdg = 1
        self.max_speed = max_speed
        self.vel = [0, 0]

        self.surf = pygame.Surface((boid_size[0]*math.sqrt(2), boid_size[1]*math.sqrt(2)))

    