import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def update_bullets(game_settings, screen, ship, aliens, bullets):
    """Update bullet positions and delete old bullets"""
    bullets.update()

    # Delete bullets not on screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets)


def ship_hit(game_settings, stats, screen, ship, aliens, bullets):
    """Respond to ship collisions"""
    if stats.ships_left > 0:
        # Lower ship  lives
        stats.ships_left -= 1

        # Clear aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_bullet_alien_collisions(game_settings, screen, ship, aliens, bullets):
    """Respond to bullet-alien collisions"""
    # Check if bullet has hit an alien
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        # Destroy bullets, increase speed, and create new fleet
        bullets.empty()
        game_settings.increase_speed()
        create_fleet(game_settings, screen, ship, aliens)


def check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets):
    """Check if aliens have passed the ship"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Same as if ship hit
            ship_hit(game_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(game_settings, stats, screen, ship, aliens, bullets):
    """Check if at edge and update position of all aliens"""
    check_fleet_edges(game_settings, aliens)
    aliens.update()

    # Check for alien-ship collision
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(game_settings, stats, screen, ship, aliens, bullets)

    # Check for aliens at bottom of screen
    check_aliens_bottom(game_settings, stats, screen, ship, aliens, bullets)


def fire_bullet(game_settings, screen, ship, bullets):
    """Fire a bullet if within limits"""
    # Create new bullet in group
    if len(bullets) < game_settings.bullets_allowed:
        new_bullet = Bullet(game_settings, screen, ship)
        bullets.add(new_bullet)


def check_keydown_events(event, game_settings, screen, ship, bullets):
    """Respond to keypress"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE:
        sys.exit()


def check_keyup_events(event, ship):
    """Respond to key releases"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(game_settings, screen, stats, play_button, ship, aliens, bullets):
    """Respond to keypress\' and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, game_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(game_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(game_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """Start game when player clicks play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        game_settings.initialize_dynamic_settings()

        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game stats
        stats.reset_stats()
        stats.game_active = True

        # Empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center the ship
        create_fleet(game_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(game_settings, screen, stats, ship, aliens, bullets, play_button):
    """Update images and render new screen"""
    # Redraw screen during each pass of loop
    screen.fill(game_settings.bg_color)

    # Redraw all bullets behind ship and aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # Draw play button if game inactive
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recent screen visible
    pygame.display.flip()


def get_number_aliens_x(game_settings, alien_width):
    """Determine how many aliens fit in a row"""
    available_space_x = game_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(game_settings, ship_height, alien_height):
    """Determine amount of rows that fit screen"""
    available_space_y = (game_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(game_settings, screen, aliens, alien_number, row_number):
    """Create and place an alien in row"""
    alien = Alien(game_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(game_settings, screen, ship, aliens):
    """Create a fleet of aliens"""
    # Create an alien and fine number of aliens in row. Spacing is one alien width
    alien = Alien(game_settings, screen)
    number_aliens_x = get_number_aliens_x(game_settings, alien.rect.width)
    number_rows = get_number_rows(game_settings, ship.rect.height, alien.rect.height)

    # Create first row of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(game_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(game_settings, aliens):
    """Respond if aliens at edge of screen"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(game_settings, aliens)
            break


def change_fleet_direction(game_settings, aliens):
    """Drop the fleet down and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += game_settings.fleet_drop_speed
    game_settings.fleet_direction *= -1
