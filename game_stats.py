class GameStats():
    """Track statistics"""
    def __init__(self, game_settings):
        """Initialize stats"""
        self.game_settings = game_settings
        self.reset_stats()
        self.game_active = False


    def reset_stats(self):
        """Initialize stats that can be changed"""
        self.ships_left = self.game_settings.ship_limit