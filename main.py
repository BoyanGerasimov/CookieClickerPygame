import pygame
import random
import math

pygame.init()

clock = pygame.time.Clock()
WIDTH = 1200
HEIGHT = 1000

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CYAN = (0, 100, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vodka Clicker")

cookie_img = pygame.image.load("Vodka.png")
cookie_img = pygame.transform.scale(cookie_img, (374, 350))
cursor_img = pygame.image.load("cursor.png")
cursor_img = pygame.transform.scale(cursor_img, (30, 30))


font = pygame.font.Font(None, 36)

cookies = 1000000
click_value = 1
cursor_cost = 10
cursor_count = 0
cursor_auto_collect = 1
grandma_cost = 40
grandma_count = 0
cps_timer = pygame.time.get_ticks()
cps_delay = 1000
cookies_per_second = 0
grandma_auto_collect = 5


def collect_cookies():
    global cookies
    cookies_from_cursors = cursor_count * cursor_auto_collect
    cookies_from_grandmas = grandma_count * grandma_auto_collect
    cookies += cookies_from_cursors + cookies_from_grandmas


def clicked():
    global cookies, click_value
    cookies += click_value


class Cookie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cookie_img
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 4, HEIGHT // 2)


class Cursor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = cursor_img
        self.rect = self.image.get_rect()
        self.radius = 100
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = 0.02

    def update(self):
        self.angle += self.speed

        x = cookie.rect.centerx + int((self.radius + 50) * math.cos(self.angle))
        y = cookie.rect.centery + int((self.radius + 50) * math.sin(self.angle))
        self.rect.center = (x, y)


class Grandma(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        x = random.randint(0, 1)
        self.image = pygame.image.load(f"grandma_{x}.png")
        self.image = pygame.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()
        self.rect.center = (
            random.randint(window_x + 20, window_x + window_width - 20),
            random.randint(grandma_window_y + 20, grandma_window_y + HEIGHT // 4),
        )


class Upgrade:
    def __init__(self, name, description, cost, effect):
        self.name = name
        self.description = description
        self.cost = cost
        self.effect = effect


def increase_click_value(value):
    global click_value
    click_value += value


def increase_auto_clicker():
    global cursor_auto_collect
    cursor_auto_collect += 1


def double_grandma_production():
    global grandma_auto_collect
    grandma_auto_collect *= 2


cookie_sprite = pygame.sprite.Group()
cursor_sprite = pygame.sprite.Group()
grandma_sprite = pygame.sprite.Group()

cookie = Cookie()
cookie_sprite.add(cookie)

window_width = WIDTH // 3
window_height = 50
window_x = WIDTH - window_width - 50
window_y = 50
cursor_window_y = window_y + window_height + 10
grandma_window_y = HEIGHT - (HEIGHT // 4) - window_height

pygame.mixer.music.load("background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

upgrades = [
    Upgrade("Power Click", "Increase the value of each click by 1", 100, lambda: increase_click_value(1)),
    Upgrade("Auto-clicker", "Automatically generate cookies per second", 500, lambda: increase_auto_clicker()),
    Upgrade("Double Production", "Double the production of all grandmas", 1000, lambda: double_grandma_production()),
    # Add more upgrades here...
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if cookie.rect.collidepoint(event.pos):
                    clicked()
                elif window_x <= event.pos[0] <= window_x + window_width:
                    if window_y <= event.pos[1] <= window_y + window_height:
                        if cookies >= cursor_cost:
                            cookies -= cursor_cost
                            cursor = Cursor()
                            cursor_sprite.add(cursor)
                            cursor_count += 1
                            cursor_cost = int(cursor_cost + 10)
                    elif cursor_window_y <= event.pos[1] <= cursor_window_y + window_height:
                        if cookies >= grandma_cost:
                            cookies -= grandma_cost
                            grandma = Grandma()
                            grandma_sprite.add(grandma)
                            grandma_count += 1
                            grandma_cost = int(grandma_cost + 40)
                    elif upgrades_window_y <= event.pos[1] <= upgrades_window_y + window_height:
                        for upgrade in upgrades:
                            if upgrade.rect.collidepoint(event.pos) and cookies >= upgrade.cost:
                                cookies -= upgrade.cost
                                upgrade.cost *= 2
                                upgrade.effect()

    cookie_sprite.update()
    cursor_sprite.update()
    grandma_sprite.update()

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (window_x, grandma_window_y - 10, window_width, HEIGHT // 4 + 50))
    cookie_sprite.draw(screen)
    cursor_sprite.draw(screen)
    grandma_sprite.draw(screen)

    cookie_text = font.render("Vodkas: " + str(cookies), True, WHITE)
    screen.blit(cookie_text, (10, 10))

    pygame.draw.rect(screen, CYAN, (window_x, window_y, window_width, window_height))
    cursor_window_text = font.render("Buy Cursor (Cost: " + str(cursor_cost) + ")", True, WHITE)
    screen.blit(cursor_window_text, (window_x + 10, window_y + 10))

    pygame.draw.rect(screen, CYAN, (window_x, cursor_window_y, window_width, window_height))
    grandma_window_text = font.render("Buy Russian (Cost: " + str(grandma_cost) + ")", True, WHITE)
    screen.blit(grandma_window_text, (window_x + 10, cursor_window_y + 10))

    upgrades_window_y = cursor_window_y + window_height + 10
    upgrade_text_offset = 60
    for i, upgrade in enumerate(upgrades):
        upgrade_rect = pygame.Rect(window_x, upgrades_window_y + (i * upgrade_text_offset), window_width, window_height)
        pygame.draw.rect(screen, CYAN, upgrade_rect)
        upgrade.rect = upgrade_rect

        upgrade_name_text = font.render(upgrade.name + " (Cost: " + str(upgrade.cost) + ")", True, WHITE)
        screen.blit(upgrade_name_text, (window_x + 10, upgrades_window_y + (i * upgrade_text_offset) + 10))

    current_time = pygame.time.get_ticks()
    if current_time - cps_timer >= cps_delay:
        collect_cookies()
        cookies_per_second = cursor_auto_collect * cursor_count + grandma_count * grandma_auto_collect
        cps_timer = current_time

    cps_text = font.render("Vodkas/sec: " + str(cookies_per_second), True, WHITE)
    screen.blit(cps_text, (10, 60))

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            pygame.mixer.Sound("click.wav").play()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
