
import pygame


def load_sounds():

	sounds = {}

	sounds["player_shot"] = pygame.mixer.Sound(
		"assets/sounds/player_shot.wav"
	)
	return sounds


def play_sound(sounds, sound_name):
	if sound_name in sounds:
		sounds[sound_name].play()
