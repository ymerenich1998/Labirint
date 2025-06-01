import pygame

pygame.init()

class GameSprite(pygame.sprite.Sprite):
  def __init__(self, sprite_image, speed, x, y):
    super().__init__()
    self.image = pygame.transform.scale(pygame.image.load(sprite_image), (65, 65))
    self.speed = speed
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
  
  def reset(self):
    win.blit(self.image, (self.rect.x, self.rect.y))

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

player = GameSprite("hero.png", 5, 5, 5)
enemy = GameSprite("cyborg.png", 2, win_width-100, win_height - 300)
treasure = GameSprite("treasure.png", 0, win_width-100, win_height - 100)

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.reset()
    enemy.reset()
    treasure.reset()
    pygame.display.flip()

pygame.quit()


