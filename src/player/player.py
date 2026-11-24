
import pygame


# ==================================
# CONFIGURAÇÕES DA NAVE
# ==================================

PLAYER_WIDTH = 80
PLAYER_HEIGHT = 61
PLAYER_SCALE = 0.8

PLAYER_SPEED = 400

PLAYER_COLOR = (0, 180, 230)
PLAYER_COCKPIT_COLOR = (100, 240, 255)
PLAYER_OUTLINE_COLOR = (0, 230, 255)
PLAYER_WING_COLOR = (15, 65, 120)
PLAYER_WING_DETAIL = (0, 160, 220)

PLAYER_ENGINE_COLOR = (255, 105, 0)
PLAYER_ENGINE_GLOW = (255, 190, 60)
PLAYER_FLAME_CORE = (255, 245, 190)
PLAYER_FLAME_TIMER = 0
PLAYER_FLAME_SPEED = 12


# ==================================
# CRIAÇÃO DA NAVE
# ==================================

def create_player(width, height):

	player = {
		"x": width / 2,
		"y": height - 100,
		"width": PLAYER_WIDTH,
		"height": PLAYER_HEIGHT,
		"speed": PLAYER_SPEED,
		"flame_timer": 0,
		"moving_left": False,
		"moving_right": False
	}

	return player


# ==================================
# MOVIMENTO DA NAVE
# ==================================

def move_player(player, keys, dt, screen_width, screen_height, margin):

	if keys[pygame.K_LEFT]:
		player["x"] -= player["speed"] * dt

	if keys[pygame.K_RIGHT]:
		player["x"] += player["speed"] * dt

	if keys[pygame.K_UP]:
		player["y"] -= player["speed"] * dt

	if keys[pygame.K_DOWN]:
		player["y"] += player["speed"] * dt

	minimum_x = margin + player["width"] / 2
	maximum_x = screen_width - margin - player["width"] / 2
	minimum_y = 40 + player["height"] / 2
	maximum_y = screen_height - player["height"] - 40

	if player["x"] < minimum_x:
		player["x"] = minimum_x

	if player["x"] > maximum_x:
		player["x"] = maximum_x

	if player["y"] < minimum_y:
		player["y"] = minimum_y

	if player["y"] > maximum_y:
		player["y"] = maximum_y

# ==================================
# ANIMACAO PLAYER
# ==================================
def update_player_animation(player, keys, dt):

	player["flame_timer"] += dt * PLAYER_FLAME_SPEED

	if player["flame_timer"] >= 2:
		player["flame_timer"] = 0

	player["moving_left"] = keys[pygame.K_LEFT]
	player["moving_right"] = keys[pygame.K_RIGHT]

	player["left_flame_length"] = 14
	player["right_flame_length"] = 14

	if player["moving_left"]:
		player["left_flame_length"] = 8
		player["right_flame_length"] = 22

	if player["moving_right"]:
		player["left_flame_length"] = 22
		player["right_flame_length"] = 8

def scale_point(x, y, scale):
	return (int(x * scale), int(y * scale))

# ==================================
# DESENHO DA NAVE
# ==================================

def draw_player(screen, player):

	x = int(player["x"])
	y = int(player["y"])
	scale = PLAYER_SCALE

	# Fuselagem central
	body_points = [
		(x, y),
		(x + int(12 * scale), y + int(24 * scale)),
		(x + int(12 * scale), y + int(62 * scale)),
		(x, y + int(70 * scale)),
		(x - int(12 * scale), y + int(62 * scale)),
		(x - int(12 * scale), y + int(24 * scale))
]

	# Cockpit luminoso
	cockpit_points = [
		(x, y + int(12 * scale)),
		(x + int(6 * scale), y + int(27 * scale)),
		(x, y + int(42 * scale)),
		(x - int(6 * scale), y + int(27 * scale))
	]

	# Motor esquerdo
	left_engine = [
		(x - int(18 * scale), y + int(48 * scale)),
		(x - int(30 * scale), y + int(58 * scale)),
		(x - int(27 * scale), y + int(70 * scale)),
		(x - int(15 * scale), y + int(65 * scale))
	]

	# Motor direito
	right_engine = [
		(x + int(18 * scale), y + int(48 * scale)),
		(x + int(30 * scale), y + int(58 * scale)),
		(x + int(27 * scale), y + int(70 * scale)),
		(x + int(15 * scale), y + int(65 * scale))
	]

	# Chama do motor esquerdo
	left_flame = [
		(x - int(18 * scale), y + int(68 * scale)),
		(x - int(24 * scale), y + int((68 + player["left_flame_length"]) * scale)),
		(x - int(18 * scale), y + int(78 * scale)),
		(x - int(12 * scale), y + int((68 + player["left_flame_length"]) * scale)),
		(x - int(15 * scale), y + int(68 * scale))
	]

	# Chama do motor direito
	right_flame = [
		(x + int(18 * scale), y + int(68 * scale)),
		(x + int(24 * scale), y + int((68 + player["right_flame_length"]) * scale)),
		(x + int(18 * scale), y + int(78 * scale)),
		(x + int(12 * scale), y + int((68 + player["right_flame_length"]) * scale)),
		(x + int(15 * scale), y + int(68 * scale))
	]

	# Asa esquerda
	left_wing = [
		(x - int(14 * scale), y + int(28 * scale)),
		(x - int(58 * scale), y + int(62 * scale)),
		(x - int(48 * scale), y + int(68 * scale)),
		(x - int(18 * scale), y + int(58 * scale)),
		(x - int(12 * scale), y + int(44 * scale))
	]

	# Asa direita
	right_wing = [
		(x + int(14 * scale), y + int(28 * scale)),
		(x + int(58 * scale), y + int(62 * scale)),
		(x + int(48 * scale), y + int(68 * scale)),
		(x + int(18 * scale), y + int(58 * scale)),
		(x + int(12 * scale), y + int(44 * scale))
	]

	# Chamas exteriores
	pygame.draw.polygon(screen, PLAYER_ENGINE_COLOR, left_flame)
	pygame.draw.polygon(screen, PLAYER_ENGINE_COLOR, right_flame)

	# Desenhar motor esquerdo
	pygame.draw.polygon(screen, PLAYER_WING_COLOR, left_engine)
	pygame.draw.polygon(screen, PLAYER_WING_DETAIL, left_engine, 2)

	# Desenhar motor direito
	pygame.draw.polygon(screen, PLAYER_WING_COLOR, right_engine)
	pygame.draw.polygon(screen, PLAYER_WING_DETAIL, right_engine, 2)

	# Desenhar asa esquerda
	pygame.draw.polygon(
		screen,
		PLAYER_WING_COLOR,
		left_wing
	)
	pygame.draw.polygon(
		screen,
		PLAYER_WING_DETAIL,
		left_wing,
		2
	)

	# Desenhar asa direita
	pygame.draw.polygon(
		screen,
		PLAYER_WING_COLOR,
		right_wing
	)
	pygame.draw.polygon(
		screen,
		PLAYER_WING_DETAIL,
		right_wing,
		2
	)

	# Corpo principal
	pygame.draw.polygon(
		screen,
		PLAYER_COLOR,
		body_points
	)

	# Contorno luminoso
	pygame.draw.polygon(
		screen,
		PLAYER_OUTLINE_COLOR,
		body_points,
		1
	)

	# Desenhar cockpit por cima da fuselagem
	pygame.draw.polygon(screen, PLAYER_COCKPIT_COLOR, cockpit_points)
	pygame.draw.polygon(screen, PLAYER_OUTLINE_COLOR, cockpit_points, 1)
