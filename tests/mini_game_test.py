from play_game import play_game
from game import game
import unittest

class TestMiniGame(unittest.TestCase):

    def test_play(self):
        "Tests basic play_game functions: moving locations, getting and dropping objects, interacting with objects, etc."
        base = game
        bedroom, closet = base['rooms'][0], base['rooms'][1]
        bed, lamp, dresser = bedroom.objects[0], bedroom.objects[1], bedroom.objects[2]
        chair = closet.objects[0]

        # go west
        update = play_game(base, 'west')[0]
        self.assertEquals(update['location'], closet)
        # go north (impossible) should not change location
        update = play_game(update, 'north')[0]
        self.assertEquals(update['location'], closet)
        # picking up chair should add it to inventory
        update = play_game(update, 'get chair')[0]
        self.assertEquals(update['inv'], [chair])
        # and remove it from closet.objects
        self.assertEquals(closet.objects, [])
        # going east again should change location to the bedroom
        update = play_game(update, 'east')[0]
        self.assertEquals(update['location'], bedroom)
        # dropping the chair should remove it from inventory
        update = play_game(update, 'drop chair')[0]
        self.assertEquals(update['inv'], [])
        # and add it to bedroom.objects
        self.assertEquals(bedroom.objects, [bed, lamp, dresser, chair])
        # turning on lamp should not change lamp.is_lit to True (because it is type Unreachable)
        update = play_game(update, 'light unreachable_lamp')[0]
        self.assertFalse(lamp.is_lit)
        # climbing on the bed should not enable us to turn the lamp on
        update = play_game(update, 'climb bed')[0]
        update = play_game(update, 'light unreachable_lamp')[0]
        self.assertFalse(lamp.is_lit)
        # climbing on the chair should set chair.has_user to True
        update = play_game(update, 'climb chair')[0]
        self.assertTrue(chair.has_user)
        # now that we are standing on the chair, turning on the lamp should set lamp.is_lit to True
        update = play_game(update, 'light unreachable_lamp')[0]
        self.assertTrue(lamp.is_lit)

if __name__ == "__main__":
    unittest.main()