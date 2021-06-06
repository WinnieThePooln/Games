'''
Function:
    大本营类
    Home in the Game
Author:
    Charles

'''
import pygame


'''大本营类'''
'''Home'''
class Home(pygame.sprite.Sprite):
    def __init__(self, position, imagepaths, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.imagepaths = imagepaths
        self.image = pygame.image.load(self.imagepaths[0])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = position
        self.alive = True
    '''被摧毁'''
    '''Be ruined'''
    def setDead(self):
        self.image = pygame.image.load(self.imagepaths[1])
        self.alive = False
    '''画到屏幕上'''
    ''' Draw it on screen '''
    def draw(self, screen):
        screen.blit(self.image, self.rect)
