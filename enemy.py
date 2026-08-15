import random
import pygame


class Enemy:
    def __init__(self, x, y, walk_distance):
        # Pool of available enemy sprite files
        sprite_files = ["temp1.png", "temp2.png", "temp3.png"]

        # Pick one random sprite image
        chosen_sprite = random.choice(sprite_files)
        self.image = pygame.image.load(chosen_sprite).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))

        # Position & Patrol Limits
        self.rect = pygame.Rect(x, y, 32, 32)
        self.start_x = x
        self.end_x = x + walk_distance

        # Speeds & Gravity
        self.patrol_speed = 2
        self.chase_speed = 3.5
        self.vel_y = 0
        self.gravity = 0.5

        self.facing_right = True

    def update(
        self, player, camera_x, camera_y, screen_width, screen_height, platforms
    ):
        # GRAVITY & GROUND COLLISION
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vel_y > 0:  # Landing on ground
                    self.rect.bottom = platform.top
                    self.vel_y = 0

        camera_rect = pygame.Rect(
            camera_x, camera_y, screen_width, screen_height
        )
        is_visible = self.rect.colliderect(camera_rect)

        if is_visible:
            if player.x > self.rect.x:
                self.rect.x += self.chase_speed
                self.facing_right = True
            elif player.x < self.rect.x:
                self.rect.x -= self.chase_speed
                self.facing_right = False
        else:
            if self.facing_right:
                self.rect.x += self.patrol_speed
                if self.rect.x >= self.end_x:
                    self.facing_right = False
            else:
                self.rect.x -= self.patrol_speed
                if self.rect.x <= self.start_x:
                    self.facing_right = True

    def check_player_collision(self, player):
        if self.rect.colliderect(player.rect):
            print("You got hit.")
            player.x, player.y = 100, 400
            player.vel_x, player.vel_y = 0, 0

    def draw(self, screen, camera_x=0, camera_y=0):
        render_img = pygame.transform.flip(
            self.image, not self.facing_right, False
        )
        screen.blit(
            render_img, (self.rect.x - camera_x, self.rect.y - camera_y)
        )