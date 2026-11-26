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
from src.game.stars import create_stars, update_stars, draw_stars
from src.game.score import create_score, add_score, draw_score, draw_lives
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
	create_enemy_projectile,
	move_enemy_projectile,
	draw_enemy_projectile,
	create_orbital_projectiles,
)
from src.enemies.enemy import (
	create_enemy,
	move_enemy,
	draw_enemy,
	check_projectile_collision,
	load_enemy_sprite_sheet,
	update_enemy_animation,
	get_unlocked_enemy_types,
	get_enemy_spawn_interval,
	get_enemy_limit,
)


# ========================================
# GAME CONFIGURATION
# ========================================

PLAYER_SHOOT_INTERVAL = 0.35
TEST_ALL_ENEMIES = False

TEST_ENEMY_TYPES = [
	"drone",
	"escaravelho",
	"nave_pesada",
	"orbital",
	"criatura",
	"batedor",
]

START_SCREEN_PATH = "assets/images/start_screen.png"
START_SCREEN_WIDTH = 500


# ========================================
# ASSET LOADING
# ========================================

def load_enemy_frames():
	"""Load the animation frames for every enemy type."""

	enemy_types = [
		"drone",
		"escaravelho",
		"nave_pesada",
		"orbital",
		"criatura",
		"batedor",
	]

	enemy_frames = {}
	index = 0

	while index < len(enemy_types):
		enemy_type = enemy_types[index]
		enemy_frames[enemy_type] = load_enemy_sprite_sheet(enemy_type)
		index += 1

	return enemy_frames


def load_start_screen():
	"""Load and scale the transparent start-screen overlay."""

	image = pygame.image.load(START_SCREEN_PATH).convert_alpha()

	image_height = int(
		image.get_height() * START_SCREEN_WIDTH / image.get_width()
	)

	image = pygame.transform.smoothscale(
		image,
		(START_SCREEN_WIDTH, image_height),
	)

	return image


# ========================================
# ENEMY SPAWNING
# ========================================

def spawn_test_enemies(enemies):
	"""Spawn one instance of each enemy type for testing."""

	if len(enemies) != 0:
		return

	index = 0

	while index < len(TEST_ENEMY_TYPES):
		enemy_type = TEST_ENEMY_TYPES[index]
		enemy = create_enemy(WIDTH, HEIGHT, enemy_type)

		enemy["x"] = 110 + index * 210
		enemy["y"] = 130

		enemies.append(enemy)
		index += 1



def spawn_enemies(enemies, score, dt, spawn_state):
	"""Spawn enemies according to the current score and difficulty."""

	spawn_state["timer"] += dt

	if spawn_state["timer"] < spawn_state["interval"]:
		return

	if len(enemies) < get_enemy_limit(score):
		unlocked_enemy_types = get_unlocked_enemy_types(score)
		enemy_type = random.choice(unlocked_enemy_types)

		enemy = create_enemy(WIDTH, HEIGHT, enemy_type)
		enemy["x"] = random.randint(80, WIDTH - 80)
		enemy["y"] = -enemy["height"] / 2

		enemies.append(enemy)

	spawn_state["timer"] = 0

	min_interval, max_interval = get_enemy_spawn_interval(score)
	spawn_state["interval"] = random.uniform(min_interval, max_interval)


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

		outside_left = projectile["x"] + projectile["width"] / 2 < 0
		outside_right = projectile["x"] - projectile["width"] / 2 > WIDTH
		outside_top = projectile["y"] + projectile["height"] / 2 < 0
		outside_bottom = projectile["y"] - projectile["height"] / 2 > HEIGHT

		if outside_left or outside_right or outside_top or outside_bottom:
			enemy_projectiles.pop(index)
		else:
			index += 1


# ========================================
# ENEMY SHOOTING
# ========================================

def fire_orbital_burst(enemy, enemy_projectiles):
	"""Add the Orbital's eight-projectile radial attack."""

	projectiles = create_orbital_projectiles(enemy)
	index = 0

	while index < len(projectiles):
		enemy_projectiles.append(projectiles[index])
		index += 1


