from Settings import *
class Hearts(pygame.sprite.Sprite):
    def __init__(self, h_id, pos, group, player_lives):
        super().__init__(group)
        self.SURFACE = pygame.display.get_surface()
        self.id = h_id
        self.lives = player_lives
        # ------------------------------HEARTS IMAGES------------------------------------------------#
        self.heart = pygame.image.load('../Assets/Player/heart.png').convert_alpha()
        self.heart_rect = self.heart.get_rect(topleft=pos)
        self.heart_empty = pygame.image.load('../Assets/Player/heart-empty.png').convert_alpha()
        self.heart_empty_rect = self.heart.get_rect(topleft=pos)
        # ------------------------------VARIABLES------------------------------------------------#
        self.image = self.heart
        self.rect = self.heart_rect

    def update(self, player_lives):
        self.SURFACE.blit(self.image, self.rect)
        self.empty_heart(player_lives)

    def empty_heart(self, player_lives):
        if player_lives < self.lives and self.id == self.lives:
            self.lives -= 1
            self.image = self.heart_empty
            self.rect = self.heart_empty_rect
        elif player_lives < self.lives:
            self.lives -= 1
