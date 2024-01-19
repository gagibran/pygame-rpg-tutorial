import pygame
import common.constants
import common.enums
import sprites.tile


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        topleft_position: tuple[int, int],
        groups: list[pygame.sprite.Group],
        collidable_sprites_group: pygame.sprite.Group,
    ):
        super().__init__(groups)
        self.image = pygame.image.load('src/assets/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=topleft_position)
        self.rect = self.rect.inflate(0, -10)
        self.direction_vector = pygame.math.Vector2()
        self.speed = common.constants.PLAYER_INITIAL_SPEED
        self.collidable_sprites_group = collidable_sprites_group

    def process_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            self.speed = common.constants.PLAYER_INITIAL_SPEED * 2
        else:
            self.speed = common.constants.PLAYER_INITIAL_SPEED
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
        self.handle_collision(common.enums.CollisionType.HORIZONTAL)
        self.rect.y += self.direction_vector.y * self.speed
        self.handle_collision(common.enums.CollisionType.VERTICAL)

    def handle_collision(self, collision_type: common.enums.CollisionType):
        collidable_sprite: sprites.tile.Tile
        for collidable_sprite in self.collidable_sprites_group:
            if (
                self.direction_vector.x > 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_type == common.enums.CollisionType.HORIZONTAL
            ):
                self.rect.right = collidable_sprite.rect.left
            if (
                self.direction_vector.x < 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_type == common.enums.CollisionType.HORIZONTAL
            ):
                self.rect.left = collidable_sprite.rect.right
            if (
                self.direction_vector.y > 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_type == common.enums.CollisionType.VERTICAL
            ):
                self.rect.bottom = collidable_sprite.rect.top
            if (
                self.direction_vector.y < 0
                and collidable_sprite.rect.colliderect(self.rect)
                and collision_type == common.enums.CollisionType.VERTICAL
            ):
                self.rect.top = collidable_sprite.rect.bottom

    def update(self):
        self.process_input()
        self.move()
