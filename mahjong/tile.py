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
