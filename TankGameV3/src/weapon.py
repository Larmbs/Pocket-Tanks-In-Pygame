from .projectile import Projectile
import threading
import time
import numpy as np
from abc import ABC, abstractmethod
from .behavior import Behavior, Bomb_Anim, Lazer_Anim
from dataclasses import dataclass
import copy

RGB = tuple[int, int, int]
@dataclass
class Weapon(ABC):
    power:int
    color:RGB
    behavior:Behavior = None

    @abstractmethod
    def __post_init__(self):
        ...

    @abstractmethod
    def fire(self):
        ...

@dataclass
class SingleShot(Weapon):
    power:int = 20
    color:RGB = (150, 20, 0)

    def __post_init__(self):
        self.behavior = Bomb_Anim(0, 0, end_time=20, radius=10)

    def fire(self, fire_data, proj_list:list):
        proj_list.append(Projectile(*fire_data.xy, fire_data.fire_angle, fire_data.power, self.power, self.behavior, self.color))

@dataclass
class BirdShot(Weapon):
    spread:float = 0.1
    power:int = 10
    color:RGB = (100, 100, 255)
    drag:float = 0.9

    def __post_init__(self):
        self.behavior = Bomb_Anim(0, 0, end_time=15, radius=6)

    def fire(self, fire_data, proj_list:list):
        i1 = copy.deepcopy(self.behavior)
        i2 = copy.deepcopy(self.behavior)
        i3 = copy.deepcopy(self.behavior)

        proj_list.append(Projectile(*fire_data.xy, fire_data.fire_angle, fire_data.power * self.drag, self.power, i3, self.color))
        
        proj_list.append(Projectile(*fire_data.xy, fire_data.fire_angle + self.spread, fire_data.power * self.drag, self.power, i1, self.color))
        
        proj_list.append(Projectile(*fire_data.xy, fire_data.fire_angle - self.spread, fire_data.power * self.drag, self.power, i2, self.color))

@dataclass
class Volley(Weapon):
    spread:float = 0.1
    power:int = 7
    color:RGB = (255, 100, 100)
    drag:float = 0.9
    shot_count:int = 10
    time_between:float = 0.2

    def __post_init__(self):
        self.behavior = Bomb_Anim(0, 0, end_time=10, radius=3)

    def fire(self, fire_data, proj_list:list):
        thread = threading.Thread(target=self.volley, args=(fire_data, proj_list))
        thread.start()

    def volley(self, fire_data, proj_list:list):
        obj = copy.deepcopy(self.behavior)
        for _ in range(self.shot_count):
            obj = copy.deepcopy(self.behavior)
            offset = (np.random.rand() - 0.5) * 2 * self.spread
            proj_list.append(Projectile(*fire_data.xy, fire_data.fire_angle + offset, fire_data.power * self.drag, self.power, obj, self.color))
            time.sleep(self.time_between)

@dataclass
class MachineGun(Weapon):
    spread:float = 0.2
    power:int = 3
    color:RGB = (200, 200, 100)
    drag:float = 0.9
    shot_count:int = 30
    time_between:float = 0.09

    def __post_init__(self):
        self.behavior = Bomb_Anim(0, 0, end_time=10, radius=1)

    def fire(self, fire_data, proj_list:list):
        thread = threading.Thread(target=self.volley, args=(fire_data, proj_list))
        thread.start()

    def volley(self, fire_data, proj_list:list):
        obj = copy.deepcopy(self.behavior)
        for _ in range(self.shot_count):
            obj = copy.deepcopy(self.behavior)
            offset = (np.random.rand() - 0.5) * 2 * self.spread
            proj_list.append(Projectile(*fire_data.xy, fire_data.fire_angle + offset, fire_data.power * self.drag, self.power, obj, self.color))
            time.sleep(self.time_between)

@dataclass
class OrbitalLazer(Weapon):
    power:int=10
    color:RGB = (107, 73, 128)

    def __post_init__(self):
        self.behavior = Lazer_Anim(0, 0, end_time=30, blast_radius=6)

    def fire(self, fire_data, proj_list:list):
        proj_list.append(Projectile(*fire_data.xy, fire_data.fire_angle, fire_data.power, self.power, self.behavior, self.color))




        

    


