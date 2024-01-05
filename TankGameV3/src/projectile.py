import pygame
import numpy as np
from .surface_helper import Helper
from .behavior import Behavior

class Projectile:
    def __init__(self, x, y, angle, v, power, behavior:Behavior, color=(255, 255, 0), radius=1):
        self.x, self.y = x, y
        self.vx, self.vy = np.cos(angle) * v, np.sin(angle) * v
        self.color = color
        self.power = power
        self.radius = radius
        self.behavior = behavior
        self.status = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy -= 0.1
    
    def get_anim(self):
        self.behavior.x = self.x
        self.behavior.y = self.y
        return self.behavior
    
    def contact(self):
        self.status = False
        
    def render(self, helper:Helper):
        self.update()
        top_level = helper.get_top_surf()

        if helper.is_in_bounds(self.x, self.y + 2):
            if helper.get_height_at_xcor(self.x) + 2 >= self.y:
                self.contact()
            pygame.draw.circle(top_level, self.color, (self.x, self.y), self.radius)
        else:
            self.contact()
