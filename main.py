import pygame

from src.game.game import run_game


def main():

	pygame.init()

	restart_game = True

	while restart_game:
		restart_game = run_game()

	pygame.quit()


if __name__ == "__main__":
    main()
