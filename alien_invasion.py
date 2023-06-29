import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from button import Button

def run_game():
    # Initialize pygame, settings, and screen object.
    pygame.init()
    game_settings = Settings()
    screen = pygame.display.set_mode((game_settings.screen_width, game_settings.screen_height))
    pygame.display.set_caption("Afahri's Alien Invasion")

    # Make the play button
    play_button = Button(game_settings, screen, "Play")
    # Instance to store game stats
    stats = GameStats(game_settings)

    # Make a ship, group of bullets, and group of aliens
    ship = Ship(game_settings, screen)
    bullets = Group()
    aliens = Group()

    # Create Fleet of aliens
    gf.create_fleet(game_settings, screen, ship, aliens)

    # Main loop for game
    while True:
        gf.check_events(game_settings, screen, stats, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(game_settings, screen, ship, aliens, bullets)
            gf.update_aliens(game_settings, stats, screen, ship, aliens, bullets)

        gf.update_screen(game_settings, screen, stats, ship, aliens, bullets, play_button)


run_game()
