import pygame as pg
from typing import Protocol


class Player(Protocol):
    def move_left(self):
        ...
    def move_right(self):
        ...
    def raise_power(self):
        ...
    def lower_power(self):
        ...

    def get_random_weapon(self):
        ...
    def calc_fire_angle(self):
        ...
    def fire(self):
        ...


class Controller:
    def __init__(self, player:Player, game):
        self.player = player
        self.game = game
        self.is_firing = False

    def handle_events(self):
        key_presses = pg.key.get_pressed()

        if key_presses[pg.K_a]:
            self.player.move_left()
        elif key_presses[pg.K_d]:
            self.player.move_right()

        if key_presses[pg.K_w]:
            self.player.raise_power()
        elif key_presses[pg.K_s]:
            self.player.lower_power()

        mouse_pos = pg.mouse.get_pos()
        self.player.calc_fire_angle(mouse_pos[0]/self.game.block_size, self.game.terrain_surf.get_height() - mouse_pos[1]/self.game.block_size)

        if key_presses[pg.K_r]:
            self.player.get_random_weapon()

        if key_presses[pg.K_SPACE] and not self.is_firing:
            self.player.fire()
            self.is_firing = True
        else:
            if not key_presses[pg.K_SPACE]:
                self.is_firing = False

class Controller2:
    def __init__(self, player:Player, game):
        self.player = player
        self.game = game
        self.is_firing = False

    def handle_events(self):
        key_presses = pg.key.get_pressed()

        if key_presses[pg.K_LEFT]:
            self.player.move_left()
        elif key_presses[pg.K_RIGHT]:
            self.player.move_right()

        if key_presses[pg.K_UP]:
            self.player.raise_power()
        elif key_presses[pg.K_DOWN]:
            self.player.lower_power()

        mouse_pos = pg.mouse.get_pos()
        self.player.calc_fire_angle(mouse_pos[0]/self.game.block_size, self.game.terrain_surf.get_height() - mouse_pos[1]/self.game.block_size)

        if key_presses[pg.K_n]:
            self.player.get_random_weapon()

        if key_presses[pg.K_m] and not self.is_firing:
            self.player.fire()
            self.is_firing = True
        else:
            if not key_presses[pg.K_m]:
                self.is_firing = False
