import pygame
from common.settings import (
    PLAYER_INITIAL_CENTER_POSITION,
    PLAYER_INITIAL_SPEED,
    TILE_SIZE,
)
from enums.collision_direction import CollisionDirection
from enums.sprite_type import SpriteType
from sprites.tile import Tile


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        groups: list[pygame.sprite.Group],
        collidable_sprites_group: pygame.sprite.Group,
    ):
        super().__init__(groups)
        self.image = pygame.image.load('src/assets/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(center=PLAYER_INITIAL_CENTER_POSITION)
        self.direction_vector = pygame.math.Vector2()
        self.speed = PLAYER_INITIAL_SPEED
        self.collidable_sprites_group = collidable_sprites_group

    def process_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed = PLAYER_INITIAL_SPEED * 2
        else:
            self.speed = PLAYER_INITIAL_SPEED
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
        self.move()
