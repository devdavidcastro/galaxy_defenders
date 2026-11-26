
import pygame
import random

from pygame._sdl2 import Window

from src.game.settings import (
	WIDTH,
	HEIGHT,
	WINDOW_TITLE,
	BACKGROUND_COLOR,
	FPS,
	PLAY_AREA_MARGIN,
)

from src.game.stars import (
	create_stars,
	update_stars,
	draw_stars,
)

from src.game.score import (
	create_score,
	add_score,
	draw_score,
	draw_lives,
)

from src.game.display import update_display

from src.player.player import (
	create_player,
	move_player,
	draw_player,
	load_player_sprite,
	load_flame_sprites,
	update_player_animation,
	draw_player_flames,
	check_player_collision,
	lose_player_life,
	update_player_invulnerability,
)

from src.projectiles.projectile import (
	create_projectile,
	move_projectile,
	draw_projectile,
	move_enemy_projectile,
	draw_enemy_projectile,
)

from src.enemies.enemy import (
	check_projectile_collision,
	get_enemy_spawn_interval
)

from src.game.high_scores import (
	load_high_scores,
	qualifies_for_high_scores,
	add_high_score,
)

from src.game.game_over import (
	draw_game_over_screen,
	load_game_over_image,
	create_game_over_image_rect,
	get_player_ranking_position
)

from src.game.enemy_manager import (
	load_enemy_frames,
	spawn_test_enemies,
	spawn_enemies,
	update_enemies,
	draw_enemies,
)

from src.game.sounds import (
	load_sounds,
	play_sound
)


# ========================================
# GAME CONFIGURATION
# ========================================

PLAYER_SHOOT_INTERVAL = 0.35
TEST_ALL_ENEMIES = False

START_SCREEN_PATH = "assets/images/start_screen.png"
START_SCREEN_WIDTH = 500


# ========================================
# ASSET LOADING
# ========================================

def load_start_screen():
	"""Load and scale the transparent start-screen overlay."""

	image = pygame.image.load(
		START_SCREEN_PATH
	).convert_alpha()

	image_height = int(
		image.get_height()
		* START_SCREEN_WIDTH
		/ image.get_width()
	)

	image = pygame.transform.smoothscale(
		image,
		(START_SCREEN_WIDTH, image_height),
	)

	return image


# ========================================
# PROJECTILE UPDATES
# ========================================

def update_player_projectiles(projectiles, dt):
	"""Move player projectiles and remove those above the screen."""

	index = 0

	while index < len(projectiles):
		projectile = projectiles[index]

		move_projectile(projectile, dt)

		if projectile["y"] + projectile["height"] / 2 < 0:
			projectiles.pop(index)
		else:
			index += 1


def update_enemy_projectiles(enemy_projectiles, dt):
	"""Move enemy projectiles and remove those outside the screen."""

	index = 0

	while index < len(enemy_projectiles):
		projectile = enemy_projectiles[index]

		move_enemy_projectile(projectile, dt)

		outside_left = (
			projectile["x"] + projectile["width"] / 2 < 0
		)
		outside_right = (
			projectile["x"] - projectile["width"] / 2 > WIDTH
		)
		outside_top = (
			projectile["y"] + projectile["height"] / 2 < 0
		)
		outside_bottom = (
			projectile["y"] - projectile["height"] / 2 > HEIGHT
		)

		if (
			outside_left
			or outside_right
			or outside_top
			or outside_bottom
		):
			enemy_projectiles.pop(index)
		else:
			index += 1


# ========================================
# COLLISION HANDLING
# ========================================

def handle_player_enemy_collisions(player, enemies):
	"""Handle direct collisions between the player and enemies."""

	index = 0

	while index < len(enemies):
		enemy = enemies[index]

		if not player["is_invulnerable"]:
			if check_player_collision(player, enemy):
				life_lost = lose_player_life(player)

				if life_lost:
					enemy["is_hit"] = True
					enemy["frame"] = 1
					enemy["animation_timer"] = 0

					if player["lives"] <= 0:
						return False

		index += 1

	return True


