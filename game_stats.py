class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = 0
        self.level = 1
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score = 0