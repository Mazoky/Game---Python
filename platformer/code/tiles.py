import pygame
from support import import_folder
class Tile (pygame.sprite.Sprite):
    def __init__(self,size,x,y):
        super().__init__()
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
    def update(self,shift): # прокрутка камеры
        self.rect.x += shift


class StaticTile(Tile):
    def __init__(self,size,x,y,surface):
        super().__init__(size,x,y)
        self.image = surface # индивидуальное изменение спрайта

class Box(StaticTile):
    def __init__(self,size,x,y):
        super().__init__(size,x,y,pygame.image.load("../graphics/terrain/box.png").convert_alpha())
        offset_y = y + size  # чтобы ящики стояли на земле, а не висели в воздухе
        self.rect = self.image.get_rect(bottomleft = (x,offset_y))


class AnimatedTile(Tile):  # класс с механизмом анимированной плитки
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self,shift):
        self.animate()
        self.rect.x += shift

class Money(AnimatedTile):
    def __init__(self,size,x,y,path):
        super().__init__(size,x,y,path)
        center_x = x + int(size / 2)
        center_y = y + int(size / 2)
        self.rect = self.image.get_rect(center = (center_x,center_y))

class Trees(AnimatedTile):
    def __init__(self,size,x,y,path,offset):
        super().__init__(size, x, y, path)
        offset_y = y - offset # смещение деревьев
        self.rect.topleft = (x,offset_y)