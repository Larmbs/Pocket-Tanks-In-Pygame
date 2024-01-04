import pygame
from src.game import Game
import sys

class App:
    def __init__(self, WIDTH=900, HEIGHT=800):
        self.RES = WIDTH, HEIGHT
        pygame.init()
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.game = Game(self.RES, 3)

    def update(self):
        self.game.update()

    def run(self):
        while True:
            self.update()

            [self.exit() for event in pygame.event.get() if event.type == pygame.QUIT]

            self.screen.blit(pygame.transform.flip(pygame.transform.scale(self.game.get_surface(), self.RES), flip_x=False, flip_y=True), (0,0))
            self.clock.tick()
            pygame.display.set_caption(f"Frame Rate: {int(self.clock.get_fps())} FPS")
            pygame.display.flip()


    def exit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()
    