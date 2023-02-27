# import the pygame module
import pygame
import window as win
import world

# Initialize a pygame clock  
clock = pygame.time.Clock()

window1 = win.Window()

world1 = world.World(window1)

boid_list = world1.create_boid_list(128)

# Variable to keep our game loop running
running = True

# game loop
while running:
    window1.fill_screen((0,0,0))
    
    world1.draw_all_boids(boid_list)
    boid_list = world1.update_all_boid_positions(boid_list)

# for loop through the event queue  
    for event in pygame.event.get():

        # Check for QUIT event      
        if event.type == pygame.QUIT:
            running = False
    
    # Limit FPS
    clock.tick(60)
    
    # Update the display using update
    # pygame.display.update()
    window1.update()