import pygame
from pygame.sprite import Sprite
class Aline(Sprite):
    def __init__(self,ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image=pygame.image.load('保国.bmp')
        self.rect =self.image.get_rect()
        self.x = self.rect.width
        self.y = self.rect.height
        self.x = float(self.rect.x)
    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right)or(self.rect.left<=0)
    def update(self):
        self.x+=self.settings.aline_speed*self.settings.fleet_direction
        self.rect.x = self.x