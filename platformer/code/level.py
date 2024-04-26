import pygame
from support import import_csv_layout, import_cut_graphics
from option import tile_size
from tiles import Tile, StaticTile, Box, Money, Trees
class Level:
    def __init__(self,level_data,surface):
        #общая настройка
        self.display_surface = surface
        self.world_shift = 0

        #настройка слаёв
        #настрока местности(платформы)
        platform_layout = import_csv_layout(level_data["platform"])  #импорт рельефа местности
        self.platform_sprites = self.create_tile_group(platform_layout, "platform")  #у каждой плитки есть свой индентификатор
        #настройка травы
        grass_layout = import_csv_layout(level_data["green"])
        self.grass_sprites = self.create_tile_group(grass_layout,"green")
        #настройка ящиков
        box_layout = import_csv_layout(level_data["box"])
        self.box_sprites = self.create_tile_group(box_layout, "box")
        #настройка монет
        money_layout = import_csv_layout(level_data["money"])
        self.money_sprites = self.create_tile_group(money_layout, "money")
        #настройка деревьев переднего фона
        fg_trees_layout = import_csv_layout(level_data["fg_trees"])
        self.fg_trees_sprites = self.create_tile_group(fg_trees_layout, "fg_trees")
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()  #создание группы плиток!?

        for row_index, row in enumerate(layout):  #enumerate сообщает внутри данного цикла по какому индексу мы находимся
            for col_index, val in enumerate(row): #col - столбец
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "platform":
                        platform_tile_list = import_cut_graphics("../graphics/terrain/terrain_tiles.png")
                        tile_surface = platform_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)

                    if type == "green":
                        grass_tile_list = import_cut_graphics("../graphics/decoration/grass/grass.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size,x,y,tile_surface)
                    #в файле tiles создаем отдельный класс для ящиков, так как их размер не соответствует размерам травы и плиткам платформы
                    if type == "box":
                        sprite = Box(tile_size,x,y)

                    if type == "money":
                        if val == "0": sprite = Money(tile_size,x,y,"../graphics/coins/gold")
                        if val == "1": sprite = Money(tile_size,x,y,"../graphics/coins/silver")
                    if type == "fg_trees":
                        sprite = Trees(tile_size,x,y,"../graphics/terrain/palm_small",38)
                    sprite_group.add(sprite)

        return sprite_group
    def run(self):
        self.platform_sprites.update(self.world_shift)
        self.platform_sprites.draw(self.display_surface)

        #grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)


        #box
        self.box_sprites.update(self.world_shift)
        self.box_sprites.draw(self.display_surface)

        #money
        self.money_sprites.update(self.world_shift)
        self.money_sprites.draw(self.display_surface)

        #fg_trees
        self.fg_trees_sprites.update(self.world_shift)
        self.fg_trees_sprites.draw(self.display_surface)
