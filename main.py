import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cookie Clicker")

cookie_img = pygame.image.load("cookie.png")
cookie_img = pygame.transform.scale(cookie_img, (374, 350))

font = pygame.font.Font(None, 36)

cookies = 0
click_value = 1


class Cookie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cookie_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 3, HEIGHT // 2)

    def clicked(self):
        global cookies, click_value
        cookies += click_value


cookie_sprite = pygame.sprite.Group()
cookie = Cookie()
cookie_sprite.add(cookie)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if cookie.rect.collidepoint(event.pos):
                    cookie.clicked()

    cookie_sprite.update()

    screen.fill(BLACK)
    cookie_sprite.draw(screen)

    cookie_text = font.render("Cookies: " + str(cookies), True, WHITE)
    screen.blit(cookie_text, (10, 10))

    pygame.display.flip()

pygame.quit()
