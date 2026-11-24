import pygame

from src.game.game import run_game


def main():

    pygame.init()

    run_game()

    pygame.quit()


if __name__ == "__main__":
    main()
