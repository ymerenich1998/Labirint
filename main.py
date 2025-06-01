import pygame

pygame.init()

win_width = 700
win_height = 500
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Лабіринт")
bg = pygame.transform.scale(pygame.image.load("background.jpg"), (win_width, win_height))
win.blit(bg, (0, 0))
clock = pygame.time.Clock()

pygame.mixer.init()

pygame.mixer.music.load("jungles.ogg")
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play()

kick = pygame.mixer.Sound("kick.ogg")
money = pygame.mixer.Sound("money.ogg")

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()


