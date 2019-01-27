import collections
import random

import yaml


class Tile:
    def __init__(self, tile_type, num):
        self.tile_type = tile_type
        self.num = num
        self.char = self.__set_char(tile_type, num)

    def __set_char(self, tile_type, num):
        yaml_path = "./mahjong/config/char.yml"

        f = open(yaml_path, "r")
        char_dict = yaml.load(f)["char"]

        key = str(num) + tile_type

        return char_dict[key]


class TilesHandler:
    def __init__(self, tiles):
        self.tiles = self.__sort_tiles(tiles)

    def __sort_tiles(self, tiles):
        tiles.sort(key=lambda tile: (tile.tile_type, tile.num))
        return tiles

    def get_tiles_in_char(self):
        tiles_in_char = ""

        for tile in self.tiles:
            tiles_in_char += tile.char

        return tiles_in_char


def create_tiles_tenpai():
    tiles = mentsu() + mentsu() + mentsu() + mentsu() + janto()

    tiles = random.sample(tiles, 13)

    if is_reasonable_tiles_num(tiles):
        return tiles
    else:
        return create_tiles_tenpai()


def mentsu():
    mentsu_type_choices = ["shuntsu", "kotsu"]
    mentsu_type = random.choice(mentsu_type_choices)

    if mentsu_type == "shuntsu":
        return shuntsu()
    elif mentsu_type == "kotsu":
        return kotsu()


def shuntsu():
    tiles_all = get_tiles_for_shuntsu()
    selected_tile = random.choice(tiles_all)

    return [Tile(selected_tile.tile_type, selected_tile.num + i) for i in range(3)]


def kotsu():
    tiles_all = get_tiles_all()
    selected_tile = random.choice(tiles_all)

    return [selected_tile for i in range(3)]


def janto():
    tiles_all = get_tiles_all()
    selected_tile = random.choice(tiles_all)

    return [selected_tile for i in range(2)]


def get_tiles_all():
    tiles_m = [Tile("m", i) for i in range(1, 10)]
    tiles_p = [Tile("p", i) for i in range(1, 10)]
    tiles_s = [Tile("s", i) for i in range(1, 10)]
    tiles_z = [Tile("z", i) for i in range(1, 8)]

    return tiles_m + tiles_p + tiles_s + tiles_z


def get_tiles_for_shuntsu():
    tiles_m = [Tile("m", i) for i in range(1, 8)]
    tiles_p = [Tile("p", i) for i in range(1, 8)]
    tiles_s = [Tile("s", i) for i in range(1, 8)]

    return tiles_m + tiles_p + tiles_s


def is_reasonable_tiles_num(tiles):
    handler = TilesHandler(tiles)
    tiles_in_char = handler.get_tiles_in_char()
    c = collections.Counter(tiles_in_char)

    if c[max(c)] < 5:
        return True
    else:
        return False
