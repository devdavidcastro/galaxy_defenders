import json
import os


# Number of records to keep
MAX_HIGH_SCORES = 10

# High scores file path
HIGH_SCORES_FILE = "assets/data/high_scores.json"


def create_high_scores():
	high_scores = []

	return high_scores

def load_high_scores():
	if not os.path.exists(HIGH_SCORES_FILE):
		return []

	with open(HIGH_SCORES_FILE, "r", encoding="utf-8") as file:
		high_scores = json.load(file)

	return high_scores

def save_high_scores(high_scores):
	os.makedirs("assets/data", exist_ok=True)

	with open(HIGH_SCORES_FILE, "w", encoding="utf-8") as file:
		json.dump(high_scores, file, indent=4)


def add_high_score(high_scores, player_name, player_score):
	new_record = {
		"name": player_name,
		"score": player_score
	}

	high_scores.append(new_record)

	high_scores.sort(
		key=lambda record: record["score"],
		reverse=True
	)

	high_scores = high_scores[:MAX_HIGH_SCORES]

	save_high_scores(high_scores)

	return high_scores


def qualifies_for_high_scores(high_scores, player_score):
	if len(high_scores) < MAX_HIGH_SCORES:
		return True

	if player_score > high_scores[-1]["score"]:
		return True

	return False
