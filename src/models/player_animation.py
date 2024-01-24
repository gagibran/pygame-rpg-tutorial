from common.utils import get_alpha_converted_surface_from_image


class PlayerAnimation:
    def __init__(self):
        self.amount_of_animation_sprites = 4
        self.walk_up_surfaces = [
            get_alpha_converted_surface_from_image(
                f'player/up/up_{animation_index}.png'
            )
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.walk_down_surfaces = [
            get_alpha_converted_surface_from_image(
                f'player/down/down_{animation_index}.png'
            )
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.walk_left_surfaces = [
            get_alpha_converted_surface_from_image(
                f'player/left/left_{animation_index}.png'
            )
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.walk_right_surfaces = [
            get_alpha_converted_surface_from_image(
                f'player/right/right_{animation_index}.png'
            )
            for animation_index in range(0, self.amount_of_animation_sprites)
        ]
        self.up_idle = get_alpha_converted_surface_from_image(
            f'player/up_idle/up_idle.png'
        )
        self.down_idle = get_alpha_converted_surface_from_image(
            f'player/down_idle/down_idle.png'
        )
        self.left_idle = get_alpha_converted_surface_from_image(
            f'player/left_idle/left_idle.png'
        )
        self.right_idle = get_alpha_converted_surface_from_image(
            f'player/right_idle/right_idle.png'
        )
        self.walk_index = 0.0
