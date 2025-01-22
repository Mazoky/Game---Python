import pygame
from game import levels

class Node(pygame.sprite.Sprite):
    def __init__(self,pos,status):
        super().__init__()
        self.image = pygame.Surface((100,80))
        if status == "available":
            self.image.fill("brown")
        else:
            self.image.fill("grey")
        self.rect = self.image.get_rect(center = pos)
class Icon(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((20,20))
        self.image.fill("green")
        self.rect = self.image.get_rect(center = pos)
class Overworld:
    def __init__(self,start_level,max_level,surface):

        # настройка
        self.display_surface = surface
        self.max_level = max_level
        self.current_level = start_level

        # спрайты
        self.setup_nodes()
        self.setup_icon()

    def setup_nodes(self):
        self.nodes = pygame.sprite.Group()
        for index, node_data in enumerate (levels.values()):
            if index <= self.max_level:
                node_sprite = Node(node_data["node_pos"], "available")                  # экземпляр node (узла)
                self.nodes.add(node_sprite)
            else:
                node_sprite = Node(node_data["node_pos"], "locked")
            self.nodes.add(node_sprite)

    def draw_paths(self):                                                                     # пути, тропы между узлами
        points = [node["node_pos"] for index,node in enumerate(levels.values()) if index <= self.max_level]
        pygame.draw.lines(self.display_surface,"red",False,points,4)

    def setup_icon(self):
        self.icon = pygame.sprite.GroupSingle()
        icon_sprite = Icon(self.nodes.sprites()[self.current_level].rect.center)
        self.icon.add(icon_sprite)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT] and self.current_level < self.max_level:
            self.current_level += 1
        elif keys[pygame.K_LEFT] and self.current_level > 0:
            self.current_level -= 1

    def update_icon_pos(self):
        self.icon.sprite.rect.center = self.nodes.sprites()[self.current_level].rect.center
    def run(self):
        self.input()
        self.update_icon_pos()
        self.draw_paths()
        self.nodes.draw(self.display_surface)
        self.icon.draw(self.display_surface)
        pass
