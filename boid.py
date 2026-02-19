import pygame
import math
import random
import utility as util

W, H = (720, 640)

boid_size = util.Vector2(4, 6)
max_speed = 2.2
max_accel = 0.3
neighbor_range = 128 # pixels
separation_range = boid_size.x + 8 # pixels

neutral_color = (255, 255, 255)
neighbors_color = (255, 0, 0)
solo_color = (0, 200, 255)

empty_vector = util.Vector2(0, 0)

class Boid:
    def __init__(self):
        self.neighbors = []

        self.hdg = 0
        self.pos = util.Vector2(random.random()* W, random.random() * H)
        self.vel = util.Vector2((random.random() - 0.5) * max_speed,(random.random() - 0.5) * max_speed)

        self.surf = pygame.Surface((boid_size.x*math.sqrt(2), boid_size.y*math.sqrt(2)))
        self.color = neutral_color

        self.max_speed = max_speed
    
    def update(self):
        # update position based on velocity
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y

        # only update heading if we're actually moving
        speed2 = self.vel.x * self.vel.x + self.vel.y * self.vel.y
        if speed2 > 1e-8:
            target = math.degrees(math.atan2(-self.vel.x, -self.vel.y))  # velocity -> sprite heading

            # smooth turn: max 5 deg/frame
            diff = (target - self.hdg + 180) % 360 - 180
            self.hdg = (self.hdg + max(-5, min(5, diff))) % 360


        if self.vel.y > 0:
            self.hdg += 180

        # limit speed to max_speed
        speed = math.sqrt(self.vel.x ** 2 + self.vel.y ** 2)
        if speed > self.max_speed:
            self.vel.x *= self.max_speed / speed
            self.vel.y *= self.max_speed / speed
    
    def get_vector_toward(self, pos: util.Vector2):
        dist = math.dist(self.pos, pos)
        x = pos.getX() - self.pos.getX()
        y = pos.getY() - self.pos.getY()

        scale = max_accel / dist if dist > 0 else max_accel

        return util.Vector2(scale * x, scale * y)

    def move_toward(self, pos: util.Vector2):
        dist = math.dist(self.pos, pos)
        x = pos.getX() - self.pos.getX()
        y = pos.getY() - self.pos.getY()

        scale = max_accel / dist if dist > 0 else max_accel

        self.vel += util.Vector2(scale * x, scale * y)
    
    def get_vector_from(self, pos: util.Vector2):
        dist = math.dist(self.pos, pos)
        x = pos.getX() - self.pos.getX()
        y = pos.getY() - self.pos.getY()

        scale = max_accel / dist if dist > 0 else max_accel

        return util.Vector2(-scale * x, -scale * y)

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

    def separation(self) -> util.Vector2:
        for b in self.neighbors:
            if b[0] is self:
                continue
            # if dist is less than separation range
            elif b[1] < separation_range:
                return self.get_vector_from(b[0].pos) * 0.33
            
        return empty_vector
    
    def alignment(self) -> util.Vector2:
        # if this boid has no neighbors, don't bother
        if len(self.neighbors) == 0:
            return empty_vector

        # average the velocity components of neighbors
        avg_vel = util.Vector2(0, 0)
        for neighbor in self.neighbors:
            avg_vel.x += neighbor[0].vel.x
            avg_vel.y += neighbor[0].vel.y

        avg_vel.x /= len(self.neighbors)
        avg_vel.y /= len(self.neighbors)

        # distance formula to get the average speed of neighbors
        avg_vel_mag = math.sqrt(avg_vel.x**2 + avg_vel.y**2)
        max_alignment_mag = .1

        # avoid dividing by 0
        if avg_vel_mag == 0:
            return empty_vector

        alignment_vector = util.Vector2(0, 0)
        alignment_vector.x = (avg_vel.x / avg_vel_mag) * max_alignment_mag
        alignment_vector.y = (avg_vel.y / avg_vel_mag) * max_alignment_mag

        # apply the new acceleration vector to this boid's velocity
        # print(alignment_vector.x, " ", alignment_vector.y)
        return alignment_vector
    
    def cohesion(self) -> util.Vector2:
        # If this boid has no neighbors, fuggetaboutit
        if len(self.neighbors) == 0:
            return empty_vector

        # Get the average position of neighbors
        avg_pos = util.Vector2(0, 0)
        for neighbor in self.neighbors:
            avg_pos.x += neighbor[0].pos.x
            avg_pos.y += neighbor[0].pos.y
        avg_pos.x /= len(self.neighbors)
        avg_pos.y /= len(self.neighbors)

        final = self.get_vector_toward(avg_pos) * 0.1

        return final
    
    def three_rules(self, boid_list):
        self.neighbors = self.get_neighbors(boid_list)

        separation_vector = self.separation()
        alignment_vector = self.alignment()
        cohesion_vector = self.cohesion()

        # print(f"{self}, sepvec: {separation_vector}, align: {alignment_vector}, cohesion: {cohesion_vector}")

        # Combine all three vectors to produce a total acceleration vector
        accel_vector = separation_vector + alignment_vector + cohesion_vector
        self.accelerate(accel_vector)