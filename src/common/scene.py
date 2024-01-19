import pygame
import common.constants
import sprites.tile
import sprites.player
import sprites.custom_groups.camera_group


class Scene:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.visible_sprites_group = sprites.custom_groups.camera_group.CameraGroup()
        self.collidable_sprites_group = pygame.sprite.Group()
        self.player: sprites.player.Player = None
        self.create_world_map()

    def create_world_map(self):
        for row_index, row in enumerate(common.constants.WORLD_MAP):
            for tile_index, tile in enumerate(row):
                x = row_index * common.constants.TILE_HORIZONTAL_SIZE
                y = tile_index * common.constants.TILE_VERTICAL_SIZE
                if tile == 'x':
                    sprites.tile.Tile(
                        (x, y),
                        [self.visible_sprites_group, self.collidable_sprites_group],
                    )
                if tile == 'p':
                    self.player = sprites.player.Player(
                        (x, y),
                        [self.visible_sprites_group],
                        self.collidable_sprites_group,
                    )

    def render(self):
        self.visible_sprites_group.draw_camera(self.player)
        self.visible_sprites_group.update()
