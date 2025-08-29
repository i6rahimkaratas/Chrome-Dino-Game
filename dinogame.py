import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinozor Oyunu")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_COLOR = (150, 150, 150)

current_dir = os.path.dirname(__file__)
assets_dir = os.path.join(current_dir, 'assets')

try:
    dino_img = pygame.image.load(os.path.join(assets_dir, 'dinosour.webp')).convert_alpha()
    cactus_img = pygame.image.load(os.path.join(assets_dir, 'kaktus.gif')).convert_alpha()
    dino_img = pygame.transform.scale(dino_img, (40, 40))
    cactus_img = pygame.transform.scale(cactus_img, (30, 40))
except pygame.error as e:
    print(f"Resim yüklenirken hata oluştu: {e}")
    print(" 'dinosour.webp' ve 'kaktus.gif' dosyalarının olduğundan emin olun.")
    pygame.quit()
    exit()

dino_width = dino_img.get_width()
dino_height = dino_img.get_height()
dino_x = 50
dino_y = SCREEN_HEIGHT - dino_height - 20
dino_vel_y = 0
gravity = 1
is_jumping = False

cactus_width = cactus_img.get_width()
cactus_height = cactus_img.get_height()
cactus_speed = 5
cactus_list = []
cactus_spawn_timer = 0
cactus_spawn_interval = 90

ground_height = 20
ground_y = SCREEN_HEIGHT - ground_height

score = 0
font = pygame.font.Font(None, 36)
game_over = False

def draw_dino(x, y):
    screen.blit(dino_img, (x, y))

def draw_cactus(x, y):
    screen.blit(cactus_img, (x, y))

def draw_ground():
    pygame.draw.rect(screen, GROUND_COLOR, (0, ground_y, SCREEN_WIDTH, ground_height))

def check_collision(dino_rect, cactus_rect):
    return dino_rect.colliderect(cactus_rect)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping and not game_over:
                is_jumping = True
                dino_vel_y = -15
            if event.key == pygame.K_r and game_over:
                game_over = False
                score = 0
                cactus_list = []
                dino_y = SCREEN_HEIGHT - dino_height - 20
                dino_vel_y = 0
                is_jumping = False

    if not game_over:
        if is_jumping:
            dino_y += dino_vel_y
            dino_vel_y += gravity
            if dino_y >= SCREEN_HEIGHT - dino_height - 20:
                dino_y = SCREEN_HEIGHT - dino_height - 20
                is_jumping = False
                dino_vel_y = 0

        cactus_spawn_timer += 1
        if cactus_spawn_timer >= cactus_spawn_interval:
            cactus_spawn_timer = 0
            new_cactus_x = SCREEN_WIDTH + random.randint(0, 100)
            cactus_list.append(pygame.Rect(new_cactus_x, SCREEN_HEIGHT - cactus_height - 20, cactus_width, cactus_height))

        for cactus in cactus_list[:]:
            cactus.x -= cactus_speed
            if cactus.x < -cactus_width:
                cactus_list.remove(cactus)
                score += 1

        dino_rect = pygame.Rect(dino_x, dino_y, dino_width, dino_height)
        for cactus in cactus_list:
            if check_collision(dino_rect, cactus):
                game_over = True

    screen.fill(WHITE)
    draw_ground()
    draw_dino(dino_x, dino_y)
    for cactus in cactus_list:
        draw_cactus(cactus.x, cactus.y)

    score_text = font.render(f"Skor: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    if game_over:
        game_over_text = font.render("OYUN BİTTİ! Yeniden Başlamak İçin 'R' Tuşuna Basın", True, BLACK)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()