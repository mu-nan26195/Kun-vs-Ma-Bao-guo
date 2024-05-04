import sys
from time import sleep
from game_stats import GameStats
from button import Button
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from aline import Aline
from scoreboard import Scoreboard
pygame.mixer.init()
music_path= r'SWIN-S - 只因你太美 [mqms2].mp3'
pygame.mixer.music.load(music_path)
pygame.mixer.music.set_volume(0.5)
class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.alines = pygame.sprite.Group()
        self._create_fleet()
        self.bg_color = (230,230,230)
        self.game_active = False
        self.play_button = Button(self,"play")
    def run_game(self):
        while True:
            self._check_events()
            if self.game_active == True:
                self.ship.update()
                self._update_bullet()
                self._update_alines()
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
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            pygame.mixer.music.play(0)
            self.bullets.empty()
            self.alines.empty()
            self._create_fleet()
            self.ship.center_ship()
            music_path2 = r'SWIN-S - 只因你太美 [mqms2].mp3'
            pygame.mixer.music.load(music_path2)
            pygame.mixer.music.play(0)
            pygame.mouse.set_visible(False)
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
    def _fire_bullet(self):
        if len(self.bullets) <self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
    def _ship_hit(self):
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.alines.empty()
            self._create_fleet()
            self.ship.center_ship()
            sleep(0.5)
        elif self.stats.score<1000:
            music_path1 = r'菜就多练.mp3'
            pygame.mixer.music.load(music_path1)
            pygame.mixer.music.play(0)
            pygame.mouse.set_visible(True)
            self.game_active = False
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    def _update_alines(self):
        self._check_fleet_edges()
        self.alines.update()
        if pygame.sprite.spritecollideany(self.ship, self.alines):
            self._ship_hit()
        self._check_aline_bottom()
    def _update_bullet(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_aline_collisions()
    def _check_bullet_aline_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets,self.alines,True,True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.aline_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.alines:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()
    def _create_fleet(self):
        aline=Aline(self)
        aline_width, aline_height = aline.rect.size
        current_x, current_y = aline_width, aline_height
        while current_y < (self.settings.screen_height -3 * aline_height):
            while current_x <(self.settings.screen_width - 2 * aline_width):
                self._create_aline(current_x,current_y)
                current_x +=2 * aline_height
            current_x = aline_width
            current_y += 2 * aline_height
    def _create_aline(self,x_position,y_position):
        new_aline = Aline(self)
        new_aline.x=x_position
        new_aline.rect.x=x_position
        new_aline.rect.y=y_position
        self.alines.add(new_aline)
    def _check_fleet_edges(self):
        for alien in self.alines.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        for aline in self.alines.sprites():
            aline.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.alines.draw(self.screen)
        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()
    def _check_aline_bottom(self):
        for alien in self.alines.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break
if __name__=="__main__":
    ai=AlienInvasion()
    ai.run_game()