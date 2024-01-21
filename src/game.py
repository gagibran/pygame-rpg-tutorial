# Based on this tutorial: https://www.youtube.com/watch?v=QU1pPzEGrqw.

import sys
import pygame
from common.settings import SCREEN_SIZE, GAME_TITLE, FPS
from common.world_map import WorldMap


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()
        self.world_map = WorldMap()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def run(self):
        while True:
            self.screen.fill('#71ddee')
            self.process_events()
            self.world_map.render()
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == '__main__':
    Game().run()
