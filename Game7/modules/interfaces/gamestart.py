'''
Function:
    游戏开始界面
Author:
    Charles
微信公众号:
    Charles的皮卡丘
'''
import sys
import pygame
from ..sprites import Dinosaur

'''Game start interface'''
'''游戏开始界面'''
def GameStartInterface(screen, sounds, cfg):
    font=pygame.font.SysFont('arial', 15)
    help = font.render(u'Use the UP and DOWN bottons to control, press UP to start', True, (0, 0, 253))
    hrect = help.get_rect()
    hrect.midtop = (200, 15)
    dino = Dinosaur(cfg.IMAGE_PATHS['dino'])
    ground = pygame.image.load(cfg.IMAGE_PATHS['ground']).subsurface((0, 0), (83, 19))
    rect = ground.get_rect()
    rect.left, rect.bottom = cfg.SCREENSIZE[0]/20, cfg.SCREENSIZE[1]
    clock = pygame.time.Clock()
    press_flag = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    press_flag = True
                    dino.jump(sounds)
        dino.update()
        screen.fill(cfg.BACKGROUND_COLOR)
        screen.blit(ground, rect)
        screen.blit(help, hrect)
        dino.draw(screen)
        pygame.display.update()
        clock.tick(cfg.FPS)
        if (not dino.is_jumping) and press_flag:
            return True