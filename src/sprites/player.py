import pygame
from common.settings import (
    PLAYER_INITIAL_CENTER_POSITION,
    PLAYER_RUN_ANIMATION_SPEED,
    PLAYER_RUN_SPEED,
    PLAYER_WALK_ANIMATION_SPEED,
    PLAYER_WALK_SPEED,
    TILE_SIZE,
)
from common.utils import get_alpha_converted_surface_from_image
from enums.collision_direction import CollisionDirection
from enums.player_direction import PlayerDirection
from enums.sprite_type import SpriteType
from models.player_animation import PlayerAnimation
from sprites.tile import Tile


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites_group: pygame.sprite.Group,
    ):
        super().__init__(groups)
        self.image = get_alpha_converted_surface_from_image(
            'player/down_idle/down_idle.png'
        )
        self.rect = self.image.get_rect(center=PLAYER_INITIAL_CENTER_POSITION)
        self.direction_vector = pygame.math.Vector2()
        self.speed = PLAYER_WALK_SPEED
        self.collidable_sprites_group = collidable_sprites_group
        self.player_animation = PlayerAnimation()
        self.player_animation_speed = PLAYER_WALK_ANIMATION_SPEED
        self.player_direction = PlayerDirection.DOWN

    def process_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed = PLAYER_RUN_SPEED
            self.player_animation_speed = PLAYER_RUN_ANIMATION_SPEED
        else:
            self.speed = PLAYER_WALK_SPEED
            self.player_animation_speed = PLAYER_WALK_ANIMATION_SPEED
        if keys[pygame.K_d]:
            self.direction_vector.x = 1
        elif keys[pygame.K_a]:
            self.direction_vector.x = -1
        else:
            self.direction_vector.x = 0
        if keys[pygame.K_s]:
            self.direction_vector.y = 1
        elif keys[pygame.K_w]:
            self.direction_vector.y = -1
        else:
            self.direction_vector.y = 0

    def get_player_direction(self):
        if self.direction_vector.y == -1 and self.direction_vector.x == -1:
            self.player_direction = PlayerDirection.UP_PLUS_LEFT
        elif self.direction_vector.y == -1 and self.direction_vector.x == 1:
            self.player_direction = PlayerDirection.UP_PLUS_RIGHT
        elif self.direction_vector.y == 1 and self.direction_vector.x == -1:
            self.player_direction = PlayerDirection.DOWN_PLUS_LEFT
        elif self.direction_vector.y == 1 and self.direction_vector.x == 1:
            self.player_direction = PlayerDirection.DOWN_PLUS_RIGHT
        elif self.direction_vector.y == -1:
            self.player_direction = PlayerDirection.UP
        elif self.direction_vector.y == 1:
            self.player_direction = PlayerDirection.DOWN
        elif self.direction_vector.x == -1:
            self.player_direction = PlayerDirection.LEFT
        elif self.direction_vector.x == 1:
            self.player_direction = PlayerDirection.RIGHT

    def set_idle_position(self):
        if self.direction_vector.y == 0 and self.direction_vector.x == 0:
            if self.player_direction == PlayerDirection.UP:
                self.image = self.player_animation.up_idle
            elif self.player_direction == PlayerDirection.DOWN:
                self.image = self.player_animation.down_idle
            elif (
                self.player_direction == PlayerDirection.LEFT
                or self.player_direction == PlayerDirection.UP_PLUS_LEFT
                or self.player_direction == PlayerDirection.DOWN_PLUS_LEFT
            ):
                self.image = self.player_animation.left_idle
            elif (
                self.player_direction == PlayerDirection.RIGHT
                or self.player_direction == PlayerDirection.UP_PLUS_RIGHT
                or self.player_direction == PlayerDirection.DOWN_PLUS_RIGHT
            ):
                self.image = self.player_animation.right_idle

    def animate_player(self):
        self.player_animation.walk_index += self.player_animation_speed
        if (
            int(self.player_animation.walk_index)
            >= self.player_animation.amount_of_animation_sprites
        ):
            self.player_animation.walk_index = 0.0
        if self.player_direction == PlayerDirection.UP:
            self.image = self.player_animation.walk_up_surfaces[
                int(self.player_animation.walk_index)
            ]
        elif self.player_direction == PlayerDirection.DOWN:
            self.image = self.player_animation.walk_down_surfaces[
                int(self.player_animation.walk_index)
            ]
        elif (
            self.player_direction == PlayerDirection.LEFT
            or self.player_direction == PlayerDirection.UP_PLUS_LEFT
            or self.player_direction == PlayerDirection.DOWN_PLUS_LEFT
        ):
            self.image = self.player_animation.walk_left_surfaces[
                int(self.player_animation.walk_index)
            ]
        elif (
            self.player_direction == PlayerDirection.RIGHT
            or self.player_direction == PlayerDirection.UP_PLUS_RIGHT
            or self.player_direction == PlayerDirection.DOWN_PLUS_RIGHT
        ):
            self.image = self.player_animation.walk_right_surfaces[
                int(self.player_animation.walk_index)
            ]

    def move(self):
        if self.direction_vector.magnitude() > 0:
            self.direction_vector = self.direction_vector.normalize()
        self.rect.x += self.direction_vector.x * self.speed
        self.handle_collision(CollisionDirection.HORIZONTAL)
        self.rect.y += self.direction_vector.y * self.speed
        self.handle_collision(CollisionDirection.VERTICAL)

    def calculate_player_hitbox_size(self, collidable_sprite: Tile):
        if collidable_sprite.sprite_type == SpriteType.INVISIBLE:
            self.rect.height = TILE_SIZE[1]
        elif collidable_sprite.rect.height > TILE_SIZE[1]:
            self.rect.height = TILE_SIZE[1] / 2.5
        else:
            self.rect.height = TILE_SIZE[1] - 10

    def handle_collision(self, collision_direction: CollisionDirection):
        collidable_sprite: Tile
        for collidable_sprite in self.collidable_sprites_group:
            if (
                self.direction_vector.x > 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_direction == CollisionDirection.HORIZONTAL
            ):
                self.rect.right = collidable_sprite.rect.left
            if (
                self.direction_vector.x < 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_direction == CollisionDirection.HORIZONTAL
            ):
                self.rect.left = collidable_sprite.rect.right
            if (
                self.direction_vector.y > 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_direction == CollisionDirection.VERTICAL
            ):
                self.rect.bottom = collidable_sprite.rect.top
            if (
                self.direction_vector.y < 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_direction == CollisionDirection.VERTICAL
            ):
                self.rect.top = collidable_sprite.rect.bottom
            self.calculate_player_hitbox_size(collidable_sprite)

    def update(self):
        self.process_input()
        self.get_player_direction()
        self.move()
        self.animate_player()
        self.set_idle_position()
