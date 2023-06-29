import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class to represent aliens"""

    def __init__(self, game_settings, screen):
        """Initialize alien and start position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.game_settings = game_settings

        # Load the image and set its rect
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Set alien at top of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # aliens exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw alien"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move alien to the right or left"""
        self.x += (self.game_settings.alien_speed_factor * self.game_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return True if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True