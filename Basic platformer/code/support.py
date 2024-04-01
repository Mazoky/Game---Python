from os import walk
import pygame

#Указываем путь до файлов персонажа
def import_folder(path):
    surface_list = []
    
    for _,__,img_file in walk(path):
        for image in img_file:
            full_path = path + "/" + image #общий принцип поиска
            image_surf = pygame.image.load(full_path).convert_alpha() #конвертирует и загружает
            surface_list.append(image_surf) #открывает
    
    return surface_list #возвращение к начальной точке

