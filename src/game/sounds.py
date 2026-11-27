
import pygame


def load_sounds():

	sounds = {}

	sounds["player_shot"] = pygame.mixer.Sound(
		"assets/sounds/player_shot.wav"
	)

	sounds["enemy_destroyed"] = pygame.mixer.Sound(
		"assets/sounds/enemy_destroyed.wav"
	)
	return sounds


def play_sound(sounds, sound_name):
	if sound_name in sounds:
		sounds[sound_name].play()

def play_game_music():
	pygame.mixer.music.load("assets/sounds/music_game.mp3")
	pygame.mixer.music.play(-1)

def stop_game_music():
	pygame.mixer.music.stop

