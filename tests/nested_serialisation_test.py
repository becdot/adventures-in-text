from game import Game
from objects import Chair, Dresser
from scaffolding import Room
from copy import deepcopy

import unittest

class Serialisation(unittest.TestCase):

    def setUp(self):
        closet = Dresser()
        closet.name = closet.id = 'closet'
        outer = Dresser()
        outer.id = outer.name = 'outer'
        chair = Chair()
        room = Room(name='room', objects=[outer, chair], exits={}, description='a room.')
        self.game = Game()
        self.game.game['rooms'] = [room]
        self.game.game['location'] = room
        self.game.game['inv'] = []
        self.game.all_objs = [outer, closet, chair]
        self.base = deepcopy(self.game)

    def serialise(self, g):
        """Takes a game instance, serialises it, and then creates a new game instance from the serialisation.
            The old and new instances should be the same."""
        base2 = deepcopy(self.base)
        old = g.game
        s = g.serialise()
        base2.deserialise(s)
        new = base2.game
        self.assertEquals(old, new)

    def test_nested_serialisation(self):
        "Tests basic game functions (same as mini_game.py) with serialisation"

        # pick up chair
        self.game.play('get chair')
        self.serialise(self.game)
        # open outer dresser
        self.game.play('open outer dresser')
        self.serialise(self.game)
        # put chair in dresser
        self.game.play('put chair in dresser')
        self.serialise(self.game)
        # get chair again
        self.game.play('get chair')
        self.serialise(self.game)
        # open inner dresser (closet)
        self.game.play('open closet')
        self.serialise(self.game)
        # put chair in closet
        self.game.play('put chair in closet')
        self.serialise(self.game)
        # close closet for good measure
        self.game.play('close closet')
        self.serialise(self.game)


if __name__ == '__main__':
    unittest.main()