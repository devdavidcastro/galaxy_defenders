
import pygame
import random

from src.player.player import (
	create_player,
	move_player,
	draw_player,
	load_player_sprite,
	load_flame_sprites,
	update_player_animation,
	draw_player_flames,
	)

from src.projectiles.projectile import (
	create_projectile,
	move_projectile,
	draw_projectile
)

# ==================================
# INICIALIZACAO DO PYGAME
# ==================================

pygame.init()


# ==================================
# CONFIGURACAO DA JANELA
# ==================================

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
FPS = 60


# ==================================
# CONFIGURACAO DA AREA DE JOGO
# ==================================

PLAY_AREA_MARGIN = 40


# ==================================
# CARREGAR IMAGEM DA NAVE
# ==================================


player_sprite = load_player_sprite()
#player_front = create_player_front(player_sprite)
flame_frames = load_flame_sprites()


# ==================================
# CRIAR JOGADOR
# ==================================

player = create_player(
	WIDTH,
	HEIGHT,
	player_sprite
	)
projectiles = []
shoot_timer = 0
SHOOT_INTERVAL = 0.35

# ==================================
# CRIAR ESTRELAS
# ==================================

stars = []

# Camada 1: distante
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


# Camada 2: intermédia
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


# Camada 3: próxima
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


# ==================================
# GAME LOOP
# ==================================

running = True

while running:

	# Calcular o tempo decorrido
	dt = clock.tick(FPS) / 1000

	# Temporizador dos disparos
	shoot_timer += dt

	if shoot_timer >= SHOOT_INTERVAL:
		projectile = create_projectile(player)
		projectiles.append(projectile)
		shoot_timer = 0

	# Movimentar e remover projéteis
	index = 0

	while index < len(projectiles):
		move_projectile(projectiles[index], dt)
		if projectiles[index]["y"] + projectiles[index]["height"] / 2 < 0:
			projectiles.pop(index)
		else:
			index += 1

	# Processar eventos
	events = pygame.event.get()
	event_index = 0

	while event_index < len(events):

		event = events[event_index]

		if event.type == pygame.QUIT:
			running = False

		event_index += 1

	# Ler o teclado
	keys = pygame.key.get_pressed()

	# Movimentar jogador
	move_player(
		player,
		keys,
		dt,
		WIDTH,
		HEIGHT,
		PLAY_AREA_MARGIN
	)

	update_player_animation(player, dt)

	# Limpar a superfície do jogo
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

	# Desenhar projetil
	index = 0
	while index < len(projectiles):
		draw_projectile(game_surface, projectiles[index])
		index += 1

	# Desenhar chamas
	draw_player_flames(
		game_surface,
		player,
		flame_frames
	)

	# Desenhar nave por cima das chamas
	draw_player(
		game_surface,
		player,
		player_sprite
	)

# ==================================
# REDIMENSIONAR A JANELA
# ==================================

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


# ==================================
# ENCERRAR PYGAME
# ==================================

pygame.quit()
