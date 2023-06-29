import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """Class to manage ship bullets"""

    def __init__(self, game_settings, screen, ship):
        """Create bullets from ships position"""
        super(Bullet, self).__init__()
        self.screen = screen

        # Create a bullet and set the position
        self.rect = pygame.Rect(0, 0, game_settings.bullet_width, game_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Bullets position as decimal value
        self.y = float(self.rect.y)

        self.color = game_settings.bullet_color
        self.speed_factor = game_settings.bullet_speed_factor

    def update(self):
        """Bullet movement"""
        # Update decimal position
        self.y -= self.speed_factor
        # Update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
