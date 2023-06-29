class Settings():
    """Class to store the screen settings."""

    def __init__(self):
        """Initial static game settings."""
        # Screen Settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (0, 0, 230)

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (250, 250, 80)
        self.bullets_allowed = 3

        # Alien Settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.2

        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize synamic settings"""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # fleet_direction of 1 = right and -1 = left
        self.fleet_direction = 1


    def increase_speed(self):
        """Increase game speed"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale