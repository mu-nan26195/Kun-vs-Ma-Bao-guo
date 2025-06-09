import pygame
from pygame.sprite import Sprite
import random


class Aline(Sprite):
    def __init__(self, ai_game, enemy_type='normal'):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.ai_game = ai_game
        self.type = enemy_type

        # 加载不同敌人图像
        if enemy_type == 'normal':
            self.image = pygame.image.load('保国.bmp')
            self.speed_factor = 1.0
            self.health = 1
            self.points = 50
        elif enemy_type == 'fast':
            self.image = pygame.image.load('fast.bmp')
            self.speed_factor = 2.0
            self.health = 1
            self.points = 75
        elif enemy_type == 'tank':
            self.image = pygame.image.load('tank.bmp')
            self.speed_factor = 0.5
            self.health = 3
            self.points = 150
        elif enemy_type == 'boss':
            self.image = pygame.image.load('boss.bmp')
            self.speed_factor = 0.3
            self.health = 10
            self.points = 500

        self.rect = self.image.get_rect()
        self.x = float(self.rect.x)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        return (self.rect.right >= screen_rect.right) or (self.rect.left <= 0)

    def update(self):
        self.x += self.settings.aline_speed * self.speed_factor * self.settings.fleet_direction
        self.rect.x = self.x

        # Boss敌人有几率发射子弹
        if self.type == 'boss' and random.random() < 0.01:
            self.fire_bullet()

    def hit(self):
        self.health -= 1
        return self.health <= 0

    def fire_bullet(self):
        enemy_bullet = Bullet(self.ai_game, 'enemy', True, self)
        self.ai_game.enemy_bullets.add(enemy_bullet)