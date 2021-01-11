from game_js import Game
from player import Player
from table import Table

p1 = Player(**{"name": "Ethan", "stack": 10})
p2 = Player(**{"name": "Jack", "stack": 20})
p3 = Player(**{"name": "Mike", "stack": 30})

t = Table(**{"blinds": [1, 2]})
t.add_player(p1)
t.add_player(p2)
t.add_player(p3)

g = Game(t)

g.play_hand()
