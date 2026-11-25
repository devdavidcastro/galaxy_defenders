
# ==================================
# CONFIGURACAO DOS INIMIGOS
# ==================================

ENEMY_TYPES = {

	"drone": {
		"name": "Drone",
		"width": 48,
		"height": 48,
		"speed_x": 120,
		"speed_y": 80,
		"can_shoot": False,
		"shoot_interval": 0,
		"health": 1,
	},

	"escaravelho": {
		"name": "Escaravelho",
		"width": 48,
		"height": 48,
		"speed_x": 120,
		"speed_y": 80,
		"can_shoot": False,
		"shoot_interval": 0,
		"health": 2,
	},

	"nave_pesada": {
		"name": "Nave Pesada",
		"width": 48,
		"height": 48,
		"speed_x": 100,
		"speed_y": 60,
		"can_shoot": True,
		"shoot_interval": 2.5,
		"health": 3,
	},

	"orbital": {
		"name": "Orbital",
		"width": 48,
		"height": 48,
		"speed_x": 180,
		"speed_y": 140,
		"can_shoot": False,
		"shoot_interval": 0,
		"health": 1,
	},

	"criatura": {
		"name": "Criatura",
		"width": 48,
		"height": 48,
		"speed_x": 140,
		"speed_y": 100,
		"can_shoot": False,
		"shoot_interval": 0,
		"health": 2,
	},

	"batedor": {
		"name": "Batedor",
		"width": 48,
		"height": 48,
		"speed_x": 200,
		"speed_y": 160,
		"can_shoot": True,
		"shoot_interval": 1.5,
		"health": 2,
	}
}
