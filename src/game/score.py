import pygame


SCORE_COLOR = (255, 255, 255)
SCORE_FONT_SIZE = 20


def create_score():

	score = 0

	return score


def add_score(score, points):

	score += points

	return score


def draw_score(screen, score, font):

	score_text = font.render(
		f"{score}",
		True,
		SCORE_COLOR
	)

	score_rect = score_text.get_rect()

	score_rect.topright = (1280 - 30, 20)

	screen.blit(score_text, score_rect)
