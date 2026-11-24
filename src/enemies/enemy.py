import pygame
import random

# ==================================
# CONFIGURACAO DOS INIMIGOS
# ==================================

ENEMY_WIDTH = 48
ENEMY_HEIGHT = 48

ENEMY_SPEED_X = 120
ENEMY_SPEED_Y = 80

ENEMY_COLOR = (180, 50, 255)

def create_enemy(screen_width):

	enemy = {
		"x": screen_width / 2,
		"y": 50,
		"width": ENEMY_WIDTH,
		"height": ENEMY_HEIGHT,
		"speed_x": ENEMY_SPEED_X,
		"speed_y": ENEMY_SPEED_Y,
		"direction": random.choice([-1, 1])
	}

	return enemy

def move_enemy(enemy, dt, screen_width):

	# Movimento horizontal
	enemy["x"] += enemy["speed_x"] * enemy["direction"] * dt

	# Movimento vertical
	enemy["y"] += enemy["speed_y"] * dt

	# Verificar a margem direita
	if enemy["x"] + enemy["width"] / 2 >= screen_width - 40:
		enemy["direction"] = -1

	# Verificar a margem esquerda
	if enemy["x"] - enemy["width"] / 2 <= 40:
		enemy["direction"] = 1


def draw_enemy(screen, enemy):

	enemy_rect = pygame.Rect(
		0,
		0,
		enemy["width"],
		enemy["height"]
	)

	enemy_rect.center = (
		int(enemy["x"]),
		int(enemy["y"])
	)

	pygame.draw.rect(
		screen,
		ENEMY_COLOR,
		enemy_rect,
		border_radius=8
	)


def check_projectile_collision(enemy, projectile):

	enemy_rect = pygame.Rect(
		0,
		0,
		enemy["width"],
		enemy["height"]
	)

	enemy_rect.center = (
		int(enemy["x"]),
		int(enemy["y"])
	)

	projectile_rect = pygame.Rect(
		0,
		0,
		projectile["width"],
		projectile["height"]
	)

	projectile_rect.center = (
		int(projectile["x"]),
		int(projectile["y"])
	)

	return enemy_rect.colliderect(projectile_rect)
