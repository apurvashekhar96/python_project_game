import pygame

from pygame.sprite import Sprite

class Ship(Sprite):
	"""A class to manage the ship."""

	def __init__(self, ai_game):
		"""Initilize the ship and set its starting position"""
		super().__init__()
		self.screen = ai_game.screen
		self.screen_rect = ai_game.screen.get_rect()
		self.settings = ai_game.settings

		#load the ship image and get its rect.
		self.ship_image = pygame.image.load('Images/alien_ship_image.bmp')
		self.image = self.ship_image #this line is needed bcz to draw the no of ships left DRAW func needs a attribute named image
		self.rect = self.ship_image.get_rect()

		#start each ship at bottom centre of screen
		self.rect.midbottom = self.screen_rect.midbottom

		#store a decimal value for ship's horizontal position
		self.x = float(self.rect.x)

		#right movement flag
		self.moving_right = False
		#left movemet flag
		self.moving_left = False

	def update(self):
		"""update ships position based on movement flags"""

		#right movement and limit it to edges(update the ship's x value not rect.x---to handle decimals)
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.x += self.settings.ship_speed

		#left movement and limit it to edges of the game screen(update yhe ships's x value not rect.x)
		if self.moving_left and self.rect.left > 0:
			self.x -= self.settings.ship_speed

		#update the actual rect.x based on value of x
		self.rect.x =self.x


	def blitme(self):
		"""Draw the ship at the current location"""
		self.screen.blit(self.ship_image, self.rect)

	def center_ship(self):
		"""center the ship on the screen"""
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)