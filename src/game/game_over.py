
import pygame

from src.game.settings import WIDTH, HEIGHT

GAME_OVER_IMAGE_PATH = "assets/images/game_over.png"
GAME_OVER_IMAGE_WIDTH = 500

# ========================================
# RANKING CONFIGURATION
# ========================================

HIGH_SCORE_LIMIT = 10

RANKING_TITLE_COLOR = (0, 255, 255)
RANKING_TEXT_COLOR = (255, 255, 255)
RANKING_GOLD_COLOR = (255, 220, 0)
RANKING_SILVER_COLOR = (220, 220, 220)
RANKING_BRONZE_COLOR = (255, 140, 0)
RANKING_ENTRY_COLOR = (0, 255, 255)


# ========================================
# GAME OVER IMAGE
# ========================================

def draw_game_over_overlay(game_surface):
	"""Draw a dark overlay over the game."""

	overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
	overlay.fill((0, 0, 0, 110))
	game_surface.blit(overlay, (0, 0))


def load_game_over_image():
	"""Load and scale the Game Over image."""

	image = pygame.image.load(
		GAME_OVER_IMAGE_PATH
	).convert_alpha()

	image_height = int(
		image.get_height()
		* GAME_OVER_IMAGE_WIDTH
		/ image.get_width()
	)

	image = pygame.transform.smoothscale(
		image,
		(GAME_OVER_IMAGE_WIDTH, image_height),
	)

	return image


def create_game_over_image_rect(game_over_image):
	"""Position the Game Over image."""

	return game_over_image.get_rect(
		midtop=(WIDTH // 2, 45)
	)


# ========================================
# HIGH SCORE RANKING
# ========================================

def get_player_ranking_position(high_scores, player_score):
	"""Return the position where the player's score belongs."""

	index = 0

	while index < len(high_scores):
		if player_score > high_scores[index]["score"]:
			return index

		index += 1

	if len(high_scores) < HIGH_SCORE_LIMIT:
		return len(high_scores)

	return HIGH_SCORE_LIMIT - 1


def get_ranking_color(index):
	"""Return the color associated with a ranking position."""

	if index == 0:
		return RANKING_GOLD_COLOR

	if index == 1:
		return RANKING_SILVER_COLOR

	if index == 2:
		return RANKING_BRONZE_COLOR

	return RANKING_TEXT_COLOR


def draw_high_scores(
	game_surface,
	high_scores,
	font,
	name_entry_active,
	player_name,
	player_score,
	player_ranking_position,
):
	"""Draw the Top 10 and the player's name entry."""

	title_font = pygame.font.Font(
		"assets/fonts/Oxanium.ttf",
		24,
	)

	title = title_font.render(
		"TOP 10 HIGH SCORES",
		True,
		RANKING_TITLE_COLOR,
	)

	title_rect = title.get_rect(
		center=(WIDTH // 2, 240)
	)

	game_surface.blit(title, title_rect)

	index = 0

	while index < HIGH_SCORE_LIMIT:
		y_position = 285 + index * 25

		is_player_position = (
			name_entry_active
			and index == player_ranking_position
		)

		if is_player_position:
			position_text = f"{index + 1:02d}."
			name_text = player_name
			score_text = str(player_score)
			color = RANKING_ENTRY_COLOR

		else:
			record_index = index

			if name_entry_active and index > player_ranking_position:
				record_index -= 1

			if record_index < len(high_scores):
				record = high_scores[record_index]

				position_text = f"{index + 1:02d}."
				name_text = record["name"]
				score_text = str(record["score"])
				color = get_ranking_color(index)

			else:
				position_text = f"{index + 1:02d}."
				name_text = "---"
				score_text = "---"
				color = RANKING_TEXT_COLOR

		position_surface = font.render(
			position_text,
			True,
			color,
		)

		name_surface = font.render(
			name_text,
			True,
			color,
		)

		score_surface = font.render(
			score_text,
			True,
			color,
		)

		game_surface.blit(
			position_surface,
			(WIDTH // 2 - 190, y_position),
		)

		game_surface.blit(
			name_surface,
			(WIDTH // 2 - 130, y_position),
		)

		score_rect = score_surface.get_rect(
			midright=(WIDTH // 2 + 190, y_position + 15)
		)

		game_surface.blit(
			score_surface,
			score_rect,
		)

		index += 1


# ========================================
# GAME OVER SCREEN
# ========================================

def draw_game_over_screen(
	game_surface,
	game_over_image,
	game_over_image_rect,
	high_scores,
	font,
	name_entry_active,
	player_name,
	player_score,
	player_ranking_position,
):
	"""Draw the complete Game Over screen."""

	draw_game_over_overlay(game_surface)

	game_surface.blit(
		game_over_image,
		game_over_image_rect,
	)

	cursor_visible = (pygame.time.get_ticks() // 500) % 2 == 0

	draw_high_scores(
		game_surface,
		high_scores,
		font,
		name_entry_active,
		player_name,
		player_score,
		player_ranking_position,
	)
	# Draw restart and exit instructions.
	controls_font = pygame.font.Font(
		"assets/fonts/Oxanium.ttf",
		20,
	)

	restart_text = controls_font.render(
		"SPACE - RESTART",
		True,
		(50, 220, 255),
	)

	exit_text = controls_font.render(
		"ESC - EXIT",
		True,
		(255, 210, 70),
	)

	restart_rect = restart_text.get_rect(
		center=(WIDTH // 2, 650)
	)

	exit_rect = exit_text.get_rect(
		center=(WIDTH // 2, 680)
	)

	if name_entry_active:

		# Draw the blinking cursor after the player's name.
		if cursor_visible:

			cursor_font = pygame.font.Font(
				"assets/fonts/Oxanium.ttf",
				20,
			)

			cursor_text = cursor_font.render(
				"_",
				True,
				RANKING_ENTRY_COLOR,
			)

			cursor_rect = cursor_text.get_rect(
				midleft=(
					WIDTH // 2 - 125 + font.size(player_name)[0],
					285 + player_ranking_position * 20 + 15,
				)
			)

			game_surface.blit(
				cursor_text,
				cursor_rect,
			)

		# Draw the name entry instruction.
		instruction_font = pygame.font.Font(
			"assets/fonts/Oxanium.ttf",
			14,
		)

		instruction_text = instruction_font.render(
			"*Enter your name and press Enter to save",
			True,
			RANKING_ENTRY_COLOR,
		)

		instruction_rect = instruction_text.get_rect(
			center=(WIDTH // 2, 540)
		)

		game_surface.blit(
			instruction_text,
			instruction_rect,
		)

	game_surface.blit(restart_text, restart_rect)
	game_surface.blit(exit_text, exit_rect)
