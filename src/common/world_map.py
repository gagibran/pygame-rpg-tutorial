import random
import pygame
from common.settings import CAMERA_INITIAL_CENTER_POSITION, TILE_SIZE
from common.tools import get_map_layer_from_csv
from enums.map_layers import MapLayer
from enums.sprite_type import SpriteType
from sprites.tile import Tile
from sprites.player import Player
from sprites.custom_groups.camera_group import CameraGroup


class WorldMap:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.ground_surface = pygame.image.load(
            'src/assets/world_map/ground.png'
        ).convert()
        self.ground_rect = self.ground_surface.get_rect(
            center=CAMERA_INITIAL_CENTER_POSITION
        )
        self.visible_sprites_group = CameraGroup(self.ground_surface, self.ground_rect)
        self.collidable_sprites_group = pygame.sprite.Group()
        self.player: Player = None
        self.add_sprites_to_world_map()

    def add_layer_by_type(
        self, tile: str, layer_type: MapLayer, tile_index: int, row_index: int
    ):
        tile_topleft_position = (
            tile_index * TILE_SIZE[0] + self.ground_rect.topleft[0],
            row_index * TILE_SIZE[1] + self.ground_rect.topleft[1],
        )
        match layer_type:
            case MapLayer.BORDER_DELIMITERS:
                self.add_border_delimiters(tile_topleft_position)
            case MapLayer.GRASS:
                self.add_grass(tile_topleft_position)
            case MapLayer.OBJECTS:
                self.add_objects(tile, tile_topleft_position)

    def process_layer(self, layer: list[list[str]], layer_type: MapLayer):
        for row_index, row in enumerate(layer):
            for tile_index, tile in enumerate(row):
                if tile != '-1':
                    self.add_layer_by_type(tile, layer_type, tile_index, row_index)

    def add_border_delimiters(self, tile_topleft_position: tuple[int, int]):
        Tile(
            tile_topleft_position,
            [self.collidable_sprites_group],
            SpriteType.INVISIBLE,
        )

    def add_grass(self, tile_topleft_position: tuple[int, int]):
        grass_image_index = random.randint(1, 3)
        grass_surface = pygame.image.load(
            f'src/assets/grass/grass_{grass_image_index}.png'
        ).convert_alpha()
        Tile(
            tile_topleft_position,
            [self.visible_sprites_group, self.collidable_sprites_group],
            SpriteType.GRASS,
            surface=grass_surface,
        )

    def add_objects(self, tile: str, tile_topleft_position: tuple[int, int]):
        grass_surface = pygame.image.load(
            f'src/assets/objects/{tile}.png'
        ).convert_alpha()
        Tile(
            tile_topleft_position,
            [self.visible_sprites_group, self.collidable_sprites_group],
            SpriteType.OBJECT,
            surface=grass_surface,
        )

    def add_sprites_to_world_map(self):
        map_layers = {
            MapLayer.BORDER_DELIMITERS: get_map_layer_from_csv(
                'src/data/map/border_delimiter.csv'
            ),
            MapLayer.GRASS: get_map_layer_from_csv('src/data/map/grass.csv'),
            MapLayer.OBJECTS: get_map_layer_from_csv('src/data/map/object.csv'),
        }
        for layer_type, layer in map_layers.items():
            self.process_layer(layer, layer_type)
        self.player = Player(
            [self.visible_sprites_group],
            self.collidable_sprites_group,
        )

    def render(self):
        self.visible_sprites_group.draw_camera(self.player.rect.center)
        self.visible_sprites_group.update()
