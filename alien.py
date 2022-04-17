

import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""A class to represent a single alien in the fleet"""

	def __init__(self, ai_game):
		"""Initialize the alien and it's starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings

		#load the alien image and set it's rect attribute
		self.image = pygame.image.load('Images/alien_image.bmp')
		self.rect = self.image.get_rect()

		#start each new alien at the top left corner
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#store the alien's exact horizontal position
		self.x = float(self.rect.x)


	def update(self):
		"""Move the alien to the left or right depending on fleet direction flag"""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		"""returns true if the alien is at any edge of the screen"""
		screen_rect = self.screen.get_rect()

		if self.rect.right >= screen_rect.right or self.rect.left <= 0:
			return True