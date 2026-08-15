import pygame


class Player:
    def __init__(self, start_x, start_y):
        # Starting Spawn
        self.spawn_x = start_x
        self.spawn_y = start_y

        # Position & Hitbox
        self.x = start_x
        self.y = start_y
        self.width = 32
        self.height = 48
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Lives & Health State
        self.max_lives = 2
        self.lives = self.max_lives

        # Invincibility Frames
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1000

        # Movement Variables
        self.vel_x = 0
        self.vel_y = 0
        self.is_grounded = False
        self.form = "SOLID"
        self.facing_right = True

        # UI Assets
        self.lives_icon = pygame.image.load("lives.png").convert_alpha()
        self.lives_icon = pygame.transform.scale(self.lives_icon, (32, 32))

    def take_damage(self):
        if not self.invincible:
            self.lives -= 1
            print(f"Lives remaining: {self.lives}")

            if self.lives <= 0:
                print("GAME OVER")
                return True  # Signals full restart to game loop

            # Brief invincibility after getting hit
            self.invincible = True
            self.invincible_timer = pygame.time.get_ticks()

        return False

    def update_invincibility(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_timer >= self.invincible_duration:
                self.invincible = False

    def reset_game(self):
        self.x = self.spawn_x
        self.y = self.spawn_y
        self.vel_x = 0
        self.vel_y = 0
        self.lives = self.max_lives
        self.invincible = False
        self.form = "SOLID"
        self.height = 48
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw_lives_ui(self, screen):
        screen_height = screen.get_height()
        start_x = 20
        start_y = screen_height - 50

        for i in range(self.lives):
            screen.blit(self.lives_icon, (start_x + (i * 40), start_y))

    def draw(self, screen):
        # Default placeholder rectangle (blue) if no sprite is loaded
        pygame.draw.rect(screen, (0, 120, 255), self.rect)
        self.draw_lives_ui(screen)


class Movement:
    def __init__(self, speed=5, gravity=0.5, jump_power=-11):
        self.speed = speed
        self.gravity = gravity
        self.jump_power = jump_power

    def handle_input(self, player):
        keys = pygame.key.get_pressed()

        # Horizontal Movement (A/D or Arrow keys)
        player.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.vel_x = -self.speed
            player.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.vel_x = self.speed
            player.facing_right = True

        # Jumping (Space, W, or Up Arrow)
        if (
            keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]
        ) and player.is_grounded:
            player.vel_y = self.jump_power
            player.is_grounded = False

    def update(self, player, platforms):
        # 1. Apply Gravity
        player.vel_y += self.gravity

        # 2. Horizontal Movement & Wall Collisions
        player.x += player.vel_x
        player.rect = pygame.Rect(
            player.x, player.y, player.width, player.height
        )
        for platform in platforms:
            if player.rect.colliderect(platform):
                if player.vel_x > 0:  # Hit left side of wall
                    player.x = platform.left - player.width
                elif player.vel_x < 0:  # Hit right side of wall
                    player.x = platform.right

        # 3. Vertical Movement & Floor/Ceiling Collisions
        player.y += player.vel_y
        player.rect = pygame.Rect(
            player.x, player.y, player.width, player.height
        )
        player.is_grounded = False

        for platform in platforms:
            if player.rect.colliderect(platform):
                if player.vel_y > 0:  # Landing on top of platform
                    player.y = platform.top - player.height
                    player.vel_y = 0
                    player.is_grounded = True
                elif player.vel_y < 0:  # Hitting ceiling
                    player.y = platform.bottom
                    player.vel_y = 0

        # Sync final rectangle position
        player.rect = pygame.Rect(
            player.x, player.y, player.width, player.height
        )