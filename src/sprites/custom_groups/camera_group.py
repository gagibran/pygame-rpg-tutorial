import pygame
from custom_types.types import VisibleSprite
from common.settings import (
    SCREEN_SIZE,
    CAMERA_SPEED,
)


class CameraGroup(pygame.sprite.Group):
    def __init__(self, ground_surface: pygame.Surface, ground_rect: pygame.Rect):
        super().__init__()
        self.half_screen_width = SCREEN_SIZE[0] / 2
        self.half_screen_height = SCREEN_SIZE[1] / 2
        self.ground_surface = ground_surface
        self.ground_rect = ground_rect
        self.screen = pygame.display.get_surface()
        self.screen_to_player_offset = [0, 0]

    def get_visible_sprite_y_position(self, visible_sprite: VisibleSprite):
        return visible_sprite.rect.y

    def calculate_screen_to_player_offset(
        self, player_center_position: tuple[int, int]
    ):
        self.screen_to_player_offset[0] += (
            player_center_position[0]
            - self.half_screen_width
            - self.screen_to_player_offset[0]
        ) * CAMERA_SPEED
        self.screen_to_player_offset[1] += (
            player_center_position[1]
            - self.half_screen_height
            - self.screen_to_player_offset[1]
        ) * CAMERA_SPEED

    def draw_ground_and_sprites(self):
        screen_to_player_offset_vector = pygame.math.Vector2(
            self.screen_to_player_offset[0], self.screen_to_player_offset[1]
        )
        self.screen.blit(
            self.ground_surface,
            self.ground_rect.topleft - screen_to_player_offset_vector,
        )
        sprite: VisibleSprite
        for sprite in sorted(self.sprites(), key=self.get_visible_sprite_y_position):
            self.screen.blit(
                sprite.image,
                sprite.rect.topleft - screen_to_player_offset_vector,
            )

    def draw_camera(self, player_center_position: tuple[int, int]):
        self.calculate_screen_to_player_offset(player_center_position)
        self.draw_ground_and_sprites()
