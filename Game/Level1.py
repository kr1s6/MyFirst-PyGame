import pygame.sprite
from Settings import *
import time
import sys
from Player import Player
from Tilemap import *
from Hearts import Hearts
from pytmx.util_pygame import load_pygame
from Slime import Slime
class Level1:
    def __init__(self):
        self.SURFACE = pygame.display.get_surface()
        self.running = True
        # ------------------------------SPRITE GROUPS----------------------------------------------#
        self.player_group = pygame.sprite.Group()
        self.hearts_group = pygame.sprite.Group()
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.pushable_tiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        # ------------------------------TILE MAP---------------------------------------------------#
        tmx = load_pygame('../Assets/Level1/tilemap.tmx')
        ground_layer = tmx.get_layer_by_name("ground")
        brick_layer = tmx.get_layer_by_name("brick")
        special_layer = tmx.get_layer_by_name("special")

        for x, y, surface in ground_layer.tiles():
            pos = (x * 64, y * 64)
            Tile(pos, surface, [self.all_sprites, self.collision_sprites])
        for x, y, surface in brick_layer.tiles():
            pos = (x * 64, y * 64)
            BrickTile(pos, surface, [self.all_sprites, self.collision_sprites, self.pushable_tiles], self.player_group)
        for x, y, surface in special_layer.tiles():
            pos = (x * 64, y * 64)
            SpecialTile(pos, surface, [self.all_sprites, self.collision_sprites, self.pushable_tiles], self.player_group)
        # -------------------------------------PLAYER----------------------------------------------------#
        self.player = Player((250, HIGH - 180), [self.all_sprites, self.player_group], self.collision_sprites,
                             self.enemies, self.pushable_tiles)
        # -------------------------------------SPRITES----------------------------------------------------#
        Slime((950, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((3000, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)

    def player_killed(self):
        if self.player.lives <= 0:
            self.player.kill()
            self.running = False
        if self.player.rect.centery >= HIGH:
            self.player.lives -= 1
            self.player.rect.center = self.player.pos
            self.all_sprites.offset = pygame.math.Vector2(0, 0)

    def make_hearts(self):
        self.hearts_group.empty()
        pos = [10, 10]
        h_id = 1
        for heart in range(self.player.lives):
            Hearts(h_id, pos, self.hearts_group)
            pos[0] += 30
            h_id += 1

    def run(self):
        self.make_hearts()
        # ---------------------------------------------------------------------------------#
        previous_time = time.time()
        while self.running:
            dt = time.time() - previous_time
            previous_time = time.time()
            # --------------------------------MAIN ACTIONS-------------------------------------#
            self.SURFACE.fill('black')
            self.all_sprites.custom_draw(self.player)
            self.all_sprites.update(dt)
            self.player_killed()
            for sprite in self.hearts_group.sprites():
                sprite.update(self.player.lives)
            # ----------------------------------------------------------------------------#
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            # ----------------------------------------------------------------------------#
            pygame.display.update()
            CLOCK.tick(60)
        self.running = True

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.SURFACE = pygame.display.get_surface()
        self.offset = pygame.math.Vector2(0, 0)
        # ------------------------------LEVEL 1 GRAPHIC----------------------------------------------#
        self.background = pygame.image.load('../Assets/Level1/background_lvl1.png').convert()
        self.background = pygame.transform.scale_by(self.background, 8)
        self.background_rect = self.background.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # ------------------------------PLAYER CENTERING----------------------------------------------#
        if player.rect.centerx >= WIDTH/2:
            self.offset.x = player.rect.centerx - WIDTH/2
        if player.rect.centery <= HIGH/2:
            self.offset.y = player.rect.centery - HIGH/2
        # ------------------------------DRAWING GRAPHICS CENTERED ON PLAYER---------------------------#
        background_offset = self.background_rect.topleft
        self.SURFACE.blit(self.background, background_offset)

        for sprite in self.sprites():
            offset_rect = sprite.rect.copy()
            offset_rect.center -= self.offset
            self.SURFACE.blit(sprite.image, offset_rect)