from random import randint

import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ss_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings

        # Load the alien image and set its rect attribute.
        self.image = pygame.image.load('images/alien_ship.png')
        self.rect = self.image.get_rect()

        # Start each new alien at a random position on the right side
        #   of the screen.
        self.rect.left = self.screen.get_rect().right
        # The farthest down the screen we'll place the alien is the height
        #   of the screen, minus the height of the alien.
        alien_top_max = self.settings.screen_height - self.rect.height
        self.rect.top = randint(0, alien_top_max)

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def update(self):
        """Move the alien steadily to the left."""
        self.x -= self.settings.alien_speed
        self.rect.x = self.x


import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ss_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()
        self.screen = ss_game.screen
        self.settings = ss_game.settings
        self.color = self.settings.bullet_color

        # Create a bullet rect at (0, 0) and then set correct position.
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midright = ss_game.ship.rect.midright

        # Store the bullet's position as a decimal value.
        self.x = float(self.rect.x)

    def update(self):
        """Move the bullet across the screen."""
        # Update the decimal position of the bullet.
        self.x += self.settings.bullet_speed
        # Update the rect position.
        self.rect.x = self.x

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen, self.color, self.rect)

    class GameStats:
        """Track statistics for the game."""

        def __init__(self, ss_game):
            """Initialize statistics."""
            self.settings = ss_game.settings
            self.reset_stats()

            # Start game in an active state.
            self.game_active = True

        def reset_stats(self):
            """Initialize statistics that can change during the game."""
            self.ships_left = self.settings.ship_limit

    class Settings:
        """A class to store all settings for Sideways Shooter."""

        def __init__(self):
            """Initialize the game's settings."""
            # Screen settings
            self.screen_width = 1200
            self.screen_height = 800
            self.bg_color = (230, 230, 230)

            # Ship settings
            self.ship_speed = 3.0
            self.ship_limit = 3

            # Bullet settings
            self.bullet_speed = 6.0
            self.bullet_width = 15
            self.bullet_height = 3
            self.bullet_color = (60, 60, 60)
            self.bullets_allowed = 3

            # Alien settings.
            #  alien_frequency controls how often a new alien appear.s
            #    Higher values -> more frequent aliens. Max = 1.0.
            self.alien_frequency = 0.015
            self.alien_speed = 6.0

    import pygame

    class Ship:
        """A class to manage the ship."""

        def __init__(self, ss_game):
            """Initialize the ship and set its starting position."""
            self.screen = ss_game.screen
            self.settings = ss_game.settings
            self.screen_rect = ss_game.screen.get_rect()

            # Load the ship image and get its rect.
            self.image = pygame.image.load('images/rocket_small.png')
            self.rect = self.image.get_rect()

            # Start each new ship at the center of the left side of the screen.
            self.center_ship()

            # Movement flags
            self.moving_up = False
            self.moving_down = False

        def update(self):
            """Update the ship's position based on movement flags."""
            # Update the ship's y value, not the rect.
            if self.moving_up and self.rect.top > 0:
                self.y -= self.settings.ship_speed
            if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
                self.y += self.settings.ship_speed

            # Update rect object from self.y.
            self.rect.y = self.y

        def center_ship(self):
            """Center the ship on the left side of the screen."""
            self.rect.midleft = self.screen_rect.midleft

            # Store a decimal value for the ship's vertical position.
            self.y = float(self.rect.y)

        def blitme(self):
            """Draw the ship at its current location."""
            self.screen.blit(self.image, self.rect)

    import sys
    from random import random

    import pygame

    from settings import Settings
    from game_stats import GameStats
    from ship import Ship
    from bullet import Bullet
    from alien import Alien

    class SidewaysShooter:
        """Overall class to manage game assets and behavior."""

        def __init__(self):
            """Initialize the game, and create game resources."""
            pygame.init()
            self.settings = Settings()

            self.screen = pygame.display.set_mode(
                (self.settings.screen_width, self.settings.screen_height))
            pygame.display.set_caption("Sideways Shooter")

            # Create an instance to store game statistics.
            self.stats = GameStats(self)

            self.ship = Ship(self)
            self.bullets = pygame.sprite.Group()
            self.aliens = pygame.sprite.Group()

        def run_game(self):
            """Start the main loop for the game."""
            while True:
                self._check_events()

                if self.stats.game_active:
                    # Consider creating a new alien.
                    self._create_alien()

                    self.ship.update()
                    self._update_bullets()
                    self._update_aliens()

                self._update_screen()

        def _check_events(self):
            """Respond to keypresses and mouse events."""
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)

        def _check_keydown_events(self, event):
            """Respond to keypresses."""
            if event.key == pygame.K_UP:
                self.ship.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.ship.moving_down = True
            elif event.key == pygame.K_SPACE:
                self._fire_bullet()
            elif event.key == pygame.K_q:
                sys.exit()

        def _check_keyup_events(self, event):
            """Respond to key releases."""
            if event.key == pygame.K_UP:
                self.ship.moving_up = False
            elif event.key == pygame.K_DOWN:
                self.ship.moving_down = False

        def _fire_bullet(self):
            """Create a new bullet and add it to the bullets group."""
            if len(self.bullets) < self.settings.bullets_allowed:
                new_bullet = Bullet(self)
                self.bullets.add(new_bullet)

        def _update_bullets(self):
            """Update position of bullets and get rid of old bullets."""
            # Update bullet positions.
            self.bullets.update()

            # Get rid of bullets that have disappeared.
            for bullet in self.bullets.copy():
                if bullet.rect.left >= self.screen.get_rect().right:
                    self.bullets.remove(bullet)

            self._check_bullet_alien_collisions()

        def _check_bullet_alien_collisions(self):
            """Check whether any bullets have hit an alien."""
            collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)

        def _create_alien(self):
            """Create an alien, if conditions are right."""
            if random() < self.settings.alien_frequency:
                alien = Alien(self)
                self.aliens.add(alien)

        def _update_aliens(self):
            """Update alien positions, and look for collisions with ship."""
            self.aliens.update()

            if pygame.sprite.spritecollideany(self.ship, self.aliens):
                self._ship_hit()

            # Look for aliens that have hit the left edge of the screen.
            self._check_aliens_left_edge()

        def _check_aliens_left_edge(self):
            """Respond to aliens that have hit left edge of the screen.
            Treat this the same as the ship getting hit.
            """

            for alien in self.aliens.sprites():
                if alien.rect.left < 0:
                    self._ship_hit()
                    break

        def _ship_hit(self):
            """Respond to an alien hitting the ship."""
            if self.stats.ships_left > 0:
                # Decrement ships left.
                self.stats.ships_left -= 1

                # Get rid of any remaining aliens and bullets.
                self.aliens.empty()
                self.bullets.empty()

                # Center the ship.
                self.ship.center_ship()
            else:
                self.stats.game_active = False

        def _update_screen(self):
            """Update images on the screen, and flip to the new screen."""
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()

            self.aliens.draw(self.screen)

            pygame.display.flip()

    if __name__ == '__main__':
        # Make a game instance, and run the game.
        ss_game = SidewaysShooter()
        ss_game.run_game()