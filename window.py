
import pygame as pg

W, H = 1280, 720
ver = "0.0.12"
title = f"Flocker {ver}"

bg_color = (60, 60, 90)

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