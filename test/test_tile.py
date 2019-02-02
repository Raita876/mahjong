#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import pytest
import yaml

from mahjong.exceptions import ArgumentError
from mahjong.tile import Tile, TilesHandler, create_tiles_tenpai


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


def test_handler_miss_args():
    tiles = "This is not list."

    with pytest.raises(ArgumentError):
        TilesHandler(tiles)


def test_handler_list_empty():
    tiles = []

    with pytest.raises(ArgumentError):
        TilesHandler(tiles)


def test_handler_sort():
    tiles_yaml = load_tiles_yaml()

    tiles = [Tile(tile["tile_type"], tile["num"]) for tile in tiles_yaml]

    random.shuffle(tiles)

    handler = TilesHandler(tiles)

    assert handler.get_tiles_in_char() == "三四五⑤⑥⑦２３７８９南南"


def test_create_tiles_tenpai_miss_args():
    with pytest.raises(ArgumentError):
        create_tiles_tenpai("d")


def test_tile_miss_type():
    with pytest.raises(ArgumentError):
        Tile("d", 7)


def test_tile_miss_num():
    with pytest.raises(ArgumentError):
        Tile("s", 10)
