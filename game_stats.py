
class GameStats:
	"""Tracks Statistics for alien Invasion"""

	def __init__(self, ai_game):
		"""Initialize game statistics"""
		self.settings = ai_game.settings
		self.reset_stats()
		self.game_active_flag = False

		#high score ahould never be reset
		self.high_score = 0

	def reset_stats(self):
		"""initialize statustics that can change during the game"""
		self.ships_left = self.settings.ship_limit
		self.score = 0
		self.level = 1