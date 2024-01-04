from abc import ABC, abstractmethod
from .surface_helper import Helper
from dataclasses import dataclass
import pygame
import numpy as np
from typing import Iterator

RGB = tuple[int, int, int]

@dataclass
class Behavior(ABC):
    x:int = 0
    y:int = 0

    end_time:int = 30
    time:int = 0
    iterator:Iterator[int] = None

    def __post_init__(self):
        self.iterator = iter(range(0, self.end_time))

    def step(self, helper:Helper):
        self.time = next(self.iterator, None)
        if self.time is None: self.end_behavior(helper)
        else: self.draw_to_top(helper)

    def over(self):
        return self.time is None

    @abstractmethod
    def draw_to_top(self, helper:Helper):
        ...
    @abstractmethod
    def end_behavior(self, helper:Helper):
        ...


@dataclass
class Bomb_Anim(Behavior):

    radius:int = 10

    ring_color:RGB = (255, 255, 255)
    ring_spacing:float = 2
    ring1_width:int = 3
    ring2_width:int = 1

    def __post_init__(self):
        super().__post_init__()
        self.unit_a_sec:float = self.radius / self.end_time 

    def draw_to_top(self, helper:Helper):
        top_surf = helper.get_top_surf()
        pygame.draw.circle(top_surf, self.ring_color, (self.x, self.y), self.time * self.unit_a_sec, self.ring1_width)
        pygame.draw.circle(top_surf, self.ring_color, (self.x, self.y), self.time * self.unit_a_sec - self.ring_spacing - self.ring1_width, self.ring1_width)

    def end_behavior(self, helper: Helper):
        terrain_surf = helper.get_terrain_surf()
        pygame.draw.circle(terrain_surf, helper.terrain.background_color, (self.x, self.y), self.end_time * self.unit_a_sec)
        helper.add_sand_to_check(self.x - self.radius, self.x + self.radius)

@dataclass
class Lazer_Anim(Behavior):
    blast_radius:int = 5
    edge_len:int = 1
    laser_edge_color:RGB = (98, 252, 115)
    laser_color:RGB = (140, 255, 152)

    def __post_init__(self):
        super().__post_init__()
        self.unit_a_sec:float = self.blast_radius / self.end_time 

    def draw_to_top(self, helper:Helper):
        top_surf = helper.get_top_surf()
        radius1 = np.sin(self.time/20) + self.unit_a_sec * self.time
        radius2 = np.sin(self.time/20) + self.unit_a_sec * self.time - 2
        pygame.draw.rect(top_surf, self.laser_edge_color, (self.x - radius1, 0, radius1*2, helper.get_world_height()))
        pygame.draw.rect(top_surf, self.laser_color, (self.x - radius2, 0, radius2*2, helper.get_world_height()))

    def end_behavior(self, helper: Helper):
        terrain_surf = helper.get_terrain_surf()
        radius1 = np.sin(self.end_time/20) + self.unit_a_sec * self.end_time
        pygame.draw.rect(terrain_surf, helper.terrain.background_color, (self.x - radius1, 0, radius1*2, helper.get_world_height()))
        helper.add_sand_to_check(self.x - radius1, self.x + radius1)

@dataclass
class Digger(Behavior):
    ...

@dataclass
class Mountain_Mover(Behavior):
    ...

@dataclass
class Split(Behavior):
    ...
