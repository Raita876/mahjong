import random

from mahjong.tile import Tile


def create_tiles_randomly(tile_type=None):
    default_tile_type = "s" if tile_type is None else tile_type

    tiles = get_tiles_specified_type(default_tile_type)

    selected_tiles = random.sample(tiles, 13)

    return selected_tiles


def get_tiles_specified_type(tile_type):
    tiles = [Tile(tile_type, i) for i in range(1, 10)] * 4

    return tiles