def handle_enemy_projectile_collisions(player, enemy_projectiles):
	"""Apply projectile damage and remove projectiles that hit the player."""

	index = 0

	while index < len(enemy_projectiles):
		projectile = enemy_projectiles[index]

		if check_player_collision(player, projectile):
			enemy_projectiles.pop(index)

			if not player["is_invulnerable"]:
				damage = 2 if projectile["type"] == "batedor" else 1
				lose_player_life(player, damage)

				if player["lives"] <= 0:
					return False
		else:
			index += 1

	return True


def handle_player_projectile_collisions(projectiles, enemies, score):
	"""Damage enemies and update the player's score."""

	projectile_index = 0

	while projectile_index < len(projectiles):
		enemy_index = 0
		collision_detected = False

		while enemy_index < len(enemies):
			enemy = enemies[enemy_index]

			if not enemy["is_destroyed"]:
				if check_projectile_collision(
					enemy,
					projectiles[projectile_index],
				):
					enemy["health"] -= 1
					projectiles.pop(projectile_index)

					if enemy["health"] <= 0:
						enemy["is_hit"] = True
						enemy["frame"] = 1
						enemy["animation_timer"] = 0
						score = add_score(score, 10)

					collision_detected = True
					break

			enemy_index += 1

		if not collision_detected:
			projectile_index += 1

	return score


# ========================================
# PROJECTILE DRAWING
# ========================================

def draw_projectiles(game_surface, projectiles, enemy_projectiles):
	"""Draw all player and enemy projectiles."""

	index = 0

	while index < len(projectiles):
		draw_projectile(game_surface, projectiles[index])
		index += 1

	index = 0

	while index < len(enemy_projectiles):
		draw_enemy_projectile(game_surface, enemy_projectiles[index])
		index += 1


# ========================================
# GAMEPLAY DRAWING
# ========================================

def draw_gameplay(
	game_surface,
	player,
	player_sprite,
	flame_frames,
	enemies,
	enemy_frames,
	projectiles,
	enemy_projectiles,
	score,
	score_font,
):
	"""Draw all active gameplay elements."""

	draw_projectiles(
		game_surface,
		projectiles,
		enemy_projectiles,
	)

	draw_player_flames(
		game_surface,
		player,
		flame_frames,
	)

	draw_player(
		game_surface,
		player,
		player_sprite,
	)

	draw_enemies(
		game_surface,
		enemies,
		enemy_frames,
	)

	draw_score(
		game_surface,
		score,
		score_font,
	)

	draw_lives(
		game_surface,
		player,
		score_font,
	)


# ========================================
# MAIN GAME
# ========================================

