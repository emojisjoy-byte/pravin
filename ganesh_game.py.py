import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ganpati Bappa Laddu Collector")

clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (255,140,0)
YELLOW = (255,215,0)
GRAY = (130,130,130)
RED = (220,50,50)
GREEN = (0,180,0)
BLUE = (50,120,255)

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

class Player:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT-120
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_s]:
            self.y += self.speed
        if keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_d]:
            self.x += self.speed

        self.x = max(50, min(WIDTH-50, self.x))
        self.y = max(50, min(HEIGHT-50, self.y))

    def draw(self):
        # Mouse
        pygame.draw.ellipse(screen, GRAY,
                            (self.x-35, self.y+15, 70, 30))

        # Ganesh head
        pygame.draw.circle(screen, ORANGE,
                           (self.x, self.y), 25)

        # Bowl
        pygame.draw.arc(screen,
                        (120,70,20),
                        (self.x-22, self.y-10, 44, 22),
                        0, 3.14, 4)

    def rect(self):
        return pygame.Rect(self.x-30,
                           self.y-30,
                           60,
                           60)

class FallingObject:
    def __init__(self, kind):
        self.kind = kind
        self.reset()

    def reset(self):
        self.x = random.randint(30, WIDTH-30)
        self.y = random.randint(-600, -50)

        if self.kind == "laddu":
            self.speed = random.randint(4,7)

        elif self.kind == "gold":
            self.speed = random.randint(5,8)

        else:
            self.speed = random.randint(6,9)

    def update(self):
        self.y += self.speed

        if self.y > HEIGHT+40:
            self.reset()

    def draw(self):
        if self.kind == "laddu":
            pygame.draw.circle(
                screen,
                YELLOW,
                (int(self.x), int(self.y)),
                15
            )

        elif self.kind == "gold":
            pygame.draw.circle(
                screen,
                (255,240,0),
                (int(self.x), int(self.y)),
                18
            )

        elif self.kind == "stone":
            pygame.draw.rect(
                screen,
                GRAY,
                (self.x-12, self.y-12, 24, 24)
            )

    def rect(self):
        return pygame.Rect(
            self.x-20,
            self.y-20,
            40,
            40
        )

def draw_text(text, font_obj, color, x, y):
    img = font_obj.render(text, True, color)
    screen.blit(img, (x, y))

player = Player()

laddus = [FallingObject("laddu") for _ in range(5)]
golds = [FallingObject("gold") for _ in range(2)]
stones = [FallingObject("stone") for _ in range(3)]

score = 0
lives = 3
level = 1

start_time = pygame.time.get_ticks()
game_duration = 60

running = True

while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed = (pygame.time.get_ticks()
               - start_time) // 1000

    remaining = max(0, game_duration - elapsed)

    if remaining <= 0 or lives <= 0:
        break

    player.move()

    level = score // 100 + 1

    for obj in laddus:
        obj.speed = 4 + level
        obj.update()

        if player.rect().colliderect(obj.rect()):
            score += 10
            obj.reset()

    for obj in golds:
        obj.speed = 5 + level
        obj.update()

        if player.rect().colliderect(obj.rect()):
            score += 50
            obj.reset()

    for obj in stones:
        obj.speed = 6 + level
        obj.update()

        if player.rect().colliderect(obj.rect()):
            lives -= 1
            obj.reset()

    screen.fill((255,245,220))

    pygame.draw.rect(
        screen,
        (230,220,180),
        (0,0,WIDTH,70)
    )

    player.draw()

    for obj in laddus:
        obj.draw()

    for obj in golds:
        obj.draw()

    for obj in stones:
        obj.draw()

    draw_text(
        f"Score: {score}",
        font,
        BLACK,
        20,
        20
    )

    draw_text(
        f"Lives: {lives}",
        font,
        RED,
        220,
        20
    )

    draw_text(
        f"Level: {level}",
        font,
        BLUE,
        400,
        20
    )

    draw_text(
        f"Time: {remaining}",
        font,
        GREEN,
        600,
        20
    )

    pygame.display.flip()

# GAME OVER SCREEN
while True:

    screen.fill(WHITE)

    draw_text(
        "GANPATI BAPPA MORIYA!",
        big_font,
        ORANGE,
        90,
        150
    )

    draw_text(
        f"Final Score: {score}",
        font,
        BLACK,
        340,
        300
    )

    draw_text(
        "Press ESC to Exit",
        font,
        BLUE,
        320,
        380
    )

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit