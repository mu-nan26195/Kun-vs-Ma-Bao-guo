import sys
import random
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from aline import Aline


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("坤哥大战马保国")

        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.sb = Scoreboard(self)

        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.alines = pygame.sprite.Group()

        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alines()
                self._check_collisions()

            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.game_active = True

            self.ship.weapons = ['normal']
            self.ship.current_weapon_index = 0

            self.bullets.empty()
            self.enemy_bullets.empty()
            self.alines.empty()

            self._create_fleet()
            self.ship.center_ship()

            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.sb.prep_weapon()

            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_TAB:
            self.ship.switch_weapon()
            self.sb.prep_weapon()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            weapon_type = 'normal'

            if self.stats.level >= 3 and random.random() < 0.3:
                weapon_type = 'laser'
            elif self.stats.level >= 5 and random.random() < 0.2:
                weapon_type = 'spread'

            new_bullet = Bullet(self, weapon_type)
            self.bullets.add(new_bullet)

            if weapon_type == 'spread':
                left_bullet = Bullet(self, 'spread')
                left_bullet.rect.x -= 20
                right_bullet = Bullet(self, 'spread')
                right_bullet.rect.x += 20
                self.bullets.add(left_bullet)
                self.bullets.add(right_bullet)

    def _update_bullets(self):
        self.bullets.update()
        self.enemy_bullets.update()

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        for bullet in self.enemy_bullets.copy():
            if bullet.rect.top >= self.settings.screen_height:
                self.enemy_bullets.remove(bullet)

    def _check_collisions(self):
        # 玩家子弹打中敌人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.alines, True, False)

        if collisions:
            for bullets, aliens in collisions.items():
                for alien in aliens:
                    if alien.hit():
                        self.stats.score += alien.points
                        self.alines.remove(alien)
            self.sb.prep_score()
            self.sb.check_high_score()

        # 敌人子弹打中玩家
        if pygame.sprite.spritecollideany(self.ship, self.enemy_bullets):
            self._ship_hit()

        # 敌人撞到玩家
        if pygame.sprite.spritecollideany(self.ship, self.alines):
            self._ship_hit()

        # 检查是否所有敌人都被消灭
        if not self.alines:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

            # 解锁新武器
            if self.stats.level == 3:
                self.ship.unlock_weapon('laser')
                self.sb.prep_weapon()  # 解锁武器后更新显示
            elif self.stats.level == 5:
                self.ship.unlock_weapon('spread')
                self.sb.prep_weapon()  # 解锁武器后更新显示

    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            self.bullets.empty()
            self.enemy_bullets.empty()
            self.alines.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _create_fleet(self):
        aline_types = ['normal', 'fast', 'tank']
        if self.stats.level % 5 == 0:
            aline_types.append('boss')

        aline = Aline(self)
        aline_width, aline_height = aline.rect.size

        available_space_x = self.settings.screen_width - 2 * aline_width
        number_columns = available_space_x // (2 * aline_width)

        available_space_y = self.settings.screen_height - 3 * aline_height
        number_rows = available_space_y // (2 * aline_height)

        for row_number in range(number_rows):
            for column_number in range(number_columns):
                x_position = aline_width + 2 * aline_width * column_number
                y_position = aline_height + 2 * aline_height * row_number
                aline_type = random.choice(aline_types)
                self._create_aline(x_position, y_position, aline_type)

    def _create_aline(self, x_position, y_position, aline_type):
        new_aline = Aline(self, aline_type)
        new_aline.x = x_position
        new_aline.rect.x = x_position
        new_aline.rect.y = y_position
        self.alines.add(new_aline)

    def _update_alines(self):
        self._check_fleet_edges()
        self.alines.update()

        # 检查是否有敌人到达底部
        for alien in self.alines.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        for alien in self.alines.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.alines.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        for bullet in self.enemy_bullets.sprites():
            bullet.draw_bullet()

        self.ship.blitme()
        self.alines.draw(self.screen)
        self.sb.show_score()

        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()