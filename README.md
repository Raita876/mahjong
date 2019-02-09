# Mahjong
This package is Mahjong Library.

# How to use

### get_tiles_in_char

handler_m = TilesHandler("①①①②③③④⑤⑥⑦⑧⑨⑨⑨")

handler_p = TilesHandler("一一一二三四五六七八九九九")

handler_s = TilesHandler("１１１２３４５６７８９９９")

print(handler_m.get_tiles_in_char())

print(handler_p.get_tiles_in_char())

print(handler_s.get_tiles_in_char())

> ①①①②③③④⑤⑥⑦⑧⑨⑨⑨

> 一一一二三四五六七八九九九

> １１１２３４５６７８９９９


### identify_target_tiles

handler = TilesHandler("１１１２３４５６７８９９９")

target_tiles = handler.identify_target_tiles()

print([tile.char for tile in target_tiles])

> ['１', '２', '３', '４', '５', '６', '７', '８', '９']