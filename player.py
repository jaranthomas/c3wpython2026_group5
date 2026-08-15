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