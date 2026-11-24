
import pygame


# ==================================
# CONFIGURAÇÕES DA NAVE
# ==================================

PLAYER_SPRITE_WIDTH = 80
PLAYER_SPEED = 400


# ==================================
# CARREGAR IMAGEM DA NAVE
# ==================================


def load_player_sprite():

	sprite_sheet = pygame.image.load(
		"assets/images/defender_sheet.png"
	).convert_alpha()

	# Recortar a terceira nave da primeira fila
	player_sprite = sprite_sheet.subsurface(
		(652, 38, 281, 337)
	).copy()

	original_width, original_height = player_sprite.get_size()

	new_height = int(
		original_height * PLAYER_SPRITE_WIDTH / original_width
	)

	player_sprite = pygame.transform.smoothscale(
		player_sprite,
		(PLAYER_SPRITE_WIDTH, new_height)
	)

	return player_sprite



# ==================================
# CRIAR CAMADA DIANTEIRA DOS MOTORES
# ==================================

def create_player_front(player_sprite):

    front_layer = pygame.Surface(
        player_sprite.get_size(),
        pygame.SRCALPHA
    )

    # Recortar a parte inferior do motor esquerdo
    left_engine = player_sprite.subsurface(
        (22, 64, 17, 10)
    )

    # Recortar a parte inferior do motor direito
    right_engine = player_sprite.subsurface(
        (45, 64, 17, 10)
    )

    # Colocar os recortes na camada transparente
    front_layer.blit(left_engine, (22, 64))
    front_layer.blit(right_engine, (45, 64))

    return front_layer


# ==================================
# DESENHAR CAMADA DIANTEIRA
# ==================================

def draw_player_front(screen, player, front_layer):

	front_rect = front_layer.get_rect(
		center=(
			int(player["x"]),
			int(player["y"])
		)
	)

	screen.blit(front_layer, front_rect)

# ==================================
# CARREGAR FOTOGRAMAS DAS CHAMAS
# ==================================


def load_flame_sprites():

	sprite_sheet = pygame.image.load(
		"assets/images/defender_sheet.png"
	).convert_alpha()

	flame_frames = []

	frame_positions = [
		(397, 390, 51, 290),
		(498, 390, 69, 290),
		(609, 390, 64, 290),
		(717, 390, 67, 290)
	]

	index = 0
	max_height = 0

	while index < len(frame_positions):

		x, y, width, height = frame_positions[index]

		frame = sprite_sheet.subsurface(
			(x, y, width, height)
		).copy()

		flame_rect = frame.get_bounding_rect()
		frame = frame.subsurface(flame_rect).copy()

		original_width, original_height = frame.get_size()

		new_width = 18
		new_height = int(
			original_height * new_width / original_width
		)

		frame = pygame.transform.smoothscale(
			frame,
			(new_width, new_height)
		)

		flame_frames.append(frame)

		if new_height > max_height:
			max_height = new_height

		index += 1

	# Uniformizar a área de todos os frames
	index = 0
	aligned_frames = []

	while index < len(flame_frames):

		aligned_frame = pygame.Surface(
			(18, max_height),
			pygame.SRCALPHA
		)

		aligned_frame.blit(
			flame_frames[index],
			(0, 0)
		)

		aligned_frames.append(aligned_frame)

		index += 1

	return aligned_frames


# ==================================
# ATUALIZAR ANIMACAO DAS CHAMAS
# ==================================

def update_player_animation(player, dt):

	player["flame_timer"] += dt

	if player["flame_timer"] >= 0.10:

		player["flame_timer"] = 0

		player["flame_frame"] += 1

		if player["flame_frame"] >= 4:
			player["flame_frame"] = 0


# ==================================
# DESENHAR CHAMAS
# ==================================


def draw_player_flames(screen, player, flame_frames):

	frame = flame_frames[player["flame_frame"]]

	engine_offset = 11

	# Posição fixa onde as chamas começam
	flame_top = (
		player["y"]
		+ player["height"] / 2
		- 55
	)

	# Motor esquerdo
	left_rect = frame.get_rect(
		midtop=(
			int(player["x"] - engine_offset),
			int(flame_top)
		)
	)

	screen.blit(frame, left_rect)

	# Motor direito
	right_rect = frame.get_rect(
		midtop=(
			int(player["x"] + engine_offset),
			int(flame_top)
		)
	)

	screen.blit(frame, right_rect)


# ==================================
# CRIAR JOGADOR
# ==================================

def create_player(width, height, player_sprite):

	sprite_width, sprite_height = player_sprite.get_size()

	player = {
		"x": width / 2,
		"y": height - 70 - sprite_height / 2,
		"width": sprite_width,
		"height": sprite_height,
		"speed": PLAYER_SPEED,
		"flame_frame": 0,
		"flame_timer": 0
	}

	return player


# ==================================
# MOVIMENTAR JOGADOR
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
	maximum_y = screen_height - 40 - player["height"] / 2

	if player["x"] < minimum_x:
		player["x"] = minimum_x

	if player["x"] > maximum_x:
		player["x"] = maximum_x

	if player["y"] < minimum_y:
		player["y"] = minimum_y

	if player["y"] > maximum_y:
		player["y"] = maximum_y


# ==================================
# DESENHAR JOGADOR
# ==================================

def draw_player(screen, player, player_sprite):

	sprite_rect = player_sprite.get_rect(
		center=(
			int(player["x"]),
			int(player["y"])
		)
	)

	screen.blit(player_sprite, sprite_rect)
