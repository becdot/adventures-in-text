from game import Game

import unittest

class Serialisation(unittest.TestCase):

    def serialise(self, g):
        """Takes a game instance, serialises it, and then creates a new game instance from the serialisation.
            The old and new instances should be the same."""
        old = g.game
        s = g.serialise()
        print s
        g = Game(s)
        new = g.game
        self.assertEquals(old, new)

    def test_mini_game_with_serialisation(self):
        "Tests basic game functions (same as mini_game.py) with serialisation"

        game = Game()
        bedroom, closet = game.game['rooms'][0], game.game['rooms'][1]
        bed, lamp, dresser = bedroom.objects[0], bedroom.objects[1], bedroom.objects[2]
        chair = closet.objects[0]

        # move west
        game.play('move west')
        self.assertEquals(game.game['location'], closet)
        self.serialise(game)
        # go north (impossible) should not change location
        game.play('north')
        self.assertEquals(game.game['location'], closet)
        self.serialise(game)
        # picking up chair should add it to inventory
        game.play('get chair')
        self.assertEquals(game.game['inv'], [chair])
        self.serialise(game)
        # and remove it from closet.objects
        self.assertEquals(closet.objects, [])
        self.serialise(game)
        # going east again should change location to the bedroom
        game.play('east')
        self.assertEquals(game.game['location'], bedroom)
        self.serialise(game)
        # dropping the chair should remove it from inventory
        game.play('drop chair')
        self.assertEquals(game.game['inv'], [])
        self.serialise(game)
        # and add it to bedroom.objects
        self.assertEquals(bedroom.objects, [bed, lamp, dresser, chair])
        self.serialise(game)
        # turning on lamp should not change lamp.is_lit to True (because it is type Unreachable)
        game.play('light lamp')
        self.assertFalse(lamp.is_lit)
        self.serialise(game)
        # climbing on the bed should not enable us to turn the lamp on
        game.play('climb bed')
        game.play('light lamp')
        self.assertFalse(lamp.is_lit)
        self.serialise(game)
        # climbing on the chair should set chair.has_user to True
        game.play('climb chair')
        self.assertTrue(chair.has_user)
        self.serialise(game)
        # now that we are standing on the chair, turning on the lamp should set lamp.is_lit to True
        game.play('light lamp')
        self.assertTrue(lamp.is_lit)
        self.serialise(game)
        # if we put the chair in the dresser, the game should serialise properly
        game.play('get off chair')
        self.assertFalse(chair.has_user)
        self.serialise(game)
        game.play('get chair')
        self.assertEquals(game.game['inv'], [chair])
        self.serialise(game)
        game.play('open dresser')
        self.assertTrue(dresser.is_open)
        self.serialise(game)
        game.play('put chair in dresser')
        self.assertEquals(dresser.objects, [chair])
        self.serialise(game)


if __name__ == '__main__':
    unittest.main()