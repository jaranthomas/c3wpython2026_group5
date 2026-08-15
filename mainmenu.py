import sys
import pygame

pygame.init()

 
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LIQUIDATION")
clock = pygame.time.Clock()


BG_TOP = (15, 12, 30)      
BG_BOTTOM = (45, 20, 70)    
PANEL_COLOR = (25, 22, 45)  
BORDER_PLAY = (0, 255, 150) 
BORDER_QUIT = (255, 0, 100) 
TEXT_COLOR = (240, 240, 255)
SHADOW_COLOR = (5, 5, 15)   


title_font = pygame.font.SysFont("Arial", 80)
button_font = pygame.font.SysFont("Arial", 32, bold=True)


def draw_gradient_bg():
  
    for y in range(HEIGHT):
        
        ratio = y / HEIGHT
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))


def draw_text_with_shadow(text, font, color, surface, x, y):
    
    
    shadow_obj = font.render(text, True, SHADOW_COLOR)
    shadow_rect = shadow_obj.get_rect(center=(x + 4, y + 4))
    surface.blit(shadow_obj, shadow_rect)
    
    
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)


def draw_styled_button(rect, text, is_hovered, theme_color):
    
    
    render_rect = rect.copy()
    if is_hovered:
        render_rect.y -= 4

    
    shadow_rect = render_rect.copy()
    shadow_rect.y += 6
    pygame.draw.rect(screen, SHADOW_COLOR, shadow_rect, border_radius=12)

    
    pygame.draw.rect(screen, PANEL_COLOR, render_rect, border_radius=12)

   
    border_thickness = 4 if is_hovered else 2
    pygame.draw.rect(screen, theme_color, render_rect, width=border_thickness, border_radius=12)

  
    draw_text_with_shadow(text, button_font, TEXT_COLOR, screen, render_rect.centerx, render_rect.centery)


def main_menu():
    
    while True:
       
        draw_gradient_bg()

        
        draw_text_with_shadow("LIQUIDATION", title_font, TEXT_COLOR, screen, WIDTH // 2, 160)

       
        mx, my = pygame.mouse.get_pos()

       
        play_button = pygame.Rect(WIDTH // 2 - 150, 320, 300, 60)
        quit_button = pygame.Rect(WIDTH // 2 - 150, 430, 300, 60)

        
        play_hover = play_button.collidepoint((mx, my))
        quit_hover = quit_button.collidepoint((mx, my))

        
        draw_styled_button(play_button, "PLAY", play_hover, BORDER_PLAY)
        draw_styled_button(quit_button, "QUIT", quit_hover, BORDER_QUIT)

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if play_hover:
                        game_loop()  
                    if quit_hover:
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(60)


def game_loop():
    
    running = True
    while running:
        screen.fill((240, 240, 255))
        
        escape_text = button_font.render("Press ESC to Exit to Menu", True, (100, 100, 150))
        escape_rect = escape_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        screen.blit(escape_text, escape_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False 

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main_menu()
