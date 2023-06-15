import pygame
import random
import os
from pygame.sprite import Group, spritecollide

FPS = 60
WIDTH = 800
HEIGHT = 570

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init()
screen_width, screen_height = 800, 570
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GAME")
clock = pygame.time.Clock()

eat_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
hit_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))

# 設定遊戲時間限制（以秒為單位）
TIME_LIMIT = 15  # 60秒

# 創建計時器
start_time = pygame.time.get_ticks()

# 設定計時器字體
font = pygame.font.Font(None, 36)

# 載入圖片
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()
player_imgs = []
for i in range(4):
    img = pygame.image.load(os.path.join("img", f"w{i}.png")).convert()
    img = pygame.transform.scale(img, (42, 74))
    player_imgs.append(img)
for i in range(4):
    img = pygame.transform.flip(player_imgs[i], True, False)
    player_imgs.append(img)

mushroom_img = pygame.image.load(os.path.join("img", "mushroom.png")).convert()
mushroom_img.set_colorkey(WHITE)
mushroom2_img = pygame.image.load(os.path.join("img", "mushroom2.png")).convert()
mushroom2_img.set_colorkey(WHITE)
font_name = os.path.join("font.ttf")


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x  # 將此行改為 x
    text_rect.top = y
    surf.blit(text_surface, text_rect)
# 遊戲開始畫面
def show_start_screen():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "遊戲標題", 60, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "按下任意按鍵開始遊戲", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "紅蘑菇加分;綠蘑菇減分", 22, WIDTH / 2, HEIGHT * 3 / 5)
    draw_text(screen, "目標:得到8分", 22, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False

    # 開始計時
    #start_time = pygame.time.get_ticks()




def show_game_over_screen():
    screen.blit(background_img, (0, 0))
    draw_text(screen, "遊戲結束", 48, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "得分: " + str(score), 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "ByeBye", 22, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()

    # 延遲 3 秒後結束遊戲
    pygame.time.delay(1000)

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYUP:
                waiting = False
    # 停止背景音樂
    pygame.mixer.music.stop()




class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_imgs[0]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.frame = pygame.time.get_ticks()
        self.i = 0
        self.i_offset = 0
        self.is_growing = False

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.frame > 100:
            self.frame = now
            self.image = player_imgs[self.i_offset + self.i % 4]
            self.image.set_colorkey(WHITE)
            self.i += 1
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.top < 0:
            self.rect.top = 0

        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.is_growing:
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def reset_size(self):
        self.image = pygame.transform.scale(self.image, (42, 74))


class Mushroom(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mushroom_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speedy = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speedy = random.randint(1, 5)


class Mushroom2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mushroom2_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -50)
        self.speedy = random.randint(1, 5)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -50)
            self.speedy = random.randint(1, 5)

# 遊戲開始畫面
show_start_screen()

# 載入背景音樂
pygame.mixer.music.load(os.path.join("sound", "background.mp3"))
# 設定音量（0.0到1.0之間）
pygame.mixer.music.set_volume(0.5)
# 播放背景音樂（-1表示無限循環播放）
pygame.mixer.music.play(-1)

# 遊戲迴圈
show_init = True
running = True
start_time = pygame.time.get_ticks()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

mushrooms = Group()
mushrooms2 = Group()  # 新增一個 Group 來管理 Mushroom2

score = 0

mushroom_spawn_time = 1000  # 每隔1秒產生一個蘑菇
mushroom2_spawn_time = 1500  # 每隔1.5秒產生一個 Mushroom2

last_mushroom_spawn = pygame.time.get_ticks()
last_mushroom2_spawn = pygame.time.get_ticks()

is_player_growing = False  # 玩家是否正在放大
player_scale_factor = 1 #玩家的放大比例

while running:
    clock.tick(FPS)
    
    # 檢查遊戲時間是否超過限制
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000  # 計算已經過去的秒數
    if elapsed_time >= TIME_LIMIT:
        running = False
        show_game_over_screen()
        # 停止背景音樂
        pygame.mixer.music.stop()

        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.speedy = -5
            elif event.key == pygame.K_DOWN:
                player.speedy = 5
            elif event.key == pygame.K_LEFT:
                player.speedx = -5
                player.i_offset = 4
            elif event.key == pygame.K_RIGHT:
                player.speedx = 5
                player.i_offset = 0
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.speedy = 0
            elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.speedx = 0

    all_sprites.update()

    now = pygame.time.get_ticks()

    # 產生蘑菇
    if now - last_mushroom_spawn > mushroom_spawn_time:
        mushroom = Mushroom()
        mushrooms.add(mushroom)
        all_sprites.add(mushroom)
        last_mushroom_spawn = now

    # 產生 Mushroom2
    if now - last_mushroom2_spawn > mushroom2_spawn_time:
        mushroom2 = Mushroom2()
        mushrooms2.add(mushroom2)
        all_sprites.add(mushroom2)
        last_mushroom2_spawn = now

    # 檢查玩家是否與蘑菇碰撞
    collided_mushrooms = spritecollide(player, mushrooms, True)
    collided_mushrooms2 = spritecollide(player, mushrooms2, True)

    # 碰撞到蘑菇
    if collided_mushrooms:
        score += 1
        eat_sound.play()
        player_scale_factor = player_scale_factor*1.05  # 每次吃到蘑菇，放大比例增加
        player.rect.width = int(player.rect.width * player_scale_factor)  # 調整玩家寬度
        player.rect.height = int(player.rect.height * player_scale_factor)  # 調整玩家高度

        # 縮放玩家圖像
        player.image = pygame.transform.scale(player.image, (player.rect.width, player.rect.height))

        # 縮放玩家所有圖案
        player_imgs_scaled = []
        for img in player_imgs:
            img_scaled = pygame.transform.scale(img, (player.rect.width, player.rect.height))
            player_imgs_scaled.append(img_scaled)
        player_imgs = player_imgs_scaled

    # 碰撞到 Mushroom2
    if collided_mushrooms2:
        score -= 1
        if score<0:
            score=0
        hit_sound.play()
        player_scale_factor = player_scale_factor*0.95  # 每次碰到 Mushroom2，放大比例減少
        if player_scale_factor < 0.1:
            player_scale_factor = 0.1
        player.rect.width = int(player.rect.width * player_scale_factor)  # 調整玩家寬度
        player.rect.height = int(player.rect.height * player_scale_factor)  # 調整玩家高度

        # 縮放玩家圖像
        player.image = pygame.transform.scale(player.image, (player.rect.width, player.rect.height))

        # 縮放玩家所有圖案
        player_imgs_scaled = []
        for img in player_imgs:
            img_scaled = pygame.transform.scale(img, (player.rect.width, player.rect.height))
            player_imgs_scaled.append(img_scaled)
        player_imgs = player_imgs_scaled

    screen.fill(BLACK)
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, "Score: " + str(score), 18, WIDTH / 2, 10)

    if score >= 8:
        running = False
        show_game_over_screen()
        # 停止背景音樂
        pygame.mixer.music.stop()

    # 繪製計時器
    timer_text = font.render("Time: " + str(TIME_LIMIT - elapsed_time), True, WHITE)
    screen.blit(timer_text, (10, 10))

    pygame.display.update()
pygame.mixer.stop()
pygame.mixer.music.stop()
pygame.quit()
