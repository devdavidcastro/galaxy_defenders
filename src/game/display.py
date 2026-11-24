import pygame

from src.game.settings import WIDTH, HEIGHT


def update_display(screen, game_surface):

	# Obter dimensoes da janela
	window_width, window_height = screen.get_size()

	# Calcular escala proporcional
	scale = min(
		window_width / WIDTH,
		window_height / HEIGHT
	)

	scaled_width = int(WIDTH * scale)
	scaled_height = int(HEIGHT * scale)

	# Redimensionar mundo do jogo
	scaled_surface = pygame.transform.scale(
		game_surface,
		(scaled_width, scaled_height)
	)

	# Centrar o jogo na janela
	offset_x = (window_width - scaled_width) // 2
	offset_y = (window_height - scaled_height) // 2

	# Limpar janela
	screen.fill((0, 0, 0))

	# Apresentar o jogo
	screen.blit(
		scaled_surface,
		(offset_x, offset_y)
	)

	pygame.display.flip()
