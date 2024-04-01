import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,size):
        super().__init__()            #x   #y
        self.image = pygame.Surface((size,size))
        self.image.fill("brown")
        self.rect = self.image.get_rect(topleft = pos)
    #способ для движения камеры
    def update(self,x_shift):
        self.rect.x += x_shift