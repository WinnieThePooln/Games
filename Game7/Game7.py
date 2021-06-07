'''
Function:
    仿谷歌浏览器小恐龙游戏
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import cfg
import sys
import random
import pygame
from modules import *

'''global varies'''
global screen,sounds,score,score_board,highest_score,highest_score_board,flag,dino,ground,cloud_sprites_group,cactus_sprites_group,ptera_sprites_group,add_obstacle_timer,score_timer,clock
'''Initialize the game'''
def initGame():
    global screen,sounds
    # 初始化游戏数据
    # Initialize the game
    pygame.init()
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('T-Rex Rush —— Charles的皮卡丘')
    # Import sound file
    # 导入所有声音文件
    sounds = {}
    for key, value in cfg.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)
    # Game start interface
    # 游戏开始界面
    GameStartInterface(screen, sounds, cfg)

'''Initialize the data'''
def initData():
    global screen, sounds, score, score_board, highest_score, highest_score_board, flag, dino, ground, cloud_sprites_group, cactus_sprites_group, ptera_sprites_group, add_obstacle_timer, score_timer, clock
    # 初始化全局变量，以及对象
    # Initialize the global varies and sprites objects
    score = 0
    score_board = Scoreboard(cfg.IMAGE_PATHS['numbers'], position=(534, 15), bg_color=cfg.BACKGROUND_COLOR)
    highest_score = highest_score
    highest_score_board = Scoreboard(cfg.IMAGE_PATHS['numbers'], position=(435, 15), bg_color=cfg.BACKGROUND_COLOR,
                                     is_highest=True)
    dino = Dinosaur(cfg.IMAGE_PATHS['dino'])
    ground = Ground(cfg.IMAGE_PATHS['ground'], position=(0, cfg.SCREENSIZE[1]))
    cloud_sprites_group = pygame.sprite.Group()
    cactus_sprites_group = pygame.sprite.Group()
    ptera_sprites_group = pygame.sprite.Group()
    add_obstacle_timer = 0
    score_timer = 0
    clock = pygame.time.Clock()

'''控制恐龙'''
'''Control the dinosaur'''
def controDinosaur():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                dino.jump(sounds)
            elif event.key == pygame.K_DOWN:
                dino.duck()
        elif event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
            dino.unduck()

'''初始化障碍物和背景'''
'''Initialize obstacles and background'''
def initObstacles():
    global screen, sounds, score, score_board, highest_score, highest_score_board, flag, dino, ground, cloud_sprites_group, cactus_sprites_group, ptera_sprites_group, add_obstacle_timer, score_timer, clock
    screen.fill(cfg.BACKGROUND_COLOR)
    # -- Add random cloud
    # --随机添加云
    if len(cloud_sprites_group) < 5 and random.randrange(0, 300) == 10:
        cloud_sprites_group.add(Cloud(cfg.IMAGE_PATHS['cloud'], position=(cfg.SCREENSIZE[0], random.randrange(30, 75))))
    # -- Add random obstacle:Cactus and Ptera
    # --随机添加仙人掌/飞龙
    add_obstacle_timer += 1
    if add_obstacle_timer > random.randrange(50, 150):
        add_obstacle_timer = 0
        random_value = random.randrange(0, 10)
        if random_value >= 5 and random_value <= 7:
            cactus_sprites_group.add(Cactus(cfg.IMAGE_PATHS['cacti']))
        else:
            position_ys = [cfg.SCREENSIZE[1] * 0.82, cfg.SCREENSIZE[1] * 0.75, cfg.SCREENSIZE[1] * 0.60,
                           cfg.SCREENSIZE[1] * 0.20]
            ptera_sprites_group.add(Ptera(cfg.IMAGE_PATHS['ptera'], position=(600, random.choice(position_ys))))

'''Update objects:dino, ground,cloud,cacuts and ptera'''
'''更新对象，恐龙，地面，仙人掌，云和飞龙'''
def updateObjects():
    global screen, sounds, score, score_board, highest_score, highest_score_board, flag, dino, ground, cloud_sprites_group, cactus_sprites_group, ptera_sprites_group, add_obstacle_timer, score_timer, clock
    # --Update objects
    # --更新游戏元素
    dino.update()
    ground.update()
    cloud_sprites_group.update()
    cactus_sprites_group.update()
    ptera_sprites_group.update()

'''Update timer, use time as score'''
'''更新计时器，使用时间作为分数'''
def updateTimer():
    global screen, sounds, score, score_board, highest_score, highest_score_board, flag, dino, ground, cloud_sprites_group, cactus_sprites_group, ptera_sprites_group, add_obstacle_timer, score_timer, clock
    score_timer += 1
    if score_timer > (cfg.FPS // 12):
        score_timer = 0
        score += 1
        score = min(score, 99999)
        if score > highest_score:
            highest_score = score
        if score % 100 == 0:
            sounds['point'].play()
        if score % 1000 == 0:
            ground.speed -= 1
            for item in cloud_sprites_group:
                item.speed -= 1
            for item in cactus_sprites_group:
                item.speed -= 1
            for item in ptera_sprites_group:
                item.speed -= 1

'''Whether the dino hit the obtacles'''
'''碰撞检测'''
def dinoHitObtacle():
    # --If the dino hit the obtacle, game over
    # --恐龙碰到障碍物 则游戏结束
    for item in cactus_sprites_group:
        if pygame.sprite.collide_mask(dino, item):
            dino.die(sounds)
    for item in ptera_sprites_group:
        if pygame.sprite.collide_mask(dino, item):
            dino.die(sounds)

'''Draw the updated object on the screen'''
'''把更新后的对象画到屏幕上'''
def drawObjects():
    global screen, sounds, score, score_board, highest_score, highest_score_board, flag, dino, ground, cloud_sprites_group, cactus_sprites_group, ptera_sprites_group, add_obstacle_timer, score_timer, clock
    # --Draw game objects on the screen
    # --将游戏元素画到屏幕上
    dino.draw(screen)
    ground.draw(screen)
    cloud_sprites_group.draw(screen)
    cactus_sprites_group.draw(screen)
    ptera_sprites_group.draw(screen)
    score_board.set(score)
    highest_score_board.set(highest_score)
    score_board.draw(screen)
    highest_score_board.draw(screen)

'''main'''
def main():
    global screen, sounds, score, score_board, highest_score, highest_score_board, flag, dino, ground, cloud_sprites_group, cactus_sprites_group, ptera_sprites_group, add_obstacle_timer, score_timer, clock
    # --Initialize the game’s screen, background music
    # --初始化游戏的屏幕 背景音乐
    initGame()
    # --Initialize global variables, as well as dinor and obstacle objects
    # --初始化全局变量 以及恐龙 障碍物对象
    initData()
    # Main loop
    # 游戏主循环
    while True:
        #Player controls the dinosaur
        #玩家控制恐龙
        controDinosaur()
        # Initialize obstacles and clouds, background color
        # 初始化障碍物，云，背景颜色
        initObstacles()
        # Update objects and timers
        # 更新对象和计时器
        updateObjects()
        updateTimer()
        # Determine whether dino hit an obstacle
        # 判断恐龙是否装上了障碍物
        dinoHitObtacle()
        # The object is changed due to player operation, and the changed object is drawn on the screen
        # 把被改变之后的对象画到屏幕上
        drawObjects()
        # --Update screen
        # --更新屏幕
        pygame.display.update()
        clock.tick(cfg.FPS)
        # --Game over
        # --游戏是否结束
        if dino.is_dead:
            break
    # Game end interface
    # 游戏结束界面
    return GameEndInterface(screen, cfg), highest_score


'''run'''
'''运行游戏'''
if __name__ == '__main__':
    highest_score = 0
    while True:
        flag, highest_score = main()
        if not flag: break