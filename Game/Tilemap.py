import pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, surface, group):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)