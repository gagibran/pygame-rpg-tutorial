import csv
import pathlib
import pygame

assets_base_path = pathlib.Path().resolve() / 'src' / 'assets'


def get_alpha_converted_surface_from_image(image_partial_path: str):
    full_path = assets_base_path / 'images' / image_partial_path
    return pygame.image.load(full_path).convert_alpha()


def get_map_layer_from_csv(map_layer_partial_path: str):
    full_path = assets_base_path / 'csv' / 'map_layers' / map_layer_partial_path
    map_layer: list[list[str]] = []
    with open(full_path) as map_layer_file:
        layer = csv.reader(map_layer_file)
        for row in layer:
            map_layer.append(row)
    return map_layer
