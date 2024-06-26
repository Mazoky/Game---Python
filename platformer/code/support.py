from csv import reader # позволяет читать файлы формата сиви
from option import tile_size
from os import walk
import pygame



def import_folder(path):
    surface_list = []

    for _,__,image_files in walk(path):
        for image in image_files:
            full_path = path + "/" + image # полный путь файла внутри этой папки
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list
def import_csv_layout(path):
    platform_map = []
    with open(path) as map:
        level = reader(map,delimiter = ',')         # reader - метод чтения файлов
        for row in level:
            platform_map.append(list(row))
        return platform_map

def import_cut_graphics(path):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / tile_size)
    tile_num_y = int(surface.get_size()[  1] / tile_size)  # определение кол-ва плиток внутри уровня

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size,tile_size),flags = pygame.SRCALPHA) # рисуется новая поверхность
            # SRCALPHA позволяет сделать все неиспользуемые пиксели невидимыми
            new_surf.blit(surface,(0,0),pygame.Rect(x,y,tile_size,tile_size))
            cut_tiles.append(new_surf)

    return cut_tiles