def update_enemy_shooting(enemy, enemy_projectiles, dt):
	"""Update an enemy's shooting behavior."""

	if not enemy["can_shoot"] or enemy["is_hit"]:
		return

	enemy["shoot_timer"] += dt

	# The Creature fires three consecutive projectiles.
	if enemy["type"] == "criatura" and enemy["burst_shots_remaining"] > 0:
		enemy["burst_shot_timer"] += dt

		if enemy["burst_shot_timer"] >= enemy["burst_shot_interval"]:
			enemy_projectiles.append(create_enemy_projectile(enemy))
			enemy["burst_shots_remaining"] -= 1
			enemy["burst_shot_timer"] = 0

		return

	if enemy["shoot_timer"] < enemy["shoot_interval"]:
		return

	if enemy["type"] == "orbital":
		fire_orbital_burst(enemy, enemy_projectiles)

	elif enemy["type"] == "criatura":
		enemy_projectiles.append(create_enemy_projectile(enemy))
		enemy["burst_shots_remaining"] = 2
		enemy["burst_shot_timer"] = 0

	else:
		# The Heavy Ship and Scout fire one projectile per attack.
		enemy_projectiles.append(create_enemy_projectile(enemy))

	enemy["shoot_timer"] = 0


# ========================================
# ENEMY UPDATES
# ========================================

def update_enemies(enemies, enemy_projectiles, dt):
	"""Move enemies, update animations and process their attacks."""

	index = 0

	while index < len(enemies):
		enemy = enemies[index]

		move_enemy(enemy, dt, WIDTH, HEIGHT)
		update_enemy_animation(enemy, dt)

		if enemy["is_destroyed"]:
			enemies.pop(index)
		else:
			update_enemy_shooting(enemy, enemy_projectiles, dt)
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
# DRAWING
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


def draw_enemies(game_surface, enemies, enemy_frames):
	"""Draw all active enemies."""

	index = 0

	while index < len(enemies):
		draw_enemy(game_surface, enemies[index], enemy_frames)
		index += 1


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
	"""Draw the active gameplay elements."""

	draw_projectiles(game_surface, projectiles, enemy_projectiles)
	draw_player_flames(game_surface, player, flame_frames)
	draw_player(game_surface, player, player_sprite)
	draw_enemies(game_surface, enemies, enemy_frames)
	draw_score(game_surface, score, score_font)
	draw_lives(game_surface, player, score_font)


# ========================================
# MAIN GAME
# ========================================

def run_game():
	# Initialize the display.
	screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
	pygame.display.set_caption(WINDOW_TITLE)

	window = Window.from_display_module()
	window.maximize()

	game_surface = pygame.Surface((WIDTH, HEIGHT))
	clock = pygame.time.Clock()

	# Load player assets and create the player.
	player_sprite = load_player_sprite()
	flame_frames = load_flame_sprites()
	player = create_player(WIDTH, HEIGHT, player_sprite)

	# Initialize projectiles.
	projectiles = []
	enemy_projectiles = []
	shoot_timer = 0

	# Initialize score and font.
	score = create_score()
	score_font = pygame.font.Font("assets/fonts/Oxanium.ttf", 30)

	# Load enemy assets.
	enemy_frames = load_enemy_frames()
	enemies = []

	# Initialize normal enemy spawning.
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

	game_started = False
	running = True

	# Main game loop.
	while running:
		dt = clock.tick(FPS) / 1000

		# Process window events.
		events = pygame.event.get()
		event_index = 0

		while event_index < len(events):
			event = events[event_index]

			if event.type == pygame.QUIT:
				running = False

			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and not game_started:
					game_started = True

			event_index += 1

		if not running:
			break

		# Keep the starfield moving in both menu and gameplay states.
		update_stars(stars, dt)

		if game_started:
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
				projectiles.append(create_projectile(player))
				shoot_timer = 0

			# Update projectiles.
			update_player_projectiles(projectiles, dt)
			update_enemy_projectiles(enemy_projectiles, dt)

			# Spawn and update enemies.
			if TEST_ALL_ENEMIES:
				spawn_test_enemies(enemies)
			else:
				spawn_enemies(enemies, score, dt, spawn_state)

			update_enemies(enemies, enemy_projectiles, dt)

			# Handle collisions.
			if not handle_player_enemy_collisions(player, enemies):
				running = False

			if running:
				if not handle_enemy_projectile_collisions(
					player,
					enemy_projectiles,
				):
					running = False

			if running:
				score = handle_player_projectile_collisions(
					projectiles,
					enemies,
					score,
				)

			# Update player effects.
			update_player_animation(player, dt)
			update_player_invulnerability(player, dt)

		# Draw the background first.
		game_surface.fill(BACKGROUND_COLOR)
		draw_stars(game_surface, stars)

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
			# Draw the transparent start-screen overlay above the stars.
			game_surface.blit(start_screen, start_screen_rect)

		update_display(screen, game_surface)
