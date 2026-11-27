import pygame

from src.game.game import run_game

from src.game.sounds import play_game_music, stop_game_music

def main():

	pygame.init()

	play_game_music()

	restart_game = True

	while restart_game:
		restart_game = run_game()

	stop_game_music()
	pygame.quit()


if __name__ == "__main__":
    main()
