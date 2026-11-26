
import pygame
import math


# ========================================
# PROJECTILE SETTINGS
# ========================================

PROJECTILE_WIDTH = 7
PROJECTILE_HEIGHT = 18

PLAYER_PROJECTILE_SPEED = 600
ENEMY_PROJECTILE_SPEED = 220
SCOUT_PROJECTILE_SPEED = 350

ENEMY_PROJECTILE_RADIUS = 3
SCOUT_PROJECTILE_RADIUS = 15


# ========================================
# PLAYER PROJECTILES
# ========================================

def create_projectile(player):
	return {
		"x": player["x"],
		"y": player["y"] - player["height"] / 2,
		"width": PROJECTILE_WIDTH,
		"height": PROJECTILE_HEIGHT,
		"speed": PLAYER_PROJECTILE_SPEED
	}


def move_projectile(projectile, dt):
	projectile["y"] -= projectile["speed"] * dt


def draw_projectile(screen, projectile):
	x = int(projectile["x"])
	y = int(projectile["y"])

	width = projectile["width"]
	height = projectile["height"]

	pygame.draw.rect(
		screen,
		(255, 125, 25),
		(x - width // 2, y - height // 2, width, height),
		border_radius=5
	)

	pygame.draw.rect(
		screen,
		(255, 225, 90),
		(x - 3, y - height // 2 + 3, 6, height - 6),
		border_radius=3
	)

	pygame.draw.rect(
		screen,
		(255, 250, 190),
		(x - 1, y - height // 2 + 5, 2, height - 10)
	)


# ========================================
# ENEMY PROJECTILES
# ========================================

def create_enemy_projectile(enemy):
	projectile_speed = ENEMY_PROJECTILE_SPEED

	if enemy["type"] == "batedor":
		projectile_speed = SCOUT_PROJECTILE_SPEED

	return {
		"x": enemy["x"],
		"y": enemy["y"] + enemy["height"] / 2,
		"width": PROJECTILE_WIDTH,
		"height": PROJECTILE_HEIGHT,
		"speed_x": 0,
		"speed_y": projectile_speed,
		"type": enemy["type"]
	}


def move_enemy_projectile(projectile, dt):
	projectile["x"] += projectile["speed_x"] * dt
	projectile["y"] += projectile["speed_y"] * dt


def draw_enemy_projectile(screen, projectile):
	x = int(projectile["x"])
	y = int(projectile["y"])

	radius = ENEMY_PROJECTILE_RADIUS

	if projectile["type"] == "batedor":
		radius = SCOUT_PROJECTILE_RADIUS

	pygame.draw.circle(
		screen,
		(255, 125, 25),
		(x, y),
		radius + 3
	)

	pygame.draw.circle(
		screen,
		(255, 225, 90),
		(x, y),
		radius
	)

	pygame.draw.circle(
		screen,
		(255, 250, 190),
		(x, y),
		max(1, radius // 2)
	)


# ========================================
# ORBITAL PROJECTILES
# ========================================

def create_orbital_projectiles(enemy):
	projectiles = []

	angle = 0
	projectile_count = 8
	angle_step = 360 / projectile_count

	while angle < 360:
		radians = math.radians(angle)

		projectile = {
			"x": enemy["x"],
			"y": enemy["y"],
			"width": PROJECTILE_WIDTH,
			"height": PROJECTILE_HEIGHT,
			"speed_x": math.cos(radians) * ENEMY_PROJECTILE_SPEED,
			"speed_y": math.sin(radians) * ENEMY_PROJECTILE_SPEED,
			"type": "orbital"
		}

		projectiles.append(projectile)
		angle += angle_step

	return projectiles
