import pygame
from .terrain import Terrain
import numpy as np

Surf = pygame.Surface

class Helper:
    def __init__(self, game, top_surf:Surf, terrain:Terrain):
        self.game = game
        self.top_surf = top_surf
        self.terrain = terrain

    def get_height_at_xcor(self, xcor):
        return self.terrain.find_top_ledge(self.clamp_xcor(xcor))
    
    def get_average_height_at_xcor(self, xcor, delta:int=1):
        return (self.get_height_at_xcor(xcor - delta) + self.get_height_at_xcor(xcor + delta))/2

    def angle_of_terrain_at_xcor(self, xcor, delta:int=2):
        height_at_x = self.get_height_at_xcor(xcor-delta)
        height_at_x_plus_dx = self.get_height_at_xcor(xcor+delta)
        
        slope = (height_at_x_plus_dx - height_at_x) / (delta*2)

        # Calculate the angle using the arctangent function
        angle_rad = np.arctan(-slope)  # Negative because terrain slope is often inverted
        return angle_rad

    def clamp_xcor(self, xcor):
        return pygame.math.clamp(int(xcor), 0, self.terrain.terrain_surf.get_width()-1)
    def clamp_ycor(self, ycor):
        return pygame.math.clamp(int(ycor), 0, self.terrain.terrain_surf.get_height()-1)

    def is_in_bounds(self, xcor, ycor) -> bool:
        if xcor >= 0 and xcor < self.top_surf.get_width():
            if ycor >= 0 and ycor < self.top_surf.get_height():
                return True
        return False
    
    def is_ground_at_point(self, xcor, ycor) -> bool:
        return self.terrain.is_ground_at_point(xcor, ycor)
    
    def add_to_projectile_list(self, projectile):
        self.game.projectiles.append(projectile)

    def add_sand_to_check(self, min_val:int, max_val:int):
        self.terrain.add_sand(min_val, max_val)

    def get_top_surf(self) -> pygame.Surface:
        return self.top_surf
    def get_terrain_surf(self) -> pygame.Surface:
        return self.terrain.terrain_surf
    
    def get_world_height(self):
        return self.top_surf.get_height()
    
