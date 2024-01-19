import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(
        self, topleft_position: tuple[int, int], groups: list[pygame.sprite.Group]
    ):
        super().__init__(groups)
        self.image = pygame.image.load('src/assets/test/rock.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=topleft_position)
        self.rect = self.rect.inflate(0, -20)
