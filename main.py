import pygame
import random
from src.player.player import create_player, move_player, draw_player, update_player_animation

# inicializacao do pygame
pygame.init()

# config da janela
WIDTH = 1280
HEIGHT = 720
screen = pygame.display.set_mode(
	(WIDTH, HEIGHT),
	pygame.RESIZABLE
	)
game_surface = pygame.Surface((WIDTH, HEIGHT))

pygame.display.set_caption("GALAXY DEFENDERS")
BACKGROUND_COLOR = (8, 12, 30)
clock = pygame.time.Clock()

# configuracao da area de jogo
PLAY_AREA_MARGIN = 40

# criacao das estrelas
stars = []

# camada 1: distante
counter = 0
while counter < 40:
	star = {
		"x": random.randint(0, WIDTH),
		"y": random.randint(0, HEIGHT),
		"speed": random.uniform(30, 60),
		"size": 1,
		"color": (90, 110, 160)
	}
	stars.append(star)
	counter += 1

# camada 2: intermedio
counter = 0
while counter < 25:
	star = {
		"x": random.randint(0, WIDTH),
		"y": random.randint(0, HEIGHT),
		"speed": random.uniform(90, 150),
		"size": 2,
		"color": (150, 180, 230)
	}
	stars.append(star)
	counter += 1

# camada 3: proximo
counter = 0
while counter < 15:
	star = {
		"x": random.randint(0, WIDTH),
		"y": random.randint(0, HEIGHT),
		"speed": random.uniform(180, 240),
		"size": 3,
		"color": (210, 230, 255)
	}
	stars.append(star)
	counter += 1

# criar jogador
player = create_player(WIDTH, HEIGHT)

# game loop
running = True

while running:

		# Calcular o tempo decorrido
		dt = clock.tick(60) / 1000

		# Processar eventos
		event_index = 0
		events = pygame.event.get()
		while event_index < len(events):
			event = events[event_index]
			if event.type == pygame.QUIT:
				running = False
			event_index += 1

		# Ler o teclado
		keys = pygame.key.get_pressed()

		# movimentar o jogador
		move_player(
			player,
			keys,
			dt,
			WIDTH,
			HEIGHT,
			PLAY_AREA_MARGIN
		)
		update_player_animation(player, keys, dt)

		# Limpar o ecrã
		game_surface.fill(BACKGROUND_COLOR)

		# Atualizar e desenhar estrelas
		index = 0
		while index < len(stars):

			star = stars[index]
			star["y"] += star["speed"] * dt

			if star["y"] > HEIGHT:
				star["y"] = 0
				star["x"] = random.randint(0, WIDTH)

			pygame.draw.circle(
				game_surface,
				star["color"],
				(int(star["x"]), int(star["y"])),
				star["size"]
			)
			index += 1

		# Desenho da nave
		draw_player(game_surface, player)

		# Atualizar o ecrã
		# Obter as dimensoes atuais da janela
		window_width, window_height = screen.get_size()

		# Calcular a escala proporcional
		scale = min(
			window_width / WIDTH,
			window_height / HEIGHT
		)

		# Calcular as novas dimensoes
		scaled_width = int(WIDTH * scale)
		scaled_height = int(HEIGHT * scale)

		# Redimensionar o mundo do jogo
		scaled_surface = pygame.transform.scale(
			game_surface,
			(scaled_width, scaled_height)
		)

		# Calcular a posicao para centrar a imagem
		offset_x = (window_width - scaled_width) // 2
		offset_y = (window_height - scaled_height) // 2

		# Limpar a janela
		screen.fill((0, 0, 0))

		# Apresentar o jogo centrado
		screen.blit(
			scaled_surface,
			(offset_x, offset_y)
		)

		pygame.display.flip()

# encerrar o pygame
pygame.quit()
