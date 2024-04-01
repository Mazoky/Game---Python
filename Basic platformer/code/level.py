import pygame
from tile import Tile
from option import *
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self,level_data,surface):
        #настройка уровня 
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0
        self.current_x = 0

        #анимация при прыжке и приземлении
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False


    #частицы при прыжке
    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,15)
        else:
            pos += pygame.math.Vector2(10,-15)
        jump_particle_sprite = ParticleEffect(pos,"jump")
        self.dust_sprite.add(jump_particle_sprite)

    #вывод игрока на уровень
    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False


    #метод создания частиц при приземлении
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    #настройка уровня в приложении
    def setup_level(self, layout):
    #создание группы спрайтов и определения координат 
        self.tile = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        
        for row_index, row in enumerate(layout):                   #layout - расположение, row - ряд, cell- ячейка
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == "x":
                    tile = Tile((x, y), tile_size)
                    self.tile.add(tile)
                if cell == "r":
                    player_sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(player_sprite)
                
    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx 
        direction_x = player.direction.x
        
        #реализация движения фона 
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4 ) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8
    
    #горизонтальное столкновение        
    def horizontal_movement_collision(self):
        player = self.player.sprite       
        player.rect.x += player.direction.x * player.speed  
        
        for sprite in self.tile.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False
            
    
    #вертикальное столкновение, занижение спрайтов на землю               
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()       
    
        for sprite in self.tile.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1: #игрок не может находиться на полу, если он прыгает или падает
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0: #не может, если находиться вверху
            player.on_ceiling = False
        
          
    #проигрыватель программы
    def run(self):

        # частицы пыли
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)


        #отрисовка группы спрайтов
        #Плитки
        self.tile.update(self.world_shift)
        self.tile.draw(self.display_surface)
        self.scroll_x()


        #Игрок
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.player.draw(self.display_surface)
        