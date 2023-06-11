from Settings import *
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, enemies, pushable_tiles):
        super().__init__(group)
        self.collision_sprites = collision_sprites
        self.enemies = enemies
        self.pushable_tiles = pushable_tiles
        # ------------------------------PLAYER IMAGES----------------------------------------------#
        player_left = pygame.image.load('../Assets/Player/avocado-left.png').convert_alpha()
        player_left2 = pygame.image.load('../Assets/Player/avocado-left2.png').convert_alpha()
        player_right = pygame.image.load('../Assets/Player/avocado-right.png').convert_alpha()
        player_right2 = pygame.image.load('../Assets/Player/avocado-right2.png').convert_alpha()
        player_jump_right = pygame.image.load('../Assets/Player/avocado-jump_right.png').convert_alpha()
        player_jump_left = pygame.image.load('../Assets/Player/avocado-jump_left.png').convert_alpha()

        self.image_list = [[player_left, player_left2], [player_right, player_right2], player_jump_left,
                           player_jump_right]
        self.player_images_index = 1
        self.animation_frame = 0
        # ------------------------------BASICS---------------------------------------------------#
        self.image = self.image_list[self.player_images_index][0]
        self.rect = self.image.get_rect(center=pos)

        self.GRAVITY = 0.8
        self.JUMP_HIGH = -18
        self.SPEED = 8
        self.pos = pos
        self.lives = PLAYER_LIVES
        self.in_air = False
        self.direction = pygame.math.Vector2(0, 0)
        self.delay = 100
        self.is_bigger = False

    def get_input(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.in_air is False:
            self.in_air = True
            self.proper_image()
            self.direction.y = self.JUMP_HIGH
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            if self.in_air is not True:
                self.player_images_index = 1
                self.animation(dt)
            else:
                self.player_images_index = 3
                self.image = self.image_list[self.player_images_index]
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            if self.in_air is not True:
                self.player_images_index = 0
                self.animation(dt)
            else:
                self.player_images_index = 2
                self.image = self.image_list[self.player_images_index]
        else:
            self.direction.x = 0

    def animation(self, dt):
        self.animation_frame += 0.1 * dt * 60
        if self.animation_frame >= len(self.image_list[self.player_images_index]):
            self.animation_frame = 0
        self.image = self.image_list[self.player_images_index][int(self.animation_frame)]

    def proper_image(self):
        if self.in_air is True:
            if self.image == self.image_list[1][0] or self.image == self.image_list[1][1]:
                self.player_images_index = 3
                self.image = self.image_list[self.player_images_index]
            elif self.image == self.image_list[0][0] or self.image == self.image_list[0][1]:
                self.player_images_index = 2
                self.image = self.image_list[self.player_images_index]
        elif self.in_air is not True:
            if self.player_images_index == 3:  # player_jump_right
                self.player_images_index = 1
                self.image = self.image_list[self.player_images_index][0]
            elif self.player_images_index == 2:  # player_jump_left
                self.player_images_index = 0
                self.image = self.image_list[self.player_images_index][0]

    def gravity(self, dt):
        self.direction.y += self.GRAVITY * dt * 60
        self.rect.y += self.direction.y * dt * 60

    def check_collision_objects(self, dt):
        hits = []
        self.pushable_tiles.update(dt)
        for sprite in self.collision_sprites:
            if self.rect.colliderect(sprite):
                hits.append(sprite)
        for enemy in self.enemies:
            if self.rect.colliderect(enemy):
                hits.append(enemy)
                if self.direction.y > 0:
                    enemy.alive = False
                if self.delay >= 100 and not self.direction.y > 0 and enemy.alive:
                    self.lives -= 1
                    self.delay = 0
            if self.delay < 100:
                self.delay += 1
        return hits

    def horizontal_collision(self, dt):
        self.rect.x += self.direction.x * self.SPEED * dt * 60
        collisions = self.check_collision_objects(dt)
        for tile in collisions:
            if self.direction.x > 0:
                self.rect.right = tile.rect.left
            elif self.direction.x < 0:
                self.rect.left = tile.rect.right

    def vertical_collision(self, dt):
        self.gravity(dt)
        collisions = self.check_collision_objects(dt)
        for tile in collisions:
            if self.direction.y > 0:
                self.rect.bottom = tile.rect.top
                self.direction.y = 0
                self.in_air = False
                self.proper_image()

            elif self.direction.y < 0:
                self.rect.top = tile.rect.bottom
                self.direction.y = 0

    def bigger(self):
        if not self.is_bigger:
            for i in range(len(self.image_list)):
                if hasattr(self.image_list[i], '__iter__'):
                    for j in range(len(self.image_list[i])):
                        self.image_list[i][j] = pygame.transform.scale_by(self.image_list[i][j], 1.5)
                else:
                    self.image_list[i] = pygame.transform.scale_by(self.image_list[i], 1.5)
            self.rect = self.rect.scale_by(1.5, 1.5)
            self.is_bigger = True

    def smaller(self):
        if self.is_bigger:
            for i in range(len(self.image_list)):
                if hasattr(self.image_list[i], '__iter__'):
                    for j in range(len(self.image_list[i])):
                        self.image_list[i][j] = pygame.transform.scale_by(self.image_list[i][j], 0.5)
                else:
                    self.image_list[i] = pygame.transform.scale_by(self.image_list[i], 0.5)
            self.rect = self.rect.scale_by(0.5, 0.5)
            self.is_bigger = False

    def update(self, dt):
        self.get_input(dt)
        self.horizontal_collision(dt)
        self.vertical_collision(dt)