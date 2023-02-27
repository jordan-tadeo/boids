import pygame
import math
import random
import numpy as np

W, H = (1280, 720)

boid_size = (4, 6)
max_speed = .33
neighbor_range = 512 # pixels
separation_range = boid_size[0] + 0 # pixels

neutral_color = (255, 255, 255)
neighbors_color = (255, 0, 0)

class Boid:
    def __init__(self):
        self.neighbors = []

        self.hdg = 0
        self.pos = [random.random()* W, random.random() * H]
        self.vel = [(random.random() - 0.4) * max_speed, -1  * max_speed]

        self.surf = pygame.Surface((boid_size[0]*math.sqrt(2), boid_size[1]*math.sqrt(2)))
        self.color = neutral_color

        self.max_speed = max_speed
    
    def update(self):
        # update position based on velocity
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]

        # update heading based on velocity
        self.hdg = math.degrees(math.atan(self.vel[0]/self.vel[1]))

        if self.vel[1] > 0:
            self.hdg += 180

        # limit speed to max_speed
        speed = math.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
        if speed > self.max_speed:
            self.vel[0] *= self.max_speed / speed
            self.vel[1] *= self.max_speed / speed
    
    def add_vector_to_vel(self, vec):
        np.add(self.vel, vec)

    def get_xy_ratio_to_point(self, point):
        x = self.pos[0] - point[0]
        y = self.pos[1] - point[1] 

        ratio = x / y



    def apply_force_from_point(self, point, mag):

        # TODO:
        #   change out this function for an "add vector" function
        #   that simply adds a vector to the velocity instead
        #   of applying a force from a point

        # get distance on Y-axis
        ydist = point[1] - self.pos[1]
        # get distance on X-axis
        xdist = point[0] - self.pos[0]

        if xdist == 0 and ydist == 0:
            force_hdg = math.radians(random.random() * 360)
        else:
            force_hdg = math.atan(ydist/xdist)

        # calculate force magnitude based on distance
        dist = math.dist(self.pos, point)
        force_mag = mag / dist if dist > 0 else mag

        # apply force to velocity
        self.vel[0] += math.sin(force_hdg) * force_mag
        self.vel[1] += math.cos(force_hdg) * force_mag

    def get_neighbors(self, boid_list) -> list:
        neighbors = []
        for b in boid_list:
            dist = math.dist(self.pos, b.pos)

            if abs(dist) < neighbor_range and b is not self:
                neighbors.append((b, dist))
        
        return neighbors

    def separation(self):
        #if len(self.neighbors) >= 1:
        #    self.color = neighbors_color
        #else:
        #    self.color = neutral_color

        for b in self.neighbors:
            if b[0] is self:
                continue
            elif b[1] < separation_range:
                # exert force in direction opposite of this neighbor
                if b[1] > 0:
                    force_mag = self.max_speed * (1 / b[1])
                else:
                    # if they are at they same point, aka dist = 0
                    force_mag = self.max_speed / 3
                self.apply_force_from_point(b[0].pos, force_mag)
    
    def alignment(self):
        if len(self.neighbors) == 0:
            return

        avg_direction = [0, 0]
        for neighbor in self.neighbors:
            avg_direction[0] += neighbor[0].vel[0]
            avg_direction[1] += neighbor[0].vel[1]

        avg_direction[0] /= len(self.neighbors)
        avg_direction[1] /= len(self.neighbors)

        avg_direction_mag = math.sqrt(avg_direction[0]**2 + avg_direction[1]**2)
        max_alignment_force = .25

        if avg_direction_mag == 0:
            return

        alignment_force = [0, 0]
        alignment_force[0] = (avg_direction[0] / avg_direction_mag) * max_alignment_force
        alignment_force[1] = (avg_direction[1] / avg_direction_mag) * max_alignment_force

        self.apply_force_from_point(alignment_force, max_alignment_force)
    
    def cohesion(self):
        if len(self.neighbors) == 0:
            return

        # Get the average position of neighbors
        avg_pos = [0, 0]
        for neighbor in self.neighbors:
            avg_pos[0] += neighbor[0].pos[0]
            avg_pos[1] += neighbor[0].pos[1]
        avg_pos[0] /= len(self.neighbors)
        avg_pos[1] /= len(self.neighbors)

        # Apply a force towards the average position
        force_mag = self.max_speed * 2
        self.apply_force_from_point(avg_pos, force_mag)


    
    def three_rules(self, boid_list):

        self.neighbors = self.get_neighbors(boid_list)

        self.separation()
        self.alignment()
        self.cohesion()

    