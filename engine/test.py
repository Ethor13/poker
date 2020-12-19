from game import Game
from player import Player
from table import Table

p1 = Player("Ethan", 10, {})
p2 = Player("Jack", 20, {})
p3 = Player("Mike", 30, {})

t = Table(5, 1, 2)
t.add_player(p1)
t.add_player(p2)
t.add_player(p3)

g = Game(t)
g.play_hand()
print(p1.get_chips(), p2.get_chips(), p3.get_chips())
