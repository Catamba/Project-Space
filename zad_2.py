import os
import sys
import random

import pygame


clock = pygame.time.Clock()


def end():
    pygame.mixer.music.set_volume(0)
    pygame.mixer.pause()
    all_sprites = pygame.sprite.Group()
    sprite = pygame.sprite.Sprite()
    sprite.image = pygame.image.load(os.path.join("data", 'End.png'))
    sprite.image = pygame.transform.scale(sprite.image, (900, 400))
    sprite.rect = sprite.image.get_rect()
    all_sprites.add(sprite)
    sprite.rect.x = -900
    sprite.rect.y = 0
    end_music.play()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        screen.fill("black")
        all_sprites.draw(screen)
        if sprite.rect.x < 0:
            sprite.rect.x = sprite.rect.x + 4
        pygame.display.update()
        clock.tick(30)



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    global event, rejim_game
    intro_text = ["- Скрол-Шутинг -", "", '',
                  "- Начать", '',
                  '- Выход']
    main_fon = pygame.transform.scale(load_image('Fon.jpg'), (width, height))
    screen.blit(main_fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 50
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if 50 < pygame.mouse.get_pos()[0] < 140 and 140 < pygame.mouse.get_pos()[1] < 170:
                    rejim_game = 1
                    return
                elif 50 < pygame.mouse.get_pos()[0] < 140 and 205 < pygame.mouse.get_pos()[1] < 235:
                    terminate()
        pygame.display.flip()
        clock.tick(50)


if __name__ == '__main__':
    pygame.init()
    stop_game = False
    size = width, height = 900, 400
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Скролл-шутер')
    inviseble = 0
    pygame.mixer.music.load('data\Fon_music.mp3')
    pygame.mixer.music.play(-1, 0.0)
    lazer = pygame.mixer.Sound('data\lazer.mp3')
    warning = pygame.mixer.Sound('data\warning.mp3')
    boom = pygame.mixer.Sound('data\_BOOM.mp3')
    end_music = pygame.mixer.Sound('data\End_music.mp3')
    start_screen()
    f = open("data\save.txt")
    record_score = f.readline()

    class Bullet(pygame.sprite.Sprite):
        image = load_image('bul.png')
        image = pygame.transform.scale(image, (40, 40))

        def __init__(self, x, y):
            super().__init__(all_sprites)
            self.image = pygame.Surface((10, 20))
            self.image = Bullet.image
            self.rect = self.image.get_rect()
            self.rect.bottom = y
            self.rect.centerx = x
            self.speedy = 10
            self.mask = pygame.mask.from_surface(self.image)


        def update(self):
            self.rect.x += self.speedy
            if self.rect.bottom < 0:
                self.kill()
            self.mask = pygame.mask.from_surface(self.image)

    class Player(pygame.sprite.Sprite):
        image = pygame.transform.flip(load_image('korab.png', -1), True, False)
        image = pygame.transform.scale(image, (90, 40))

        def __init__(self, *group):
            # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
            # Это очень важно!!!
            super().__init__(all_sprites)
            self.image = Player.image
            self.rect = self.image.get_rect()
            self.healts = 4
            self.rect.x = 50
            self.rect.y = 150
            self.iteration = 1
            self.iteration2 = 20
            self.mask = pygame.mask.from_surface(self.image)
            self.score = 0

        def update(self):
            self.iteration += 1
            if self.iteration % 5 == 0:
                self.rect = self.rect.move(0, (random.randrange(-1, 2)))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.rect.y > -2:
                    self.rect = self.rect.move(0, -5)

                if event.key == pygame.K_DOWN and self.rect.y < 340:
                    self.rect = self.rect.move(0, 5)

                if event.key == pygame.K_KP1:
                    self.shoot()
            if self.iteration2:
                self.iteration2 -= 1
            self.mask = pygame.mask.from_surface(self.image)


        def shoot(self):
            if self.iteration2 == 0:
                lazer.play()
                bullet = Bullet(self.rect.centerx + 50, self.rect.centery + 30)
                all_sprites.add(bullet)
                bullets.add(bullet)
                self.iteration2 = 20


    class Mob(pygame.sprite.Sprite):
        image = pygame.transform.flip(load_image('mete.png', -1), False, False)
        image = pygame.transform.scale(image, (30, 30))
        def __init__(self):
            super().__init__(all_sprites)
            self.image = pygame.Surface((50, 50))
            self.image = Mob.image
            self.rect = self.image.get_rect()
            self.rect.x = 910
            self.rect.y = random.randrange(50, 360)
            # self.speedy = random.randrange(-8, -1)
            self.speedx = random.randrange(-5, -1)
            self.mask = pygame.mask.from_surface(self.image)


        def update(self):
            self.rect.x += self.speedx
            # self.rect.y += self.speedy
            if self.rect.x + 100 < 0:
                self.rect.x = 910
                self.rect.y = random.randrange(50, 360)
                # self.speedy = random.randrange(1, 8)
            self.mask = pygame.mask.from_surface(self.image)



    all_sprites = pygame.sprite.Group()
    hero = Player(all_sprites)
    mobs = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    fon = pygame.transform.scale(load_image('fon_ss.jpg'), (width, height))
    for i in range(8):
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
    running = True
    fps = 60
    while running:
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    stop_game = not(stop_game)


        pygame.draw.rect(screen, 'green', (hero.rect.x, hero.rect.y, 50, 50))
        if stop_game:
            continue
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            boom.play()
            hero.score += 100
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        # hits = pygame.sprite.spritecollide(hero, mobs, False)
        # if hits:
        #     running = False
        hits = pygame.sprite.spritecollide(hero, mobs, False, pygame.sprite.collide_circle)
        if hits and not inviseble:
            hero.healts -= 1
            warning.play()
            inviseble = 300
            if hero.healts == 0:
                if int(hero.score) > int(record_score):
                    f2 = open("data\save.txt", 'w')
                    f2.write(str(hero.score))
                end()
                terminate()
        if inviseble > 0:
            inviseble -= 1


        all_sprites.update()
        screen.blit(fon, (0, 0))
        all_sprites.draw(screen)

        for i in range(hero.healts - 1):
            pygame.draw.rect(screen, 'yellow', (hero.rect.x, hero.rect.y - 2, 30 * i + 1, 4))

        font = pygame.font.Font(None, 50)
        text_coord = 10
        string_rendered = font.render(str(hero.score), 1, pygame.Color('WHITE'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 400
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 50)
        text_coord = 10
        string_rendered = font.render(str(record_score), 1, pygame.Color('WHITE'))
        intro_rect = string_rendered.get_rect()
        intro_rect.top = text_coord
        intro_rect.x = 20
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


        clock.tick(fps)
        pygame.display.flip()
    pygame.exit()
