import pygame
from .terrain import Terrain
from .surface_helper import Helper
from .player import Tank
from .controller import Controller, Controller2
from .projectile import Projectile
from .behavior import Behavior
from dataclasses import dataclass

@dataclass
class Game_Objects:
    players:list
    controllers:list
    projs:list
    behave:list


def create_surface(res, block_size):
    return pygame.Surface((int(res[0]/block_size), int(res[1]/block_size)), pygame.SRCALPHA)

class Game:
    def __init__(self, res, block_size):
        self.res = res
        self.block_size = block_size
        self.top_surf = create_surface(self.res, self.block_size)
        self.terrain_surf = create_surface(self.res, self.block_size)
        self.terrain = Terrain(self.terrain_surf)
        self.helper = Helper(self, self.top_surf, self.terrain)

        self.player = Tank(100, 100)
        self.player2 = Tank(150, 100)
        self.controller = Controller(self.player, self)
        self.controller2 = Controller2(self.player2, self)

        self.projectiles:list[Projectile] = []
        self.behave:list[Behavior] = []

        self.counter = 0
        self.tick_rate = 4

    def update(self):
        self.counter += 1
        self.controller.handle_events()
        self.controller2.handle_events()
        if self.counter % self.tick_rate == 0:
            self.top_surf.fill((0, 0, 0, 0))
            self.terrain.update()
            self.player.render(self.helper)
            self.player2.render(self.helper)

            for projectile in self.projectiles:
                projectile.render(self.helper)
                if not projectile.status:
                    self.behave.append(projectile.get_anim())
                    self.projectiles.remove(projectile)

            for anim in self.behave:
                anim.step(self.helper)
                if anim.over():
                    self.behave.remove(anim)
    
    def get_surface(self) -> pygame.Surface:
        combined_surface = self.terrain_surf.copy()
        combined_surface.blit(self.top_surf, (0,0))
        return combined_surface

    

