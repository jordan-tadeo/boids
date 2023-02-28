
import pygame as pg
import boid as b

boid_size = b.boid_size

class World:
    def __init__(self, window):
        self.screen = window.screen
        self.W, self.H = pg.display.get_window_size()

    def create_boid_list(self, n: int) -> list:
        boid_list = []
        for i in range(n):
            boid_list.append(b.Boid())
        
        return boid_list

    def infinite_edges(self, boid_list: list) -> list:
        for boid in boid_list:
            if boid.pos.x > self.W:
                boid.pos.x = 0
            elif boid.pos.x < 0:
                boid.pos.x = self.W
            if boid.pos.y > self.H:
                boid.pos.y = 0
            elif boid.pos.y < 0:
                boid.pos.y = self.H
        return boid_list

    def update_all_boid_positions(self, boid_list: list) -> list:
        for boid in boid_list:
            # Update boid position
            boid.update()
            boid.three_rules(boid_list)

        return self.infinite_edges(boid_list)

    def draw_all_boids(self, boid_list: list) -> None:
        for boid in boid_list:
            x = boid.pos.x
            y = boid.pos.y
            color = boid.color
            surf = boid.surf
            hdg = boid.hdg

            # Create surface with alpha channel and fill with transparent color
            surf_alpha = surf.convert_alpha()
            surf_alpha.fill((0, 0, 0, 0))

            # Draw triangle on surface
            pg.draw.polygon(surf_alpha, color, [(boid_size.x / 2, 0), (0, boid_size.y), (boid_size.x, boid_size.y)])

            # Rotate surface by heading angle and blit onto screen
            rotated_surf = pg.transform.rotate(surf_alpha, hdg)
            self.screen.blit(rotated_surf, rotated_surf.get_rect(center=(x, y)))