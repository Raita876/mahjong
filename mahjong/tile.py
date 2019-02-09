import collections
import copy
import random

import yaml

from mahjong.exceptions import ArgumentError


class Tile:
    def __init__(self, tile=None):
        if type(tile) is tuple:
            tile_tuple = tile
        elif type(tile) is str:
            tile_tuple = self.__to_tile_tuple(tile)
        else:
            raise ArgumentError("Args is tuple or str")

        self.__is_appropriate_type(tile_tuple[0])

        self.__is_appropriate_num(tile_tuple[0], tile_tuple[1])

        self.tile_type = tile_tuple[0]
        self.num = tile_tuple[1]
        self.char = self.__set_char(tile_tuple[0], tile_tuple[1])

    def __eq__(self, other):
        if not isinstance(other, Tile):
            return NotImplemented
        return (self.tile_type, self.num) == (other.tile_type, other.num)

    def __hash__(self):
        return hash(self.char)

    def __set_char(self, tile_type, num):
        char_dict = self.__get_char_yaml()["char"]

        key = str(num) + tile_type

        return char_dict[key]

    def __to_tile_tuple(self, tile_in_char):
        tile_dict = self.__get_tile_num_yaml()

        if tile_in_char not in tile_dict:
            raise ArgumentError("Args is not appropriate.")

        return tile_dict[tile_in_char]["type"], tile_dict[tile_in_char]["num"]

    def __get_char_yaml(self):
        yaml_path = "./mahjong/config/char.yml"
        f = open(yaml_path, "r")
        return yaml.load(f)

    def __get_tile_num_yaml(self):
        yaml_path = "./mahjong/config/type_num.yml"
        f = open(yaml_path, "r")
        return yaml.load(f)

    def __is_appropriate_type(self, tile_type):
        if tile_type != "m" and tile_type != "p" and tile_type != "s" and tile_type != "z":
            raise ArgumentError("Tile-Type is not appropriate. must be 'm' or 'p' or 's' or 'z'.")

    def __is_appropriate_num(self, tile_type, num):
        if tile_type == "z":
            min_num = 1
            max_num = 7
        else:
            min_num = 1
            max_num = 9

        if num < min_num or num > max_num:
            raise ArgumentError("Tile-Num is not appropriate.")


