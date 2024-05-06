import pygame
from support import import_csv_layout, import_cut_graphics
from option import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Box, Money, Trees
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect

class Level:
    def __init__(self,level_data,surface):
        # общая настройка
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None


        # настройка игрока
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout)

        # настройка частиц
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False


        # настройка местности
        platform_layout = import_csv_layout(level_data["platform"])  # импорт рельефа местности
        self.platform_sprites = self.create_tile_group(platform_layout, "platform")  # у каждой плитки есть свой индентификатор
        # настройка травы
        grass_layout = import_csv_layout(level_data["green"])
        self.grass_sprites = self.create_tile_group(grass_layout,"green")
        # настройка ящиков
        box_layout = import_csv_layout(level_data["box"])
        self.box_sprites = self.create_tile_group(box_layout, "box")
        # настройка монет
        money_layout = import_csv_layout(level_data["money"])
        self.money_sprites = self.create_tile_group(money_layout, "money")
        # настройка деревьев переднего фона
        fg_trees_layout = import_csv_layout(level_data["fg_trees"])
        self.fg_trees_sprites = self.create_tile_group(fg_trees_layout, "fg_trees")
        # настройка деревьев заднего фона
        bg_trees_layout = import_csv_layout(level_data["bg_trees"])
        self.bg_trees_sprites = self.create_tile_group(bg_trees_layout, "bg_trees")
        # настройка нпс
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemy_sprites = self.create_tile_group(enemy_layout, "enemies")
        # настройка stop_enemy
        stop_enemy_layout = import_csv_layout(level_data["stop_enemy"])
        self.stop_enemy_sprites = self.create_tile_group(stop_enemy_layout, "stop_enemy")
        # настройка декораций
        self.sky = Sky(8)  # линия горизонта
        level_width = len(platform_layout[0]) * tile_size  # ширина уровня
        self.water = Water(screen_height - 30, level_width) # уровень воды
        self.clouds = Clouds(500,level_width,25)

    def create_tile_group(self,layout,type):
        sprite_group = pygame.sprite.Group()  # создание группы плиток

        for row_index, row in enumerate(layout):  # enumerate сообщает внутри данного цикла по какому индексу мы находимся
            for col_index, val in enumerate(row): # col - столбец
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
                    # в файле tiles создаем отдельный класс для ящиков, так как их размер не соответствует размерам травы и плиткам платформы
                    if type == "box":
                        sprite = Box(tile_size,x,y)

                    if type == "money":
                        if val == "0": sprite = Money(tile_size,x,y,"../graphics/coins/gold")
                        if val == "1": sprite = Money(tile_size,x,y,"../graphics/coins/silver")
                    if type == "fg_trees":
                        if val == "2": sprite = Trees(tile_size,x,y,"../graphics/terrain/palm_small",38)
                        if val == "1": sprite = Trees(tile_size,x,y,"../graphics/terrain/palm_large", 64)
                    if type == "bg_trees":
                        sprite = Trees(tile_size,x,y,"../graphics/terrain/palm_bg",64)
                    if type == "enemies":
                        sprite = Enemy(tile_size,x,y)
                    if type == "stop_enemy":
                        sprite = Tile(tile_size,x,y)
                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self,layout):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0": # игрок
                    sprite = Player((x,y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)
                if val == "1": # цель
                    helmet_surface = pygame.image.load("../graphics/character/helmet.png").convert_alpha()
                    sprite = StaticTile(tile_size,x,y,helmet_surface)
                    self.goal.add(sprite)
    # столкновение с ограничением и переворот врага
    def enemy_collision_reverse(self):
        for enemy in self.enemy_sprites.sprites():
            if pygame.sprite.spritecollide(enemy,self.stop_enemy_sprites,False):
                enemy.reverse()
    def create_jump_particles(self,pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10,15)
        else:
            pos += pygame.math.Vector2(10,-15)
        jump_particle_sprite = ParticleEffect(pos,"jump")
        self.dust_sprite.add(jump_particle_sprite)

    def horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.platform_sprites.sprites() + self.box_sprites.sprites() + self.fg_trees_sprites.sprites() # сталкивающиеся спрайты

        for sprite in collidable_sprites:
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

    # вертикальное столкновение, занижение спрайтов на землю
    def vertical_movement_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.platform_sprites.sprites() + self.box_sprites.sprites() + self.fg_trees_sprites.sprites()

        for sprite in  collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:  # игрок не может находиться на полу, если он прыгает или падает
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:  # не может, если находиться вверху
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        # реализация движения фона
        if player_x < screen_width / 4 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 4) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False


    # метод создания частиц при приземлении
    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    def run(self):
        # отрисовка слоев, порядок обязателен!

        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface,self.world_shift)

        # bg_trees
        self.bg_trees_sprites.update(self.world_shift)
        self.bg_trees_sprites.draw(self.display_surface)

        # platform
        self.platform_sprites.update(self.world_shift)
        self.platform_sprites.draw(self.display_surface)

        # enemy
        self.enemy_sprites.update(self.world_shift)
        self.stop_enemy_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemy_sprites.draw(self.display_surface)

        # box
        self.box_sprites.update(self.world_shift)
        self.box_sprites.draw(self.display_surface)

        # grass
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # money
        self.money_sprites.update(self.world_shift)
        self.money_sprites.draw(self.display_surface)

        # fg_trees
        self.fg_trees_sprites.update(self.world_shift)
        self.fg_trees_sprites.draw(self.display_surface)

        # particles
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # player sprites
        self.player.update()
        self.horizontal_movement_collision()
        self.get_player_on_ground()
        self.vertical_movement_collision()
        self.create_landing_dust()
        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        # water
        self.water.draw(self.display_surface, self.world_shift)
