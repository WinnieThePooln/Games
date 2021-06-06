'''
Function:
    滑雪小游戏
作者:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import cfg
import pygame
import random


'''滑雪者类'''
'''Skier object  '''
class SkierClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #The direction of the skier:
        ''' -2 far left
            -1 left
            0 forward
            1 to the right
            2 far right '''
        # 滑雪者的朝向(-2到2)
        self.direction = 0
        self.imagepaths = cfg.SKIER_IMAGE_PATHS[:-1]
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = [320, 100]
        self.speed = [self.direction, 6-abs(self.direction)*2]

    '''Change the directions of the skier'''
    '''改变滑雪者的朝向. 负数为向左，正数为向右，0为向前'''
    def turn(self, num):
        self.direction += num
        self.direction = max(-2, self.direction)
        self.direction = min(2, self.direction)
        center = self.rect.center
        self.image = pygame.image.load(self.imagepaths[self.direction])
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speed = [self.direction, 6-abs(self.direction)*2]
        return self.speed

    '''The movement of skiers'''
    '''移动滑雪者'''
    def move(self):
        self.rect.centerx += self.speed[0]
        self.rect.centerx = max(20, self.rect.centerx)
        self.rect.centerx = min(620, self.rect.centerx)
    ''' If a skier hits a tree, set the skier to fall'''
    '''设置为摔倒状态'''
    def setFall(self):
        self.image = pygame.image.load(cfg.SKIER_IMAGE_PATHS[-1])
    '''Set the skier to stand up'''
    '''设置为站立状态'''
    def setForward(self):
        self.direction = 0
        self.image = pygame.image.load(self.imagepaths[self.direction])


'''障碍物类'''
'''Obstracle object'''
class ObstacleClass(pygame.sprite.Sprite):
    def __init__(self, img_path, location, attribute):
        pygame.sprite.Sprite.__init__(self)
        self.img_path = img_path
        self.image = pygame.image.load(self.img_path)
        self.location = location
        self.rect = self.image.get_rect()
        self.rect.center = self.location
        self.attribute = attribute
        self.passed = False
    '''Movement'''
    '''移动'''
    def move(self, num):
        self.rect.centery = self.location[1] - num


'''创建障碍物'''
'''Create obstracles'''
def createObstacles(s, e, num=10):
    obstacles = pygame.sprite.Group()
    locations = []
    for i in range(num):
        row = random.randint(s, e)
        col = random.randint(0, 9)
        location  = [col*64+20, row*64+20]
        if location not in locations:
            locations.append(location)
            attribute = random.choice(list(cfg.OBSTACLE_PATHS.keys()))
            img_path = cfg.OBSTACLE_PATHS[attribute]
            obstacle = ObstacleClass(img_path, location, attribute)
            obstacles.add(obstacle)
    return obstacles


'''合并障碍物'''
'''Merge obstacles'''
def AddObstacles(obstacles0, obstacles1):
    obstacles = pygame.sprite.Group()
    for obstacle in obstacles0:
        obstacles.add(obstacle)
    for obstacle in obstacles1:
        obstacles.add(obstacle)
    return obstacles


'''显示游戏开始界面'''
'''Show the game start interface'''
def ShowStartInterface(screen, screensize):
    screen.fill((255, 255, 255))
    tfont = pygame.font.Font(cfg.FONTPATH, screensize[0]//5)
    cfont = pygame.font.Font(cfg.FONTPATH, screensize[0]//20)
    title = tfont.render(u'Ski Game', True, (255, 0, 0))
    # --玩家指引
    # --Play guide
    content = cfont.render(u'Press any key to start the game', True, (0, 0, 255))
    help = cfont.render(u'Use the A and D bottons to control', True, (0, 0, 255))
    trect = title.get_rect()
    trect.midtop = (screensize[0]/2, screensize[1]/5)
    crect = content.get_rect()
    crect.midtop = (screensize[0]/2, screensize[1]/2)
    hrect = content.get_rect()
    hrect.midtop = (screensize[0]/2, screensize[1]/1.5)
    screen.blit(title, trect)
    screen.blit(content, crect)
    screen.blit(help, hrect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                return
        pygame.display.update()


'''显示分数'''
'''Display score'''
def showScore(screen, score, pos=(10, 10)):
    font = pygame.font.Font(cfg.FONTPATH, 30)
    score_text = font.render("Score: %s" % score, True, (0, 0, 0))
    screen.blit(score_text, pos)


'''更新当前帧的游戏画面'''
'''Update current frame'''
def updateFrame(screen, obstacles, skier, score):
    screen.fill((255, 255, 255))
    obstacles.draw(screen)
    screen.blit(skier.image, skier.rect)
    showScore(screen, score)
    pygame.display.update()

global screen,skier,speed,obstacles0,obstacles1,obstaclesflag,obstacles,clock,distance,score,speed
'''Initialize the game'''
def initGame():
    # 初始化游戏数据
    # Initialize the game
    global screen, skier, speed, obstacles0, obstacles1, obstaclesflag, obstacles, clock, distance, score, speed
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(cfg.BGMPATH)
    pygame.mixer.music.set_volume(0.4)
    pygame.mixer.music.play(-1)
    screen = pygame.display.set_mode(cfg.SCREENSIZE)
    pygame.display.set_caption('Ski game-Charles Pikachu')
    ShowStartInterface(screen, cfg.SCREENSIZE)

def initData():
    # 初始化全局变量，以及滑雪者，障碍物对象
    # Initialize the global varies and skier, obstacles objects
    global screen, skier, speed, obstacles0, obstacles1, obstaclesflag, obstacles, clock, distance, score, speed
    skier = SkierClass()
    obstacles0 = createObstacles(20, 29)
    obstacles1 = createObstacles(10, 19)
    obstaclesflag = 0
    obstacles = AddObstacles(obstacles0, obstacles1)
    clock = pygame.time.Clock()
    score = 0
    speed = [0, 6]


def controlSkier():
    # --Capture keyboard events
    # --事件捕获
    global screen, skier, speed, obstacles0, obstacles1, obstaclesflag, obstacles, clock, distance, score, speed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                speed = skier.turn(-1)
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                speed = skier.turn(1)

def updateObjects():
    global screen, skier, speed, obstacles0, obstacles1, obstaclesflag, obstacles, clock, distance, score, speed
    # --Update the current frame data
    # --更新当前游戏帧的数据
    skier.move()
    distance += speed[1]
    if distance >= 640 and obstaclesflag == 0:
        obstaclesflag = 1
        obstacles0 = createObstacles(20, 29)
        obstacles = AddObstacles(obstacles0, obstacles1)
    if distance >= 1280 and obstaclesflag == 1:
        obstaclesflag = 0
        distance -= 1280
        for obstacle in obstacles0:
            obstacle.location[1] = obstacle.location[1] - 1280
        obstacles1 = createObstacles(10, 19)
        obstacles = AddObstacles(obstacles0, obstacles1)
    for obstacle in obstacles:
        obstacle.move(distance)

def skierHitObstacle():
    global screen, skier, speed, obstacles0, obstacles1, obstaclesflag, obstacles, clock, distance, score, speed
    # --碰撞检测
    # --Whether the skier hit the tree or flag
    hitted_obstacles = pygame.sprite.spritecollide(skier, obstacles, False)
    if hitted_obstacles:
        if hitted_obstacles[0].attribute == "tree" and not hitted_obstacles[0].passed:
            score -= 50
            skier.setFall()
            updateFrame(screen, obstacles, skier, score)
            pygame.time.delay(1000)
            skier.setForward()
            speed = [0, 6]
            hitted_obstacles[0].passed = True
        elif hitted_obstacles[0].attribute == "flag" and not hitted_obstacles[0].passed:
            score += 10
            obstacles.remove(hitted_obstacles[0])
'''Main function'''
'''主程序'''
def main():
    global screen, skier, speed, obstacles0, obstacles1, obstaclesflag, obstacles, clock, distance, score, speed
    # --Initialize the game’s screen, background music
    # --初始化游戏的屏幕 背景音乐
    initGame()
    # --Initialize global variables, as well as skier and obstacle objects
    # --初始化全局变量，以及滑雪者，障碍物对象
    initData()
    while True:
        # --Use a and d to control skier
        # --使用a和b键盘 控制滑雪者
        controlSkier()
        # --Update the skier and obstacle status
        # 更新滑雪者和障碍物状态
        updateObjects()
        # --Determine if the skier hit the tree or reached the scoring point
        # --判断滑雪者是撞到树还是撞到得分点
        skierHitObstacle()
        # --Update current frame
        # --更新屏幕
        updateFrame(screen, obstacles, skier, score)
        clock.tick(cfg.FPS)

'''运行主函数'''
'''run'''
if __name__ == '__main__':
    main()