def run_game():
	"""Initialize and run the main game loop."""

	restart_game = False
	game_over = False
	name_entry_active = False
	player_name = ""
	player_ranking_position = None

	high_scores = load_high_scores()
	sounds = load_sounds()
	# Initialize the display.
	screen = pygame.display.get_surface()

	if screen is None:
		screen = pygame.display.set_mode(
			(WIDTH, HEIGHT),
			pygame.RESIZABLE,
		)

		pygame.display.set_caption(WINDOW_TITLE)

		window = Window.from_display_module()
		window.maximize()

	game_surface = pygame.Surface((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	# Load player assets and create the player.
	player_sprite = load_player_sprite()
	flame_frames = load_flame_sprites()

	player = create_player(
		WIDTH,
		HEIGHT,
		player_sprite,
	)

	# Initialize projectiles.
	projectiles = []
	enemy_projectiles = []
	shoot_timer = 0

	# Initialize score and font.
	score = create_score()
	score_font = pygame.font.Font(
		"assets/fonts/Oxanium.ttf",
		20,
	)

	# Load enemy assets.
	enemy_frames = load_enemy_frames()
	enemies = []

	# Initialize enemy spawning.
	min_interval, max_interval = get_enemy_spawn_interval(score)

	spawn_state = {
		"timer": 0,
		"interval": random.uniform(min_interval, max_interval),
	}

	# Initialize the background and start screen.
	stars = create_stars()

	start_screen = load_start_screen()
	start_screen_rect = start_screen.get_rect(
		center=(WIDTH // 2, HEIGHT // 2)
	)

	# Load the Game Over screen.
	game_over_image = load_game_over_image()

	game_over_image_rect = create_game_over_image_rect(
		game_over_image
	)

	game_started = False
	running = True

	# Main game loop.
	while running:

		# Check whether the player has lost all lives.
		if player["lives"] <= 0 and not game_over:
			game_over = True

			if qualifies_for_high_scores(high_scores, score):
				name_entry_active = True

				player_ranking_position = get_player_ranking_position(
				high_scores,
				score,
				)

		dt = clock.tick(FPS) / 1000


		# Process window events.
		events = pygame.event.get()
		event_index = 0

		while event_index < len(events):
			event = events[event_index]

			if event.type == pygame.QUIT:
				running = False

			elif event.type == pygame.KEYDOWN:

				# GAME OVER CONTROLS
				if game_over and not name_entry_active:

					if event.key == pygame.K_ESCAPE:
						running = False

					elif event.key == pygame.K_SPACE:
						running = False
						restart_game = True

				# PLAYER NAME ENTRY
				elif name_entry_active:

					if event.key == pygame.K_BACKSPACE:
						player_name = player_name[:-1]

					elif event.key == pygame.K_RETURN:
						if player_name.strip():
							high_scores = add_high_score(
								high_scores,
								player_name.strip(),
								score,
							)

							name_entry_active = False

					elif (
						len(player_name) < 10
						and event.unicode.isprintable()
					):
						player_name += event.unicode

				# START GAME
				elif event.key == pygame.K_SPACE and not game_started:
					game_started = True

			event_index += 1

		if restart_game:
			return True


		if not running:
			break

		# Keep the starfield moving in all game states.
		update_stars(stars, dt)

		# Update gameplay while the game is active.
		if game_started and not game_over:

			# Read input and move the player.
			keys = pygame.key.get_pressed()

			move_player(
				player,
				keys,
				dt,
				WIDTH,
				HEIGHT,
				PLAY_AREA_MARGIN,
			)

			# Fire player projectiles.
			shoot_timer += dt

			if shoot_timer >= PLAYER_SHOOT_INTERVAL:
				projectiles.append(
					create_projectile(player)
				)

				play_sound(sounds, "player_shot")

				shoot_timer = 0

			# Update projectiles.
			update_player_projectiles(
				projectiles,
				dt,
			)

			update_enemy_projectiles(
				enemy_projectiles,
				dt,
			)

			# Spawn and update enemies.
			if TEST_ALL_ENEMIES:
				spawn_test_enemies(enemies)
			else:
				spawn_enemies(
					enemies,
					score,
					dt,
					spawn_state,
				)

			update_enemies(
				enemies,
				enemy_projectiles,
				dt,
			)

			# Handle collisions.
			handle_player_enemy_collisions(
				player,
				enemies,
			)

			if player["lives"] > 0:
				handle_enemy_projectile_collisions(
					player,
					enemy_projectiles,
				)

			if player["lives"] > 0:
				score = handle_player_projectile_collisions(
					projectiles,
					enemies,
					score,
				)

			# Update player effects.
			update_player_animation(player, dt)
			update_player_invulnerability(player, dt)

		# Draw the background.
		game_surface.fill(BACKGROUND_COLOR)
		draw_stars(game_surface, stars)

		# Draw the start screen or active gameplay.
		if game_started:
			draw_gameplay(
				game_surface,
				player,
				player_sprite,
				flame_frames,
				enemies,
				enemy_frames,
				projectiles,
				enemy_projectiles,
				score,
				score_font,
			)
		else:
			game_surface.blit(
				start_screen,
				start_screen_rect,
			)

		# Draw the Game Over screen above the gameplay.
		if game_over:
			draw_game_over_screen(
				game_surface,
				game_over_image,
				game_over_image_rect,
				high_scores,
				score_font,
				name_entry_active,
				player_name,
				score,
				player_ranking_position,
			)

		# Update the window display.
		update_display(
			screen,
			game_surface,
		)
