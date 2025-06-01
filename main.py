import pygame

pygame.init()

win_width = 700
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Лабіринт")
clock = pygame.time.Clock()

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    win.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()


