# Mahjong
This package is Mahjong Library.

# How to use

### get_tiles
```
handler = TilesHandler()    # random create
handler_m = TilesHandler("①①①②③③④⑤⑥⑦⑧⑨⑨⑨")
handler_p = TilesHandler("一一一二三四五六七八九九九")
handler_s = TilesHandler("１１１２３４５６７８９９９")
handler_z = TilesHandler("東南南西西北北白白発発中中")

print(handler_m.get_tiles_in_char())
print(handler_p.get_tiles_in_char())
print(handler_s.get_tiles_in_char())
print(handler_z.get_tiles_in_char())
```

```
一二三①②③⑦⑦１１２３３
①①①②③③④⑤⑥⑦⑧⑨⑨⑨
一一一二三四五六七八九九九
１１１２３４５６７８９９９
東南南西西北北白白発発中中
```


### identify_target_tiles

```
handler = TilesHandler("１１１２３４５６７８９９９")
target_tiles = handler.identify_target_tiles()
print([tile.char for tile in target_tiles])
```

```
['１', '２', '３', '４', '５', '６', '７', '８', '９']
```

```
handler = TilesHandler("一二三①②③⑦⑦１２３３４")
target_tiles = handler.identify_target_tiles()
print([tile.char for tile in target_tiles])
```

```
['２', '５']
```