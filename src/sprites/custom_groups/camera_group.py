import pygame
from custom_types.types import VisibleSprite
from common.constants import (
    CAMERA_INITIAL_CENTER_POSITION,
    MAX_CAMERA_ZOOM,
    MIN_CAMERA_ZOOM,
    SCREEN_SIZE,
    CAMERA_SPEED,
    ZOOM_SPEED,
)
from sprites.player import Player


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.half_screen_width = SCREEN_SIZE[0] // 2
        self.half_screen_height = SCREEN_SIZE[1] // 2
        self.ground_surface = pygame.image.load(
            'src/assets/world_map/ground.png'
        ).convert()
        self.ground_rect = self.ground_surface.get_rect(
            center=CAMERA_INITIAL_CENTER_POSITION
        )
        self.screen = pygame.display.get_surface()
        self.screen_to_player_offset = [0, 0]
        self.zoom = 1
        self.zoom_surface_size = (
            SCREEN_SIZE[0] / MIN_CAMERA_ZOOM,
            SCREEN_SIZE[1] / MIN_CAMERA_ZOOM,
        )

    def get_visible_sprite_y_position(self, visible_sprite: VisibleSprite):
        return visible_sprite.rect.y

    def draw_zoom_surface(self):
        zoom_surface = pygame.Surface(self.zoom_surface_size, pygame.SRCALPHA)
        return zoom_surface

    def calculate_screen_to_player_offset(self, player: Player):
        self.screen_to_player_offset[0] += (
            player.rect.centerx
            - self.half_screen_width
            - self.screen_to_player_offset[0]
        ) * CAMERA_SPEED
        self.screen_to_player_offset[1] += (
            player.rect.centery
            - self.half_screen_height
            - self.screen_to_player_offset[1]
        ) * CAMERA_SPEED

    def draw_ground_and_sprites_onto_zoom_surface(self, zoom_surface: pygame.Surface):
        screen_to_player_offset_vector = pygame.math.Vector2(
            self.screen_to_player_offset[0], self.screen_to_player_offset[1]
        )
        zoom_to_screen_offset_vector = pygame.math.Vector2(
            (self.zoom_surface_size[0] - SCREEN_SIZE[0]) // 2,
            (self.zoom_surface_size[1] - SCREEN_SIZE[1]) // 2,
        )
        camera_movement_offset_vector = (
            screen_to_player_offset_vector - zoom_to_screen_offset_vector
        )
        zoom_surface.blit(
            self.ground_surface,
            self.ground_rect.topleft - camera_movement_offset_vector,
        )
        sprite: VisibleSprite
        for sprite in sorted(self.sprites(), key=self.get_visible_sprite_y_position):
            zoom_surface.blit(
                sprite.image,
                sprite.rect.topleft - camera_movement_offset_vector,
            )

    def handle_zoom_keyboard_input(self):
        keys = pygame.key.get_pressed()
        if (
            (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
            and keys[pygame.K_EQUALS]
            and self.zoom < MAX_CAMERA_ZOOM
        ):
            self.zoom = round(self.zoom + ZOOM_SPEED, 2)
        elif (
            (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT])
            and keys[pygame.K_MINUS]
            and self.zoom > MIN_CAMERA_ZOOM
        ):
            self.zoom = round(self.zoom - ZOOM_SPEED, 2)
        elif (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and keys[pygame.K_0]:
            self.zoom = 1

    def apply_zoom(self, zoom_surface: pygame.Surface):
        zoom_surface = pygame.transform.scale(
            zoom_surface,
            (
                zoom_surface.get_width() * self.zoom,
                zoom_surface.get_height() * self.zoom,
            ),
        )
        zoom_rect = zoom_surface.get_rect(
            center=(self.half_screen_width, self.half_screen_height)
        )
        self.screen.blit(zoom_surface, zoom_rect)

    def draw_camera(self, player: Player):
        zoom_surface = self.draw_zoom_surface()
        self.calculate_screen_to_player_offset(player)
        self.draw_ground_and_sprites_onto_zoom_surface(zoom_surface)
        self.handle_zoom_keyboard_input()
        self.apply_zoom(zoom_surface)
