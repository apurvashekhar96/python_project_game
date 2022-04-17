import sys

from time import sleep

import pygame

from settings import Settings

from button import Button

from ship import Ship

from bullets import Bullets

from alien import Alien

from game_stats import GameStats

from scoreboard import Scoreboard

class AlienInvasion:
	"""Overall class to manage game assets and bahviour"""

	def __init__(self):
		"""Initialise the game and create game resources"""

		#initialize pygame
		pygame.init()
         
         #initialize an instance of settings class
		self.settings = Settings()
         
         #initialize an attribute screen 
		self.screen = pygame.display.set_mode((0, 0), self.settings.flags)
		self.settings.screen_width = self.screen.get_rect().width
		self.settings.screen_height = self.screen.get_rect().height
		pygame.display.set_caption("Alien Invasion")

		#cretae an instance to store game statistics
		#and also create a game scoreboard
		self.stats = GameStats(self)
		self.sb = Scoreboard(self)

		#call ship module and initialize it
		self.ship = Ship(self)

		#create the bullet group using sprite
		self.bullets = pygame.sprite.Group()

		#create alien group using sprite
		self.aliens = pygame.sprite.Group()
		self._create_fleet()

		#make the play button
		self.play_button = Button(self, "PLAY")


	def run_game(self):
		"""Start the main loop for the game"""
		while True:
			#call helper method _check_events.
			self._check_events()


			if self.stats.game_active_flag:
				#move the ship to the right
				self.ship.update()

				#update bullets
				self._update_bullets()

				#update aliens
				self._update_aliens()

			#call helper module _update_screen
			self._update_screen()
			
			



            

	def _check_events(self):
		"""check and respond to mouse and keyboard movements"""
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()

			elif event.type == pygame.KEYDOWN:
				self._check_keydown_events(event)
				
			elif event.type == pygame.KEYUP:
				self._check_keyrelease_events(event)

			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = pygame.mouse.get_pos()
				self._check_play_button(mouse_pos)


	def _check_play_button(self, mouse_pos):
		"""start a new game when the player clicks play"""
		button_clicked = self.play_button.rect.collidepoint(mouse_pos)
		if button_clicked and not self.stats.game_active_flag:
			#reset the game statistics
			self.stats.reset_stats()
			self.stats.game_active_flag = True
			self.sb.prep_score()
			self.sb.prep_level()
			self.sb.prep_ships()

			#get rid of any remainig aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and center the ship
			self._create_fleet()
			self.ship.center_ship()

			#reset the game settings to initail speedds
			self.settings.initialize_dynamic_settings()

			#hide the mouse cursor
			pygame.mouse.set_visible(False)
				

	def _check_keydown_events(self, event):
		"""check for key down presses"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = True
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = True

		#check for spacebar for bullet firing
		elif event.key == pygame.K_SPACE:
			self._fire_bullet()


		# press q to quit the game
		elif event.key == pygame.K_q:
			sys.exit()


	def _check_keyrelease_events(self, event):
		"""check for key releases"""
		if event.key == pygame.K_RIGHT:
			self.ship.moving_right = False
		elif event.key == pygame.K_LEFT:
			self.ship.moving_left = False


	def _fire_bullet(self):
		"""create a new bullet and add it to bullet group"""
		if len(self.bullets) < self.settings.bullets_allowed:
			self.new_bullet = Bullets(self)
			self.bullets.add(self.new_bullet)

	def _update_bullets(self):
		"""update position of new bullets and get rid of old bullets"""
		#update bullet position
		self.bullets.update()
		#get rid of old bullets
		for bullet in self.bullets.copy():
			if bullet.rect.bottom <= 0:
				self.bullets.remove(bullet)

		self._check_bullet_alien_collisions()



	def _check_bullet_alien_collisions(self):
		#check for any bullets that have hit aliens.
		#if yes, delete the bullet and the alien.

		collisions = pygame.sprite.groupcollide(
			self.bullets, self.aliens, True, True)

		if collisions:
			for aliens in collisions.values():
				self.stats.score += self.settings.alien_points
			self.sb.prep_score()
			self.sb.check_high_score()

		#add new fleet if all aliens destroyed
		if not self.aliens:
			#destroy existing bullets and create new fleet.
			self.bullets.empty()
			self._create_fleet()
			#increase the game's tempo. 
			self.settings.increase_speed()

			#increase game level
			self.stats.level += 1
			self.sb.prep_level()


	def _update_aliens(self):
		"""check if any alien is at the edge of the screen,
		 then update the position of all aliens in the fleet"""
		self._check_fleet_edges()
		self.aliens.update()

		#look for alien ship collison.
		if pygame.sprite.spritecollideany(self.ship, self.aliens):
			self._ship_hit()

		#look if any alien reached bottom of the screen
		self._check_aliens_reaching_bottom()


	def _create_fleet(self):
		"""Create the fleet of aliens"""

		#make an alien. find the no of aliens in a row
		#space between each alien is one alien_width
		alien = Alien(self)
		alien_width, alien_height = alien.rect.size
		available_space_x = self.settings.screen_width - (2 * alien_width)
		number_aliens_x = (available_space_x // (2 * alien_width)) 
		#the extra space appearing on the rightmost will be used to move the aliens to the right.

		#determine the number of rows of aliens
		ship_height = self.ship.rect.height
		available_space_y = (self.settings.screen_height - (3 *  alien_height) - ship_height)
		number_rows = available_space_y // (2 * alien_height)

		#create full fleet of aliens.
		for row_number in range(number_rows):
			for alien_number in range(number_aliens_x):
				self._create_alien(alien_number, row_number)



	def _create_alien(self, alien_number, row_number):
			#create an alien an place it in the row.
			alien = Alien(self)
			alien_width, alien_height = alien.rect.size
			alien.x = alien_width + (2 * alien_width * alien_number)
			alien.rect.x = alien.x
			alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
			self.aliens.add(alien)


	def _check_fleet_edges(self):
		"""respond if alien reaches an edge"""
		for alien in self.aliens.sprites():
			if alien.check_edges():
				self._change_fleet_direction()
				break

	def _change_fleet_direction(self):
		"""drop the entire fleet and change direction of fleet"""
		for alien in self.aliens.sprites():
			alien.rect.y += self.settings.alien_drop_speed
		self.settings.fleet_direction *= -1
					


	def _update_screen(self):
		"""Update images on the screen and flip the screen"""

		#redraw the screen during each pass through the loop.
		self.screen.fill(self.settings.bg_color)
		self.ship.blitme()

		#draw the bullets
		for bullet in self.bullets.sprites():
			bullet.draw_bullet()

		#draw the aliens
		self.aliens.draw(self.screen)

		#draw the score info
		self.sb.show_score()

		#Draw the play button if the game is inactive
		if not self.stats.game_active_flag:
			self.play_button.draw_button()

		#Make the most recently drawn screen visible.
		pygame.display.flip()

		


	def _ship_hit(self):
		"""respond to ship being hit by an alien"""
		if self.stats.ships_left > 0:

			#Decrement ships_left and update scoreboard for no of ships left
			self.stats.ships_left -= 1
			self.sb.prep_ships()

			#get rid of all remaining aliens and bullets
			self.aliens.empty()
			self.bullets.empty()

			#create a new fleet and centre the ship
			self._create_fleet()
			self.ship.center_ship()

			#pause for a while
			sleep(1.0)
		else:
			self.stats.game_active_flag = False
			pygame.mouse.set_visible(True)

	def _check_aliens_reaching_bottom(self):
		"""check if any alien reachd to the bottom of the screen"""
		screen_rect = self.screen.get_rect()
		for alien in self.aliens.sprites():
			if alien.rect.bottom >= screen_rect.bottom:
				#treat it the same as ship hit
				self._ship_hit()
				break

if __name__ == '__main__':
	#make a game instance and run the game.
	ai = AlienInvasion()
	ai.run_game()