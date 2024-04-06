import pygame
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_assets() #импортирует файлы персонажа
        self.frame_index = 0 #значение кадра
        self.animation_speed = 0.15 #скорость анимации
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)   #начальная позиция игрока
        
        #механика движения игрока
        self.direction = pygame.math.Vector2(0,0)     #направление игрока при помощи вектора
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -16
        
        #все, что связано с частицами 
        self.import_particles() #импорт частиц
        self.particles_frame_index = 0
        self.particles_animation_speed = 0.15
        self.display_surface = surface
        self.create_jump_particles = create_jump_particles
        
        
        
        #статус  игрока
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    #Метод для заргрузки файлов персонажа
    def import_character_assets(self):
        character_path = "../graphics/character/"
        self.animations = {"idle": [], "run": [], "jump": [], "fall": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    
    #Добавление частиц при приземлении
    def import_particles(self):
        self.particles = import_folder("../graphics/character/dust_particles/run")

    #Анимация персонажа
    def animate(self):
        animation = self.animations[self.status]
        
        #Проходим по индексу кадра и создаем анимацию персонажа
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        image = animation[int(self.frame_index)]   
        if self.facing_right:
           self.image = image
        else:
           flipped_image = pygame.transform.flip(image,True,False) #смена сторон персонажа
           self.image = flipped_image
           
        #создание нового прямоугольника
        if self.on_ground and self.on_right:  
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
             
        elif self.on_ceiling and self.on_right:  
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    #Анимация частиц
    def run_particles_animation(self):
        if self.status == "run" and self.on_ground:
            self.particles_frame_index += self.particles_animation_speed
            if self.particles_frame_index >= len(self.particles):
                self.particles_frame_index = 0

            dust_particle = self.particles[int(self.particles_frame_index)]

            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(10,10)  #анимация частиц с левой стороны, когда игрок направлен вправо
                self.display_surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(10,10)  #наоборот
                flipped_particle = pygame.transform.flip(dust_particle, True, False)
                self.display_surface.blit(flipped_particle, pos)

    #Движение игрока
    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
            pass
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
            pass
        else:
            self.direction.x = 0
            pass
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)  # появление пыльных частиц во время прыжка игрока

    #Статус движения или бездействия игрока
    def get_status(self):
        if self.direction.y < 0:
            self.status = "jump"
        elif self.direction.y > 1:
            self.status = "fall"
        else:
            if self.direction.x != 0:
                self.status = "run"
            else:
                self.status = "idle"
           
        
    #Метод применения силы тяжести
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        
    #Метод прыжка
    def jump(self):
        self.direction.y = self.jump_speed

    #Метод обновления самого себя
    def update(self):
        self.get_input()
        self.animate()
        self.get_status()
        self.run_particles_animation()
    
        