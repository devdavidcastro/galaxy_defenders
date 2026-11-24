import pygame
import random

from src.game.settings import WIDTH, HEIGHT


def create_stars():

	stars = []

	# Camada 1: distante
	counter = 0

	while counter < 40:

		star = {
			"x": random.randint(0, WIDTH),
			"y": random.randint(0, HEIGHT),
			"speed": random.uniform(30, 60),
			"size": 1,
			"color": (90, 110, 160)
		}

		stars.append(star)
		counter += 1

	# Camada 2: intermédia
	counter = 0

	while counter < 25:

		star = {
			"x": random.randint(0, WIDTH),
			"y": random.randint(0, HEIGHT),
			"speed": random.uniform(90, 150),
			"size": 2,
			"color": (150, 180, 230)
		}

		stars.append(star)
		counter += 1

	# Camada 3: próxima
	counter = 0

	while counter < 15:

		star = {
			"x": random.randint(0, WIDTH),
			"y": random.randint(0, HEIGHT),
			"speed": random.uniform(180, 240),
			"size": 3,
			"color": (210, 230, 255)
		}

		stars.append(star)
		counter += 1

	return stars


def update_stars(stars, dt):

	index = 0

	while index < len(stars):

		star = stars[index]

		star["y"] += star["speed"] * dt

		if star["y"] > HEIGHT:
			star["y"] = 0
			star["x"] = random.randint(0, WIDTH)

		index += 1


def draw_stars(screen, stars):

	index = 0

	while index < len(stars):

		star = stars[index]

		pygame.draw.circle(
			screen,
			star["color"],
			(int(star["x"]), int(star["y"])),
			star["size"]
		)

		index += 1
