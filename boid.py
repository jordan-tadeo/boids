import pygame
import math
import random
import numpy as np
import utility as util

W, H = (1280, 720)

boid_size = util.Vector2(4, 6)
max_speed = 5
max_accel = 2
neighbor_range = 512 # pixels
separation_range = boid_size.x + 0 # pixels

neutral_color = (255, 255, 255)
neighbors_color = (255, 0, 0)

class Boid:
    def __init__(self):
        self.neighbors = []

        self.hdg = 0
        self.pos = util.Vector2(random.random()* W, random.random() * H)
        self.vel = util.Vector2((random.random() - 0.4) * max_speed, -1  * max_speed)

        self.surf = pygame.Surface((boid_size.x*math.sqrt(2), boid_size.y*math.sqrt(2)))
        self.color = neutral_color

        self.max_speed = max_speed
    
    def update(self):
        # update position based on velocity
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # update heading based on velocity
        self.hdg = math.degrees(math.atan(self.vel.x/self.vel.y))

        if self.vel.y > 0:
            self.hdg += 180

        # limit speed to max_speed
        speed = math.sqrt(self.vel.x ** 2 + self.vel.y ** 2)
        if speed > self.max_speed:
            self.vel.x *= self.max_speed / speed
            self.vel.y *= self.max_speed / speed

    def move_toward(self, pos: util.Vector2):
        dist = math.dist(self.pos, pos)
        x = pos.getX() - self.pos.getX()
        y = pos.getY() - self.pos.getY()

        scale = max_accel / dist if dist > 0 else max_accel

        self.vel += util.Vector2(scale * x, scale * y)

    def move_away_from(self, pos: util.Vector2):
        dist = math.dist(self.pos, pos)
        x = pos.getX() - self.pos.getX()
        y = pos.getY() - self.pos.getY()

        scale = max_accel / dist if dist > 0 else max_accel

        self.vel -= util.Vector2(scale * x, scale * y)
    
    def accelerate(self, acc: util.Vector2):
        self.vel += acc

    def get_neighbors(self, boid_list) -> list:
        neighbors = []
        for b in boid_list:
            dist = math.dist(self.pos, b.pos)

            if abs(dist) < neighbor_range and b is not self:
                neighbors.append((b, dist))
        
        return neighbors

    def separation(self):
        for b in self.neighbors:
            if b[0] is self:
                continue
            # if dist is less than separation range
            elif b[1] < separation_range:
                self.move_away_from(b[0].pos)
    
    def alignment(self):



        """Basically useless right now. Need to implement a version of alignment that
        works on ratios of velocity components instead of angles"""





        # if this boid has no neighbors, don't bother
        if len(self.neighbors) == 0:
            return

        # average the velocity components of neighbors
        avg_vel = util.Vector2(0, 0)
        for neighbor in self.neighbors:
            avg_vel.x += neighbor[0].vel.x
            avg_vel.y += neighbor[0].vel.y

        avg_vel.x /= len(self.neighbors)
        avg_vel.y /= len(self.neighbors)

        # distance formula to get the average speed of neighbors
        avg_vel_mag = math.sqrt(avg_vel.x**2 + avg_vel.y**2)
        max_alignment_vel = .05

        # avoid dividing by 0
        if avg_vel_mag == 0:
            return

        alignment_vel = util.Vector2(0, 0)
        alignment_vel.x = (avg_vel.x / avg_vel_mag) * max_alignment_vel
        alignment_vel.y = (avg_vel.y / avg_vel_mag) * max_alignment_vel

        # self.apply_force_from_point(alignment_vel, max_alignment_vel)
        self.accelerate(util.Vector2(alignment_vel.x, alignment_vel.y))
    
    def cohesion(self):
        # If this boid has no neighbors, fuggetaboutit
        if len(self.neighbors) == 0:
            return

        # Get the average position of neighbors
        avg_pos = util.Vector2(0, 0)
        for neighbor in self.neighbors:
            avg_pos.x += neighbor[0].pos.x
            avg_pos.y += neighbor[0].pos.y
        avg_pos.x /= len(self.neighbors)
        avg_pos.y /= len(self.neighbors)

        self.move_toward(avg_pos)


    
    def three_rules(self, boid_list):

        self.neighbors = self.get_neighbors(boid_list)

        self.separation()
        self.alignment()
        self.cohesion()

    