import pygame
from noise import pnoise1
from typing import Callable, Union
import numpy as np
import numba as nb

Surf = pygame.Surface

TERRAIN_PARAMS = {'min': 20,
                    'max': 150,
                    'scale': 150,
                    'offset': np.random.randint(0, 1_000),
                    'octaves': 3,
                    'persistence': 0.6,
                    'lacunarity': 2.5,
                    'repeat': 2048}

def create_height_func(min, max, scale, offset, **kwargs) -> Callable:
    amplitude = max - min + 5
    def height_func(x_val):
        value = pnoise1(x_val / scale + offset, **kwargs, base=1)
        normalized_value = 0.5 * (value + 1.0)
        return min + normalized_value * amplitude if normalized_value < 0.8 else 0.8*amplitude + min
    return height_func

def create_terrain(surface:Surf, height_func, COLOR) -> pygame.Surface:
    for i in range(surface.get_width()):
        pygame.draw.line(surface, COLOR, (i,0), (i,int(height_func(i))))
    return surface

class Terrain:
    def __init__(self, terrain_surf:pygame.Surface):
        self.func = create_height_func(**TERRAIN_PARAMS)
        self.terrain_color = (80, 47, 87)
        self.background_color = (0, 0, 0)
        terrain_surf.fill(self.background_color)
        self.terrain_surf = create_terrain(terrain_surf, self.func, self.terrain_color)

        self.falling_sand:set[int] = set([])

    def is_ground_at_point(self, xcor, ycor) -> bool:
        return self.terrain_surf.get_at((int(xcor), int(ycor))) == self.terrain_color
    
    def add_sand(self, min_val, max_val):
        min_val = pygame.math.clamp(int(min_val), 0, self.terrain_surf.get_width() - 1)
        max_val = pygame.math.clamp(int(max_val), 0, self.terrain_surf.get_width() - 1)
        self.falling_sand.update(range(min_val, max_val))

    def find_top_and_bottom_ledge(self, xcor) -> Union[tuple[int, int], tuple[int, None]]:
        return self.find_top_ledge(xcor), self.find_bottom_ledge(xcor)

    def find_top_ledge(self, xcor) -> int:
        max_val = int(self.func(xcor))
        res = 0
        for y in range(1, max_val + 1):
            if self.terrain_surf.get_at((xcor, y + 1)) == self.background_color:
                if self.terrain_surf.get_at((xcor, y)) == self.terrain_color:
                    res = y 
                    break

        return res

    def find_bottom_ledge(self, xcor) -> Union[int, None]:
        max_val = int(self.func(xcor))
        min_val = None
        for y in range(1, max_val + 1):
            if self.terrain_surf.get_at((xcor, y)) == self.terrain_color:
                if self.terrain_surf.get_at((xcor, y - 1)) == self.background_color:
                    min_val = y
                    break
        return min_val

    def update_sand(self):
        to_remove = []
        for x in self.falling_sand:
            top_ledge, bottom_ledge = self.find_top_and_bottom_ledge(x)

            if bottom_ledge is not None:
                pygame.draw.line(self.terrain_surf, self.background_color, (x, bottom_ledge), (x, top_ledge))
                pygame.draw.line(self.terrain_surf, self.terrain_color, (x, bottom_ledge - 1), (x, top_ledge - 1))
            else:
                to_remove.append(x)
        
        [self.falling_sand.remove(value) for value in to_remove]

    def update(self):
        self.update_sand()
