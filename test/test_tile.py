#!/usr/bin/python
# -*- coding: utf-8 -*-
import random

import pytest
import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

from mahjong.exceptions import ArgumentError
from mahjong.tile import Tile, TilesHandler, create_tiles_tenpai


def load_tiles_yaml():
    yaml_path = "./test/sample/tiles.yml"
    f = open(yaml_path, "r")

    tiles_yaml = yaml.load(f, Loader=Loader)

    return tiles_yaml


def test_tile_char():
    tiles_yaml = load_tiles_yaml()

    for tile in tiles_yaml:
        assert_tile = Tile(tile=(tile["tile_type"], tile["num"]))

        assert tile["char"] == assert_tile.char


def test_handler():
    tiles_yaml = load_tiles_yaml()

    tiles = [Tile(tile=(tile["tile_type"], tile["num"]))
             for tile in tiles_yaml]

    handler = TilesHandler(tiles)

    assert handler.get_tiles_in_char() == "三四五⑤⑥⑦２３７８９南南"


def test_handler_from_str():
    handler = TilesHandler("四五②②⑥⑦⑧５５５発発発")

    assert handler.get_tiles_in_char() == "四五②②⑥⑦⑧５５５発発発"


def test_handler_mps():
    handler = TilesHandler("12356m456p789s南南")

    assert handler.get_tiles_in_char() == "一二三五六④⑤⑥７８９南南"


def test_handler_create_tenpai():
    handler = TilesHandler()

    assert len(handler.get_tiles_in_char()) == 13


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

    tiles = [Tile(tile=(tile["tile_type"], tile["num"]))
             for tile in tiles_yaml]

    random.shuffle(tiles)

    handler = TilesHandler(tiles)

    assert handler.get_tiles_in_char() == "三四五⑤⑥⑦２３７８９南南"


def test_create_tiles_tenpai_miss_args():
    with pytest.raises(ArgumentError):
        create_tiles_tenpai("d")


def test_tile_args_is_tuple():
    assert Tile(tile=("m", 3)).char == "三"


def test_tile_args_is_str():
    assert Tile(tile="九").tile_type == "m"
    assert Tile(tile="７").num == 7


def test_tile_miss_type():
    with pytest.raises(ArgumentError):
        Tile(tile=("d", 7))


def test_tile_miss_num():
    with pytest.raises(ArgumentError):
        Tile(tile=("s", 10))


def test_identify():
    handler = TilesHandler("三四五⑤⑥⑦２３７８９南南")
    target_tiles = handler.identify_target_tiles()

    assert [tile.char for tile in target_tiles] == ["１", "４"]


def test_identify_irregular():
    handler = TilesHandler("２２２３３３４４４５７８９")
    target_tiles = handler.identify_target_tiles()

    assert [tile.char for tile in target_tiles] == ["２", "３", "４", "５", "６"]
