from Settings import *
class Potion(pygame.sprite.Sprite):
    def __init__(self, pos, all_sprites_group, collision_sprites, player_group, tile_top):
        super().__init__(all_sprites_group)
        self.image = pygame.image.load('../Assets/potion.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        # ------------------------------VARIABLES----------------------------------------------#
        self.GRAVITY = 0.8
        self.SPEED = 2
        self.tile_top = tile_top
        self.direction = pygame.math.Vector2(1, 0)
        self.go_out = False
        self.start = False
        # ------------------------------COLLISION---------------------------------------------------#
        self.collision_sprites = collision_sprites
        self.player_group = player_group

    def gravity(self, dt):
        self.direction.y += self.GRAVITY * dt * 60
        self.rect.y += self.direction.y * dt * 60

    def get_player(self):
        for player in self.player_group:
            return player

    def check_collision_objects(self):
        player = self.get_player()
        hits = []
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite):
                hits.append(sprite)
        if self.rect.colliderect(player):
            player.lives += 1
            player.bigger()
            self.kill()
        return hits

    def horizontal_collision(self, dt):
        collisions = self.check_collision_objects()
        for tile in collisions:
            if self.direction.x > 0:
                self.direction.x = -1
                self.rect.right = tile.rect.left - 10 * dt * 60
            elif self.direction.x < 0:
                self.direction.x = 1
                self.rect.left = tile.rect.right + 10 * dt * 60

    def vertical_collision(self, dt):
        self.gravity(dt)
        collisions = self.check_collision_objects()
        for tile in collisions:
            if self.direction.y > 0:
                self.rect.bottom = tile.rect.top
                self.direction.y = 0
            elif self.direction.y < 0:
                self.rect.top = tile.rect.bottom
                self.direction.y = 0

    def going_out(self, dt):
        self.direction.y = -1
        self.rect.bottom += self.direction.y * self.SPEED * dt * 60
        if self.rect.bottom < self.tile_top:
            self.start = False
            self.go_out = True

    def update(self, dt):
        if self.start:
            self.going_out(dt)

        if self.go_out:
            self.rect.x += self.direction.x * self.SPEED * dt * 60
            self.horizontal_collision(dt)
            self.vertical_collision(dt)

        if self.rect.x <= -60:
            self.kill()