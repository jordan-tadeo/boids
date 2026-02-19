# Drift through coded skies\n# Quiet wings align at dusk\n# Pixels learn to flow\n\nimport pygame
import src.window as window
import src.world as world

clock = pygame.time.Clock()

window1 = window.Window()

world1 = world.World(window1)

boid_list = world1.create_boid_list(128)

# game loop
running = True
while running:
    window1.fill_screen()
    
    world1.draw_all_boids(boid_list)

    boid_list = world1.update_all_boid_positions(boid_list)

    # Update the display
    window1.update()

    # loop through the event queue  
    for event in pygame.event.get():
        # Check for QUIT event    
        if event.type == pygame.QUIT:
            running = False
    
    # Limit FPS
    clock.tick(60)