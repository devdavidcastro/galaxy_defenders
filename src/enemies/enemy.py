import pygame
import random

from src.enemies.enemy_config import ENEMY_TYPES

# ==================================
# CONFIGURACAO DOS INIMIGOS
# ==================================

ENEMY_WIDTH = 35
ENEMY_HEIGHT = 35

ENEMY_SPEED_X = 120
ENEMY_SPEED_Y = 80

ENEMY_COLOR = (180, 50, 255)


def create_enemy(screen_width, enemy_type="drone"):

	config = ENEMY_TYPES[enemy_type]

	enemy = {

		"type": enemy_type,

		"x": random.randint(
			80,
			screen_width - 80
		),

		"y": -config["height"] / 2,
		"width": config["width"],
		"height": config["height"],
		"speed_x": config["speed_x"],
		"speed_y": config["speed_y"],
		"direction": random.choice([-1, 1]),
		"vertical_direction": 1,
		"zigzag_timer": 0,
		"zigzag_interval": 1.2,
		"can_shoot": config["can_shoot"],
		"shoot_interval": config["shoot_interval"],
		"shoot_timer": 0,
		"frame": 0,
		"animation_timer": 0,
		"is_hit": False,
		"is_destroyed": False,
		"health": config["health"]
	}

	return enemy

# ==================================
# MOVIMENTAR INIMIGOS
# ==================================

def move_enemy(enemy, dt, screen_width, screen_height):

	if enemy["type"] == "orbital":

		move_orbital(
			enemy,
			dt,
			screen_width,
			screen_height
		)
	elif enemy["type"] == "nave_pesada":

		move_orbital(
			enemy,
			dt,
			screen_width,
			screen_height
		)

	else:

		move_basic(
			enemy,
			dt,
			screen_width,
			screen_height
		)

def move_basic(enemy, dt, screen_width, screen_height):

	if enemy["is_hit"]:
		return

	# Movimento horizontal
	enemy["x"] += enemy["speed_x"] * enemy["direction"] * dt

	# Movimento vertical
	enemy["y"] += enemy["speed_y"] * enemy["vertical_direction"] * dt

	# Verificar a margem direita
	if enemy["x"] + enemy["width"] / 2 >= screen_width - 40:
		enemy["direction"] = -1

	# Verificar a margem esquerda
	if enemy["x"] - enemy["width"] / 2 <= 40:
		enemy["direction"] = 1

	# Verificar o limite inferior
	if enemy["y"] + enemy["height"] / 2 >= screen_height - 40:
		enemy["vertical_direction"] = -1

	# Verificar o limite superior
	if enemy["y"] - enemy["height"] / 2 <= 40:
		enemy["vertical_direction"] = 1



def draw_enemy(screen, enemy, enemy_frames):

	enemy_type = enemy["type"]
	enemy_sprite = enemy_frames[enemy_type][enemy["frame"]]
	enemy_rect = enemy_sprite.get_rect()
	enemy_rect.center = (
		enemy["x"],
		enemy["y"]
	)

	screen.blit(enemy_sprite, enemy_rect)


def check_projectile_collision(enemy, projectile):

	# Ignorar inimigos que ainda estao fora do ecra
	if enemy["y"] + enemy["height"] / 2 < 0:
		return False

	enemy_rect = pygame.Rect(0, 0, enemy["width"], enemy["height"])
	enemy_rect.center = (int(enemy["x"]), int(enemy["y"]))

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


def load_enemy_sprite_sheet(enemy_type):

	enemy_numbers = {
		"drone": 1,
		"escaravelho": 2,
		"nave_pesada": 3,
		"orbital": 4,
		"criatura": 5,
		"batedor": 6
	}

	sprite_number = enemy_numbers[enemy_type]

	sprite_sheet_path = (
		f"assets/images/inimigo{sprite_number}_hit_spritesheet.png"
	)

	sprite_sheet = pygame.image.load(
		sprite_sheet_path
	).convert_alpha()

	frames = []

	frame_index = 0

	while frame_index < 5:

		frame = pygame.Surface(
			(128, 128),
			pygame.SRCALPHA
		)

		frame.blit(
			sprite_sheet,
			(0, 0),
			(frame_index * 128, 0, 128, 128)
		)

		frame = pygame.transform.scale(
			frame,
			(48, 48)
		)

		frames.append(frame)

		frame_index += 1

	return frames


