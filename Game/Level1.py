import pygame.sprite
import time
import sys
from Tilemap import *
from Hearts import Hearts
from pytmx.util_pygame import load_pygame
from Slime import Slime
from Level import Level
class Level1(Level):
    def __init__(self):
        super().__init__()
        self.SURFACE = pygame.display.get_surface()
        self.running = True
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
            SpecialTile(pos, surface, [self.all_sprites, self.collision_sprites, self.pushable_tiles,
                                       self.front_sprites], self.player_group, self.hearts_group)
        # -------------------------------------SPRITES----------------------------------------------------#
        Slime((950, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((3000, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((2200, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((2900, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((4360, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((3850, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((4000, HIGH - 180), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((4140, 340), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((4050, 340), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((5334, 670), [self.all_sprites, self.enemies], self.collision_sprites, self.player)
        Slime((5000, 670), [self.all_sprites, self.enemies], self.collision_sprites, self.player)

    def player_killed(self):
        if self.player.lives <= 0:
            self.player.kill()
            self.running = False
        if self.player.rect.centery >= HIGH:
            if self.player.lives >= 3:
                self.player.lives = 1
            else:
                self.player.lives -= 1
            self.player.smaller()
            self.player.rect.center = self.player.pos
            self.all_sprites.offset = pygame.math.Vector2(0, 0)

    def make_hearts(self):
        self.hearts_group.empty()
        pos = [10, 10]
        h_id = 1
        for heart in range(self.player.lives):
            Hearts(h_id, pos, self.hearts_group, self.player.lives)
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
            self.front_sprites.custom_draw(self.player)
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