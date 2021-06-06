'''
Function:
    Bunnies and Badgers
Author: 
    Charles
Test
'''
import sys
import cfg
import math
import random
import pygame
from modules import *

#Initialize global variables
# 初始化
global screen
global game_images
global game_sounds
global font
# 定义兔子
global bunny
# 跟踪玩家的精度变量, 记录了射出的箭头数和被击中的獾的数量.
global acc_record
# 生命值
global healthvalue
# 弓箭
global arrow_sprites_group
# 獾
global badguy_sprites_group
global badguy
# 定义了一个定时器, 使得游戏里经过一段时间后就新建一支獾
global badtimer
global badtimer1
global clock


'''游戏初始化'''
'''Initialize game sounds, pictures, and screen'''
def initGame():
    # 初始化pygame, 设置展示窗口
    pygame.init()
    pygame.mixer.init()
    global  screen
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Bunnies and Badgers —— Charles的皮卡丘')
    # 加载必要的游戏素材
    global  game_images
    game_images = {}
    for key, value in cfg.IMAGE_PATHS.items():
        game_images[key] = pygame.image.load(value)
    global  game_sounds
    game_sounds = {}
    for key, value in cfg.SOUNDS_PATHS.items():
        if key != 'moonlight':
            game_sounds[key] = pygame.mixer.Sound(value)

'''数据初始化'''
'''Initialize global variables'''
def initData():
    global  font
    font = pygame.font.Font(None, 24)
    # 定义兔子
    global bunny
    bunny = BunnySprite(image=game_images.get('rabbit'), position=(100, 100))
    # 跟踪玩家的精度变量, 记录了射出的箭头数和被击中的獾的数量.
    global acc_record
    acc_record = [0., 0.]
    # 生命值
    global  healthvalue
    healthvalue = 194
    #弓箭
    global  arrow_sprites_group
    arrow_sprites_group = pygame.sprite.Group()
    # 獾
    global badguy,badguy_sprites_group
    badguy_sprites_group = pygame.sprite.Group()
    badguy = BadguySprite(game_images.get('badguy'), position=(640, 100))
    badguy_sprites_group.add(badguy)
    # 定义了一个定时器, 使得游戏里经过一段时间后就新建一支獾
    global badtimer,badtimer1,clock
    badtimer = 100
    badtimer1 = 0
    # 游戏主循环, running变量会跟踪游戏是否结束, exitcode变量会跟踪玩家是否胜利.
    clock = pygame.time.Clock()

'''更新弓箭状态'''
'''Update arrow status'''
def updateArrow():
    # --更新弓箭
    for arrow in arrow_sprites_group:
        if arrow.update(cfg.SCREENSIZE):
            arrow_sprites_group.remove(arrow)

'''更新兔子'''
'''Update the status of the bunny, the bunny can move in four directions'''
def updateBunny():
    # ----移动兔子
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w]:
        bunny.move(cfg.SCREENSIZE, 'up')
    elif key_pressed[pygame.K_s]:
        bunny.move(cfg.SCREENSIZE, 'down')
    elif key_pressed[pygame.K_a]:
        bunny.move(cfg.SCREENSIZE, 'left')
    elif key_pressed[pygame.K_d]:
        bunny.move(cfg.SCREENSIZE, 'right')

'''更新坏人状态'''
'''Update bad guy status,the bad guys move from right to left'''
def updateBadguy():
    # --更新獾
    global  badtimer,badtimer1,badguy_sprites_group,healthvalue
    if badtimer == 0:
        badguy = BadguySprite(game_images.get('badguy'), position=(640, random.randint(50, 430)))
        badguy_sprites_group.add(badguy)
        badtimer = 100 - (badtimer1 * 2)
        badtimer1 = 20 if badtimer1 >= 20 else badtimer1 + 2
    badtimer -= 1
    for badguy in badguy_sprites_group:
        if badguy.update():
            game_sounds['hit'].play()
            healthvalue -= random.randint(4, 8)
            badguy_sprites_group.remove(badguy)

'''判定箭是否击中坏人 '''
'''Determine if the arrow hit the bad guy'''
def arrowHitBadguy():
    global  badguy_sprites_group,arrow_sprites_group
    for arrow in arrow_sprites_group:
        for badguy in badguy_sprites_group:
            if pygame.sprite.collide_mask(arrow, badguy):
                game_sounds['enemy'].play()
                arrow_sprites_group.remove(arrow)
                badguy_sprites_group.remove(badguy)
                acc_record[0] += 1

