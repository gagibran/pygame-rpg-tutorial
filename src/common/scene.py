import pygame
from common.constants import TILE_SIZE
from sprites.tile import Tile
from sprites.player import Player
from sprites.custom_groups.camera_group import CameraGroup


class Scene:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites_group = CameraGroup()
        self.collidable_sprites_group = pygame.sprite.Group()
        self.player: Player = None
        self.create_world_map()

    def create_world_map(self):
        # for row_index, row in enumerate(WORLD_MAP):
        #     for tile_index, tile in enumerate(row):
        #         x = row_index * TILE_HORIZONTAL_SIZE
        #         y = tile_index * TILE_VERTICAL_SIZE
        #         if tile == 'x':
        #             Tile(
        #                 (x, y),
        #                 [self.visible_sprites_group, self.collidable_sprites_group],
        #             )
        #         if tile == 'p':
        #             self.player = Player(
        #                 (x, y),
        #                 [self.visible_sprites_group],
        #                 self.collidable_sprites_group,
        #             )
        self.player = Player(
            [self.visible_sprites_group],
            self.collidable_sprites_group,
        )

    def render(self):
        self.visible_sprites_group.draw_camera(self.player)
        self.visible_sprites_group.update()
