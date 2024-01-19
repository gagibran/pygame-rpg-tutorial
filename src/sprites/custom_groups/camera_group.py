import pygame
import custom_types.types
import common.constants
import sprites.player


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.camera_offset_x = 0
        self.camera_offset_y = 0

    def get_visible_sprite_y_position(
        self, visible_sprite: custom_types.types.VisibleSprite
    ):
        return visible_sprite.rect.y

    def draw_camera(self, player: sprites.player.Player):
        self.camera_offset_x += (
            player.rect.centerx
            - common.constants.SCREEN_WIDTH // 2
            - self.camera_offset_x
        ) * common.constants.CAMERA_SPEED
        self.camera_offset_y += (
            player.rect.centery
            - common.constants.SCREEN_HEIGHT // 2
            - self.camera_offset_y
        ) * common.constants.CAMERA_SPEED
        camera_offset_vector = pygame.math.Vector2(
            self.camera_offset_x, self.camera_offset_y
        )
        sprite: custom_types.types.VisibleSprite
        for sprite in sorted(self.sprites(), key=self.get_visible_sprite_y_position):
            offset_sprite_vector = sprite.rect.topleft - camera_offset_vector
            pygame.display.get_surface().blit(sprite.image, offset_sprite_vector)
