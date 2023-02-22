import pygame
import math

# Define triangle vertices (in this case, an equilateral triangle)
vertices = [(0, -50), (50, 50), (-50, 50)]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((640, 480))

# Load the triangle image
triangle_surf = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.polygon(triangle_surf, (255, 255, 255), vertices)

# Get the rectangle that encompasses the surface and center it
triangle_rect = triangle_surf.get_rect()
triangle_rect.center = screen.get_rect().center

# Main loop
clock = pygame.time.Clock()
angle = 0
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Rotate the triangle surface around its center
    rotated_surf = pygame.transform.rotate(triangle_surf, angle)
    rotated_rect = rotated_surf.get_rect(center=triangle_rect.center)

    # Draw the rotated triangle on the screen
    screen.fill((0, 0, 0))
    screen.blit(rotated_surf, rotated_rect)

    # Update the screen
    pygame.display.update()

    # Increment the rotation angle
    angle += 1

    # Limit the frame rate
    clock.tick(60)
