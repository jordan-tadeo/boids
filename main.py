# import the pygame module
import pygame
import boid as b
import math
import random

W, H = 1280, 720

# Define the background colour
# using RGB color coding.
background_color = (10, 40, 20)
boid_color = (255, 255, 255)

# get boid size from boid class file
boid_size = b.boid_size

# Program version number
ver = '0.0.8'

# Define the dimensions of
# screen object(width,height)
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption(f'Flocker {ver}')

# Initialize a pygame clock  
clock = pygame.time.Clock()

# ------- FUNCTIONS ----------

def create_boid_list(n: int) -> list[b.Boid]:
    boid_list = []
    for i in range(n):
        boid_list.append(b.Boid())
    
    return boid_list

def infinite_edges(boid_list: list[b.Boid]) -> list[b.Boid]:
    for boid in boid_list:
        if boid.pos[0] > W:
            boid.pos[0] = 0
        elif boid.pos[0] < 0:
            boid.pos[0] = W
        if boid.pos[1] > H:
            boid.pos[1] = 0
        elif boid.pos[1] < 0:
            boid.pos[1] = H
    return boid_list

def update_all_boid_positions(boid_list: list[b.Boid]) -> list[b.Boid]:
    for boid in boid_list:
        # Update boid position
        boid.update()
        boid.three_rules(boid_list)

    return infinite_edges(boid_list)

def draw_all_boids(boid_list: list[b.Boid]) -> None:
    for boid in boid_list:
        x = boid.pos[0]
        y = boid.pos[1]
        color = boid.color
        surf = boid.surf
        hdg = boid.hdg

        # Create surface with alpha channel and fill with transparent color
        surf_alpha = surf.convert_alpha()
        surf_alpha.fill((0, 0, 0, 0))

        # Draw triangle on surface
        pygame.draw.polygon(surf_alpha, color, [(boid_size[0] / 2, 0), (0, boid_size[1]), (boid_size[0], boid_size[1])])

        # Rotate surface by heading angle and blit onto screen
        rotated_surf = pygame.transform.rotate(surf_alpha, hdg)
        screen.blit(rotated_surf, rotated_surf.get_rect(center=(x, y)))

boid_list = create_boid_list(256)

# Variable to keep our game loop running
running = True

# game loop
while running:
    screen.fill(background_color)
    
    draw_all_boids(boid_list)
    boid_list = update_all_boid_positions(boid_list)

# for loop through the event queue  
    for event in pygame.event.get():

        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
    
    # Limit FPS
    clock.tick(60)
    
    # Update the display using update
    pygame.display.update()