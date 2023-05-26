import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cookie Clicker")

cookie_img = pygame.image.load("cookie.png")
cookie_img = pygame.transform.scale(cookie_img, (374, 350))
cursor_img = pygame.image.load("cursor.png")
cursor_img = pygame.transform.scale(cursor_img, (30, 30))

font = pygame.font.Font(None, 36)

cookies = 0
click_value = 1
cursor_cost = 10
cursor_count = 0
cursor_auto_collect = 1
cps_timer = pygame.time.get_ticks()
cps_delay = 1000
cookies_per_second = 0


def collect_cookies():
    global cookies
    cookies_from_cursors = cursor_count*cursor_auto_collect
    cookies += cookies_from_cursors


class Cookie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cookie_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 3, HEIGHT // 2)

    def clicked(self):
        global cookies, click_value
        cookies += click_value


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cursor_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50))
        self.auto_collect = cursor_auto_collect

    def update(self):
        global cookies
        cookies += self.auto_collect


cookie_sprite = pygame.sprite.Group()
cursor_sprite = pygame.sprite.Group()
cookie = Cookie()
cookie_sprite.add(cookie)

window_width = 270
window_height = 50
window_x = WIDTH - window_width - 50
window_y = 50

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if cookie.rect.collidepoint(event.pos):
                    cookie.clicked()
                if window_x <= event.pos[0] <= window_x + window_width:
                    if window_y <= event.pos[1] <= window_y + window_height:
                        if cookies >= cursor_cost:
                            cookies -= cursor_cost
                            cursor = Cursor()
                            cursor_sprite.add(cursor)
                            cursor_count += 1
                            cursor_cost = int(cursor_cost + 10)

    cookie_sprite.update()

    screen.fill(BLACK)
    cookie_sprite.draw(screen)
    cursor_sprite.draw(screen)

    cookie_text = font.render("Cookies: " + str(cookies), True, WHITE)
    screen.blit(cookie_text, (10, 10))

    pygame.draw.rect(screen, CYAN, (window_x, window_y, window_width, window_height))
    window_text = font.render("Buy Cursor (Cost: " + str(cursor_cost) + ")", True, WHITE)
    screen.blit(window_text, (window_x + 10, window_y + 10))

    current_time = pygame.time.get_ticks()
    if current_time - cps_timer >= cps_delay:
        collect_cookies()
        cookies_per_second = cursor_auto_collect * cursor_count
        cps_timer = current_time

    cps_text = font.render("Cookies/sec: " + str(cookies_per_second), True, WHITE)
    screen.blit(cps_text, (10, 90))

    pygame.display.flip()

pygame.quit()
