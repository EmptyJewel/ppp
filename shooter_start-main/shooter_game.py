from pygame import *
from random import randint
from time import time as timer

# фонова музика
mixer.init()
mixer.music.load('space.mp3')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
rel_sound = mixer.Sound('rel.mp3')

font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 80)
win = font2.render('Ти виграв', True, (255, 255, 255))
lose = font2.render('Ти програв', True, (0 ,0 ,0 ))

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
        bullet = Bullet("bullet.png",self.rect.centerx,self.rect.top,30,45,-15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.x -= self.speed
        global lost
        if self.rect.x < 0:
            self.rect.y = randint(0, 300)
            self.rect.x = 700
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width  - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()

# нам потрібні такі картинки:
img_back = "galaxy.jpg"  # фон гри
img_hero = "rocket.png"
img_enemy = "ufo.png"
img_asteroid = "asteroid.png"

score = 0
lost = 0
max_lost = 5
goal = 50
life = 3

# створюємо віконце
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Purple World")
background = transform.scale(image.load(img_back), (win_width, win_height))

ship = Player(img_hero,5,win_height - 100, 80, 100,10)

bullets = sprite.Group()
monsters = sprite.Group()
asteroids = sprite.Group()

for i in range(1,5):
    monster = Enemy(img_enemy, 700,randint(0, 300), 100, 100, randint(1, 6))
    monsters.add(monster)

for i in range(1,3):
    asteroid = Asteroid(img_asteroid, randint(80,win_width - 80), -40, 70, 80, randint(3, 5))
    asteroids.add(asteroid)



# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна
finish = False
rel_time = False
num_fire = 0
clock = time.Clock()
FPS = 30

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 1 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 1 and rel_time == False:
                    last_time = timer()
                    rel_time = True


    if not finish:
        window.blit(background,(0,0))

        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 1.5:
                reload = font2.render('Wait,reload...', 1, (150,0,0))
                window.blit(reload, (win_width/2-200,win_height-100))
            else:
                num_fire = 0
                rel_time = False
                rel_sound.play()

        collides = sprite.groupcollide(monsters, bullets, True,True)
        for collide in collides:
            score += 1
            monster = Enemy(img_enemy,700,randint(100, 300), 100, 100, randint(1, 6))
            monsters.add(monster)

        #if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
        #    finish = True
        #    window.blit(lose, (200,200))
        if sprite.spritecollide(ship, monsters, False):
            sprite.spritecollide(ship, monsters, True)
            monster = Enemy(img_enemy,700,randint(100, 300), 100, 100, randint(1, 6))
            monsters.add(monster)
            life -=1

        if sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, asteroids, True)
            asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 70, 80, randint(3, 5))
            asteroids.add(asteroid)
            life -=1

        if score >= goal:
            finish = True
            window.blit(win, (200,200))

        if lost >= max_lost or life == 0:
            finish = True
            window.blit(lose, (200, 200))

    text = font1.render("Рахунок:" + str(score), 1, (255, 255, 255))
    window.blit(text, (10, 20))

    text_lose = font1.render("Пропущено:" + str(lost), 1, (255, 255, 255))
    window.blit(text_lose, (10, 50))

    text_life = font1.render(str(life), 1, (0, 150, 0))
    window.blit(text_life, (650, 10))

    display.update()
    clock.tick(FPS)