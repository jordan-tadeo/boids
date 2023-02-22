# import the pygame module
import pygame
import boid as b
  
# Define the background colour
# using RGB color coding.
background_color = (10, 40, 20)
boid_color = (255, 255, 255)

# Define boid size
boid_size = b.boid_size
  
# Define the dimensions of
# screen object(width,height)
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Flocker 0.0.1')

# Initialize a pygame clock  
clock = pygame.time.Clock()

# ------- FUNCTIONS ----------

def create_boid_list(n: int) -> list[b.Boid]:
    boid_list = []
    for i in range(n):
        boid_list.append(b.Boid())
    
    return boid_list

def update_all_boid_positions(boid_list: list[b.Boid]) -> list[b.Boid]:
    for boid in boid_list:
        boid.pos[0] += boid.vel[0]
        boid.pos[1] += boid.vel[1]
        boid.hdg += 2

    return boid_list

def draw_all_boids(boid_list: list[b.Boid]) -> None:
    for boid in boid_list:
        x = boid.pos[0]
        y = boid.pos[1]
        surf = boid.surf
        hdg = boid.hdg

        surf_rect = surf.get_rect()
        surf_rect.center = (x, y)
        
        surf.set_colorkey((0,0,0))
        surf.fill((0,0,0))

        pygame.draw.polygon(surf, boid_color,
        [(boid_size[0]/2, 0), (0, boid_size[1]), (boid_size[0], boid_size[1])])

        rotated_surf = pygame.transform.rotate(surf, hdg)
        rotated_rect = rotated_surf.get_rect(center=surf_rect.center)
        screen.blit(rotated_surf, rotated_rect)

boid_list = create_boid_list(1)

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