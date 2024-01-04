import pygame
from .surface_helper import Helper
import numpy as np
from .projectile import Projectile
from .weapon import BirdShot, SingleShot, Volley, MachineGun, OrbitalLazer

#class Tank:
    #pass

class Player:
    pass

class CPU:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.power = 10

    def calc_fire_angle(self, target_x, target_y):
        delta_x = target_x - self.x
        delta_y = target_y - self.y
        time = np.random.randint(10,20)
        g=0.01
        return (np.arcsin(delta_y/(self.power*time)-(g*time)/(2*self.power)) + np.arccos(delta_x/(self.power*time)))/2

class Fire_Data:
    def __init__(self, tank):
        self.fire_angle:float = 0
        self.max_power:float = 20
        self.min_power:float = 5
        self.power:float = 1
        self.tank:"Tank" = tank

    @property
    def x(self):
        return self.tank.get_barrel_x_y()[0]
    @property
    def y(self):
        return self.tank.get_barrel_x_y()[1]
    @property
    def xy(self):
        return self.tank.get_barrel_x_y()
        

class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.fire_data = Fire_Data(tank=self)
        self.proj = []

        self.next_proj = None
        self.get_random_weapon()

        self.max_steepness = np.radians(70)

        self.sprite = Tank_Sprite("/Users/liam/Desktop/TankGameV3/assets/tank1.png")

    def get_random_weapon(self):
        option = np.random.randint(0,5)

        if option == 1:
            shot = BirdShot()
        elif option == 0:
            shot = SingleShot()
        elif option == 2:
            shot = Volley()
        elif option == 3:
            shot = MachineGun()
        elif option == 4:
            shot = OrbitalLazer()

        self.next_proj = shot

    def move_left(self):
        self.vx -= 0.1

    def move_right(self):
        self.vx += 0.1

    def calc_fire_angle(self, m_x, m_y):
        self.fire_data.fire_angle = np.arctan2(m_y-self.y, m_x-self.x)

    def raise_power(self):
        if self.fire_data.power < self.fire_data.max_power:
            self.fire_data.power += 0.01

    def lower_power(self):
        if self.fire_data.power > self.fire_data.min_power:
            self.fire_data.power -= 0.01

    def fire(self):
        self.next_proj.fire(self.fire_data, self.proj)
        self.get_random_weapon()

    def update(self, helper:Helper):
        angle_of_terrain = helper.angle_of_terrain_at_xcor(self.x)
        if self.vx > 0:
            if -angle_of_terrain <= self.max_steepness:
                self.x += self.vx
        else:
            if angle_of_terrain <= self.max_steepness:
                self.x += self.vx

        self.vx *= 0.4

        if helper.get_average_height_at_xcor(self.x) + 2 < self.y:
            self.y -= self.vy
            self.vy += 0.1
        else:
            self.y = helper.get_average_height_at_xcor(self.x) + 2
            self.vy = 0


        for proj in self.proj:
            helper.add_to_projectile_list(proj)
            self.proj.remove(proj)
        

    def render(self, helper:Helper):
        self.update(helper)
        self.sprite.draw_tank(helper, self)

    def get_barrel_x_y(self):
        return self.x + np.cos(self.fire_data.fire_angle) * 10, self.y + np.sin(self.fire_data.fire_angle) * 10 + 4
        
class Tank_Sprite:
    def __init__(self, image_path):
        self.tank_image = pygame.transform.flip(pygame.transform.scale(pygame.image.load(image_path),(20,10)), flip_x=False, flip_y=True)
        self.original_tank_image = self.tank_image

    def draw_tank(self, helper:Helper, tank: Tank):
        top_surf = helper.get_top_surf()
        rotated_tank_image = pygame.transform.rotate(self.original_tank_image, np.degrees(helper.angle_of_terrain_at_xcor(tank.x)))
        rect = rotated_tank_image.get_rect(center=(tank.x, tank.y + 4))
        pygame.draw.line(top_surf, (150, 150, 150), (tank.x, tank.y + 4), tank.get_barrel_x_y())
        top_surf.blit(rotated_tank_image, rect.topleft)
