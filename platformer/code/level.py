import pygame
from support import import_csv_layout, import_cut_graphics
from option import tile_size
from tiles import Tile
class Level:
    def __init__(self,level_data,surface):
        #общая настройка
        self.display_surface = surface
        self.world_shift = 0

        #настрока местности(платформы)
        platform_layout = import_csv_layout(level_data["platform"])  #импорт рельефа местности
        self.platform_sprites = self.create_tile_group(platform_layout, "platform")  #у каждой плитки есть свой индентификатор
    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()  #создание группы плиток!?

        for row_index, row in enumerate(layout):  #enumerate сообщает внутри данного цикла по какому индексу мы находимся
            for col_index, val in enumerate(row): #col - столбец
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size

                    if type == "platform":
                        platform_tile_list = import_cut_graphics("../graphics/terrain/terrain_tiles.png")
                        sprite = Tile(tile_size,x,y)
                        sprite_group.add(sprite)


        return sprite_group
    def run(self):
        self.platform_sprites.draw(self.display_surface)
        self.platform_sprites.update(self.world_shift)