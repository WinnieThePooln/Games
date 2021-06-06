'''
Function:
    用于运行某一游戏关卡
    Used to run a game level
Author:
    Charles
'''
import sys
import pygame
import random
from .sprites import *


'''用于运行某一游戏关卡'''
'''Used to run a game level'''
class GameLevel():
    def __init__(self, gamelevel, levelfilepath, sounds, is_dual_mode, cfg, **kwargs):
        # 关卡地图路径
        # Level map path
        self.gamelevel = gamelevel
        self.levelfilepath = levelfilepath
        # 音效
        # sound
        self.sounds = sounds
        # 是否为双人模式
        # Whether to double mode or not
        self.is_dual_mode = is_dual_mode
        # 地图规模参数
        # Map size parameter
        self.border_len = cfg.BORDER_LEN
        self.grid_size = cfg.GRID_SIZE
        self.width, self.height = cfg.WIDTH, cfg.HEIGHT
        self.panel_width = cfg.PANEL_WIDTH
        # 图片路径
        # Image path
        self.scene_image_paths = cfg.SCENE_IMAGE_PATHS
        self.other_image_paths = cfg.OTHER_IMAGE_PATHS
        self.player_tank_image_paths = cfg.PLAYER_TANK_IMAGE_PATHS
        self.bullet_image_paths = cfg.BULLET_IMAGE_PATHS
        self.enemy_tank_image_paths = cfg.ENEMY_TANK_IMAGE_PATHS
        self.food_image_paths = cfg.FOOD_IMAGE_PATHS
        self.home_image_paths = cfg.HOME_IMAGE_PATHS
        # 字体
        # Font
        self.font = pygame.font.Font(cfg.FONTPATH, cfg.HEIGHT//30)
        # 关卡场景元素
        # Level Scene Elements
        self.scene_elems = {
            'brick_group': pygame.sprite.Group(), 
            'iron_group': pygame.sprite.Group(),
            'ice_group': pygame.sprite.Group(), 
            'river_group': pygame.sprite.Group(),
            'tree_group': pygame.sprite.Group()
        }
        # 解析关卡文件
        # Parse the level file
        self.__parseLevelFile()
    '''开始游戏'''
    '''Start the game'''
    def start(self, screen):
        screen = pygame.display.set_mode((self.width+self.panel_width, self.height))
        # 背景图片
        # background image
        background_img = pygame.image.load(self.other_image_paths.get('background'))
        # 定义精灵组
        # Define a Sprite group
        player_tanks_group = pygame.sprite.Group()
        enemy_tanks_group = pygame.sprite.Group()
        player_bullets_group = pygame.sprite.Group()
        enemy_bullets_group = pygame.sprite.Group()
        foods_group = pygame.sprite.Group()
        # 定义敌方坦克生成事件
        # Define enemy tank spawn events
        generate_enemies_event = pygame.constants.USEREVENT
        pygame.time.set_timer(generate_enemies_event, 20000)
        # 我方大本营
        # Our Headquarters
        home = Home(position=self.home_position, imagepaths=self.home_image_paths)
        # 我方坦克
        # Our Tanks
        tank_player1 = PlayerTank('player1', position=self.player_tank_positions[0], player_tank_image_paths=self.player_tank_image_paths, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, protected_mask_path=self.other_image_paths.get('protect'), boom_image_path=self.other_image_paths.get('boom_static'))
        player_tanks_group.add(tank_player1)
        if self.is_dual_mode:
            tank_player2 = PlayerTank('player2', position=self.player_tank_positions[1], player_tank_image_paths=self.player_tank_image_paths, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, protected_mask_path=self.other_image_paths.get('protect'), boom_image_path=self.other_image_paths.get('boom_static'))
            player_tanks_group.add(tank_player2)
        # 敌方坦克
        # Enemy Tanks
        for position in self.enemy_tank_positions:
            enemy_tanks_group.add(EnemyTank(enemy_tank_image_paths=self.enemy_tank_image_paths, appear_image_path=self.other_image_paths.get('appear'), position=position, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, food_image_paths=self.food_image_paths, boom_image_path=self.other_image_paths.get('boom_static')))
        # 游戏开始音乐
        # The game starts with music
        self.sounds['start'].play()
        clock = pygame.time.Clock()
        # 该关卡通过与否的flags
        # flags whether the level passes or not
        is_win = False
        is_running = True
        # 游戏主循环
        # Main Loop
        while is_running:
            screen.fill((0, 0, 0))
            screen.blit(background_img, (0, 0))
            # 用户事件捕捉
            # User event capture
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # --敌方坦克生成
                # -- Enemy tank spawn
                elif event.type == generate_enemies_event:
                    if self.max_enemy_num > len(enemy_tanks_group):
                        for position in self.enemy_tank_positions:
                            if len(enemy_tanks_group) == self.total_enemy_num:
                                break
                            enemy_tank = EnemyTank(enemy_tank_image_paths=self.enemy_tank_image_paths, appear_image_path=self.other_image_paths.get('appear'), position=position, border_len=self.border_len, screensize=[self.width, self.height], bullet_image_paths=self.bullet_image_paths, food_image_paths=self.food_image_paths, boom_image_path=self.other_image_paths.get('boom_static'))
                            if (not pygame.sprite.spritecollide(enemy_tank, enemy_tanks_group, False, None)) and (not pygame.sprite.spritecollide(enemy_tank, player_tanks_group, False, None)):
                                enemy_tanks_group.add(enemy_tank)
            # --用户按键
            # --User keys
            key_pressed = pygame.key.get_pressed()
            # 玩家一, WSAD移动, 空格键射击
            # Player 1, WSAD move, the space bar shooting
            if tank_player1.num_lifes >= 0:
                if key_pressed[pygame.K_w]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('up', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_s]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('down', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_a]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('left', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_d]:
                    player_tanks_group.remove(tank_player1)
                    tank_player1.move('right', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player1)
                elif key_pressed[pygame.K_SPACE]:
                    bullet = tank_player1.shoot()
                    if bullet:
                        self.sounds['fire'].play() if tank_player1.tanklevel < 2 else self.sounds['Gunfire'].play()
                        player_bullets_group.add(bullet)
            # 玩家二, ↑↓←→移动, 小键盘0键射击
            # Player 2, ↑↓←→ Move, 0 key shooting on the keypad
            if self.is_dual_mode and (tank_player2.num_lifes >= 0):
                if key_pressed[pygame.K_UP]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('up', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_DOWN]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('down', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_LEFT]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('left', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_RIGHT]:
                    player_tanks_group.remove(tank_player2)
                    tank_player2.move('right', self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                    player_tanks_group.add(tank_player2)
                elif key_pressed[pygame.K_KP0]:
                    bullet = tank_player2.shoot()
                    if bullet:
                        player_bullets_group.add(bullet)
                        self.sounds['fire'].play() if tank_player2.tanklevel < 2 else self.sounds['Gunfire'].play()
            # 碰撞检测
            # Collision Detection
            # --子弹和砖墙
            # -- Bullets and brick walls
            pygame.sprite.groupcollide(player_bullets_group, self.scene_elems.get('brick_group'), True, True)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('brick_group'), True, True)
            # --子弹和铁墙
            # -- Bullets and iron walls
            for bullet in player_bullets_group:
                if pygame.sprite.spritecollide(bullet, self.scene_elems.get('iron_group'), bullet.is_stronger, None):
                    player_bullets_group.remove(bullet)
            pygame.sprite.groupcollide(enemy_bullets_group, self.scene_elems.get('iron_group'), True, False)
            # --子弹撞子弹
            # -- Bullets collide bullets
            pygame.sprite.groupcollide(player_bullets_group, enemy_bullets_group, True, True)
            # --我方子弹撞敌方坦克
            # -- Our bullets hit enemy tanks
            for tank in enemy_tanks_group:
                if pygame.sprite.spritecollide(tank, player_bullets_group, True, None):
                    if tank.food:
                        foods_group.add(tank.food)
                        tank.food = None
                    if tank.decreaseTankLevel():
                        self.sounds['bang'].play()
                        self.total_enemy_num -= 1
            # --敌方子弹撞我方坦克
            # -- Enemy bullets hit our tanks
            for tank in player_tanks_group:
                if pygame.sprite.spritecollide(tank, enemy_bullets_group, True, None):
                    if tank.is_protected:
                        self.sounds['blast'].play()
                    else:
                        if tank.decreaseTankLevel():
                            self.sounds['bang'].play()
                        if tank.num_lifes < 0:
                            player_tanks_group.remove(tank)
            # --我方子弹撞我方大本营
            # -- Our bullets hit our base camp
            if pygame.sprite.spritecollide(home, player_bullets_group, True, None):
                is_win = False
                is_running = False
                home.setDead()
            # --敌方子弹撞我方大本营
            # -- Enemy bullets hit our base camp
            if pygame.sprite.spritecollide(home, enemy_bullets_group, True, None):
                is_win = False
                is_running = False
                home.setDead()
            # --我方坦克在植物里
            # -- Our tanks are in the plants
            if pygame.sprite.groupcollide(player_tanks_group, self.scene_elems.get('tree_group'), False, False):
                self.sounds['hit'].play()
            # --我方坦克吃到食物
            # --Our tanks are getting food
            for player_tank in player_tanks_group:
                for food in foods_group:
                    if pygame.sprite.collide_rect(player_tank, food):
                        if food.name == 'boom':
                            self.sounds['add'].play()
                            for _ in enemy_tanks_group:
                                self.sounds['bang'].play()
                            self.total_enemy_num -= len(enemy_tanks_group)
                            enemy_tanks_group = pygame.sprite.Group()
                        elif food.name == 'clock':
                            self.sounds['add'].play()
                            for enemy_tank in enemy_tanks_group:
                                enemy_tank.setStill()
                        elif food.name == 'gun':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                        elif food.name == 'iron':
                            self.sounds['add'].play()
                            self.__pretectHome()
                        elif food.name == 'protect':
                            self.sounds['add'].play()
                            player_tank.setProtected()
                        elif food.name == 'star':
                            self.sounds['add'].play()
                            player_tank.improveTankLevel()
                            player_tank.improveTankLevel()
                        elif food.name == 'tank':
                            self.sounds['add'].play()
                            player_tank.addLife()
                        foods_group.remove(food)
            # 画场景地图
            # Draw a Scene Map
            for key, value in self.scene_elems.items():
                if key in ['ice_group', 'river_group']:
                    value.draw(screen)
            # 更新并画我方子弹
            # Update and draw our bullets
            for bullet in player_bullets_group:
                if bullet.move():
                    player_bullets_group.remove(bullet)
            player_bullets_group.draw(screen)
            # 更新并画敌方子弹
            # Update and draw enemy bullets
            for bullet in enemy_bullets_group:
                if bullet.move():
                    enemy_bullets_group.remove(bullet)
            enemy_bullets_group.draw(screen)
            # 更新并画我方坦克
            # Update and draw our tanks
            for tank in player_tanks_group:
                tank.update()
                tank.draw(screen)
            # 更新并画敌方坦克
            # Update and draw enemy tanks
            for tank in enemy_tanks_group:
                enemy_tanks_group.remove(tank)
                data_return = tank.update(self.scene_elems, player_tanks_group, enemy_tanks_group, home)
                enemy_tanks_group.add(tank)
                if data_return.get('bullet'):
                    enemy_bullets_group.add(data_return.get('bullet'))
                if data_return.get('boomed'):
                    enemy_tanks_group.remove(tank)
            enemy_tanks_group.draw(screen)
            # 画场景地图
            # Draw a Scene Map
            for key, value in self.scene_elems.items():
                if key not in ['ice_group', 'river_group']:
                    value.draw(screen)
            # 画大本营
            # Draw a Family
            home.draw(screen)
            # 更新并显示食物
            # Update and display food
            for food in foods_group:
                if food.update():
                    foods_group.remove(food)
            foods_group.draw(screen)
            self.__showGamePanel(screen, tank_player1, tank_player2) if self.is_dual_mode else self.__showGamePanel(screen, tank_player1)
            # 我方坦克都挂了
            # Our tanks are all dead
            if len(player_tanks_group) == 0:
                is_win = False
                is_running = False
            # 敌方坦克都挂了
            # The enemy tanks are dead
            if self.total_enemy_num <= 0:
                is_win = True
                is_running = False
            pygame.display.flip()
            clock.tick(60)
        screen = pygame.display.set_mode((self.width, self.height))
        return is_win
    '''显示游戏面板'''
    '''Show Game Panel'''
    def __showGamePanel(self, screen, tank_player1, tank_player2=None):
        color_white = (255, 255, 255)
        # 玩家一操作提示
        # Player 1 operation prompts
        player1_operate_tip = self.font.render('Operate-P1:', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_w: Up', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*2/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_s: Down', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*3/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_a: Left', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*4/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_d: Right', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*5/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)
        player1_operate_tip = self.font.render('K_SPACE: Shoot', True, color_white)
        player1_operate_tip_rect = player1_operate_tip.get_rect()
        player1_operate_tip_rect.left, player1_operate_tip_rect.top = self.width+5, self.height*6/30
        screen.blit(player1_operate_tip, player1_operate_tip_rect)

        # 玩家二操作提示
        # Player 2 operation prompts
        player2_operate_tip = self.font.render('Operate-P2:', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*8/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_UP: Up', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*9/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_DOWN: Down', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*10/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_LEFT: Left', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*11/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_RIGHT: Right', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*12/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        player2_operate_tip = self.font.render('K_KP0: Shoot', True, color_white)
        player2_operate_tip_rect = player2_operate_tip.get_rect()
        player2_operate_tip_rect.left, player2_operate_tip_rect.top = self.width+5, self.height*13/30
        screen.blit(player2_operate_tip, player2_operate_tip_rect)
        # 玩家一状态提示
        # Player 1 status alert
        player1_state_tip = self.font.render('State-P1:', True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*15/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        player1_state_tip = self.font.render('Life: %s' % tank_player1.num_lifes, True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*16/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        player1_state_tip = self.font.render('TLevel: %s' % tank_player1.tanklevel, True, color_white)
        player1_state_tip_rect = player1_state_tip.get_rect()
        player1_state_tip_rect.left, player1_state_tip_rect.top = self.width+5, self.height*17/30
        screen.blit(player1_state_tip, player1_state_tip_rect)
        # 玩家二状态提示
        # Player 2 status prompts
        player2_state_tip = self.font.render('State-P2:', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*19/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        player2_state_tip = self.font.render('Life: %s' % tank_player2.num_lifes, True, color_white) if tank_player2 else self.font.render('Life: None', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*20/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        player2_state_tip = self.font.render('TLevel: %s' % tank_player2.tanklevel, True, color_white) if tank_player2 else self.font.render('TLevel: None', True, color_white)
        player2_state_tip_rect = player2_state_tip.get_rect()
        player2_state_tip_rect.left, player2_state_tip_rect.top = self.width+5, self.height*21/30
        screen.blit(player2_state_tip, player2_state_tip_rect)
        # 当前关卡
        # Current Level
        game_level_tip = self.font.render('Game Level: %s' % self.gamelevel, True, color_white)
        game_level_tip_rect = game_level_tip.get_rect()
        game_level_tip_rect.left, game_level_tip_rect.top = self.width+5, self.height*23/30
        screen.blit(game_level_tip, game_level_tip_rect)
        game_level_tip = self.font.render('Bullet are', True, color_white)
        game_level_tip_rect = game_level_tip.get_rect()
        game_level_tip_rect.left, game_level_tip_rect.top = self.width+5, self.height*24/30
        screen.blit(game_level_tip, game_level_tip_rect)
        game_level_tip = self.font.render('Infinite', True, color_white)
        game_level_tip_rect = game_level_tip.get_rect()
        game_level_tip_rect.left, game_level_tip_rect.top = self.width+5, self.height*25/30
        screen.blit(game_level_tip, game_level_tip_rect)


        # 剩余敌人数量
        # Number of remaining enemies
        remaining_enemy_tip = self.font.render('Remain Enemy: %s' % self.total_enemy_num, True, color_white)
        remaining_enemy_tip_rect = remaining_enemy_tip.get_rect()
        remaining_enemy_tip_rect.left, remaining_enemy_tip_rect.top = self.width+5, self.height*27/30
        screen.blit(remaining_enemy_tip, remaining_enemy_tip_rect)
    '''保护大本营'''
    '''Protect Base Camp'''
    def __pretectHome(self):
        for x, y in self.home_around_positions:
            self.scene_elems['iron_group'].add(Iron((x, y), self.scene_image_paths.get('iron')))
    '''解析关卡文件'''
    '''Parsing Level Files'''
    def __parseLevelFile(self):
        f = open(self.levelfilepath, errors='ignore')
        num_row = -1
        for line in f.readlines():
            line = line.strip('\n')
            # 注释
            # comment line
            if line.startswith('#') or (not line):
                continue
            # 敌方坦克总数量
            # Total number of enemy tanks
            elif line.startswith('%TOTALENEMYNUM'):
                self.total_enemy_num = int(line.split(':')[-1])
            # 场上敌方坦克最大数量
            # Maximum number of enemy tanks in the field
            elif line.startswith('%MAXENEMYNUM'):
                self.max_enemy_num = int(line.split(':')[-1])
            # 大本营位置
            # Location of Base Camp
            elif line.startswith('%HOMEPOS'):
                self.home_position = line.split(':')[-1]
                self.home_position = [int(self.home_position.split(',')[0]), int(self.home_position.split(',')[1])]
                self.home_position = (self.border_len+self.home_position[0]*self.grid_size, self.border_len+self.home_position[1]*self.grid_size)
            # 大本营周围位置
            # Location around base camp
            elif line.startswith('%HOMEAROUNDPOS'):
                self.home_around_positions = line.split(':')[-1]
                self.home_around_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.home_around_positions.split(' ')]
                self.home_around_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.home_around_positions]
            # 我方坦克初始位置
            # Initial position of our tanks
            elif line.startswith('%PLAYERTANKPOS'):
                self.player_tank_positions = line.split(':')[-1]
                self.player_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.player_tank_positions.split(' ')]
                self.player_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.player_tank_positions]
            # 敌方坦克初始位置
            # Initial position of enemy tank
            elif line.startswith('%ENEMYTANKPOS'):
                self.enemy_tank_positions = line.split(':')[-1]
                self.enemy_tank_positions = [[int(pos.split(',')[0]), int(pos.split(',')[1])] for pos in self.enemy_tank_positions.split(' ')]
                self.enemy_tank_positions = [(self.border_len+pos[0]*self.grid_size, self.border_len+pos[1]*self.grid_size) for pos in self.enemy_tank_positions]
            # 地图元素
            # Map Element
            else:
                num_row += 1
                for num_col, elem in enumerate(line.split(' ')):
                    position = self.border_len+num_col*self.grid_size, self.border_len+num_row*self.grid_size
                    if elem == 'B':
                        self.scene_elems['brick_group'].add(Brick(position, self.scene_image_paths.get('brick')))
                    elif elem == 'I':
                        self.scene_elems['iron_group'].add(Iron(position, self.scene_image_paths.get('iron')))
                    elif elem == 'R':
                        self.scene_elems['river_group'].add(River(position, self.scene_image_paths.get(random.choice(['river1', 'river2']))))
                    elif elem == 'C':
                        self.scene_elems['ice_group'].add(Ice(position, self.scene_image_paths.get('ice')))
                    elif elem == 'T':
                        self.scene_elems['tree_group'].add(Tree(position, self.scene_image_paths.get('tree')))
