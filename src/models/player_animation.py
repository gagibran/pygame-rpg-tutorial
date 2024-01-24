import pygame


class PlayerAnimation:
    def __init__(self):
        self.amount_of_animation_sprites = 4
        self.walk_up_surfaces = [
            pygame.image.load(
                f'src/assets/player/up/up_{animation_index}.png'
            ).convert_alpha()
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.walk_down_surfaces = [
            pygame.image.load(
                f'src/assets/player/down/down_{animation_index}.png'
            ).convert_alpha()
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.walk_left_surfaces = [
            pygame.image.load(
                f'src/assets/player/left/left_{animation_index}.png'
            ).convert_alpha()
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.walk_right_surfaces = [
            pygame.image.load(
                f'src/assets/player/right/right_{animation_index}.png'
            ).convert_alpha()
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.up_idle = pygame.image.load(
            f'src/assets/player/up_idle/up_idle.png'
        ).convert_alpha()
        self.down_idle = pygame.image.load(
            f'src/assets/player/down_idle/down_idle.png'
        ).convert_alpha()
        self.left_idle = pygame.image.load(
            f'src/assets/player/left_idle/left_idle.png'
        ).convert_alpha()
        self.right_idle = pygame.image.load(
            f'src/assets/player/right_idle/right_idle.png'
        ).convert_alpha()
        self.walk_index = 0.0
