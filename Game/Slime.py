import pygame
import random

class Slime(pygame.sprite.Sprite):
    def __init__(self, place_to_stand, group):
        super().__init__(group)
        self.WIDTH = pygame.display.get_window_size()[0]
        self.HIGH = pygame.display.get_window_size()[1]
        self.place_to_stand = place_to_stand
        self.GRAVITY = 1
        self.jump = False
        self.JUMP_HIGH = 10
        self.y_velocity = self.JUMP_HIGH
        self.JUMP_DELAY = 100
        self.jump_timer = 0

        slime_left = pygame.image.load('Game/Assets/Slimes/slime-left.png').convert_alpha()
        slime_left = pygame.transform.scale_by(slime_left, 3)
        slime_right = pygame.image.load('Game/Assets/Slimes/slime-right.png').convert_alpha()
        slime_right = pygame.transform.scale_by(slime_right, 3)

        self.enemy_images = [slime_left, slime_right]
        self.enemy_images_index = 0
        self.animation_frame = 0
        self.image = self.enemy_images[self.enemy_images_index]
        self.rect = self.image.get_rect(midbottom=(random.randint(self.WIDTH - 100, self.WIDTH), self.place_to_stand))

    def apply_gravity(self):
        if self.jump is True:
            self.rect.x -= 5
            self.rect.y -= self.y_velocity
            self.y_velocity -= self.GRAVITY
            if self.y_velocity < -self.JUMP_HIGH:
                self.jump = False
                self.y_velocity = self.JUMP_HIGH
        else:
            self.rect.bottom = self.place_to_stand

    def slime_jump(self):
        if self.jump_timer == self.JUMP_DELAY:
            self.jump = True
            self.jump_timer = 0
        else:
            self.jump_timer += 1

    def update(self):
        self.slime_jump()
        self.apply_gravity()
        if self.rect.x <= -60:
            self.kill()