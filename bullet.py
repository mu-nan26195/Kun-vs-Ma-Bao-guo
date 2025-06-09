import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game, bullet_type='normal', from_enemy=False, enemy=None):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.type = bullet_type
        self.from_enemy = from_enemy

        # 获取武器配置
        weapon_config = self.settings.weapon_types.get(bullet_type, {})

        self.color = weapon_config.get('color', (60, 60, 60))
        self.speed = weapon_config.get('speed', 2.5)
        self.damage = weapon_config.get('damage', 1)
        self.width = weapon_config.get('width', 3)
        self.height = weapon_config.get('height', 15)

        self.rect = pygame.Rect(0, 0, self.width, self.height)

        # 设置初始位置
        if from_enemy and enemy:
            self.rect.midtop = enemy.rect.midbottom
            self.speed = -abs(self.speed)  # 敌人子弹向下
        else:
            self.rect.midbottom = ai_game.ship.rect.midtop
            self.speed = abs(self.speed)  # 玩家子弹向上

        self.y = float(self.rect.y)

    def update(self):
        self.y -= self.speed
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)