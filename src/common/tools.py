import csv


def get_map_layer_from_csv(csv_path):
    map_layer: list[list[str]] = []
    with open(csv_path) as map_layout_file:
        layout = csv.reader(map_layout_file)
        for row in layout:
            map_layer.append(row)
    return map_layer
