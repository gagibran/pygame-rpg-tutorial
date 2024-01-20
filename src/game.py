# Based on this tutorial: https://www.youtube.com/watch?v=QU1pPzEGrqw.

import sys
import pygame
from common.constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_TITLE, FPS
from common.scene import Scene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.scene = Scene()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.screen.fill('black')
            self.process_events()
            self.scene.render()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Game().run()
