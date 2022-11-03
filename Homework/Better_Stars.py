import sys
import pygame
from pygame.sprite import Sprite
from random import randint


class StarInvasion:
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Star Invasion")

        self.stars = pygame.sprite.Group()

        self._create_fleet()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_q:
            sys.exit()

    def _create_fleet(self):
        star = Star(self)
        star_width, star_height = star.rect.size
        available_space_x = self.settings.screen_width - (star_width)
        number_stars_x = available_space_x // (2 * star_width)
        available_space_y = (self.settings.screen_height -
                             (3 * star_height))
        number_rows = available_space_y // (2 * star_height)

        for row_number in range(number_rows):
            for star_number in range(number_stars_x):
                self._create_star(star_number, row_number)

    def _create_star(self, star_number, row_number):
        star = Star(self)
        star_width, star_height = star.rect.size
        star.rect.x = star_width + 2 * star_width * star_number
        star.rect.y = star.rect.height + 2 * star.rect.height * row_number

        star.rect.x += randint(-5, 5)
        star.rect.y += randint(-5, 5)

        self.stars.add(star)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.stars.draw(self.screen)

        pygame.dispaly.flip()

    def run_game(self):
        while True:
            self._check_events()
            self._update_screen()


if __name__ == '__main__':
    si = StarInvasion()
    si.run_game()


class Settings:
    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (255, 255, 255)


class Star(Sprite):
    def __init__(self, si_game):
        super().__init__()
        self.screen = si_game.screen

        self.image = pygame.image.load('../images/star.png')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.y = float(self.rect.y)
