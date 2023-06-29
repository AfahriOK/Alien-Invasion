import pygame


class Ship():

    def __init__(self, game_settings, screen):
        """Initialize the ship and starting position"""
        self.screen = screen
        self.game_settings = game_settings

        # Load the ship image and its rectangle
        self.image = pygame.image.load('images/spacecraft.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()


        # Start ship at bottom center of screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Decimal value for ships center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update ships position based on movement flag"""
        # Update the ships center value, not rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.game_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.game_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)


    def center_ship(self):
        """Center the ship on screen"""
        self.center = self.screen_rect.centerx