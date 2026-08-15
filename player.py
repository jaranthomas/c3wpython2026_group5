import pygame
import sys


class Player:
    def __init__(self, start_x, start_y, sprite_path="player.png"):
        # Starting Spawn
        self.spawn_x = start_x
        self.spawn_y = start_y

        # Position
        self.x = start_x
        self.y = start_y

        # Collision Hitbox
        self.width = 32
        self.height = 48

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        # -------------------------
        # Player Sprite
        # -------------------------

        self.sprite_width = 128
        self.sprite_height = 128

        self.sprite = pygame.image.load(
            sprite_path
        ).convert_alpha()

        self.sprite = pygame.transform.scale(
            self.sprite,
            (self.sprite_width, self.sprite_height)
        )

        # Move the visual sprite down.
        # Increase this if the player still looks like it is floating.
        self.sprite_y_offset = 27

        # -------------------------
        # Lives & Health
        # -------------------------

        self.max_lives = 2
        self.lives = self.max_lives

        # -------------------------
        # Invincibility
        # -------------------------

        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1000

        # -------------------------
        # Movement
        # -------------------------

        self.vel_x = 0
        self.vel_y = 0

        self.is_grounded = False
        self.form = "SOLID"
        self.facing_right = True

        # -------------------------
        # Lives Icon
        # -------------------------

        self.lives_icon = pygame.image.load(
            "lives.png"
        ).convert_alpha()

        self.lives_icon = pygame.transform.scale(
            self.lives_icon,
            (128, 128)
        )

    # ==================================================
    # DAMAGE
    # ==================================================

    def take_damage(self):

        if not self.invincible:

            self.lives -= 1

            print(
                f"Lives remaining: {self.lives}"
            )

            if self.lives <= 0:

                print("GAME OVER")

                return True

            self.invincible = True

            self.invincible_timer = (
                pygame.time.get_ticks()
            )

        return False

    # ==================================================
    # INVINCIBILITY
    # ==================================================

    def update_invincibility(self):

        if self.invincible:

            current_time = pygame.time.get_ticks()

            if (
                current_time
                - self.invincible_timer
                >= self.invincible_duration
            ):

                self.invincible = False

    # ==================================================
    # RESET
    # ==================================================

    def reset_game(self):

        self.x = self.spawn_x
        self.y = self.spawn_y

        self.vel_x = 0
        self.vel_y = 0

        self.lives = self.max_lives

        self.invincible = False
        self.form = "SOLID"

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    # ==================================================
    # LIVES UI
    # ==================================================

    def draw_lives_ui(self, screen):

        screen_height = screen.get_height()

        start_x = 20
        start_y = screen_height - 50

        for i in range(self.lives):

            screen.blit(
                self.lives_icon,
                (
                    start_x + (i * 40),
                    start_y
                )
            )

    # ==================================================
    # DRAW PLAYER
    # ==================================================

    def draw(self, screen):

        # Create a rectangle for the 128x128 sprite
        sprite_rect = self.sprite.get_rect()

        # Centre the sprite horizontally
        # and align its bottom with the hitbox
        sprite_rect.midbottom = self.rect.midbottom

        # Move the visual sprite down
        sprite_rect.y += self.sprite_y_offset

        # Flip the sprite when moving left
        if not self.facing_right:

            flipped_sprite = pygame.transform.flip(
                self.sprite,
                True,
                False
            )

            screen.blit(
                flipped_sprite,
                sprite_rect
            )

        else:

            screen.blit(
                self.sprite,
                sprite_rect
            )

        # Draw lives
        self.draw_lives_ui(screen)


# ======================================================
# MOVEMENT
# ======================================================

class Movement:

    def __init__(
        self,
        speed=5,
        gravity=0.5,
        jump_power=-11
    ):

        self.speed = speed
        self.gravity = gravity
        self.jump_power = jump_power

    # ==================================================
    # INPUT
    # ==================================================

    def handle_input(self, player):

        keys = pygame.key.get_pressed()

        # -------------------------
        # Horizontal Movement
        # -------------------------

        player.vel_x = 0

        if (
            keys[pygame.K_LEFT]
            or keys[pygame.K_a]
        ):

            player.vel_x = -self.speed

            player.facing_right = False

        if (
            keys[pygame.K_RIGHT]
            or keys[pygame.K_d]
        ):

            player.vel_x = self.speed

            player.facing_right = True

        # -------------------------
        # Jumping
        # -------------------------

        if (
            keys[pygame.K_SPACE]
            or keys[pygame.K_w]
            or keys[pygame.K_UP]
        ) and player.is_grounded:

            player.vel_y = self.jump_power

            player.is_grounded = False

    # ==================================================
    # UPDATE
    # ==================================================

    def update(self, player, platforms):

        # -------------------------
        # Gravity
        # -------------------------

        player.vel_y += self.gravity

        # -------------------------
        # Horizontal Movement
        # -------------------------

        player.x += player.vel_x

        player.rect = pygame.Rect(
            player.x,
            player.y,
            player.width,
            player.height
        )

        # Wall collisions
        for platform in platforms:

            if player.rect.colliderect(platform):

                if player.vel_x > 0:

                    player.x = (
                        platform.left
                        - player.width
                    )

                elif player.vel_x < 0:

                    player.x = platform.right

        # -------------------------
        # Vertical Movement
        # -------------------------

        player.y += player.vel_y

        player.rect = pygame.Rect(
            player.x,
            player.y,
            player.width,
            player.height
        )

        player.is_grounded = False

        # Floor and ceiling collisions
        for platform in platforms:

            if player.rect.colliderect(platform):

                # Landing on platform
                if player.vel_y > 0:

                    player.y = (
                        platform.top
                        - player.height
                    )

                    player.vel_y = 0

                    player.is_grounded = True

                # Hitting ceiling
                elif player.vel_y < 0:

                    player.y = platform.bottom

                    player.vel_y = 0

        # -------------------------
        # Sync Hitbox
        # -------------------------

        player.rect = pygame.Rect(
            player.x,
            player.y,
            player.width,
            player.height
        )