'''在屏幕中画出对象'''
'''Draw objects on the screen'''
def drawObjects():
    # --画出弓箭
    arrow_sprites_group.draw(screen)
    # --画出獾
    badguy_sprites_group.draw(screen)
    # --画出兔子
    bunny.draw(screen, pygame.mouse.get_pos())
    # --画出城堡健康值, 首先画了一个全红色的生命值条, 然后根据城堡的生命值往生命条里面添加绿色.
    screen.blit(game_images.get('healthbar'), (5, 5))
    for i in range(healthvalue):
        screen.blit(game_images.get('health'), (i + 8, 8))

'''在屏幕中画出背景 '''
'''Draw the background on the screen '''
def drawBackground():
    # --在给屏幕画任何东西之前用黑色进行填充
    screen.fill(0)
    # --添加的风景也需要画在屏幕上
    for x in range(cfg.SCREENSIZE[0] // game_images['grass'].get_width() + 1):
        for y in range(cfg.SCREENSIZE[1] // game_images['grass'].get_height() + 1):
            screen.blit(game_images['grass'], (x * 100, y * 100))
    for i in range(4): screen.blit(game_images['castle'], (0, 30 + 105 * i))

''' 兔子射击 '''
''' Control rabbit shooting'''
def shooting():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game_sounds['shoot'].play()
            acc_record[1] += 1
            mouse_pos = pygame.mouse.get_pos()
            angle = math.atan2(mouse_pos[1] - (bunny.rotated_position[1] + 32),
                               mouse_pos[0] - (bunny.rotated_position[0] + 26))
            arrow = ArrowSprite(game_images.get('arrow'),
                                (angle, bunny.rotated_position[0] + 32, bunny.rotated_position[1] + 26))
            arrow_sprites_group.add(arrow)

'''生成倒计时 '''
'''Generate countdown in the upper right corner '''
def countDown():
    # --倒计时信息
    countdown_text = font.render(str((90000 - pygame.time.get_ticks()) // 60000) + ":" + str(
        (90000 - pygame.time.get_ticks()) // 1000 % 60).zfill(2), True, (0, 0, 0))
    countdown_rect = countdown_text.get_rect()
    countdown_rect.topright = [635, 5]
    screen.blit(countdown_text, countdown_rect)

'''主函数'''
# 游戏主循环, running变量会跟踪游戏是否结束, exitcode变量会跟踪玩家是否胜利.
def main():
    #初始化游戏声音，游戏素材，以及全局变量
    #Initialize game sounds, game materials, and global variables
    initGame()
    initData()
    # 播放背景音乐
    #Play background music
    pygame.mixer.music.load(cfg.SOUNDS_PATHS['moonlight'])
    pygame.mixer.music.play(-1, 0.0)
    running, exitcode = True, False
    global screen,game_images,game_sounds,font,bunny,acc_record,healthvalue,arrow_sprites_group,badguy_sprites_group,badguy,badtimer,badtimer1,clock
    # 游戏主循环, running变量会跟踪游戏是否结束, exitcode变量会跟踪玩家是否胜利.
    # The main loop, which controls the running of the game
    while running:
        # --生成背景和倒计时信息
        # --Generate background and countdown information
        drawBackground()
        countDown()
        # --退出与射击
        # --Control quit and shooting
        shooting()
        # --更新对象状态
        # --update objects
        updateBunny()
        updateArrow()
        updateBadguy()
        arrowHitBadguy()
        drawObjects()

        # --判断游戏是否结束
        # - Determine whether the game is over
        if pygame.time.get_ticks() >= 90000:
            running, exitcode = False, True
        if healthvalue <= 0:
            running, exitcode = False, False


        # --更新屏幕
        # --Refresh the screen
        pygame.display.flip()
        clock.tick(cfg.FPS)

    # 计算准确率
    # Calculate accuracy
    accuracy = acc_record[0] / acc_record[1] * 100 if acc_record[1] > 0 else 0
    accuracy = '%.2f' % accuracy

    #显示游戏结束页面
    # Display endgame interface
    showEndGameInterface(screen, exitcode, accuracy, game_images)

'''运行游戏'''
'''run'''
if __name__ == '__main__':
    main()