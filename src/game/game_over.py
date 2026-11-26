import pygame

from src.game.settings import WIDTH, HEIGHT

GAME_OVER_IMAGE_PATH = "assets/images/game_over.png"
GAME_OVER_IMAGE_WIDTH = 500

def draw_game_over_overlay(game_surface):

	overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	overlay.fill((0, 0, 0, 110))
	game_surface.blit(overlay, (0, 0))

def load_game_over_image():

	image = pygame.image.load(
		GAME_OVER_IMAGE_PATH
	).convert_alpha()
	image_height = int(
		image.get_height()
		* GAME_OVER_IMAGE_WIDTH
		/ image.get_width()
	)
	image = pygame.transform.smoothscale(
		image,
		(GAME_OVER_IMAGE_WIDTH, image_height),
	)
	return image

def draw_game_over_screen(game_surface, game_over_image, game_over_image_rect):
	draw_game_over_overlay(game_surface)

	game_surface.blit(
		game_over_image,
		game_over_image_rect
	)

def create_game_over_image_rect(game_over_image):
	return game_over_image.get_rect(
		midtop=(WIDTH // 2, 45)
	)
