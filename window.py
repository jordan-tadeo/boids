
import pygame as pg

W, H = 640, 480
ver = "0.0.12"
title = f"Flocker {ver}"

bg_color = (20, 20, 30)

class Window:
    def __init__(self, width=W, height=H, title=title):

        # Define the dimensions of
        # screen object(width,height)
        self.screen = pg.display.set_mode((W, H))
        pg.display.set_caption(title)
    
    def fill_screen(self, color=bg_color):
        self.screen.fill(color)
    
    def update(self):
        pg.display.update()