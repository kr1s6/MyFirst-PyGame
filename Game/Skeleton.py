import random
import pygame

class Skeleton(pygame.sprite.Sprite):
    def __init__(self, place_to_stand, group):
        super().__init__(group)
        self.WIDTH = pygame.display.get_window_size()[0]
        self.HIGH = pygame.display.get_window_size()[1]
        self.place_to_stand = place_to_stand
        self.GRAVITY = 0

        enemy_left = pygame.image.load('Game/Assets/Skeleton/skeleton-left.png').convert_alpha()
        enemy_left2 = pygame.image.load('Game/Assets/Skeleton/skeleton-left2.png').convert_alpha()
        enemy_right = pygame.image.load('Game/Assets/Skeleton/skeleton-right.png').convert_alpha()
        enemy_right2 = pygame.image.load('Game/Assets/Skeleton/skeleton-right2.png').convert_alpha()

        image_list = [[enemy_left, enemy_left2], [enemy_right, enemy_right2]]
        for i in range(len(image_list)):
            if hasattr(image_list[i], '__iter__'):
                for j in range(len(image_list[i])):
                  image_list[i][j] = pygame.transform.scale_by(image_list[i][j], 4)
            else:
                image_list[i] = pygame.transform.scale_by(image_list[i], 4)

        self.enemy_images = image_list
        self.enemy_images_index = 0
        self.animation_frame = 0
        self.image = self.enemy_images[self.enemy_images_index][self.animation_frame]
        self.rect = self.image.get_rect(midbottom=(random.randint(self.WIDTH + 10, self.WIDTH + 200), self.place_to_stand))

    def apply_gravity(self):
        if self.rect.bottom < self.place_to_stand:
            self.GRAVITY += 1
            self.rect.y += self.GRAVITY
        elif self.rect.bottom == self.place_to_stand:
            self.GRAVITY = 0
        elif self.rect.bottom >= self.place_to_stand:
            self.rect.bottom = self.place_to_stand

    def animation(self):
        self.animation_frame += 0.1
        if self.animation_frame >= len(self.enemy_images[self.enemy_images_index]):
            self.animation_frame = 0
        self.image = self.enemy_images[self.enemy_images_index][int(self.animation_frame)]

    def update(self):
        self.apply_gravity()
        self.animation()
        self.rect.x -= 2
        if self.rect.x <= -60:
            self.kill()