class Settings:
    """A class to store all settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings"""
        self.screen_width = 1000
        self.screen_height = 600
        self.bg_color = (255, 255, 255)

        self.ship_speed = 2
        self.ship_limit = 3

        self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 5

        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
