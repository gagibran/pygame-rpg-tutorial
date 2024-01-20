import pygame
from custom_types.types import VisibleSprite
from common.constants import (
    MAX_CAMERA_ZOOM,
    MIN_CAMERA_ZOOM,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    CAMERA_SPEED,
    ZOOM_SPEED,
)
from sprites.player import Player


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.get_surface()
        self.camera_movement_offset_x = 0
        self.camera_movement_offset_y = 0
        self.zoom = 1
        self.ground_surface = pygame.image.load(
            'src/assets/world_map/ground.png'
        ).convert()
        self.ground_rect = self.ground_surface.get_rect()

    def get_visible_sprite_y_position(self, visible_sprite: VisibleSprite):
        return visible_sprite.rect.y

    def handle_zoom_keyboard_input(self):
        keys = pygame.key.get_pressed()
        if (
            (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
            and keys[pygame.K_EQUALS]
            and self.zoom < MAX_CAMERA_ZOOM
        ):
            self.zoom += ZOOM_SPEED
        elif (
            (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
            and keys[pygame.K_MINUS]
            and self.zoom > MIN_CAMERA_ZOOM
        ):
            self.zoom -= ZOOM_SPEED

    def draw_zoom_surface(self):
        zoom_surface = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        return zoom_surface

    def calculate_camera_movement_offset_based_on_player_position(self, player: Player):
        self.camera_movement_offset_x += (
            player.rect.centerx - SCREEN_WIDTH // 2 - self.camera_movement_offset_x
        ) * CAMERA_SPEED
        self.camera_movement_offset_y += (
            player.rect.centery - SCREEN_HEIGHT // 2 - self.camera_movement_offset_y
        ) * CAMERA_SPEED

    def draw_ground_and_sprites_onto_zoom_surface(self, zoom_surface: pygame.Surface):
        camera_offset_vector = pygame.math.Vector2(
            self.camera_movement_offset_x, self.camera_movement_offset_y
        )
        zoom_surface.blit(
            self.ground_surface, self.ground_rect.topleft - camera_offset_vector
        )
        sprite: VisibleSprite
        for sprite in sorted(self.sprites(), key=self.get_visible_sprite_y_position):
            zoom_surface.blit(sprite.image, sprite.rect.topleft - camera_offset_vector)

    def handle_zoom(self, zoom_surface: pygame.Surface):
        zoom_surface = pygame.transform.scale(
            zoom_surface,
            (
                zoom_surface.get_width() * self.zoom,
                zoom_surface.get_height() * self.zoom,
            ),
        )
        zoom_rect = zoom_surface.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        )
        self.screen.blit(zoom_surface, zoom_rect)

    def draw_camera(self, player: Player):
        zoom_surface = self.draw_zoom_surface()
        self.calculate_camera_movement_offset_based_on_player_position(player)
        self.draw_ground_and_sprites_onto_zoom_surface(zoom_surface)
        self.handle_zoom_keyboard_input()
        self.handle_zoom(zoom_surface)