class TilesHandler:
    def __init__(self, tiles=None):
        if tiles is None:
            self.tiles = create_tiles_tenpai()
        elif type(tiles) is str:
            self.tiles = self.__init_tiles(self.__to_list_tiles_str(tiles))
        else:
            self.tiles = self.__init_tiles(tiles)

    def __init_tiles(self, tiles):
        if type(tiles) is not list:
            raise ArgumentError("Argument must be a List.")

        if len(tiles) == 0:
            raise ArgumentError("Tiles is empty.")

        return self.__sort_tiles(tiles)

    def __to_list_tiles_str(self, tiles_str):
        return [Tile(tile=char) for char in list(tiles_str)]

    def __sort_tiles(self, tiles):
        tiles.sort(key=lambda tile: (tile.tile_type, tile.num))
        return tiles

    def get_tiles_in_char(self):
        tiles_in_char = ""

        for tile in self.tiles:
            tiles_in_char += tile.char

        return tiles_in_char

    def identify_target_tiles(self):
        target_tiles = []

        around_tiles = self.__around_tiles()

        for tile in around_tiles:
            # print(tile.char)
            if self.__is_fifth_tile(tile):
                continue

            check_tiles = self.__sort_tiles(self.tiles + [tile])

            if self.__is_completed_tiles(check_tiles):
                target_tiles.append(tile)

        return self.__sort_tiles(target_tiles)

    def __is_fifth_tile(self, tile):
        if self.tiles.count(tile) >= 4:
            return True
        else:
            return False

    def __around_tiles(self):
        unique_tiles = list(set(self.tiles))
        around_tiles = []

        for tile in unique_tiles:
            around_tiles.append(tile)

            if tile.tile_type == "z":
                continue

            if tile.num - 1 >= 1:
                around_tiles.append(Tile(tile=(tile.tile_type, tile.num - 1)))
            if tile.num + 1 <= 9:
                around_tiles.append(Tile(tile=(tile.tile_type, tile.num + 1)))

        return list(set(around_tiles))

    def __is_completed_tiles(self, tiles):
        tiles_in_char = list([t.char for t in tiles])

        for tile in tiles:
            target_tiles_in_char = copy.deepcopy(tiles_in_char)

            if tiles_in_char.count(tile.char) >= 2:
                for i in range(2):
                    target_tiles_in_char.remove(tile.char)
            else:
                continue

            target_tiles_in_char = self.__remove_kotsu(target_tiles_in_char)
            if len(target_tiles_in_char) == 0:
                return True

            # print(target_tiles_in_char)

            target_tiles_in_char = self.__remove_shuntsu(target_tiles_in_char)
            if len(target_tiles_in_char) == 0:
                return True

            # print(target_tiles_in_char)

        return False

    def __remove_kotsu(self, tiles_in_char):
        kotsu_tiles = [items[0] for items in collections.Counter(tiles_in_char).items() if items[1] >= 3]

        for delete_tile in kotsu_tiles:
            for i in range(3):
                tiles_in_char.remove(delete_tile)

        return tiles_in_char

    def __remove_shuntsu(self, tiles_in_char):
        self.deepcopy = copy.deepcopy(tiles_in_char)
        target_tiles_in_char = self.deepcopy

        while (True):
            tile = Tile(tile=target_tiles_in_char[0])
            if tile.num > 7 or tile.tile_type == "z":
                break

            shuntsu_tiles_in_char = [
                tile.char,
                Tile(tile=(tile.tile_type, tile.num + 1)).char,
                Tile(tile=(tile.tile_type, tile.num + 2)).char
            ]

            if shuntsu_tiles_in_char[0] in target_tiles_in_char and shuntsu_tiles_in_char[1] in target_tiles_in_char and \
                    shuntsu_tiles_in_char[2] in target_tiles_in_char:
                target_tiles_in_char.remove(shuntsu_tiles_in_char[0])
                target_tiles_in_char.remove(shuntsu_tiles_in_char[1])
                target_tiles_in_char.remove(shuntsu_tiles_in_char[2])
            else:
                break

            if len(target_tiles_in_char) == 0:
                break

        return target_tiles_in_char


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

    return [Tile(tile=(selected_tile.tile_type, selected_tile.num + i)) for i in range(3)]


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
    if tile_type is None:
        tile_type = ["m", "p", "s", "z"]

    if "m" in tile_type:
        tiles_m = [Tile(tile=("m", i)) for i in range(1, 10)]
    else:
        tiles_m = []

    if "p" in tile_type:
        tiles_p = [Tile(tile=("p", i)) for i in range(1, 10)]
    else:
        tiles_p = []

    if "s" in tile_type:
        tiles_s = [Tile(tile=("s", i)) for i in range(1, 10)]
    else:
        tiles_s = []

    if "z" in tile_type:
        tiles_z = [Tile(tile=("z", i)) for i in range(1, 8)]
    else:
        tiles_z = []

    return tiles_m + tiles_p + tiles_s + tiles_z


def get_tiles_for_shuntsu():
    tiles_m = [Tile(tile=("m", i)) for i in range(1, 8)]
    tiles_p = [Tile(tile=("p", i)) for i in range(1, 8)]
    tiles_s = [Tile(tile=("s", i)) for i in range(1, 8)]

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
    tiles = [Tile(tile=(tile_type, i)) for i in range(1, 10)]

    return tiles


def get_tiles_specified_type_for_shuntsu(tile_type):
    tiles = [Tile(tile=(tile_type, i)) for i in range(1, 8)]

    return tiles
