import pygame
import random

from pygame._sdl2 import Window

from src.game.settings import (
	WIDTH,
	HEIGHT,
	WINDOW_TITLE,
	BACKGROUND_COLOR,
	FPS,
	PLAY_AREA_MARGIN
)

from src.game.stars import (
	create_stars,
	update_stars,
	draw_stars
)

from src.game.score import (
	create_score,
	add_score,
	draw_score
)

from src.game.display import update_display

from src.player.player import (
	create_player,
	move_player,
	draw_player,
	load_player_sprite,
	load_flame_sprites,
	update_player_animation,
	draw_player_flames
)

from src.projectiles.projectile import (
	create_projectile,
	move_projectile,
	draw_projectile
)

from src.enemies.enemy import (
	create_enemy,
	move_enemy,
	draw_enemy,
	check_projectile_collision
)


def run_game():

	# ==================================
	# CONFIGURACAO DA JANELA
	# ==================================

	screen = pygame.display.set_mode(
		(WIDTH, HEIGHT),
		pygame.RESIZABLE
	)

	pygame.display.set_caption(WINDOW_TITLE)
	window = Window.from_display_module()
	window.maximize()

	game_surface = pygame.Surface((WIDTH, HEIGHT))

	pygame.display.set_caption(WINDOW_TITLE)

	clock = pygame.time.Clock()

	# ==================================
	# CRIAR JOGADOR
	# ==================================

	player_sprite = load_player_sprite()
	flame_frames = load_flame_sprites()

	player = create_player(
		WIDTH,
		HEIGHT,
		player_sprite
	)

	# ==================================
	# CRIAR PROJETEIS
	# ==================================

	projectiles = []

	shoot_timer = 0
	SHOOT_INTERVAL = 0.35

	# ==================================
	# CONFIGURACAO DOS INIMIGOS
	# ==================================

	enemies = []

	ENEMY_LIMIT = 5

	ENEMY_MIN_SPAWN_INTERVAL = 1.0
	ENEMY_MAX_SPAWN_INTERVAL = 3.5

	enemy_spawn_timer = 0

	enemy_spawn_interval = random.uniform(
		ENEMY_MIN_SPAWN_INTERVAL,
		ENEMY_MAX_SPAWN_INTERVAL
	)

	# ==================================
	# CRIAR ESTRELAS
	# ==================================

	stars = create_stars()

	# ==================================
	# CRIAR PONTUACAO
	# ==================================

	score = create_score()

	score_font = pygame.font.Font(
		"assets/fonts/Oxanium.ttf",
		30
	)

	# ==================================
	# GAME LOOP
	# ==================================

	running = True

	while running:

		dt = clock.tick(FPS) / 1000

		# ----------------------------------
		# PROCESSAR EVENTOS
		# ----------------------------------

		events = pygame.event.get()
		event_index = 0

		while event_index < len(events):

			event = events[event_index]

			if event.type == pygame.QUIT:
				running = False

			event_index += 1

		if not running:
			break

		# ----------------------------------
		# LER TECLADO
		# ----------------------------------

		keys = pygame.key.get_pressed()

		move_player(
			player,
			keys,
			dt,
			WIDTH,
			HEIGHT,
			PLAY_AREA_MARGIN
		)

		# ----------------------------------
		# DISPARAR PROJETEIS
		# ----------------------------------

		shoot_timer += dt

		if shoot_timer >= SHOOT_INTERVAL:

			projectile = create_projectile(player)
			projectiles.append(projectile)

			shoot_timer = 0

		# ----------------------------------
		# MOVIMENTAR PROJETEIS
		# ----------------------------------

		index = 0

		while index < len(projectiles):

			move_projectile(projectiles[index], dt)

			if projectiles[index]["y"] + projectiles[index]["height"] / 2 < 0:
				projectiles.pop(index)

			else:
				index += 1

		# ----------------------------------
		# CRIAR INIMIGOS
		# ----------------------------------

		enemy_spawn_timer += dt

		if enemy_spawn_timer >= enemy_spawn_interval:

			if len(enemies) < ENEMY_LIMIT:

				enemy = create_enemy(WIDTH)

				enemy["x"] = random.randint(80, WIDTH - 80)
				enemy["y"] = -enemy["height"] / 2

				enemies.append(enemy)

			enemy_spawn_timer = 0

			enemy_spawn_interval = random.uniform(
				ENEMY_MIN_SPAWN_INTERVAL,
				ENEMY_MAX_SPAWN_INTERVAL
			)

		# ----------------------------------
		# MOVIMENTAR INIMIGOS
		# ----------------------------------

		index = 0

		while index < len(enemies):

			move_enemy(enemies[index], dt, WIDTH)

			index += 1

		# ----------------------------------
		# VERIFICAR COLISOES
		# ----------------------------------

		projectile_index = 0

		while projectile_index < len(projectiles):

			enemy_index = 0
			collision_detected = False

			while enemy_index < len(enemies):

				if check_projectile_collision(
					enemies[enemy_index],
					projectiles[projectile_index]
				):

					enemies.pop(enemy_index)
					projectiles.pop(projectile_index)

					score = add_score(score, 10)

					collision_detected = True
					break

				enemy_index += 1

			if not collision_detected:
				projectile_index += 1

		# ----------------------------------
		# ATUALIZAR ANIMACAO DO JOGADOR
		# ----------------------------------

		update_player_animation(player, dt)

		# ----------------------------------
		# ATUALIZAR ESTRELAS
		# ----------------------------------

		update_stars(stars, dt)

		# ==================================
		# DESENHAR ELEMENTOS
		# ==================================

		game_surface.fill(BACKGROUND_COLOR)

		draw_stars(game_surface, stars)

		# Desenhar projetis
		index = 0

		while index < len(projectiles):

			draw_projectile(
				game_surface,
				projectiles[index]
			)

			index += 1

		# Desenhar chamas
		draw_player_flames(
			game_surface,
			player,
			flame_frames
		)

		# Desenhar jogador
		draw_player(
			game_surface,
			player,
			player_sprite
		)

		# Desenhar inimigos
		index = 0

		while index < len(enemies):

			draw_enemy(
				game_surface,
				enemies[index]
			)

			index += 1

		# Desenhar pontuacao
		draw_score(
			game_surface,
			score,
			score_font
		)

		# ==================================
		# APRESENTAR JOGO
		# ==================================

		update_display(
			screen,
			game_surface
		)
