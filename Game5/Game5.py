'''
Function:
    经典坦克大战小游戏
    Classic tank war games
Author:
    Charles

'''
import os
import cfg
import pygame
from modules import *


'''main function'''
def main(cfg):
    # 游戏初始化
    # Game Initialization
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT))
    pygame.display.set_caption(cfg.TITLE)
    # 加载游戏素材
    # Loading Game Material
    sounds = {}
    for key, value in cfg.AUDIO_PATHS.items():
        sounds[key] = pygame.mixer.Sound(value)
        sounds[key].set_volume(1)
    # 开始界面
    # Game Interface
    is_dual_mode = gameStartInterface(screen, cfg)
    # 关卡数
    # Game Level
    levelfilepaths = [os.path.join(cfg.LEVELFILEDIR, filename) for filename in sorted(os.listdir(cfg.LEVELFILEDIR))]
    # 主循环
    # main loop
    for idx, levelfilepath in enumerate(levelfilepaths):
        switchLevelIterface(screen, cfg, idx+1)
        game_level = GameLevel(idx+1, levelfilepath, sounds, is_dual_mode, cfg)
        is_win = game_level.start(screen)
        if not is_win: break
    is_quit_game = gameEndIterface(screen, cfg, is_win)
    return is_quit_game

'''加载'''
'''run'''
if __name__ == '__main__':
    while True:
        is_quit_game = main(cfg)
        if is_quit_game:
            break
