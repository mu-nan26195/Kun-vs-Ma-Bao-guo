class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_speed = 3.0
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 10

        # 外星人设置
        self.aline_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 1表示右移，-1表示左移

        # 游戏加速设置
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # 武器系统
        self.weapon_types = {
            'normal': {'speed': 2.5, 'damage': 1, 'width': 3, 'height': 15, 'color': (60, 60, 60)},
            'laser': {'speed': 4.0, 'damage': 2, 'width': 8, 'height': 30, 'color': (255, 0, 0)},
            'spread': {'speed': 3.0, 'damage': 1, 'width': 5, 'height': 10, 'color': (0, 255, 0)},
            'enemy': {'speed': 1.5, 'damage': 1, 'width': 6, 'height': 12, 'color': (255, 165, 0)}
        }

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.aline_speed = 1.0
        self.aline_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.aline_speed *= self.speedup_scale
        self.aline_points = int(self.aline_points * self.score_scale)