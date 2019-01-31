#!/usr/bin/python
# -*- coding: utf-8 -*-
import re

from mahjong.tile import TilesHandler, create_tiles_randomly, create_tiles_tenpai


def test_create_mentin_len():
    tiles = create_tiles_randomly()

    assert len(tiles) == 13


def test_create_mentin_regex():
    handler_m = TilesHandler(create_tiles_randomly("m"))
    handler_p = TilesHandler(create_tiles_randomly("p"))
    handler_s = TilesHandler(create_tiles_randomly("s"))

    pattern_m = "[一二三四五六七八九]"
    pattern_p = "[①-⑨]"
    pattern_s = "[１-９]"

    assert re.match(pattern_m, handler_m.get_tiles_in_char()) is not None

    assert re.match(pattern_p, handler_p.get_tiles_in_char()) is not None

    assert re.match(pattern_s, handler_s.get_tiles_in_char()) is not None


def test_create_mentin_tenpai_regex():
    handler_m = TilesHandler(create_tiles_tenpai("m"))
    handler_p = TilesHandler(create_tiles_tenpai("p"))
    handler_s = TilesHandler(create_tiles_tenpai("s"))

    pattern_m = "[一二三四五六七八九]"
    pattern_p = "[①-⑨]"
    pattern_s = "[１-９]"

    assert re.match(pattern_m, handler_m.get_tiles_in_char()) is not None

    assert re.match(pattern_p, handler_p.get_tiles_in_char()) is not None

    assert re.match(pattern_s, handler_s.get_tiles_in_char()) is not None
