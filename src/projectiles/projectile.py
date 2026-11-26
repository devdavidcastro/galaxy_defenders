import pygame

PROJECTILE_WIDTH = 7
PROJECTILE_HEIGHT = 18
PROJECTILE_SPEED = 600

def create_projectile(player):

	projectile = {
		"x": player["x"],
		"y": player["y"] - player["height"] / 2,
		"width": PROJECTILE_WIDTH,
		"height": PROJECTILE_HEIGHT,
		"speed": PROJECTILE_SPEED
	}

	return projectile

def move_projectile(projectile, dt):

	projectile["y"] -= projectile["speed"] * dt

def draw_projectile(screen, projectile):

	x = int(projectile["x"])
	y = int(projectile["y"])

	width = projectile["width"]
	height = projectile["height"]

	# Bordas laranja
	pygame.draw.rect(
		screen,
		(255, 125, 25),
		(x - width // 2, y - height // 2, width, height),
		border_radius=5
	)

	# Centro amarelo
	pygame.draw.rect(
		screen,
		(255, 225, 90),
		(x - 3, y - height // 2 + 3, 6, height - 6),
		border_radius=3
	)

	# Núcleo luminoso
	pygame.draw.rect(
		screen,
		(255, 250, 190),
		(x - 1, y - height // 2 + 5, 2, height - 10)
	)

# ==================================
# CRIAR PROJÉTIL INIMIGO
# ==================================

def create_enemy_projectile(enemy):

	projectile = {
		"x": enemy["x"],
		"y": enemy["y"] + enemy["height"] / 2,
		"width": PROJECTILE_WIDTH,
		"height": PROJECTILE_HEIGHT,
		"speed": 220
	}

	return projectile

# ==================================
# MOVIMENTAR PROJÉTIL INIMIGO
# ==================================

def move_enemy_projectile(projectile, dt):

	projectile["y"] += projectile["speed"] * dt

# ==================================
# DESENHAR PROJÉTIL INIMIGO
# ==================================

def draw_enemy_projectile(screen, projectile):

	draw_projectile(screen, projectile)

def create_enemy_projectile(enemy):
	projectile = {
		"x": enemy["x"],
		"y": enemy["y"] + enemy["height"] / 2,
		"width": PROJECTILE_WIDTH,
		"height": PROJECTILE_HEIGHT,
		"speed": 220
	}
	return projectile


def move_enemy_projectile(projectile, dt):
	projectile["y"] += projectile["speed"] * dt


def draw_enemy_projectile(screen, projectile):
	draw_projectile(screen, projectile)
