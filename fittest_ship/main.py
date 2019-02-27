import pygame
from random import choice

WIN_WIDTH = 800
WIN_HEIGHT = 800
BG_COLOR = (25, 25, 25)
ACCELERATION = 0.5
MAX_SPEED = 10
SHIP_WIDTH = 44
SHIP_HEIGHT = 30

pygame.init()
gameDisplay = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

shipImgs = (pygame.image.load('ship_low.png'), pygame.image.load('ship.png'),
            pygame.image.load('ship_med.png'), pygame.image.load('ship_full.png'))

def ship(x, y):
    img = choice(shipImgs)
    gameDisplay.blit(img, (x, y))


def run():
    x = (WIN_WIDTH * 0.45)
    y = (WIN_HEIGHT * 0.55)

    x_change = 0
    y_change = 0

    crashed = False
    while not crashed:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                x_change -= ACCELERATION
            elif event.key == pygame.K_RIGHT:
                x_change += ACCELERATION
            if event.key == pygame.K_UP:
                y_change -= ACCELERATION
            elif event.key == pygame.K_DOWN:
                y_change += ACCELERATION
        else:
            x_change = x_change * 0.98
            y_change = y_change * 0.98

        x_repel = abs(x_change * 0.9) + 0.1
        y_repel = abs(y_change * 0.9) + 0.1

        if x > WIN_WIDTH - SHIP_WIDTH:
            x_change -= x_repel
        elif x < 0:
            x_change += x_repel

        if y > WIN_HEIGHT - SHIP_HEIGHT:
            y_change -= y_repel
        elif y < 0:
            y_change += y_repel

        x += x_change
        y += y_change

        if x_change > MAX_SPEED:
            x_change = 5
        elif x_change < -MAX_SPEED:
            x_change = -5
        if y_change > MAX_SPEED:
            y_change = 5
        elif y_change < -MAX_SPEED:
            y_change = -5

        gameDisplay.fill(BG_COLOR)

        ship(x, y)

        pygame.display.update()
        clock.tick(60)


run()
pygame.quit()
quit()
