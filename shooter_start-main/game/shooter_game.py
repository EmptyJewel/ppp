from pygame import *
from random import randint

# фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('YOU NATO!', True, (0, 0, 0))
lose = font2.render('YOU GAY!', True, (0 ,0 ,0 ))

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,50,75,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width  - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

# нам потрібні такі картинки:
img_back = "galaxy.jpg"  # фон гри
img_hero = "rocket.png"
img_enemy = "ufo.png"

score = 0
lost = 0
max_lost = 10
goal = 100

# створюємо віконце
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero,5,win_height - 100, 80, 100,10)

bullets = sprite.Group()
monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80,win_width - 80), -40, 80, 50, randint(1, 3))
    monsters.add(monster)

# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна
finish = False
clock = time.Clock()
FPS = 60

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background,(0,0))

        text = font1.render("Рахунок:" + str(score),1, (255,255,255))
        window.blit(text, (10,20))

        text_lose = font1.render("Пропущено:" + str(lost),1, (255,255,255))
        window.blit(text_lose, (10,50))

        ship.update()
        monsters.update()
        bullets.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        collides = sprite.groupcollide(monsters, bullets, True,True)
        for collide in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
            monsters.add(monster)

        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            finish = True
            window.blit(lose, (200,200))

        if score >= goal:
            finish = True
            window.blit(win, (200,200))

    display.update()
    clock.tick(FPS)