# ==================================
# ANIMACAO DE DESTRUICAO
# ==================================

ENEMY_HIT_FRAME_DURATION = 0.07


def update_enemy_animation(enemy, dt):

	if not enemy["is_hit"]:
		return

	enemy["animation_timer"] += dt

	if enemy["animation_timer"] >= ENEMY_HIT_FRAME_DURATION:
		enemy["animation_timer"] = 0
		enemy["frame"] += 1

		if enemy["frame"] >= 5:
			enemy["is_destroyed"] = True

def get_unlocked_enemy_types(score):

	if score < 100:
		return ["drone"]

	elif score < 200:
		return ["drone", "escaravelho"]

	elif score < 700:
		return ["drone", "escaravelho", "nave_pesada"]

	elif score < 900:
		return ["drone", "escaravelho", "nave_pesada", "orbital"]

	else:
		return [
			"drone",
			"escaravelho",
			"nave_pesada",
			"orbital",
			"criatura",
			"batedor"
		]

def get_enemy_limit(score):

	if score < 100:
		return 10

	elif score < 200:
		return 12

	elif score < 300:
		return 14

	elif score < 400:
		return 16

	elif score < 500:
		return 18

	elif score < 600:
		return 20

	elif score < 700:
		return 23

	elif score < 800:
		return 26

	elif score < 900:
		return 29

	elif score < 1000:
		return 32

	elif score < 1200:
		return 35

	elif score < 1500:
		return 38

	elif score < 1800:
		return 42

	elif score < 2000:
		return 46

	else:
		return 50

def get_enemy_spawn_interval(score):

	if score < 100:
		return 0.8, 1.8

	elif score < 200:
		return 0.7, 1.5

	elif score < 300:
		return 0.6, 1.3

	elif score < 400:
		return 0.5, 1.1

	elif score < 500:
		return 0.4, 0.9

	elif score < 600:
		return 0.35, 0.8

	elif score < 700:
		return 0.3, 0.7

	elif score < 800:
		return 0.25, 0.6

	elif score < 900:
		return 0.2, 0.5

	else:
		return 0.15, 0.4

# ==================================
# MOVIMENTO DO DRONE
# ==================================

def move_drone(enemy, dt, screen_width, screen_height):

	move_basic(
		enemy,
		dt,
		screen_width,
		screen_height
	)

# ==================================
# MOVIMENTO DO ORBITAL
# ==================================

def move_orbital(enemy, dt, screen_width, screen_height):

	if enemy["is_hit"]:
		return

	# Movimento em ziguezague
	enemy["zigzag_timer"] += dt

	if enemy["zigzag_timer"] >= enemy["zigzag_interval"]:

		enemy["direction"] *= -1
		enemy["zigzag_timer"] = 0

	# Movimento horizontal
	enemy["x"] += (
		enemy["speed_x"] *
		enemy["direction"] *
		dt
	)

	# Movimento vertical
	enemy["y"] += (
		enemy["speed_y"] *
		enemy["vertical_direction"] *
		dt
	)

	# Limites laterais
	if enemy["x"] + enemy["width"] / 2 >= screen_width - 40:
		enemy["x"] = screen_width - 40 - enemy["width"] / 2
		enemy["direction"] = -1

	if enemy["x"] - enemy["width"] / 2 <= 40:
		enemy["x"] = 40 + enemy["width"] / 2
		enemy["direction"] = 1

	# Limites verticais
	if enemy["y"] + enemy["height"] / 2 >= screen_height - 40:
		enemy["y"] = screen_height - 40 - enemy["height"] / 2
		enemy["vertical_direction"] = -1

	if enemy["y"] - enemy["height"] / 2 <= 40:
		enemy["y"] = 40 + enemy["height"] / 2
		enemy["vertical_direction"] = 1
