from game_js import Game
from player import Player
from table import Table
import sys
import json

game_state = json.loads(sys.argv[1])
last_decision = sys.argv[2]

g = Game.load_game_state(game_state, last_decision)
g.play_hand()
