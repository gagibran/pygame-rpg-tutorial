import pygame
from common.settings import TILE_SIZE
from enums.sprite_type import SpriteType


class Tile(pygame.sprite.Sprite):
    def __init__(
        self,
        topleft_position: tuple[int, int],
        belonging_groups: list[pygame.sprite.Group],
        sprite_type: SpriteType,
        surface=pygame.Surface(TILE_SIZE),
    ):
        super().__init__(belonging_groups)
        self.sprite_type = sprite_type
        self.image = surface
        self.rect = self.calculate_tile_size_by_sprite_type(topleft_position)
        self.rect = self.rect.inflate(0, -40)

    def calculate_tile_size_by_sprite_type(self, topleft_position: tuple[int, int]):
        rect_topleft = topleft_position
        if self.sprite_type == SpriteType.OBJECT:
            rect_topleft = (topleft_position[0], topleft_position[1] - TILE_SIZE[1])
        return self.image.get_rect(topleft=rect_topleft)
