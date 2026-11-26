
import random

from src.game.settings import WIDTH, HEIGHT

from src.enemies.enemy import (
	create_enemy,
	move_enemy,
	draw_enemy,
	load_enemy_sprite_sheet,
	update_enemy_animation,
	get_unlocked_enemy_types,
	get_enemy_spawn_interval,
	get_enemy_limit,
)

from src.projectiles.projectile import (
	create_enemy_projectile,
	create_orbital_projectiles,
)


# ========================================
# ENEMY CONFIGURATION
# ========================================

TEST_ENEMY_TYPES = [
	"drone",
	"escaravelho",
	"nave_pesada",
	"orbital",
	"criatura",
	"batedor",
]


# ========================================
# ENEMY ASSET LOADING
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
# ENEMY DRAWING
# ========================================

def draw_enemies(game_surface, enemies, enemy_frames):
	"""Draw all active enemies."""

	index = 0

	while index < len(enemies):
		draw_enemy(game_surface, enemies[index], enemy_frames)
		index += 1
