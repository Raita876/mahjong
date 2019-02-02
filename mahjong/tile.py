import collections
import random

import yaml

from mahjong.exceptions import ArgumentError


class Tile:
    def __init__(self, tile_type: str, num: int):
        self.__is_appropriate_type(tile_type)

        self.__is_appropriate_num(num, tile_type)

        self.tile_type = tile_type
        self.num = num
        self.char = self.__set_char(tile_type, num)

    def __set_char(self, tile_type, num):
        yaml_path = "./mahjong/config/char.yml"

        f = open(yaml_path, "r")
        char_dict = yaml.load(f)["char"]

        key = str(num) + tile_type

        return char_dict[key]

    def __is_appropriate_type(self, tile_type):
        if tile_type != "m" and tile_type != "p" and tile_type != "s" and tile_type != "z":
            raise ArgumentError("Tile-Type is not appropriate. must be 'm' or 'p' or 's' or 'z'.")

    def __is_appropriate_num(self, num, tile_type):
        if tile_type == "z":
            min_num = 1
            max_num = 7
        else:
            min_num = 1
            max_num = 9

        if num < min_num or num > max_num:
            raise ArgumentError("Tile-Num is not appropriate.")


class TilesHandler:
    def __init__(self, tiles):
        self.tiles = self.__init_tiles(tiles)

    def __init_tiles(self, tiles):
        if type(tiles) is not list:
            raise ArgumentError("Argument must be a List.")

        if len(tiles) == 0:
            raise ArgumentError("Tiles is empty.")

        return self.__sort_tiles(tiles)

    def __sort_tiles(self, tiles):
        tiles.sort(key=lambda tile: (tile.tile_type, tile.num))
        return tiles

    def get_tiles_in_char(self):
        tiles_in_char = ""

        for tile in self.tiles:
            tiles_in_char += tile.char

        return tiles_in_char


def create_tiles_tenpai(tile_type=None):
    tiles = mentsu(tile_type) + mentsu(tile_type) + mentsu(tile_type) + mentsu(tile_type) + janto(tile_type)

    tiles = random.sample(tiles, 13)

    if is_reasonable_tiles_num(tiles):
        return tiles
    else:
        return create_tiles_tenpai(tile_type)


def mentsu(tile_type=None):
    mentsu_type_choices = ["shuntsu", "kotsu"]
    mentsu_type = random.choice(mentsu_type_choices)

    if mentsu_type == "shuntsu":
        return shuntsu(tile_type)
    elif mentsu_type == "kotsu":
        return kotsu(tile_type)


def shuntsu(tile_type=None):
    if tile_type is None:
        tiles_all = get_tiles_for_shuntsu()
    elif tile_type == "m" or tile_type == "p" or tile_type == "s":
        tiles_all = get_tiles_specified_type_for_shuntsu(tile_type)
    else:
        raise ArgumentError("Tile-Type is not appropriate. must be 'm' or 'p' or 's'.")

    selected_tile = random.choice(tiles_all)

    return [Tile(selected_tile.tile_type, selected_tile.num + i) for i in range(3)]


def kotsu(tile_type=None):
    if tile_type is None:
        tiles_all = get_tiles_all()
    elif tile_type == "m" or tile_type == "p" or tile_type == "s" or tile_type == "z":
        tiles_all = get_tiles_specified_type(tile_type)
    else:
        raise ArgumentError("Tile-Type is not appropriate. must be 'm' or 'p' or 's' or 'z'.")

    selected_tile = random.choice(tiles_all)

    return [selected_tile for i in range(3)]


def janto(tile_type=None):
    if tile_type is None:
        tiles_all = get_tiles_all()
    elif tile_type == "m" or tile_type == "p" or tile_type == "s" or tile_type == "z":
        tiles_all = get_tiles_specified_type(tile_type)
    else:
        raise ArgumentError("Tile-Type is not appropriate. must be 'm' or 'p' or 's' or 'z'.")

    selected_tile = random.choice(tiles_all)

    return [selected_tile for i in range(2)]


def get_tiles_all(tile_type=None):
    tiles_m = [Tile("m", i) for i in range(1, 10)]
    tiles_p = [Tile("p", i) for i in range(1, 10)]
    tiles_s = [Tile("s", i) for i in range(1, 10)]
    tiles_z = [Tile("z", i) for i in range(1, 8)]

    return tiles_m + tiles_p + tiles_s + tiles_z


def get_tiles_for_shuntsu(tile_type=None):
    tiles_m = [Tile("m", i) for i in range(1, 8)]
    tiles_p = [Tile("p", i) for i in range(1, 8)]
    tiles_s = [Tile("s", i) for i in range(1, 8)]

    return tiles_m + tiles_p + tiles_s


def is_reasonable_tiles_num(tiles):
    handler = TilesHandler(tiles)
    tiles_in_char = handler.get_tiles_in_char()
    c = collections.Counter(tiles_in_char)

    if max(c.values()) < 5:
        return True
    else:
        return False


def create_tiles_randomly(tile_type=None):
    default_tile_type = "s" if tile_type is None else tile_type

    tiles = get_tiles_specified_type(default_tile_type) * 4

    selected_tiles = random.sample(tiles, 13)

    return selected_tiles


def get_tiles_specified_type(tile_type):
    tiles = [Tile(tile_type, i) for i in range(1, 10)]

    return tiles


def get_tiles_specified_type_for_shuntsu(tile_type):
    tiles = [Tile(tile_type, i) for i in range(1, 8)]

    return tiles
