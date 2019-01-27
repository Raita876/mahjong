#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import yaml

from mahjong.tile import Tile, TilesHandler


def load_tiles_yaml():
    yaml_path = "./test/sample/tiles.yml"
    f = open(yaml_path, "r")

    tiles_yaml = yaml.load(f)

    return tiles_yaml


def test_tile_char():
    tiles_yaml = load_tiles_yaml()

    for tile in tiles_yaml:
        assert_tile = Tile(tile["tile_type"], tile["num"])

        assert tile["char"] == assert_tile.char


def test_handler():
    tiles_yaml = load_tiles_yaml()

    tiles = [Tile(tile["tile_type"], tile["num"]) for tile in tiles_yaml]

    handler = TilesHandler(tiles)

    assert handler.get_tiles_in_char() == "三四五⑤⑥⑦２３７８９南南"


def test_handler_sort():
    tiles_yaml = load_tiles_yaml()

    tiles = [Tile(tile["tile_type"], tile["num"]) for tile in tiles_yaml]

    random.shuffle(tiles)

    handler = TilesHandler(tiles)

    assert handler.get_tiles_in_char() == "三四五⑤⑥⑦２３７８９南南"
