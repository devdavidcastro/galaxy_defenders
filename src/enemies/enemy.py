import pygame
import random
import math

from src.enemies.enemy_config import ENEMY_TYPES

# ==================================
# CONFIGURACAO DOS INIMIGOS
# ==================================

ENEMY_WIDTH = 35
ENEMY_HEIGHT = 35

ENEMY_SPEED_X = 120
ENEMY_SPEED_Y = 80

ENEMY_COLOR = (180, 50, 255)


def create_enemy(screen_width, screen_height, enemy_type="drone"):

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
		"health": config["health"],
		"burst_shots_remaining": 0,
		"burst_shot_timer": 0,
		"burst_shot_interval": 0.25,
		"target_x": random.randint(100, screen_width - 100),
		"target_y": random.randint(100, screen_height - 250),
		"target_timer": 0,
		"target_interval": 2.0,
	}

	return enemy

# ==================================
# MOVIMENTAR INIMIGOS
# ==================================

def move_criatura(enemy, dt, screen_width, screen_height):

	if enemy["is_hit"]:
		return

	enemy["target_timer"] += dt

	# Escolher um novo destino
	if enemy["target_timer"] >= enemy["target_interval"]:

		enemy["target_x"] = random.randint(80, screen_width - 80)
		enemy["target_y"] = random.randint(80, screen_height - 200)

		enemy["target_timer"] = 0

	# Calcular a direcao do movimento
	dx = enemy["target_x"] - enemy["x"]
	dy = enemy["target_y"] - enemy["y"]

	distance = math.sqrt(dx ** 2 + dy ** 2)

	# Aproximar-se do destino
	if distance > 5:

		enemy["x"] += (dx / distance) * enemy["speed_x"] * dt
		enemy["y"] += (dy / distance) * enemy["speed_y"] * dt

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

	elif enemy["type"] == "criatura" or enemy["type"] == "batedor":
		move_criatura(enemy, dt, screen_width, screen_height)

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

	if not enemy["is_hit"] or enemy["is_destroyed"]:
		return

	enemy["animation_timer"] += dt

	if enemy["animation_timer"] >= ENEMY_HIT_FRAME_DURATION:
		enemy["animation_timer"] = 0

		if enemy["frame"] >= 4:
			enemy["is_destroyed"] = True
		else:
			enemy["frame"] += 1

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
		return 6

	elif score < 200:
		return 8

	elif score < 300:
		return 9

	elif score < 400:
		return 10

	elif score < 500:
		return 12

	elif score < 600:
		return 14

	elif score < 700:
		return 16

	elif score < 800:
		return 18

	elif score < 900:
		return 20

	elif score < 1000:
		return 22

	elif score < 1200:
		return 24

	elif score < 1500:
		return 27

	elif score < 1800:
		return 30

	elif score < 2000:
		return 33

	else:
		return 36



def get_enemy_spawn_interval(score):

	if score < 100:
		return 1.2, 2.4

	elif score < 200:
		return 1.1, 2.2

	elif score < 300:
		return 1.0, 2.0

	elif score < 400:
		return 0.9, 1.8

	elif score < 500:
		return 0.8, 1.6

	elif score < 600:
		return 0.7, 1.4

	elif score < 700:
		return 0.6, 1.2

	elif score < 800:
		return 0.5, 1.1

	elif score < 900:
		return 0.4, 1.0

	else:
		return 0.3, 0.8


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
