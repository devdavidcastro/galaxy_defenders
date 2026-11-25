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
		"can_shoot": config["can_shoot"],
		"shoot_interval": config["shoot_interval"],
		"shoot_timer": 0,
		"frame": 0,
		"animation_timer": 0,
		"is_hit": False,
		"is_destroyed": False
	}

	return enemy


def move_enemy(enemy, dt, screen_width):

	if enemy["is_hit"]:
		return

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



def draw_enemy(screen, enemy, enemy_frames):

	enemy_sprite = enemy_frames[enemy["frame"]]
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


def load_enemy_sprite_sheet():

	sprite_sheet = pygame.image.load(
		"assets/images/inimigo1_hit_spritesheet.png"
	).convert_alpha()

	frames = []

	frame_width = 128
	frame_height = 128

	frame_index = 0

	while frame_index < 5:

		frame = pygame.Surface(
			(frame_width, frame_height),
			pygame.SRCALPHA
		)

		frame_x = frame_index * frame_width

		frame.blit(
			sprite_sheet,
			(0, 0),
			(frame_x, 0, frame_width, frame_height)
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

	elif score < 300:
		return ["drone", "escaravelho", "nave_pesada"]

	elif score < 400:
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
