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
    self.start_x = x
    self.start_y = y

  def reset(self):
    win.blit(self.image, (self.rect.x, self.rect.y))

  def reset_position(self):
    self.rect.x = self.start_x
    self.rect.y = self.start_y

class Player(GameSprite):
  def update(self):
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x > 0:
      self.rect.x -= self.speed
    if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x < win_width - 65:
      self.rect.x += self.speed
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y > 0:
      self.rect.y -= self.speed
    if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y < win_height - 65:
      self.rect.y += self.speed

class Enemy(GameSprite):
  def __init__(self, sprite_image, speed, x, y, start=0, end=700-65, plane="left_right"):
    'plane = "left_right" or "up_down"'
    super().__init__(sprite_image, speed, x, y)
    self.start = start
    self.end = end
    self.plane = plane
    if plane=="left_right":self.direction = "left"
    elif plane=="up_down":self.direction = "up"
    else:print('''ERORR 'plane = "left_right" or "up_down"''');0/0

  def update(self):
    if self.plane=="left_right":
      if self.rect.x <= self.start:
        self.direction = "right"
      if self.rect.x >= self.end:
        self.direction = "left"

      if self.direction == "left":
        self.rect.x -= self.speed
      else:
        self.rect.x += self.speed
    else:
      if self.rect.y <= self.start:
        self.direction = "down"
      if self.rect.y >= self.end:
        self.direction = "up"

      if self.direction == "up":
        self.rect.y -= self.speed
      else:
        self.rect.y += self.speed

  def reset_position(self):
    self.rect.x = self.start_x
    self.rect.y = self.start_y
    self.direction = "left"
    
class Wall(pygame.sprite.Sprite):
  def __init__(self, x, y, width, height, color = (0, 0, 0)):
    super().__init__()
    self.image = pygame.Surface((width, height))
    self.image.fill(color) 
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
  
  def draw(self):
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

def create_objects():
  player = Player("hero.png", 5, 5, 5)
  enemies = pygame.sprite.Group()
  enemies.add(
    Enemy("cyborg.png", 2, win_width-100, win_height - 300, win_width-250, win_width-65, "left_right"),
    Enemy("cyborg.png", 3, 200, 200, 100, 400),
    Enemy("cyborg.png", 1, 400, 100, 300, 600),
    Enemy("cyborg.png", 1, 400, 100, 42, 300, "up_down")
  )
  walls = pygame.sprite.Group()
  walls.add(
    Wall(100, 100, 200, 10),  # Horizontal wall
    Wall(100, 200, 10, 100),  # Vertical wall
    Wall(300, 100, 10, 200),  # Vertical wall
    Wall(400, 300, 200, 10),  # Horizontal wall
  )
  treasure = GameSprite("treasure.png", 0, win_width-100, win_height - 100)
  return player, enemies, treasure, walls

player, enemies, treasure, walls = create_objects()

running = True
finish = False
while running:
  clock.tick(60)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN:
      if finish and event.key == pygame.K_r:
        player, enemies, treasure, walls = create_objects()
        finish = False

  if not finish:
    win.blit(bg, (0, 0))
    walls.draw(win)
    player.update()
    enemies.update()
    player.reset()
    enemies.draw(win)
    treasure.reset()
    if pygame.sprite.spritecollideany(player, enemies):
      finish = True
      kick.play()
      win.blit(bg, (0, 0))
      font = pygame.font.SysFont("Arial", 48)
      text = font.render("Ви програли!", True, (255, 0, 0))
      win.blit(text, (win_width // 2 - 125, win_height // 2 - 50))
    if pygame.sprite.spritecollideany(player, walls):
      player.reset_position()
    if pygame.sprite.collide_rect(player, treasure):
      finish = True
      money.play()
      win.blit(bg, (0, 0))
      font = pygame.font.SysFont("Arial", 48)
      text = font.render("Ви виграли!", True, (0, 255, 0))
      win.blit(text, (win_width // 2 - 100, win_height // 2 - 50))
  else:
    font = pygame.font.SysFont("Arial", 32)
    text = font.render("Натисніть R для рестарту", True, (255, 0, 0))
    win.blit(text, (200, win_height // 2 + 50))

  pygame.display.flip()

pygame.quit()
