import pygame
from time import sleep

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

class Player(GameSprite):
  def update(self):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and self.rect.x > 0:
      self.rect.x -= self.speed
    if keys[pygame.K_RIGHT] and self.rect.x < win_width - 65:
      self.rect.x += self.speed
    if keys[pygame.K_UP] and self.rect.y > 0:
      self.rect.y -= self.speed
    if keys[pygame.K_DOWN] and self.rect.y < win_height - 65:
      self.rect.y += self.speed

class Enemy(GameSprite):
  def __init__(self, sprite_image, speed, x, y, start=0, end=700-65):
    super().__init__(sprite_image, speed, x, y)
    self.start = start
    self.end = end
    self.direction = "left"

  def update(self):
    if self.rect.x <= self.start:
      self.direction = "right"
    if self.rect.x >= self.end:
      self.direction = "left"

    if self.direction == "left":
      self.rect.x -= self.speed
    else:
      self.rect.x += self.speed

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

player = Player("hero.png", 5, 5, 5)

# Создаём группу врагов
enemies = pygame.sprite.Group()
enemies.add(
  Enemy("cyborg.png", 2, win_width-100, win_height - 300, win_width-250, win_width-65),
  Enemy("cyborg.png", 3, 200, 200, 100, 400),
  Enemy("cyborg.png", 1, 400, 100, 300, 600)
)

treasure = GameSprite("treasure.png", 0, win_width-100, win_height - 100)

running = True
finish = False
while running:
  clock.tick(60)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  if not finish:
    win.blit(bg, (0, 0))
    player.update()
    enemies.update()
    player.reset()
    enemies.draw(win)
    treasure.reset()
    if pygame.sprite.spritecollideany(player, enemies):
      finish = True
      kick.play()
      sleep(1)

  pygame.display.flip()

pygame.quit()
